// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var algorithm_1 = require("@phosphor/algorithm");
var coreutils_1 = require("@jupyterlab/coreutils");
var apputils_1 = require("@jupyterlab/apputils");
var mimemodel_1 = require("./mimemodel");
var renderers_1 = require("./renderers");
var widgets_1 = require("./widgets");
/**
 * A composite renderer.
 *
 * #### Notes
 * When rendering a mimebundle, a mimeType is selected from the mimeTypes by
 * searching through the `this.order` list. The first mimeType found in the
 * bundle determines the renderer that will be used.
 *
 * You can add a renderer by adding it to the `renderers` object and
 * registering the mimeType in the `order` array.
 *
 * Untrusted bundles are handled differently from trusted ones.  Untrusted
 * bundles will only render outputs that can be rendered "safely"
 * (see [[RenderMime.IRenderer.isSafe]]) or can be "sanitized"
 * (see [[RenderMime.IRenderer.isSanitizable]]).
 */
var RenderMime = (function () {
    /**
     * Construct a renderer.
     */
    function RenderMime(options) {
        if (options === void 0) { options = {}; }
        this._renderers = Object.create(null);
        this._order = [];
        if (options.items) {
            for (var _i = 0, _a = options.items; _i < _a.length; _i++) {
                var item = _a[_i];
                this._order.push(item.mimeType);
                this._renderers[item.mimeType] = item.renderer;
            }
        }
        this.sanitizer = options.sanitizer || apputils_1.defaultSanitizer;
        this._resolver = options.resolver || null;
        this._handler = options.linkHandler || null;
    }
    Object.defineProperty(RenderMime.prototype, "resolver", {
        /**
         * The object used to resolve relative urls for the rendermime instance.
         */
        get: function () {
            return this._resolver;
        },
        set: function (value) {
            this._resolver = value;
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(RenderMime.prototype, "linkHandler", {
        /**
         * The object used to handle path opening links.
         */
        get: function () {
            return this._handler;
        },
        set: function (value) {
            this._handler = value;
        },
        enumerable: true,
        configurable: true
    });
    /**
     * Get an iterator over the ordered list of mimeTypes.
     *
     * #### Notes
     * These mimeTypes are searched from beginning to end, and the first matching
     * mimeType is used.
     */
    RenderMime.prototype.mimeTypes = function () {
        return new algorithm_1.ArrayIterator(this._order);
    };
    /**
     * Render a mime model.
     *
     * @param model - the mime model to render.
     *
     * #### Notes
     * Renders the model using the preferred mime type.  See
     * [[preferredMimeType]].
     */
    RenderMime.prototype.render = function (model) {
        var mimeType = this.preferredMimeType(model);
        if (!mimeType) {
            return this._handleError(model);
        }
        var rendererOptions = {
            mimeType: mimeType,
            model: model,
            resolver: this._resolver,
            sanitizer: this.sanitizer,
            linkHandler: this._handler
        };
        return this._renderers[mimeType].render(rendererOptions);
    };
    /**
     * Find the preferred mimeType for a model.
     *
     * @param model - the mime model of interest.
     *
     * #### Notes
     * The mimeTypes in the model are checked in preference order
     * until a renderer returns `true` for `.canRender`.
     */
    RenderMime.prototype.preferredMimeType = function (model) {
        var _this = this;
        var sanitizer = this.sanitizer;
        return algorithm_1.find(this._order, function (mimeType) {
            if (model.data.has(mimeType)) {
                var options = { mimeType: mimeType, model: model, sanitizer: sanitizer };
                var renderer = _this._renderers[mimeType];
                var canRender = false;
                try {
                    canRender = renderer.canRender(options);
                }
                catch (err) {
                    console.error("Got an error when checking the renderer for the mimeType '" + mimeType + "'\n", err);
                }
                if (canRender) {
                    return true;
                }
            }
        });
    };
    /**
     * Clone the rendermime instance with shallow copies of data.
     *
     * #### Notes
     * The resolver is explicitly not cloned in this operation.
     */
    RenderMime.prototype.clone = function () {
        var _this = this;
        var items = algorithm_1.toArray(algorithm_1.map(this._order, function (mimeType) {
            return { mimeType: mimeType, renderer: _this._renderers[mimeType] };
        }));
        return new RenderMime({
            items: items,
            sanitizer: this.sanitizer,
            linkHandler: this._handler
        });
    };
    /**
     * Add a renderer by mimeType.
     *
     * @param item - A renderer item.
     *
     * @param index - The optional order index.
     *
     * ####Notes
     * Negative indices count from the end, so -1 refers to the last index.
     * Use the index of `.order.length` to add to the end of the render precedence list,
     * which would make the new renderer the last choice.
     * The renderer will replace an existing renderer for the given
     * mimeType.
     */
    RenderMime.prototype.addRenderer = function (item, index) {
        if (index === void 0) { index = 0; }
        var mimeType = item.mimeType, renderer = item.renderer;
        var orig = algorithm_1.ArrayExt.removeFirstOf(this._order, mimeType);
        if (orig !== -1 && orig < index) {
            index -= 1;
        }
        this._renderers[mimeType] = renderer;
        algorithm_1.ArrayExt.insert(this._order, index, mimeType);
    };
    /**
     * Remove a renderer by mimeType.
     *
     * @param mimeType - The mimeType of the renderer.
     */
    RenderMime.prototype.removeRenderer = function (mimeType) {
        delete this._renderers[mimeType];
        algorithm_1.ArrayExt.removeFirstOf(this._order, mimeType);
    };
    /**
     * Get a renderer by mimeType.
     *
     * @param mimeType - The mimeType of the renderer.
     *
     * @returns The renderer for the given mimeType, or undefined if the mimeType is unknown.
     */
    RenderMime.prototype.getRenderer = function (mimeType) {
        return this._renderers[mimeType];
    };
    /**
     * Return a widget for an error.
     */
    RenderMime.prototype._handleError = function (model) {
        var errModel = new mimemodel_1.MimeModel({
            data: {
                'application/vnd.jupyter.stderr': 'Unable to render data'
            }
        });
        var options = {
            mimeType: 'application/vnd.jupyter.stderr',
            model: errModel,
            sanitizer: this.sanitizer,
        };
        return new widgets_1.RenderedText(options);
    };
    return RenderMime;
}());
exports.RenderMime = RenderMime;
/**
 * The namespace for RenderMime statics.
 */
(function (RenderMime) {
    /**
     * Get an array of the default renderer items.
     */
    function getDefaultItems() {
        var renderers = Private.defaultRenderers;
        var items = [];
        var mimes = {};
        for (var _i = 0, renderers_2 = renderers; _i < renderers_2.length; _i++) {
            var renderer = renderers_2[_i];
            for (var _a = 0, _b = renderer.mimeTypes; _a < _b.length; _a++) {
                var mime = _b[_a];
                if (mime in mimes) {
                    continue;
                }
                mimes[mime] = true;
                items.push({ mimeType: mime, renderer: renderer });
            }
        }
        return items;
    }
    RenderMime.getDefaultItems = getDefaultItems;
    /**
     * A default resolver that uses a session and a contents manager.
     */
    var UrlResolver = (function () {
        /**
         * Create a new url resolver for a console.
         */
        function UrlResolver(options) {
            this._session = options.session;
            this._contents = options.contents;
        }
        /**
         * Resolve a relative url to a correct server path.
         */
        UrlResolver.prototype.resolveUrl = function (url) {
            if (coreutils_1.URLExt.isLocal(url)) {
                var cwd = coreutils_1.PathExt.dirname(this._session.path);
                url = coreutils_1.PathExt.resolve(cwd, url);
            }
            return Promise.resolve(url);
        };
        /**
         * Get the download url of a given absolute server path.
         */
        UrlResolver.prototype.getDownloadUrl = function (path) {
            if (coreutils_1.URLExt.isLocal(path)) {
                return this._contents.getDownloadUrl(path);
            }
            return Promise.resolve(path);
        };
        return UrlResolver;
    }());
    RenderMime.UrlResolver = UrlResolver;
})(RenderMime = exports.RenderMime || (exports.RenderMime = {}));
exports.RenderMime = RenderMime;
/**
 * The namespace for private module data.
 */
var Private;
(function (Private) {
    /**
     * The default renderer instances.
     */
    Private.defaultRenderers = [
        new renderers_1.JavaScriptRenderer(),
        new renderers_1.HTMLRenderer(),
        new renderers_1.MarkdownRenderer(),
        new renderers_1.LatexRenderer(),
        new renderers_1.SVGRenderer(),
        new renderers_1.ImageRenderer(),
        new renderers_1.PDFRenderer(),
        new renderers_1.TextRenderer()
    ];
})(Private = exports.Private || (exports.Private = {}));

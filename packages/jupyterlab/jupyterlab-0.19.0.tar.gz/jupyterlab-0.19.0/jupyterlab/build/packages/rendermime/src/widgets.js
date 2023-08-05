// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
"use strict";
var __extends = (this && this.__extends) || (function () {
    var extendStatics = Object.setPrototypeOf ||
        ({ __proto__: [] } instanceof Array && function (d, b) { d.__proto__ = b; }) ||
        function (d, b) { for (var p in b) if (b.hasOwnProperty(p)) d[p] = b[p]; };
    return function (d, b) {
        extendStatics(d, b);
        function __() { this.constructor = d; }
        d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
var ansi_up_1 = require("ansi_up");
var codemirror_1 = require("@jupyterlab/codemirror");
var marked = require("marked");
var widgets_1 = require("@phosphor/widgets");
var _1 = require(".");
/*
 * The class name added to common rendered HTML.
 */
exports.HTML_COMMON_CLASS = 'jp-RenderedHTMLCommon';
/*
 * The class name added to rendered HTML.
 */
var HTML_CLASS = 'jp-RenderedHTML';
/*
 * The class name added to rendered markdown.
 */
var MARKDOWN_CLASS = 'jp-RenderedMarkdown';
/*
 * The class name added to rendered Latex.
 */
var LATEX_CLASS = 'jp-RenderedLatex';
/*
 * The class name added to rendered images.
 */
var IMAGE_CLASS = 'jp-RenderedImage';
/*
 * The class name added to rendered text.
 */
var TEXT_CLASS = 'jp-RenderedText';
/**
 * The class name added to an error output.
 */
var ERROR_CLASS = 'jp-mod-error';
/*
 * The class name added to rendered javascript.
 */
var JAVASCRIPT_CLASS = 'jp-RenderedJavascript';
/*
 * The class name added to rendered SVG.
 */
var SVG_CLASS = 'jp-RenderedSVG';
/*
 * The class name added to rendered PDF.
 */
var PDF_CLASS = 'jp-RenderedPDF';
/*
 * A widget for displaying any widget whoes representation is rendered HTML
 * */
var RenderedHTMLCommon = (function (_super) {
    __extends(RenderedHTMLCommon, _super);
    /* Construct a new rendered HTML common widget.*/
    function RenderedHTMLCommon(options) {
        var _this = _super.call(this) || this;
        _this.addClass(exports.HTML_COMMON_CLASS);
        return _this;
    }
    return RenderedHTMLCommon;
}(widgets_1.Widget));
exports.RenderedHTMLCommon = RenderedHTMLCommon;
/**
 * A widget for displaying HTML and rendering math.
 */
var RenderedHTML = (function (_super) {
    __extends(RenderedHTML, _super);
    /**
     * Construct a new html widget.
     */
    function RenderedHTML(options) {
        var _this = _super.call(this, options) || this;
        _this._urlResolved = null;
        _this.addClass(HTML_CLASS);
        var source = Private.getSource(options);
        if (!options.model.trusted) {
            source = options.sanitizer.sanitize(source);
        }
        Private.appendHtml(_this.node, source);
        if (options.resolver) {
            _this._urlResolved = Private.handleUrls(_this.node, options.resolver, options.linkHandler);
        }
        return _this;
    }
    /**
     * A message handler invoked on an `'after-attach'` message.
     */
    RenderedHTML.prototype.onAfterAttach = function (msg) {
        var _this = this;
        if (this._urlResolved) {
            this._urlResolved.then(function () { _1.typeset(_this.node); });
        }
        else {
            _1.typeset(this.node);
        }
    };
    return RenderedHTML;
}(RenderedHTMLCommon));
exports.RenderedHTML = RenderedHTML;
/**
 * A widget for displaying Markdown with embeded latex.
 */
var RenderedMarkdown = (function (_super) {
    __extends(RenderedMarkdown, _super);
    /**
     * Construct a new markdown widget.
     */
    function RenderedMarkdown(options) {
        var _this = _super.call(this, options) || this;
        _this._rendered = false;
        _this._urlResolved = null;
        _this.addClass(MARKDOWN_CLASS);
        // Initialize the marked library if necessary.
        Private.initializeMarked();
        var source = Private.getSource(options);
        var parts = _1.removeMath(source);
        // Add the markdown content asynchronously.
        marked(parts['text'], function (err, content) {
            if (err) {
                console.error(err);
                return;
            }
            content = _1.replaceMath(content, parts['math']);
            if (!options.model.trusted) {
                content = options.sanitizer.sanitize(content);
            }
            Private.appendHtml(_this.node, content);
            if (options.resolver) {
                _this._urlResolved = Private.handleUrls(_this.node, options.resolver, options.linkHandler);
            }
            Private.headerAnchors(_this.node);
            _this.fit();
            _this._rendered = true;
            if (_this.isAttached) {
                if (_this._urlResolved) {
                    _this._urlResolved.then(function () { _1.typeset(_this.node); });
                }
                else {
                    _1.typeset(_this.node);
                }
            }
        });
        return _this;
    }
    /**
     * A message handler invoked on an `'after-attach'` message.
     */
    RenderedMarkdown.prototype.onAfterAttach = function (msg) {
        if (this._rendered) {
            _1.typeset(this.node);
        }
    };
    return RenderedMarkdown;
}(RenderedHTMLCommon));
exports.RenderedMarkdown = RenderedMarkdown;
/**
 * A widget for displaying LaTeX output.
 */
var RenderedLatex = (function (_super) {
    __extends(RenderedLatex, _super);
    /**
     * Construct a new latex widget.
     */
    function RenderedLatex(options) {
        var _this = _super.call(this) || this;
        var source = Private.getSource(options);
        _this.node.textContent = source;
        _this.addClass(LATEX_CLASS);
        return _this;
    }
    /**
     * A message handler invoked on an `'after-attach'` message.
     */
    RenderedLatex.prototype.onAfterAttach = function (msg) {
        _1.typeset(this.node);
    };
    return RenderedLatex;
}(widgets_1.Widget));
exports.RenderedLatex = RenderedLatex;
/**
 * A widget for displaying rendered images.
 */
var RenderedImage = (function (_super) {
    __extends(RenderedImage, _super);
    /**
     * Construct a new rendered image widget.
     */
    function RenderedImage(options) {
        var _this = _super.call(this) || this;
        var img = document.createElement('img');
        var source = Private.getSource(options);
        img.src = "data:" + options.mimeType + ";base64," + source;
        var metadata = options.model.metadata.get(options.mimeType);
        if (metadata) {
            var metaJSON = metadata;
            if (typeof metaJSON['height'] === 'number') {
                img.height = metaJSON['height'];
            }
            if (typeof metaJSON['width'] === 'number') {
                img.width = metaJSON['width'];
            }
        }
        _this.node.appendChild(img);
        _this.addClass(IMAGE_CLASS);
        return _this;
    }
    return RenderedImage;
}(widgets_1.Widget));
exports.RenderedImage = RenderedImage;
/**
 * A widget for displaying rendered text.
 */
var RenderedText = (function (_super) {
    __extends(RenderedText, _super);
    /**
     * Construct a new rendered text widget.
     */
    function RenderedText(options) {
        var _this = _super.call(this) || this;
        var source = Private.getSource(options);
        var data = ansi_up_1.escape_for_html(source);
        var pre = document.createElement('pre');
        pre.innerHTML = ansi_up_1.ansi_to_html(data);
        _this.node.appendChild(pre);
        _this.addClass(TEXT_CLASS);
        if (options.mimeType === 'application/vnd.jupyter.stderr') {
            _this.addClass(ERROR_CLASS);
        }
        return _this;
    }
    return RenderedText;
}(widgets_1.Widget));
exports.RenderedText = RenderedText;
/**
 * A widget for displaying rendered JavaScript.
 */
var RenderedJavaScript = (function (_super) {
    __extends(RenderedJavaScript, _super);
    /**
     * Construct a new rendered JavaScript widget.
     */
    function RenderedJavaScript(options) {
        var _this = _super.call(this) || this;
        var s = document.createElement('script');
        s.type = options.mimeType;
        var source = Private.getSource(options);
        s.textContent = source;
        _this.node.appendChild(s);
        _this.addClass(JAVASCRIPT_CLASS);
        return _this;
    }
    return RenderedJavaScript;
}(widgets_1.Widget));
exports.RenderedJavaScript = RenderedJavaScript;
/**
 * A widget for displaying rendered SVG content.
 */
var RenderedSVG = (function (_super) {
    __extends(RenderedSVG, _super);
    /**
     * Construct a new rendered SVG widget.
     */
    function RenderedSVG(options) {
        var _this = _super.call(this) || this;
        _this._urlResolved = null;
        var source = Private.getSource(options);
        _this.node.innerHTML = source;
        var svgElement = _this.node.getElementsByTagName('svg')[0];
        if (!svgElement) {
            throw new Error('SVGRender: Error: Failed to create <svg> element');
        }
        if (options.resolver) {
            _this._urlResolved = Private.handleUrls(_this.node, options.resolver, options.linkHandler);
        }
        _this.addClass(SVG_CLASS);
        return _this;
    }
    return RenderedSVG;
}(widgets_1.Widget));
exports.RenderedSVG = RenderedSVG;
/**
 * A widget for displaying rendered PDF content.
 */
var RenderedPDF = (function (_super) {
    __extends(RenderedPDF, _super);
    /**
     * Construct a new rendered PDF widget.
     */
    function RenderedPDF(options) {
        var _this = _super.call(this) || this;
        var source = Private.getSource(options);
        var a = document.createElement('a');
        a.target = '_blank';
        a.textContent = 'View PDF';
        a.href = "data:application/pdf;base64," + source;
        _this.node.appendChild(a);
        _this.addClass(PDF_CLASS);
        return _this;
    }
    return RenderedPDF;
}(widgets_1.Widget));
exports.RenderedPDF = RenderedPDF;
/**
 * The namespace for module private data.
 */
var Private;
(function (Private) {
    /**
     * Extract the source text from render options.
     */
    function getSource(options) {
        return String(options.model.data.get(options.mimeType));
    }
    Private.getSource = getSource;
    /**
     * Append trusted html to a node.
     */
    function appendHtml(node, html) {
        try {
            var range = document.createRange();
            node.appendChild(range.createContextualFragment(html));
        }
        catch (error) {
            console.warn('Environment does not support Range ' +
                'createContextualFragment, falling back on innerHTML');
            node.innerHTML = html;
        }
    }
    Private.appendHtml = appendHtml;
    /**
     * Resolve the relative urls in element `src` and `href` attributes.
     *
     * @param node - The head html element.
     *
     * @param resolver - A url resolver.
     *
     * @param linkHandler - An optional link handler for nodes.
     *
     * @returns a promise fulfilled when the relative urls have been resolved.
     */
    function handleUrls(node, resolver, linkHandler) {
        var promises = [];
        // Handle HTML Elements with src attributes.
        var nodes = node.querySelectorAll('*[src]');
        for (var i = 0; i < nodes.length; i++) {
            promises.push(handleAttr(nodes[i], 'src', resolver));
        }
        var anchors = node.getElementsByTagName('a');
        for (var i = 0; i < anchors.length; i++) {
            promises.push(handleAnchor(anchors[i], resolver, linkHandler || null));
        }
        var links = node.getElementsByTagName('link');
        for (var i = 0; i < links.length; i++) {
            promises.push(handleAttr(links[i], 'href', resolver));
        }
        return Promise.all(promises).then(function () { return void 0; });
    }
    Private.handleUrls = handleUrls;
    /**
     * Handle a node with a `src` or `href` attribute.
     */
    function handleAttr(node, name, resolver) {
        var source = node.getAttribute(name);
        if (!source) {
            return Promise.resolve(void 0);
        }
        node.setAttribute(name, '');
        return resolver.resolveUrl(source).then(function (path) {
            return resolver.getDownloadUrl(path);
        }).then(function (url) {
            node.setAttribute(name, url);
        });
    }
    /**
     * Apply ids to headers.
     */
    function headerAnchors(node) {
        var headerNames = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6'];
        for (var _i = 0, headerNames_1 = headerNames; _i < headerNames_1.length; _i++) {
            var headerType = headerNames_1[_i];
            var headers = node.getElementsByTagName(headerType);
            for (var i = 0; i < headers.length; i++) {
                var header = headers[i];
                header.id = header.innerHTML.replace(/ /g, '-');
                var anchor = document.createElement('a');
                anchor.target = '_self';
                anchor.textContent = '¶';
                anchor.href = '#' + header.id;
                anchor.classList.add('jp-InternalAnchorLink');
                header.appendChild(anchor);
            }
        }
    }
    Private.headerAnchors = headerAnchors;
    /**
     * Handle an anchor node.
     */
    function handleAnchor(anchor, resolver, linkHandler) {
        anchor.target = '_blank';
        var href = anchor.getAttribute('href');
        if (!href) {
            return Promise.resolve(void 0);
        }
        return resolver.resolveUrl(href).then(function (path) {
            if (linkHandler) {
                linkHandler.handleLink(anchor, path);
            }
            return resolver.getDownloadUrl(path);
        }).then(function (url) {
            anchor.href = url;
        });
    }
})(Private || (Private = {}));
/**
 * A namespace for private module data.
 */
(function (Private) {
    var initialized = false;
    /**
     * Support GitHub flavored Markdown, leave sanitizing to external library.
     */
    function initializeMarked() {
        if (initialized) {
            return;
        }
        initialized = true;
        marked.setOptions({
            gfm: true,
            sanitize: false,
            tables: true,
            // breaks: true; We can't use GFM breaks as it causes problems with tables
            langPrefix: "cm-s-" + codemirror_1.CodeMirrorEditor.DEFAULT_THEME + " language-",
            highlight: function (code, lang, callback) {
                if (!lang) {
                    // no language, no highlight
                    if (callback) {
                        callback(null, code);
                        return;
                    }
                    else {
                        return code;
                    }
                }
                codemirror_1.requireMode(lang).then(function (spec) {
                    var el = document.createElement('div');
                    if (!spec) {
                        console.log("No CodeMirror mode: " + lang);
                        callback(null, code);
                        return;
                    }
                    try {
                        codemirror_1.runMode(code, spec.mime, el);
                        callback(null, el.innerHTML);
                    }
                    catch (err) {
                        console.log("Failed to highlight " + lang + " code", err);
                        callback(err, code);
                    }
                }).catch(function (err) {
                    console.log("No CodeMirror mode: " + lang);
                    console.log("Require CodeMirror mode error: " + err);
                    callback(null, code);
                });
            }
        });
    }
    Private.initializeMarked = initializeMarked;
})(Private || (Private = {}));

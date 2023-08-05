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
var widgets_1 = require("@phosphor/widgets");
var docregistry_1 = require("@jupyterlab/docregistry");
/**
 * The class name added to a imagewidget.
 */
var IMAGE_CLASS = 'jp-ImageWidget';
/**
 * A widget for images.
 */
var ImageWidget = (function (_super) {
    __extends(ImageWidget, _super);
    /**
     * Construct a new image widget.
     */
    function ImageWidget(context) {
        var _this = _super.call(this, { node: Private.createNode() }) || this;
        _this._scale = 1;
        _this._context = context;
        _this.node.tabIndex = -1;
        _this.addClass(IMAGE_CLASS);
        _this._onTitleChanged();
        context.pathChanged.connect(_this._onTitleChanged, _this);
        context.ready.then(function () {
            _this.update();
            context.model.contentChanged.connect(_this.update, _this);
            context.fileChanged.connect(_this.update, _this);
        });
        return _this;
    }
    Object.defineProperty(ImageWidget.prototype, "context", {
        /**
         * The image widget's context.
         */
        get: function () {
            return this._context;
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(ImageWidget.prototype, "scale", {
        /**
         * The scale factor for the image.
         */
        get: function () {
            return this._scale;
        },
        set: function (value) {
            if (value === this._scale) {
                return;
            }
            this._scale = value;
            var scaleNode = this.node.querySelector('div');
            var transform;
            transform = "scale(" + value + ")";
            scaleNode.style.transform = transform;
        },
        enumerable: true,
        configurable: true
    });
    /**
     * Dispose of the resources used by the widget.
     */
    ImageWidget.prototype.dispose = function () {
        this._context = null;
        _super.prototype.dispose.call(this);
    };
    /**
     * Handle `update-request` messages for the widget.
     */
    ImageWidget.prototype.onUpdateRequest = function (msg) {
        var context = this._context;
        if (this.isDisposed || !context.isReady) {
            return;
        }
        var cm = context.contentsModel;
        var content = context.model.toString();
        var src = "data:" + cm.mimetype + ";" + cm.format + "," + content;
        this.node.querySelector('img').setAttribute('src', src);
    };
    /**
     * Handle `'activate-request'` messages.
     */
    ImageWidget.prototype.onActivateRequest = function (msg) {
        this.node.focus();
    };
    /**
     * Handle a change to the title.
     */
    ImageWidget.prototype._onTitleChanged = function () {
        this.title.label = this._context.path.split('/').pop();
    };
    return ImageWidget;
}(widgets_1.Widget));
exports.ImageWidget = ImageWidget;
/**
 * A widget factory for images.
 */
var ImageWidgetFactory = (function (_super) {
    __extends(ImageWidgetFactory, _super);
    function ImageWidgetFactory() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    /**
     * Create a new widget given a context.
     */
    ImageWidgetFactory.prototype.createNewWidget = function (context) {
        return new ImageWidget(context);
    };
    return ImageWidgetFactory;
}(docregistry_1.ABCWidgetFactory));
exports.ImageWidgetFactory = ImageWidgetFactory;
/**
 * A namespace for image widget private data.
 */
var Private;
(function (Private) {
    /**
     * Create the node for the image widget.
     */
    function createNode() {
        var node = document.createElement('div');
        var innerNode = document.createElement('div');
        var image = document.createElement('img');
        node.appendChild(innerNode);
        innerNode.appendChild(image);
        return node;
    }
    Private.createNode = createNode;
})(Private || (Private = {}));

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
var widgets_2 = require("@phosphor/widgets");
var coreutils_1 = require("@jupyterlab/coreutils");
var docregistry_1 = require("@jupyterlab/docregistry");
var rendermime_1 = require("@jupyterlab/rendermime");
/**
 * The class name added to a Jupyter MarkdownWidget
 */
var MD_CLASS = 'jp-MarkdownWidget';
/**
 * The timeout to wait for change activity to have ceased before rendering.
 */
var RENDER_TIMEOUT = 1000;
/**
 * A widget for rendered markdown.
 */
var MarkdownWidget = (function (_super) {
    __extends(MarkdownWidget, _super);
    /**
     * Construct a new markdown widget.
     */
    function MarkdownWidget(context, rendermime) {
        var _this = _super.call(this) || this;
        _this._context = null;
        _this._monitor = null;
        _this._rendermime = null;
        _this.addClass(MD_CLASS);
        _this.layout = new widgets_1.PanelLayout();
        _this.title.label = context.path.split('/').pop();
        _this._rendermime = rendermime;
        rendermime.resolver = context;
        _this._context = context;
        context.pathChanged.connect(_this._onPathChanged, _this);
        // Throttle the rendering rate of the widget.
        _this._monitor = new coreutils_1.ActivityMonitor({
            signal: context.model.contentChanged,
            timeout: RENDER_TIMEOUT
        });
        _this._monitor.activityStopped.connect(_this.update, _this);
        return _this;
    }
    Object.defineProperty(MarkdownWidget.prototype, "context", {
        /**
         * The markdown widget's context.
         */
        get: function () {
            return this._context;
        },
        enumerable: true,
        configurable: true
    });
    /**
     * Dispose of the resources held by the widget.
     */
    MarkdownWidget.prototype.dispose = function () {
        if (this.isDisposed) {
            return;
        }
        this._monitor.dispose();
        _super.prototype.dispose.call(this);
    };
    /**
     * Handle `'activate-request'` messages.
     */
    MarkdownWidget.prototype.onActivateRequest = function (msg) {
        this.node.tabIndex = -1;
        this.node.focus();
    };
    /**
     * Handle an `after-attach` message to the widget.
     */
    MarkdownWidget.prototype.onAfterAttach = function (msg) {
        this.update();
    };
    /**
     * Handle an `update-request` message to the widget.
     */
    MarkdownWidget.prototype.onUpdateRequest = function (msg) {
        var context = this._context;
        var model = context.model;
        var layout = this.layout;
        var data = { 'text/markdown': model.toString() };
        var mimeModel = new rendermime_1.MimeModel({ data: data, trusted: false });
        var widget = this._rendermime.render(mimeModel);
        if (layout.widgets.length) {
            layout.widgets[0].dispose();
        }
        layout.addWidget(widget);
    };
    /**
     * Handle a path change.
     */
    MarkdownWidget.prototype._onPathChanged = function () {
        this.title.label = this._context.path.split('/').pop();
    };
    return MarkdownWidget;
}(widgets_2.Widget));
exports.MarkdownWidget = MarkdownWidget;
/**
 * A widget factory for Markdown.
 */
var MarkdownWidgetFactory = (function (_super) {
    __extends(MarkdownWidgetFactory, _super);
    /**
     * Construct a new markdown widget factory.
     */
    function MarkdownWidgetFactory(options) {
        var _this = _super.call(this, options) || this;
        _this._rendermime = null;
        _this._rendermime = options.rendermime;
        return _this;
    }
    /**
     * Create a new widget given a context.
     */
    MarkdownWidgetFactory.prototype.createNewWidget = function (context) {
        return new MarkdownWidget(context, this._rendermime.clone());
    };
    return MarkdownWidgetFactory;
}(docregistry_1.ABCWidgetFactory));
exports.MarkdownWidgetFactory = MarkdownWidgetFactory;

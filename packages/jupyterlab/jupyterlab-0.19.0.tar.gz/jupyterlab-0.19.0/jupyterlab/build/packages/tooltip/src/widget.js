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
var apputils_1 = require("@jupyterlab/apputils");
var rendermime_1 = require("@jupyterlab/rendermime");
/**
 * The class name added to each tooltip.
 */
var TOOLTIP_CLASS = 'jp-Tooltip';
/**
 * The class added to widgets that have spawned a tooltip and anchor it.
 */
var ANCHOR_CLASS = 'jp-Tooltip-anchor';
/**
 * The minimum height of a tooltip widget.
 */
var MIN_HEIGHT = 20;
/**
 * The maximum height of a tooltip widget.
 */
var MAX_HEIGHT = 250;
/**
 * A flag to indicate that event handlers are caught in the capture phase.
 */
var USE_CAPTURE = true;
/**
 * A tooltip widget.
 */
var TooltipWidget = (function (_super) {
    __extends(TooltipWidget, _super);
    /**
     * Instantiate a tooltip.
     */
    function TooltipWidget(options) {
        var _this = _super.call(this) || this;
        _this._content = null;
        _this.layout = new widgets_1.PanelLayout();
        _this.anchor = options.anchor;
        _this.addClass(TOOLTIP_CLASS);
        _this.anchor.addClass(ANCHOR_CLASS);
        _this._editor = options.editor;
        _this._rendermime = options.rendermime;
        var model = new rendermime_1.MimeModel({
            data: options.bundle,
            trusted: true
        });
        _this._content = _this._rendermime.render(model);
        if (_this._content) {
            _this.layout.addWidget(_this._content);
        }
        return _this;
    }
    /**
     * Dispose of the resources held by the widget.
     */
    TooltipWidget.prototype.dispose = function () {
        if (this.anchor && !this.anchor.isDisposed) {
            this.anchor.removeClass(ANCHOR_CLASS);
        }
        if (this._content) {
            this._content.dispose();
            this._content = null;
        }
        _super.prototype.dispose.call(this);
    };
    /**
     * Handle the DOM events for the widget.
     *
     * @param event - The DOM event sent to the widget.
     *
     * #### Notes
     * This method implements the DOM `EventListener` interface and is
     * called in response to events on the dock panel's node. It should
     * not be called directly by user code.
     */
    TooltipWidget.prototype.handleEvent = function (event) {
        if (this.isHidden || this.isDisposed) {
            return;
        }
        switch (event.type) {
            case 'keydown':
                if (this.node.contains(event.target)) {
                    if (event.keyCode === 27) {
                        this.dispose();
                    }
                    return;
                }
                this.dispose();
                break;
            case 'mousedown':
                if (this.node.contains(event.target)) {
                    this.activate();
                    return;
                }
                this.dispose();
                break;
            case 'scroll':
                this._evtScroll(event);
                break;
            default:
                break;
        }
    };
    /**
     * Handle `'activate-request'` messages.
     */
    TooltipWidget.prototype.onActivateRequest = function (msg) {
        this.node.tabIndex = -1;
        this.node.focus();
    };
    /**
     * Handle `'after-attach'` messages.
     */
    TooltipWidget.prototype.onAfterAttach = function (msg) {
        document.addEventListener('keydown', this, USE_CAPTURE);
        document.addEventListener('mousedown', this, USE_CAPTURE);
        this.anchor.node.addEventListener('scroll', this, USE_CAPTURE);
        this.update();
    };
    /**
     * Handle `before-detach` messages for the widget.
     */
    TooltipWidget.prototype.onBeforeDetach = function (msg) {
        document.removeEventListener('keydown', this, USE_CAPTURE);
        document.removeEventListener('mousedown', this, USE_CAPTURE);
        this.anchor.node.removeEventListener('scroll', this, USE_CAPTURE);
    };
    /**
     * Handle `'update-request'` messages.
     */
    TooltipWidget.prototype.onUpdateRequest = function (msg) {
        this._setGeometry();
        _super.prototype.onUpdateRequest.call(this, msg);
    };
    /**
     * Handle scroll events for the widget
     */
    TooltipWidget.prototype._evtScroll = function (event) {
        // All scrolls except scrolls in the actual hover box node may cause the
        // referent editor that anchors the node to move, so the only scroll events
        // that can safely be ignored are ones that happen inside the hovering node.
        if (this.node.contains(event.target)) {
            return;
        }
        this.update();
    };
    /**
     * Set the geometry of the tooltip widget.
     */
    TooltipWidget.prototype._setGeometry = function () {
        // Find the start of the current token for hover box placement.
        var editor = this._editor;
        var cursor = editor.getCursorPosition();
        var end = editor.getOffsetAt(cursor);
        var line = editor.getLine(cursor.line);
        var tokens = line.substring(0, end).split(/\W+/);
        var last = tokens[tokens.length - 1];
        var start = last ? end - last.length : end;
        var position = editor.getPositionAt(start);
        var anchor = editor.getCoordinateForPosition(position);
        var style = window.getComputedStyle(this.node);
        var paddingLeft = parseInt(style.paddingLeft, 10) || 0;
        // Calculate the geometry of the tooltip.
        apputils_1.HoverBox.setGeometry({
            anchor: anchor,
            host: editor.host,
            maxHeight: MAX_HEIGHT,
            minHeight: MIN_HEIGHT,
            node: this.node,
            offset: { horizontal: -1 * paddingLeft },
            privilege: 'below'
        });
    };
    return TooltipWidget;
}(widgets_2.Widget));
exports.TooltipWidget = TooltipWidget;

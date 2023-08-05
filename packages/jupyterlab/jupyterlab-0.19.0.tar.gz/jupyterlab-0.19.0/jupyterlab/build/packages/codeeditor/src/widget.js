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
/**
 * The class name added to an editor widget that has a primary selection.
 */
var HAS_SELECTION_CLASS = 'jp-mod-has-primary-selection';
/**
 * A widget which hosts a code editor.
 */
var CodeEditorWidget = (function (_super) {
    __extends(CodeEditorWidget, _super);
    /**
     * Construct a new code editor widget.
     */
    function CodeEditorWidget(options) {
        var _this = _super.call(this) || this;
        _this._editor = null;
        _this._needsRefresh = false;
        var editor = _this._editor = options.factory({
            host: _this.node,
            model: options.model,
            uuid: options.uuid,
            wordWrap: options.wordWrap,
            readOnly: options.readOnly,
            selectionStyle: options.selectionStyle
        });
        editor.model.selections.changed.connect(_this._onSelectionsChanged, _this);
        return _this;
    }
    Object.defineProperty(CodeEditorWidget.prototype, "editor", {
        /**
         * Get the editor wrapped by the widget.
         */
        get: function () {
            return this._editor;
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(CodeEditorWidget.prototype, "model", {
        /**
         * Get the model used by the widget.
         */
        get: function () {
            return this._editor.model;
        },
        enumerable: true,
        configurable: true
    });
    /**
     * Dispose of the resources held by the widget.
     */
    CodeEditorWidget.prototype.dispose = function () {
        if (this.isDisposed) {
            return;
        }
        _super.prototype.dispose.call(this);
        this._editor.dispose();
        this._editor = null;
    };
    /**
     * Handle the DOM events for the widget.
     *
     * @param event - The DOM event sent to the widget.
     *
     * #### Notes
     * This method implements the DOM `EventListener` interface and is
     * called in response to events on the panel's DOM node. It should
     * not be called directly by user code.
     */
    CodeEditorWidget.prototype.handleEvent = function (event) {
        switch (event.type) {
            case 'focus':
                this._evtFocus(event);
                break;
            default:
                break;
        }
    };
    /**
     * Handle `'activate-request'` messages.
     */
    CodeEditorWidget.prototype.onActivateRequest = function (msg) {
        this._editor.focus();
    };
    /**
     * A message handler invoked on an `'after-attach'` message.
     */
    CodeEditorWidget.prototype.onAfterAttach = function (msg) {
        _super.prototype.onAfterAttach.call(this, msg);
        this.node.addEventListener('focus', this, true);
        if (this.isVisible) {
            this._editor.refresh();
            this._needsRefresh = false;
        }
    };
    /**
     * A message handler invoked on an `'after-show'` message.
     */
    CodeEditorWidget.prototype.onAfterShow = function (msg) {
        this._editor.refresh();
        this._needsRefresh = false;
    };
    /**
     * Handle `before-detach` messages for the widget.
     */
    CodeEditorWidget.prototype.onBeforeDetach = function (msg) {
        this.node.removeEventListener('focus', this, true);
    };
    /**
     * A message handler invoked on a `'resize'` message.
     */
    CodeEditorWidget.prototype.onResize = function (msg) {
        if (msg.width >= 0 && msg.height >= 0) {
            this._editor.setSize(msg);
            this._needsRefresh = false;
        }
        else if (this._editor.hasFocus()) {
            this._editor.refresh();
            this._needsRefresh = false;
        }
        else {
            this._needsRefresh = true;
        }
    };
    /**
     * Handle `focus` events for the widget.
     */
    CodeEditorWidget.prototype._evtFocus = function (event) {
        if (this._needsRefresh) {
            this._editor.refresh();
            this._needsRefresh = false;
        }
    };
    /**
     * Handle a change in model selections.
     */
    CodeEditorWidget.prototype._onSelectionsChanged = function () {
        var _a = this._editor.getSelection(), start = _a.start, end = _a.end;
        if (start.column !== end.column || start.line !== end.line) {
            this.addClass(HAS_SELECTION_CLASS);
        }
        else {
            this.removeClass(HAS_SELECTION_CLASS);
        }
    };
    return CodeEditorWidget;
}(widgets_1.Widget));
exports.CodeEditorWidget = CodeEditorWidget;

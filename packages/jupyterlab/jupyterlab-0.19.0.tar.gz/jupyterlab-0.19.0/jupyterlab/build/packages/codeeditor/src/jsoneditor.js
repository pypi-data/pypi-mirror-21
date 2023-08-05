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
var coreutils_1 = require("@phosphor/coreutils");
var widgets_1 = require("@phosphor/widgets");
var virtualdom_1 = require("@phosphor/virtualdom");
var _1 = require(".");
/**
 * The class name added to a JSONEditorWidget instance.
 */
var METADATA_CLASS = 'jp-JSONEditorWidget';
/**
 * The class name added when the Metadata editor contains invalid JSON.
 */
var ERROR_CLASS = 'jp-mod-error';
/**
 * The class name added to the editor host node.
 */
var HOST_CLASS = 'jp-JSONEditorWidget-host';
/**
 * The class name added to the button area.
 */
var BUTTON_AREA_CLASS = 'jp-JSONEditorWidget-buttons';
/**
 * The class name added to the revert button.
 */
var REVERT_CLASS = 'jp-JSONEditorWidget-revertButton';
/**
 * The class name added to the commit button.
 */
var COMMIT_CLASS = 'jp-JSONEditorWidget-commitButton';
/**
 * A widget for editing observable JSON.
 */
var JSONEditorWidget = (function (_super) {
    __extends(JSONEditorWidget, _super);
    /**
     * Construct a new metadata editor.
     */
    function JSONEditorWidget(options) {
        var _this = _super.call(this, { node: Private.createEditorNode() }) || this;
        _this._dataDirty = false;
        _this._inputDirty = false;
        _this._source = null;
        _this._originalValue = null;
        _this._changeGuard = false;
        _this.addClass(METADATA_CLASS);
        var host = _this.editorHostNode;
        var model = new _1.CodeEditor.Model();
        model.value.text = 'No data!';
        model.mimeType = 'application/json';
        model.value.changed.connect(_this._onValueChanged, _this);
        _this.model = model;
        _this.editor = options.editorFactory({ host: host, model: model });
        _this.editor.readOnly = true;
        return _this;
    }
    Object.defineProperty(JSONEditorWidget.prototype, "editorHostNode", {
        /**
         * Get the editor host node used by the metadata editor.
         */
        get: function () {
            return this.node.getElementsByClassName(HOST_CLASS)[0];
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(JSONEditorWidget.prototype, "revertButtonNode", {
        /**
         * Get the revert button used by the metadata editor.
         */
        get: function () {
            return this.node.getElementsByClassName(REVERT_CLASS)[0];
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(JSONEditorWidget.prototype, "commitButtonNode", {
        /**
         * Get the commit button used by the metadata editor.
         */
        get: function () {
            return this.node.getElementsByClassName(COMMIT_CLASS)[0];
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(JSONEditorWidget.prototype, "source", {
        /**
         * The observable source.
         */
        get: function () {
            return this._source;
        },
        set: function (value) {
            if (this._source === value) {
                return;
            }
            if (this._source) {
                this._source.changed.disconnect(this._onSourceChanged, this);
            }
            this._source = value;
            this.editor.readOnly = !value;
            if (value) {
                value.changed.connect(this._onSourceChanged, this);
            }
            this._setValue();
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(JSONEditorWidget.prototype, "isDirty", {
        /**
         * Get whether the editor is dirty.
         */
        get: function () {
            return this._dataDirty || this._inputDirty;
        },
        enumerable: true,
        configurable: true
    });
    /**
     * Handle the DOM events for the widget.
     *
     * @param event - The DOM event sent to the widget.
     *
     * #### Notes
     * This method implements the DOM `EventListener` interface and is
     * called in response to events on the notebook panel's node. It should
     * not be called directly by user code.
     */
    JSONEditorWidget.prototype.handleEvent = function (event) {
        switch (event.type) {
            case 'blur':
                this._evtBlur(event);
                break;
            case 'click':
                this._evtClick(event);
                break;
            default:
                break;
        }
    };
    /**
     * Handle `after-attach` messages for the widget.
     */
    JSONEditorWidget.prototype.onAfterAttach = function (msg) {
        var node = this.editorHostNode;
        node.addEventListener('blur', this, true);
        this.revertButtonNode.hidden = true;
        this.commitButtonNode.hidden = true;
        this.revertButtonNode.addEventListener('click', this);
        this.commitButtonNode.addEventListener('click', this);
    };
    /**
     * Handle `before-detach` messages for the widget.
     */
    JSONEditorWidget.prototype.onBeforeDetach = function (msg) {
        var node = this.editorHostNode;
        node.removeEventListener('blur', this, true);
        this.revertButtonNode.removeEventListener('click', this);
        this.commitButtonNode.removeEventListener('click', this);
    };
    /**
     * Handle a change to the metadata of the source.
     */
    JSONEditorWidget.prototype._onSourceChanged = function (sender, args) {
        if (this._changeGuard) {
            return;
        }
        if (this._inputDirty || this.editor.hasFocus()) {
            this._dataDirty = true;
            return;
        }
        this._setValue();
    };
    /**
     * Handle change events.
     */
    JSONEditorWidget.prototype._onValueChanged = function () {
        var valid = true;
        try {
            var value = JSON.parse(this.editor.model.value.text);
            this.removeClass(ERROR_CLASS);
            this._inputDirty = (!this._changeGuard && !coreutils_1.JSONExt.deepEqual(value, this._originalValue));
        }
        catch (err) {
            this.addClass(ERROR_CLASS);
            this._inputDirty = true;
            valid = false;
        }
        this.revertButtonNode.hidden = !this._inputDirty;
        this.commitButtonNode.hidden = !valid || !this._inputDirty;
    };
    /**
     * Handle blur events for the text area.
     */
    JSONEditorWidget.prototype._evtBlur = function (event) {
        // Update the metadata if necessary.
        if (!this._inputDirty && this._dataDirty) {
            this._setValue();
        }
    };
    /**
     * Handle click events for the buttons.
     */
    JSONEditorWidget.prototype._evtClick = function (event) {
        var target = event.target;
        if (target === this.revertButtonNode) {
            this._setValue();
        }
        else if (target === this.commitButtonNode) {
            if (!this.commitButtonNode.hidden && !this.hasClass(ERROR_CLASS)) {
                this._changeGuard = true;
                this._mergeContent();
                this._changeGuard = false;
                this._setValue();
            }
        }
    };
    /**
     * Merge the user content.
     */
    JSONEditorWidget.prototype._mergeContent = function () {
        var model = this.editor.model;
        var current = this._getContent() || {};
        var old = this._originalValue;
        var user = JSON.parse(model.value.text);
        var source = this.source;
        // If it is in user and has changed from old, set in current.
        for (var key in user) {
            if (!coreutils_1.JSONExt.deepEqual(user[key], old[key])) {
                current[key] = user[key];
            }
        }
        // If it was in old and is not in user, remove from current.
        for (var key in old) {
            if (!(key in user)) {
                delete current[key];
                source.delete(key);
            }
        }
        // Set the values.
        for (var key in current) {
            source.set(key, current[key]);
        }
    };
    /**
     * Get the metadata from the owner.
     */
    JSONEditorWidget.prototype._getContent = function () {
        var source = this._source;
        if (!source) {
            return void 0;
        }
        var content = {};
        for (var _i = 0, _a = source.keys(); _i < _a.length; _i++) {
            var key = _a[_i];
            content[key] = source.get(key);
        }
        return content;
    };
    /**
     * Set the value given the owner contents.
     */
    JSONEditorWidget.prototype._setValue = function () {
        this._dataDirty = false;
        this._inputDirty = false;
        this.revertButtonNode.hidden = true;
        this.commitButtonNode.hidden = true;
        this.removeClass(ERROR_CLASS);
        var model = this.editor.model;
        var content = this._getContent();
        this._changeGuard = true;
        if (content === void 0) {
            model.value.text = 'No data!';
            this._originalValue = null;
        }
        else {
            var value = JSON.stringify(content, null, 2);
            model.value.text = value;
            this._originalValue = content;
        }
        this.editor.refresh();
        this._changeGuard = false;
        this.commitButtonNode.hidden = true;
        this.revertButtonNode.hidden = true;
    };
    return JSONEditorWidget;
}(widgets_1.Widget));
exports.JSONEditorWidget = JSONEditorWidget;
/**
 * The namespace for module private data.
 */
var Private;
(function (Private) {
    /**
     * Create the node for the EditorWdiget.
     */
    function createEditorNode() {
        var cancelTitle = 'Revert changes to data';
        var confirmTitle = 'Commit changes to data';
        return virtualdom_1.VirtualDOM.realize(virtualdom_1.h.div({ className: METADATA_CLASS }, virtualdom_1.h.div({ className: BUTTON_AREA_CLASS }, virtualdom_1.h.span({ className: REVERT_CLASS, title: cancelTitle }), virtualdom_1.h.span({ className: COMMIT_CLASS, title: confirmTitle })), virtualdom_1.h.div({ className: HOST_CLASS })));
    }
    Private.createEditorNode = createEditorNode;
})(Private || (Private = {}));

// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var signaling_1 = require("@phosphor/signaling");
var rendermime_1 = require("@jupyterlab/rendermime");
/**
 * An object that handles code inspection.
 */
var InspectionHandler = (function () {
    /**
     * Construct a new inspection handler for a widget.
     */
    function InspectionHandler(options) {
        this._disposed = new signaling_1.Signal(this);
        this._editor = null;
        this._ephemeralCleared = new signaling_1.Signal(this);
        this._inspected = new signaling_1.Signal(this);
        this._pending = 0;
        this._rendermime = null;
        this._standby = true;
        this.session = options.session;
        this._rendermime = options.rendermime;
    }
    Object.defineProperty(InspectionHandler.prototype, "disposed", {
        /**
         * A signal emitted when the handler is disposed.
         */
        get: function () {
            return this._disposed;
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(InspectionHandler.prototype, "ephemeralCleared", {
        /**
         * A signal emitted when inspector should clear all items with no history.
         */
        get: function () {
            return this._ephemeralCleared;
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(InspectionHandler.prototype, "inspected", {
        /**
         * A signal emitted when an inspector value is generated.
         */
        get: function () {
            return this._inspected;
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(InspectionHandler.prototype, "editor", {
        /**
         * The editor widget used by the inspection handler.
         */
        get: function () {
            return this._editor;
        },
        set: function (newValue) {
            if (newValue === this._editor) {
                return;
            }
            if (this._editor && !this._editor.isDisposed) {
                this._editor.model.value.changed.disconnect(this.onTextChanged, this);
            }
            var editor = this._editor = newValue;
            if (editor) {
                // Clear ephemeral inspectors in preparation for a new editor.
                this._ephemeralCleared.emit(void 0);
                editor.model.value.changed.connect(this.onTextChanged, this);
            }
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(InspectionHandler.prototype, "standby", {
        /**
         * Indicates whether the handler makes API inspection requests or stands by.
         *
         * #### Notes
         * The use case for this attribute is to limit the API traffic when no
         * inspector is visible.
         */
        get: function () {
            return this._standby;
        },
        set: function (value) {
            this._standby = value;
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(InspectionHandler.prototype, "isDisposed", {
        /**
         * Get whether the inspection handler is disposed.
         *
         * #### Notes
         * This is a read-only property.
         */
        get: function () {
            return this._editor === null;
        },
        enumerable: true,
        configurable: true
    });
    /**
     * Dispose of the resources used by the handler.
     */
    InspectionHandler.prototype.dispose = function () {
        if (this._editor === null) {
            return;
        }
        this._editor = null;
        this._rendermime = null;
        this._disposed.emit(void 0);
        signaling_1.Signal.clearData(this);
    };
    /**
     * Handle a text changed signal from an editor.
     *
     * #### Notes
     * Update the hints inspector based on a text change.
     */
    InspectionHandler.prototype.onTextChanged = function () {
        var _this = this;
        // If the handler is in standby mode, bail.
        if (this._standby) {
            return;
        }
        var editor = this.editor;
        var code = editor.model.value.text;
        var position = editor.getCursorPosition();
        var offset = editor.getOffsetAt(position);
        var update = { content: null, type: 'hints' };
        // Clear hints if the new text value is empty or kernel is unavailable.
        if (!code || !this.session.kernel) {
            this._inspected.emit(update);
            return;
        }
        var contents = {
            code: code,
            cursor_pos: offset,
            detail_level: 0
        };
        var pending = ++this._pending;
        this.session.kernel.requestInspect(contents).then(function (msg) {
            var value = msg.content;
            // If handler has been disposed, bail.
            if (_this.isDisposed) {
                _this._inspected.emit(update);
                return;
            }
            // If a newer text change has created a pending request, bail.
            if (pending !== _this._pending) {
                _this._inspected.emit(update);
                return;
            }
            // Hint request failures or negative results fail silently.
            if (value.status !== 'ok' || !value.found) {
                _this._inspected.emit(update);
                return;
            }
            var data = value.data;
            var trusted = true;
            var model = new rendermime_1.MimeModel({ data: data, trusted: trusted });
            update.content = _this._rendermime.render(model);
            _this._inspected.emit(update);
        });
    };
    return InspectionHandler;
}());
exports.InspectionHandler = InspectionHandler;

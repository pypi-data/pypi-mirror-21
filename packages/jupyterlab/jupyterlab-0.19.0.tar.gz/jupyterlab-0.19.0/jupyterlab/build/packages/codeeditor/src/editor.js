// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var signaling_1 = require("@phosphor/signaling");
var coreutils_1 = require("@jupyterlab/coreutils");
var coreutils_2 = require("@jupyterlab/coreutils");
/**
 * A namespace for code editors.
 *
 * #### Notes
 * - A code editor is a set of common assumptions which hold for all concrete editors.
 * - Changes in implementations of the code editor should only be caused by changes in concrete editors.
 * - Common JLab services which are based on the code editor should belong to `IEditorServices`.
 */
var CodeEditor;
(function (CodeEditor) {
    /**
     * The default implementation of the editor model.
     */
    var Model = (function () {
        /**
         * Construct a new Model.
         */
        function Model(options) {
            this._selections = new coreutils_2.ObservableMap();
            this._isDisposed = false;
            this._mimeTypeChanged = new signaling_1.Signal(this);
            options = options || {};
            this._value = new coreutils_1.ObservableString(options.value);
            this._mimetype = options.mimeType || 'text/plain';
        }
        Object.defineProperty(Model.prototype, "mimeTypeChanged", {
            /**
             * A signal emitted when a mimetype changes.
             */
            get: function () {
                return this._mimeTypeChanged;
            },
            enumerable: true,
            configurable: true
        });
        Object.defineProperty(Model.prototype, "value", {
            /**
             * Get the value of the model.
             */
            get: function () {
                return this._value;
            },
            enumerable: true,
            configurable: true
        });
        Object.defineProperty(Model.prototype, "selections", {
            /**
             * Get the selections for the model.
             */
            get: function () {
                return this._selections;
            },
            enumerable: true,
            configurable: true
        });
        Object.defineProperty(Model.prototype, "mimeType", {
            /**
             * A mime type of the model.
             */
            get: function () {
                return this._mimetype;
            },
            set: function (newValue) {
                var oldValue = this._mimetype;
                if (oldValue === newValue) {
                    return;
                }
                this._mimetype = newValue;
                this._mimeTypeChanged.emit({
                    name: 'mimeType',
                    oldValue: oldValue,
                    newValue: newValue
                });
            },
            enumerable: true,
            configurable: true
        });
        Object.defineProperty(Model.prototype, "isDisposed", {
            /**
             * Whether the model is disposed.
             */
            get: function () {
                return this._isDisposed;
            },
            enumerable: true,
            configurable: true
        });
        /**
         * Dipose of the resources used by the model.
         */
        Model.prototype.dispose = function () {
            if (this._isDisposed) {
                return;
            }
            this._isDisposed = true;
            signaling_1.Signal.clearData(this);
            this._selections.dispose();
            this._value.dispose();
        };
        return Model;
    }());
    CodeEditor.Model = Model;
})(CodeEditor = exports.CodeEditor || (exports.CodeEditor = {}));

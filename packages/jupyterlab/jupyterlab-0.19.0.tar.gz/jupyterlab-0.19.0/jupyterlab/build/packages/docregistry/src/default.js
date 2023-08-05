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
var codemirror_1 = require("@jupyterlab/codemirror");
var signaling_1 = require("@phosphor/signaling");
var codeeditor_1 = require("@jupyterlab/codeeditor");
/**
 * The default implementation of a document model.
 */
var DocumentModel = (function (_super) {
    __extends(DocumentModel, _super);
    /**
     * Construct a new document model.
     */
    function DocumentModel(languagePreference) {
        var _this = _super.call(this) || this;
        _this._defaultLang = '';
        _this._dirty = false;
        _this._readOnly = false;
        _this._contentChanged = new signaling_1.Signal(_this);
        _this._stateChanged = new signaling_1.Signal(_this);
        _this._defaultLang = languagePreference || '';
        _this.value.changed.connect(_this.triggerContentChange, _this);
        return _this;
    }
    Object.defineProperty(DocumentModel.prototype, "contentChanged", {
        /**
         * A signal emitted when the document content changes.
         */
        get: function () {
            return this._contentChanged;
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(DocumentModel.prototype, "stateChanged", {
        /**
         * A signal emitted when the document state changes.
         */
        get: function () {
            return this._stateChanged;
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(DocumentModel.prototype, "dirty", {
        /**
         * The dirty state of the document.
         */
        get: function () {
            return this._dirty;
        },
        set: function (newValue) {
            if (newValue === this._dirty) {
                return;
            }
            var oldValue = this._dirty;
            this._dirty = newValue;
            this.triggerStateChange({ name: 'dirty', oldValue: oldValue, newValue: newValue });
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(DocumentModel.prototype, "readOnly", {
        /**
         * The read only state of the document.
         */
        get: function () {
            return this._readOnly;
        },
        set: function (newValue) {
            if (newValue === this._readOnly) {
                return;
            }
            var oldValue = this._readOnly;
            this._readOnly = newValue;
            this.triggerStateChange({ name: 'readOnly', oldValue: oldValue, newValue: newValue });
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(DocumentModel.prototype, "defaultKernelName", {
        /**
         * The default kernel name of the document.
         *
         * #### Notes
         * This is a read-only property.
         */
        get: function () {
            return '';
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(DocumentModel.prototype, "defaultKernelLanguage", {
        /**
         * The default kernel language of the document.
         *
         * #### Notes
         * This is a read-only property.
         */
        get: function () {
            return this._defaultLang;
        },
        enumerable: true,
        configurable: true
    });
    /**
     * Serialize the model to a string.
     */
    DocumentModel.prototype.toString = function () {
        return this.value.text;
    };
    /**
     * Deserialize the model from a string.
     *
     * #### Notes
     * Should emit a [contentChanged] signal.
     */
    DocumentModel.prototype.fromString = function (value) {
        this.value.text = value;
    };
    /**
     * Serialize the model to JSON.
     */
    DocumentModel.prototype.toJSON = function () {
        return JSON.stringify(this.value.text);
    };
    /**
     * Deserialize the model from JSON.
     *
     * #### Notes
     * Should emit a [contentChanged] signal.
     */
    DocumentModel.prototype.fromJSON = function (value) {
        this.fromString(JSON.parse(value));
    };
    /**
     * Trigger a state change signal.
     */
    DocumentModel.prototype.triggerStateChange = function (args) {
        this._stateChanged.emit(args);
    };
    /**
     * Trigger a content changed signal.
     */
    DocumentModel.prototype.triggerContentChange = function () {
        this._contentChanged.emit(void 0);
        this.dirty = true;
    };
    return DocumentModel;
}(codeeditor_1.CodeEditor.Model));
exports.DocumentModel = DocumentModel;
/**
 * An implementation of a model factory for text files.
 */
var TextModelFactory = (function () {
    function TextModelFactory() {
        this._isDisposed = false;
    }
    Object.defineProperty(TextModelFactory.prototype, "name", {
        /**
         * The name of the model type.
         *
         * #### Notes
         * This is a read-only property.
         */
        get: function () {
            return 'text';
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(TextModelFactory.prototype, "contentType", {
        /**
         * The type of the file.
         *
         * #### Notes
         * This is a read-only property.
         */
        get: function () {
            return 'file';
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(TextModelFactory.prototype, "fileFormat", {
        /**
         * The format of the file.
         *
         * This is a read-only property.
         */
        get: function () {
            return 'text';
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(TextModelFactory.prototype, "isDisposed", {
        /**
         * Get whether the model factory has been disposed.
         */
        get: function () {
            return this._isDisposed;
        },
        enumerable: true,
        configurable: true
    });
    /**
     * Dispose of the resources held by the model factory.
     */
    TextModelFactory.prototype.dispose = function () {
        this._isDisposed = true;
    };
    /**
     * Create a new model.
     *
     * @param languagePreference - An optional kernel language preference.
     *
     * @returns A new document model.
     */
    TextModelFactory.prototype.createNew = function (languagePreference) {
        return new DocumentModel(languagePreference);
    };
    /**
     * Get the preferred kernel language given an extension.
     */
    TextModelFactory.prototype.preferredLanguage = function (ext) {
        return codemirror_1.findModeByExtension(ext.slice(1));
    };
    return TextModelFactory;
}());
exports.TextModelFactory = TextModelFactory;
/**
 * An implementation of a model factory for base64 files.
 */
var Base64ModelFactory = (function (_super) {
    __extends(Base64ModelFactory, _super);
    function Base64ModelFactory() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    Object.defineProperty(Base64ModelFactory.prototype, "name", {
        /**
         * The name of the model type.
         *
         * #### Notes
         * This is a read-only property.
         */
        get: function () {
            return 'base64';
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(Base64ModelFactory.prototype, "contentType", {
        /**
         * The type of the file.
         *
         * #### Notes
         * This is a read-only property.
         */
        get: function () {
            return 'file';
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(Base64ModelFactory.prototype, "fileFormat", {
        /**
         * The format of the file.
         *
         * This is a read-only property.
         */
        get: function () {
            return 'base64';
        },
        enumerable: true,
        configurable: true
    });
    return Base64ModelFactory;
}(TextModelFactory));
exports.Base64ModelFactory = Base64ModelFactory;
/**
 * The default implemetation of a widget factory.
 */
var ABCWidgetFactory = (function () {
    /**
     * Construct a new `ABCWidgetFactory`.
     */
    function ABCWidgetFactory(options) {
        this._isDisposed = false;
        this._widgetCreated = new signaling_1.Signal(this);
        this._name = options.name;
        this._defaultFor = options.defaultFor ? options.defaultFor.slice() : [];
        this._fileExtensions = options.fileExtensions.slice();
        this._modelName = options.modelName || 'text';
        this._preferKernel = !!options.preferKernel;
        this._canStartKernel = !!options.canStartKernel;
    }
    Object.defineProperty(ABCWidgetFactory.prototype, "widgetCreated", {
        /**
         * A signal emitted when a widget is created.
         */
        get: function () {
            return this._widgetCreated;
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(ABCWidgetFactory.prototype, "isDisposed", {
        /**
         * Get whether the model factory has been disposed.
         */
        get: function () {
            return this._isDisposed;
        },
        enumerable: true,
        configurable: true
    });
    /**
     * Dispose of the resources held by the document manager.
     */
    ABCWidgetFactory.prototype.dispose = function () {
        this._isDisposed = true;
    };
    Object.defineProperty(ABCWidgetFactory.prototype, "name", {
        /**
         * The name of the widget to display in dialogs.
         */
        get: function () {
            return this._name;
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(ABCWidgetFactory.prototype, "fileExtensions", {
        /**
         * The file extensions the widget can view.
         */
        get: function () {
            return this._fileExtensions.slice();
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(ABCWidgetFactory.prototype, "modelName", {
        /**
         * The registered name of the model type used to create the widgets.
         */
        get: function () {
            return this._modelName;
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(ABCWidgetFactory.prototype, "defaultFor", {
        /**
         * The file extensions for which the factory should be the default.
         */
        get: function () {
            return this._defaultFor.slice();
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(ABCWidgetFactory.prototype, "preferKernel", {
        /**
         * Whether the widgets prefer having a kernel started.
         */
        get: function () {
            return this._preferKernel;
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(ABCWidgetFactory.prototype, "canStartKernel", {
        /**
         * Whether the widgets can start a kernel when opened.
         */
        get: function () {
            return this._canStartKernel;
        },
        enumerable: true,
        configurable: true
    });
    /**
     * Create a new widget given a document model and a context.
     *
     * #### Notes
     * It should emit the [widgetCreated] signal with the new widget.
     */
    ABCWidgetFactory.prototype.createNew = function (context) {
        var widget = this.createNewWidget(context);
        this._widgetCreated.emit(widget);
        return widget;
    };
    return ABCWidgetFactory;
}());
exports.ABCWidgetFactory = ABCWidgetFactory;

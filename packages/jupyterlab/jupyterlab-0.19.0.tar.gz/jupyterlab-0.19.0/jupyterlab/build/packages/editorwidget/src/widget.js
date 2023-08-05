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
var docregistry_1 = require("@jupyterlab/docregistry");
var codeeditor_1 = require("@jupyterlab/codeeditor");
/**
 * The class name added to a dirty widget.
 */
var DIRTY_CLASS = 'jp-mod-dirty';
/**
 * The class name added to a jupyter editor widget.
 */
var EDITOR_CLASS = 'jp-EditorWidget';
/**
 * A document widget for editors.
 */
var EditorWidget = (function (_super) {
    __extends(EditorWidget, _super);
    /**
     * Construct a new editor widget.
     */
    function EditorWidget(options) {
        var _this = _super.call(this, {
            factory: options.factory,
            model: options.context.model
        }) || this;
        var context = _this._context = options.context;
        var editor = _this.editor;
        _this.addClass(EDITOR_CLASS);
        _this._mimeTypeService = options.mimeTypeService;
        editor.model.value.text = context.model.toString();
        context.pathChanged.connect(_this._onPathChanged, _this);
        context.ready.then(function () { _this._onContextReady(); });
        _this._onPathChanged();
        return _this;
    }
    Object.defineProperty(EditorWidget.prototype, "context", {
        /**
         * Get the context for the editor widget.
         */
        get: function () {
            return this._context;
        },
        enumerable: true,
        configurable: true
    });
    /**
     * Handle actions that should be taken when the context is ready.
     */
    EditorWidget.prototype._onContextReady = function () {
        if (this.isDisposed) {
            return;
        }
        var contextModel = this._context.model;
        var editor = this.editor;
        var editorModel = editor.model;
        // Set the editor model value.
        editorModel.value.text = contextModel.toString();
        // Prevent the initial loading from disk from being in the editor history.
        editor.clearHistory();
        this._handleDirtyState();
        // Wire signal connections.
        contextModel.stateChanged.connect(this._onModelStateChanged, this);
        contextModel.contentChanged.connect(this._onContentChanged, this);
    };
    /**
     * Handle a change to the context model state.
     */
    EditorWidget.prototype._onModelStateChanged = function (sender, args) {
        if (args.name === 'dirty') {
            this._handleDirtyState();
        }
    };
    /**
     * Handle the dirty state of the context model.
     */
    EditorWidget.prototype._handleDirtyState = function () {
        if (this._context.model.dirty) {
            this.title.className += " " + DIRTY_CLASS;
        }
        else {
            this.title.className = this.title.className.replace(DIRTY_CLASS, '');
        }
    };
    /**
     * Handle a change in context model content.
     */
    EditorWidget.prototype._onContentChanged = function () {
        var editorModel = this.editor.model;
        var oldValue = editorModel.value.text;
        var newValue = this._context.model.toString();
        if (oldValue !== newValue) {
            editorModel.value.text = newValue;
        }
    };
    /**
     * Handle a change to the path.
     */
    EditorWidget.prototype._onPathChanged = function () {
        var editor = this.editor;
        var path = this._context.path;
        editor.model.mimeType = this._mimeTypeService.getMimeTypeByFilePath(path);
        this.title.label = path.split('/').pop();
    };
    return EditorWidget;
}(codeeditor_1.CodeEditorWidget));
exports.EditorWidget = EditorWidget;
/**
 * A widget factory for editors.
 */
var EditorWidgetFactory = (function (_super) {
    __extends(EditorWidgetFactory, _super);
    /**
     * Construct a new editor widget factory.
     */
    function EditorWidgetFactory(options) {
        var _this = _super.call(this, options.factoryOptions) || this;
        _this._services = options.editorServices;
        return _this;
    }
    /**
     * Create a new widget given a context.
     */
    EditorWidgetFactory.prototype.createNewWidget = function (context) {
        var func = this._services.factoryService.newDocumentEditor.bind(this._services.factoryService);
        var factory = function (options) {
            options.lineNumbers = true;
            options.readOnly = false;
            options.wordWrap = true;
            return func(options);
        };
        return new EditorWidget({
            factory: factory,
            context: context,
            mimeTypeService: this._services.mimeTypeService
        });
    };
    return EditorWidgetFactory;
}(docregistry_1.ABCWidgetFactory));
exports.EditorWidgetFactory = EditorWidgetFactory;

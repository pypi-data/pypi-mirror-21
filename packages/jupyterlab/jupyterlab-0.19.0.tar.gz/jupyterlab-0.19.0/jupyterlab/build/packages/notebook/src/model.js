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
var algorithm_1 = require("@phosphor/algorithm");
var docregistry_1 = require("@jupyterlab/docregistry");
var cells_1 = require("@jupyterlab/cells");
var coreutils_1 = require("@jupyterlab/coreutils");
var celllist_1 = require("./celllist");
/**
 * An implementation of a notebook Model.
 */
var NotebookModel = (function (_super) {
    __extends(NotebookModel, _super);
    /**
     * Construct a new notebook model.
     */
    function NotebookModel(options) {
        if (options === void 0) { options = {}; }
        var _this = _super.call(this, options.languagePreference) || this;
        _this._cells = null;
        _this._nbformat = coreutils_1.nbformat.MAJOR_VERSION;
        _this._nbformatMinor = coreutils_1.nbformat.MINOR_VERSION;
        _this._metadata = new coreutils_1.ObservableJSON();
        var factory = (options.contentFactory || NotebookModel.defaultContentFactory);
        _this.contentFactory = factory;
        _this._cells = new celllist_1.CellList();
        // Add an initial code cell by default.
        _this._cells.pushBack(factory.createCodeCell({}));
        _this._cells.changed.connect(_this._onCellsChanged, _this);
        // Handle initial metadata.
        var name = options.languagePreference || '';
        _this._metadata.set('language_info', { name: name });
        _this._ensureMetadata();
        _this._metadata.changed.connect(_this.triggerContentChange, _this);
        return _this;
    }
    Object.defineProperty(NotebookModel.prototype, "metadata", {
        /**
         * The metadata associated with the notebook.
         */
        get: function () {
            return this._metadata;
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(NotebookModel.prototype, "cells", {
        /**
         * Get the observable list of notebook cells.
         */
        get: function () {
            return this._cells;
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(NotebookModel.prototype, "nbformat", {
        /**
         * The major version number of the nbformat.
         */
        get: function () {
            return this._nbformat;
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(NotebookModel.prototype, "nbformatMinor", {
        /**
         * The minor version number of the nbformat.
         */
        get: function () {
            return this._nbformatMinor;
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(NotebookModel.prototype, "defaultKernelName", {
        /**
         * The default kernel name of the document.
         */
        get: function () {
            var spec = this._metadata.get('kernelspec');
            return spec ? spec.name : '';
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(NotebookModel.prototype, "defaultKernelLanguage", {
        /**
         * The default kernel language of the document.
         */
        get: function () {
            var info = this._metadata.get('language_info');
            return info ? info.name : '';
        },
        enumerable: true,
        configurable: true
    });
    /**
     * Dispose of the resources held by the model.
     */
    NotebookModel.prototype.dispose = function () {
        // Do nothing if already disposed.
        if (this._cells === null) {
            return;
        }
        var cells = this._cells;
        this._cells = null;
        this._metadata.dispose();
        cells.dispose();
        _super.prototype.dispose.call(this);
    };
    /**
     * Serialize the model to a string.
     */
    NotebookModel.prototype.toString = function () {
        return JSON.stringify(this.toJSON());
    };
    /**
     * Deserialize the model from a string.
     *
     * #### Notes
     * Should emit a [contentChanged] signal.
     */
    NotebookModel.prototype.fromString = function (value) {
        this.fromJSON(JSON.parse(value));
    };
    /**
     * Serialize the model to JSON.
     */
    NotebookModel.prototype.toJSON = function () {
        var cells = [];
        for (var i = 0; i < this.cells.length; i++) {
            var cell = this.cells.at(i);
            cells.push(cell.toJSON());
        }
        this._ensureMetadata();
        var metadata = Object.create(null);
        for (var _i = 0, _a = this.metadata.keys(); _i < _a.length; _i++) {
            var key = _a[_i];
            metadata[key] = JSON.parse(JSON.stringify(this.metadata.get(key)));
        }
        return {
            metadata: metadata,
            nbformat_minor: this._nbformatMinor,
            nbformat: this._nbformat,
            cells: cells
        };
    };
    /**
     * Deserialize the model from JSON.
     *
     * #### Notes
     * Should emit a [contentChanged] signal.
     */
    NotebookModel.prototype.fromJSON = function (value) {
        var cells = [];
        var factory = this.contentFactory;
        for (var _i = 0, _a = value.cells; _i < _a.length; _i++) {
            var cell = _a[_i];
            switch (cell.cell_type) {
                case 'code':
                    cells.push(factory.createCodeCell({ cell: cell }));
                    break;
                case 'markdown':
                    cells.push(factory.createMarkdownCell({ cell: cell }));
                    break;
                case 'raw':
                    cells.push(factory.createRawCell({ cell: cell }));
                    break;
                default:
                    continue;
            }
        }
        this.cells.beginCompoundOperation();
        this.cells.clear();
        this.cells.pushAll(cells);
        this.cells.endCompoundOperation();
        var oldValue = 0;
        var newValue = 0;
        this._nbformatMinor = coreutils_1.nbformat.MINOR_VERSION;
        this._nbformat = coreutils_1.nbformat.MAJOR_VERSION;
        if (value.nbformat !== this._nbformat) {
            oldValue = this._nbformat;
            this._nbformat = newValue = value.nbformat;
            this.triggerStateChange({ name: 'nbformat', oldValue: oldValue, newValue: newValue });
        }
        if (value.nbformat_minor > this._nbformatMinor) {
            oldValue = this._nbformatMinor;
            this._nbformatMinor = newValue = value.nbformat_minor;
            this.triggerStateChange({ name: 'nbformatMinor', oldValue: oldValue, newValue: newValue });
        }
        // Update the metadata.
        this._metadata.clear();
        var metadata = value.metadata;
        for (var key in metadata) {
            // orig_nbformat is not intended to be stored per spec.
            if (key === 'orig_nbformat') {
                continue;
            }
            this._metadata.set(key, metadata[key]);
        }
        this._ensureMetadata();
        this.dirty = true;
    };
    /**
     * Handle a change in the cells list.
     */
    NotebookModel.prototype._onCellsChanged = function (list, change) {
        var _this = this;
        switch (change.type) {
            case 'add':
                algorithm_1.each(change.newValues, function (cell) {
                    cell.contentChanged.connect(_this.triggerContentChange, _this);
                });
                break;
            case 'remove':
                algorithm_1.each(change.oldValues, function (cell) {
                });
                break;
            case 'set':
                algorithm_1.each(change.newValues, function (cell) {
                    cell.contentChanged.connect(_this.triggerContentChange, _this);
                });
                algorithm_1.each(change.oldValues, function (cell) {
                });
                break;
            default:
                return;
        }
        var factory = this.contentFactory;
        // Add code cell if there are no cells remaining.
        if (!this._cells.length) {
            // Add the cell in a new context to avoid triggering another
            // cell changed event during the handling of this signal.
            requestAnimationFrame(function () {
                if (!_this.isDisposed && !_this._cells.length) {
                    _this._cells.pushBack(factory.createCodeCell({}));
                }
            });
        }
        this.triggerContentChange();
    };
    /**
     * Make sure we have the required metadata fields.
     */
    NotebookModel.prototype._ensureMetadata = function () {
        var metadata = this._metadata;
        if (!metadata.has('language_info')) {
            metadata.set('language_info', { name: '' });
        }
        if (!metadata.has('kernelspec')) {
            metadata.set('kernelspec', { name: '', display_name: '' });
        }
    };
    return NotebookModel;
}(docregistry_1.DocumentModel));
exports.NotebookModel = NotebookModel;
/**
 * The namespace for the `NotebookModel` class statics.
 */
(function (NotebookModel) {
    /**
     * The default implementation of an `IContentFactory`.
     */
    var ContentFactory = (function () {
        /**
         * Create a new cell model factory.
         */
        function ContentFactory(options) {
            this.codeCellContentFactory = (options.codeCellContentFactory ||
                cells_1.CodeCellModel.defaultContentFactory);
        }
        /**
         * Create a new code cell.
         *
         * @param source - The data to use for the original source data.
         *
         * @returns A new code cell. If a source cell is provided, the
         *   new cell will be intialized with the data from the source.
         *   If the contentFactory is not provided, the instance
         *   `codeCellContentFactory` will be used.
         */
        ContentFactory.prototype.createCodeCell = function (options) {
            if (options.contentFactory) {
                options.contentFactory = this.codeCellContentFactory;
            }
            return new cells_1.CodeCellModel(options);
        };
        /**
         * Create a new markdown cell.
         *
         * @param source - The data to use for the original source data.
         *
         * @returns A new markdown cell. If a source cell is provided, the
         *   new cell will be intialized with the data from the source.
         */
        ContentFactory.prototype.createMarkdownCell = function (options) {
            return new cells_1.MarkdownCellModel(options);
        };
        /**
         * Create a new raw cell.
         *
         * @param source - The data to use for the original source data.
         *
         * @returns A new raw cell. If a source cell is provided, the
         *   new cell will be intialized with the data from the source.
         */
        ContentFactory.prototype.createRawCell = function (options) {
            return new cells_1.RawCellModel(options);
        };
        return ContentFactory;
    }());
    NotebookModel.ContentFactory = ContentFactory;
    /**
     * The default `ContentFactory` instance.
     */
    NotebookModel.defaultContentFactory = new ContentFactory({});
})(NotebookModel = exports.NotebookModel || (exports.NotebookModel = {}));
exports.NotebookModel = NotebookModel;

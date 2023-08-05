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
var signaling_1 = require("@phosphor/signaling");
var codeeditor_1 = require("@jupyterlab/codeeditor");
var coreutils_2 = require("@jupyterlab/coreutils");
var outputarea_1 = require("@jupyterlab/outputarea");
/**
 * An implementation of the cell model.
 */
var CellModel = (function (_super) {
    __extends(CellModel, _super);
    /**
     * Construct a cell model from optional cell content.
     */
    function CellModel(options) {
        var _this = _super.call(this) || this;
        /**
         * A signal emitted when the state of the model changes.
         */
        _this.contentChanged = new signaling_1.Signal(_this);
        /**
         * A signal emitted when a model state changes.
         */
        _this.stateChanged = new signaling_1.Signal(_this);
        _this._metadata = new coreutils_2.ObservableJSON();
        _this._trusted = false;
        _this.value.changed.connect(_this.onGenericChange, _this);
        var cell = options.cell;
        if (!cell) {
            return _this;
        }
        _this._trusted = !!cell.metadata['trusted'];
        delete cell.metadata['trusted'];
        if (Array.isArray(cell.source)) {
            _this.value.text = cell.source.join('\n');
        }
        else {
            _this.value.text = cell.source;
        }
        var metadata = coreutils_1.JSONExt.deepCopy(cell.metadata);
        if (_this.type !== 'raw') {
            delete metadata['format'];
        }
        if (_this.type !== 'code') {
            delete metadata['collapsed'];
            delete metadata['scrolled'];
        }
        for (var key in metadata) {
            _this._metadata.set(key, metadata[key]);
        }
        _this._metadata.changed.connect(_this.onGenericChange, _this);
        return _this;
    }
    Object.defineProperty(CellModel.prototype, "metadata", {
        /**
         * The metadata associated with the cell.
         */
        get: function () {
            return this._metadata;
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(CellModel.prototype, "trusted", {
        /**
         * Get the trusted state of the model.
         */
        get: function () {
            return this._trusted;
        },
        /**
         * Set the trusted state of the model.
         */
        set: function (newValue) {
            if (this._trusted === newValue) {
                return;
            }
            var oldValue = this._trusted;
            this._trusted = newValue;
            this.onTrustedChanged(newValue);
            this.stateChanged.emit({ name: 'trusted', oldValue: oldValue, newValue: newValue });
        },
        enumerable: true,
        configurable: true
    });
    /**
     * Dispose of the resources held by the model.
     */
    CellModel.prototype.dispose = function () {
        this._metadata.dispose();
        _super.prototype.dispose.call(this);
    };
    /**
     * Serialize the model to JSON.
     */
    CellModel.prototype.toJSON = function () {
        var metadata = Object.create(null);
        for (var _i = 0, _a = this.metadata.keys(); _i < _a.length; _i++) {
            var key = _a[_i];
            var value = JSON.parse(JSON.stringify(this.metadata.get(key)));
            metadata[key] = value;
        }
        if (this.trusted) {
            metadata['trusted'] = true;
        }
        return {
            cell_type: this.type,
            source: this.value.text,
            metadata: metadata,
        };
    };
    /**
     * Handle a change to the trusted state.
     *
     * The default implementation is a no-op.
     */
    CellModel.prototype.onTrustedChanged = function (value) { };
    /**
     * Handle a change to the observable value.
     */
    CellModel.prototype.onGenericChange = function () {
        this.contentChanged.emit(void 0);
    };
    return CellModel;
}(codeeditor_1.CodeEditor.Model));
exports.CellModel = CellModel;
/**
 * An implementation of a raw cell model.
 */
var RawCellModel = (function (_super) {
    __extends(RawCellModel, _super);
    function RawCellModel() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    Object.defineProperty(RawCellModel.prototype, "type", {
        /**
         * The type of the cell.
         */
        get: function () {
            return 'raw';
        },
        enumerable: true,
        configurable: true
    });
    return RawCellModel;
}(CellModel));
exports.RawCellModel = RawCellModel;
/**
 * An implementation of a markdown cell model.
 */
var MarkdownCellModel = (function (_super) {
    __extends(MarkdownCellModel, _super);
    /**
     * Construct a markdown cell model from optional cell content.
     */
    function MarkdownCellModel(options) {
        var _this = _super.call(this, options) || this;
        // Use the Github-flavored markdown mode.
        _this.mimeType = 'text/x-ipythongfm';
        return _this;
    }
    Object.defineProperty(MarkdownCellModel.prototype, "type", {
        /**
         * The type of the cell.
         */
        get: function () {
            return 'markdown';
        },
        enumerable: true,
        configurable: true
    });
    return MarkdownCellModel;
}(CellModel));
exports.MarkdownCellModel = MarkdownCellModel;
/**
 * An implementation of a code cell Model.
 */
var CodeCellModel = (function (_super) {
    __extends(CodeCellModel, _super);
    /**
     * Construct a new code cell with optional original cell content.
     */
    function CodeCellModel(options) {
        var _this = _super.call(this, options) || this;
        _this._outputs = null;
        _this._executionCount = null;
        var factory = (options.contentFactory ||
            CodeCellModel.defaultContentFactory);
        var trusted = _this.trusted;
        var cell = options.cell;
        var outputs = [];
        if (cell && cell.cell_type === 'code') {
            _this.executionCount = cell.execution_count;
            outputs = cell.outputs;
        }
        _this._outputs = factory.createOutputArea({
            trusted: trusted,
            values: outputs
        });
        _this._outputs.stateChanged.connect(_this.onGenericChange, _this);
        return _this;
    }
    Object.defineProperty(CodeCellModel.prototype, "type", {
        /**
         * The type of the cell.
         */
        get: function () {
            return 'code';
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(CodeCellModel.prototype, "executionCount", {
        /**
         * The execution count of the cell.
         */
        get: function () {
            return this._executionCount || null;
        },
        set: function (newValue) {
            if (newValue === this._executionCount) {
                return;
            }
            var oldValue = this.executionCount;
            this._executionCount = newValue || null;
            this.contentChanged.emit(void 0);
            this.stateChanged.emit({ name: 'executionCount', oldValue: oldValue, newValue: newValue });
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(CodeCellModel.prototype, "outputs", {
        /**
         * The cell outputs.
         */
        get: function () {
            return this._outputs;
        },
        enumerable: true,
        configurable: true
    });
    /**
     * Dispose of the resources held by the model.
     */
    CodeCellModel.prototype.dispose = function () {
        if (this.isDisposed) {
            return;
        }
        this._outputs.dispose();
        this._outputs = null;
        _super.prototype.dispose.call(this);
    };
    /**
     * Serialize the model to JSON.
     */
    CodeCellModel.prototype.toJSON = function () {
        var cell = _super.prototype.toJSON.call(this);
        cell.execution_count = this.executionCount || null;
        cell.outputs = this.outputs.toJSON();
        return cell;
    };
    /**
     * Handle a change to the trusted state.
     *
     * The default implementation is a no-op.
     */
    CodeCellModel.prototype.onTrustedChanged = function (value) {
        this._outputs.trusted = value;
    };
    return CodeCellModel;
}(CellModel));
exports.CodeCellModel = CodeCellModel;
/**
 * The namespace for `CodeCellModel` statics.
 */
(function (CodeCellModel) {
    /**
     * The default implementation of an `IContentFactory`.
     */
    var ContentFactory = (function () {
        function ContentFactory() {
        }
        /**
         * Create an output area.
         */
        ContentFactory.prototype.createOutputArea = function (options) {
            return new outputarea_1.OutputAreaModel(options);
        };
        return ContentFactory;
    }());
    CodeCellModel.ContentFactory = ContentFactory;
    /**
     * The shared `ConetntFactory` instance.
     */
    CodeCellModel.defaultContentFactory = new ContentFactory();
})(CodeCellModel = exports.CodeCellModel || (exports.CodeCellModel = {}));
exports.CodeCellModel = CodeCellModel;

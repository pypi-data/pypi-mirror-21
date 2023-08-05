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
var docregistry_1 = require("@jupyterlab/docregistry");
var table_1 = require("./table");
var toolbar_1 = require("./toolbar");
/**
 * The class name added to a CSV widget.
 */
var CSV_CLASS = 'jp-CSVWidget';
/**
 * The class name added to a CSV widget warning.
 */
var CSV_WARNING_CLASS = 'jp-CSVWidget-warning';
/**
 * A widget for CSV tables.
 */
var CSVWidget = (function (_super) {
    __extends(CSVWidget, _super);
    /**
     * Construct a new CSV widget.
     */
    function CSVWidget(options) {
        var _this = _super.call(this) || this;
        _this._context = null;
        _this._model = null;
        _this._table = null;
        _this._toolbar = null;
        _this._warning = null;
        var context = _this._context = options.context;
        var layout = _this.layout = new widgets_1.PanelLayout();
        _this.addClass(CSV_CLASS);
        _this.title.label = context.path.split('/').pop();
        _this._warning = new widgets_2.Widget();
        _this._warning.addClass(CSV_WARNING_CLASS);
        _this._model = new table_1.CSVModel({ content: context.model.toString() });
        _this._table = new table_1.CSVTable();
        _this._table.model = _this._model;
        _this._model.maxExceeded.connect(_this._onMaxExceeded, _this);
        _this._toolbar = new toolbar_1.CSVToolbar();
        _this._toolbar.delimiterChanged.connect(_this._onDelimiterChanged, _this);
        layout.addWidget(_this._toolbar);
        layout.addWidget(_this._table);
        layout.addWidget(_this._warning);
        context.pathChanged.connect(_this._onPathChanged, _this);
        context.model.contentChanged.connect(_this._onContentChanged, _this);
        return _this;
    }
    Object.defineProperty(CSVWidget.prototype, "context", {
        /**
         * The CSV widget's context.
         */
        get: function () {
            return this._context;
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(CSVWidget.prototype, "model", {
        /**
         * The CSV data model.
         */
        get: function () {
            return this._model;
        },
        enumerable: true,
        configurable: true
    });
    /**
     * Dispose of the resources used by the widget.
     */
    CSVWidget.prototype.dispose = function () {
        if (this._model === null) {
            return;
        }
        var model = this._model;
        var table = this._table;
        var toolbar = this._toolbar;
        var warning = this._warning;
        this._model = null;
        this._table = null;
        this._toolbar = null;
        this._warning = null;
        model.dispose();
        table.dispose();
        toolbar.dispose();
        warning.dispose();
        _super.prototype.dispose.call(this);
    };
    /**
     * Handle `'activate-request'` messages.
     */
    CSVWidget.prototype.onActivateRequest = function (msg) {
        this.node.tabIndex = -1;
        this.node.focus();
    };
    /**
     * Handle a max exceeded in a csv widget.
     */
    CSVWidget.prototype._onMaxExceeded = function (sender, overflow) {
        var available = overflow.available, maximum = overflow.maximum;
        var message = "Table is too long to render,\n      rendering " + maximum + " of " + available + " rows";
        this._warning.node.textContent = message;
    };
    /**
     * Handle a change in delimiter.
     */
    CSVWidget.prototype._onDelimiterChanged = function (sender, delimiter) {
        this._table.model.delimiter = delimiter;
    };
    /**
     * Handle a change in content.
     */
    CSVWidget.prototype._onContentChanged = function () {
        this._table.model.content = this._context.model.toString();
    };
    /**
     * Handle a change in path.
     */
    CSVWidget.prototype._onPathChanged = function () {
        this.title.label = this._context.path.split('/').pop();
    };
    return CSVWidget;
}(widgets_2.Widget));
exports.CSVWidget = CSVWidget;
/**
 * A widget factory for CSV widgets.
 */
var CSVWidgetFactory = (function (_super) {
    __extends(CSVWidgetFactory, _super);
    function CSVWidgetFactory() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    /**
     * Create a new widget given a context.
     */
    CSVWidgetFactory.prototype.createNewWidget = function (context) {
        return new CSVWidget({ context: context });
    };
    return CSVWidgetFactory;
}(docregistry_1.ABCWidgetFactory));
exports.CSVWidgetFactory = CSVWidgetFactory;

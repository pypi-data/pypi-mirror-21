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
var dsv = require("d3-dsv");
var signaling_1 = require("@phosphor/signaling");
var virtualdom_1 = require("@phosphor/virtualdom");
var apputils_1 = require("@jupyterlab/apputils");
/**
 * The hard limit on the number of rows to display.
 */
exports.DISPLAY_LIMIT = 1000;
/**
 * The class name added to a csv table widget.
 */
var CSV_TABLE_CLASS = 'jp-CSVTable';
/**
 * A CSV table content model.
 */
var CSVModel = (function (_super) {
    __extends(CSVModel, _super);
    /**
     * Instantiate a CSV model.
     */
    function CSVModel(options) {
        if (options === void 0) { options = {}; }
        var _this = _super.call(this) || this;
        _this._maxExceeded = new signaling_1.Signal(_this);
        _this._content = options.content || '';
        _this._delimiter = options.delimiter || ',';
        return _this;
    }
    Object.defineProperty(CSVModel.prototype, "maxExceeded", {
        /**
         * A signal emitted when the parsed value's rows exceed the display limit. It
         * emits the length of the parsed value.
         */
        get: function () {
            return this._maxExceeded;
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(CSVModel.prototype, "content", {
        /**
         * The raw model content.
         */
        get: function () {
            return this._content;
        },
        set: function (content) {
            if (this._content === content) {
                return;
            }
            this._content = content;
            this.stateChanged.emit(void 0);
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(CSVModel.prototype, "delimiter", {
        /**
         * The CSV delimiter value.
         */
        get: function () {
            return this._delimiter;
        },
        set: function (delimiter) {
            if (this._delimiter === delimiter) {
                return;
            }
            this._delimiter = delimiter;
            this.stateChanged.emit(void 0);
        },
        enumerable: true,
        configurable: true
    });
    /**
     * Parse the content using the model's delimiter.
     *
     * #### Notes
     * This method will always return parsed content that has at most the display
     * limit worth of rows, currently maxing out at 1000 rows.
     */
    CSVModel.prototype.parse = function () {
        var output = dsv.dsvFormat(this._delimiter).parse(this._content);
        var available = output.length;
        var maximum = exports.DISPLAY_LIMIT;
        if (available > maximum) {
            // Mutate the array instead of slicing in order to conserve memory.
            output.splice(maximum);
            this._maxExceeded.emit({ available: available, maximum: maximum });
        }
        return output;
    };
    return CSVModel;
}(apputils_1.VDomModel));
exports.CSVModel = CSVModel;
/**
 * A CSV table content widget.
 */
var CSVTable = (function (_super) {
    __extends(CSVTable, _super);
    /**
     * Instantiate a new CSV table widget.
     */
    function CSVTable() {
        var _this = _super.call(this) || this;
        _this.addClass(CSV_TABLE_CLASS);
        _this.addClass('jp-RenderedHTMLCommon');
        return _this;
    }
    /**
     * Render the content as virtual DOM nodes.
     */
    CSVTable.prototype.render = function () {
        if (!this.model) {
            return virtualdom_1.h.table([virtualdom_1.h.thead(), virtualdom_1.h.tbody()]);
        }
        var rows = this.model.parse();
        var cols = rows.columns || [];
        return virtualdom_1.h.table([
            virtualdom_1.h.thead(cols.map(function (col) { return virtualdom_1.h.th(col); })),
            virtualdom_1.h.tbody(rows.map(function (row) { return virtualdom_1.h.tr(cols.map(function (col) { return virtualdom_1.h.td(row[col]); })); }))
        ]);
    };
    return CSVTable;
}(apputils_1.VDomWidget));
exports.CSVTable = CSVTable;

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
var signaling_1 = require("@phosphor/signaling");
var widgets_1 = require("@phosphor/widgets");
/**
 * The supported parsing delimiters.
 */
exports.DELIMITERS = [',', ';', '\t'];
/**
 * The labels for each delimiter as they appear in the dropdown menu.
 */
exports.LABELS = [',', ';', '\\t'];
/**
 * The class name added to a csv toolbar widget.
 */
var CSV_TOOLBAR_CLASS = 'jp-CSVToolbar';
/**
 * The class name added to a csv toolbar's dropdown element.
 */
var CSV_TOOLBAR_DROPDOWN_CLASS = 'jp-CSVToolbar-dropdown';
/**
 * A widget for CSV widget toolbars.
 */
var CSVToolbar = (function (_super) {
    __extends(CSVToolbar, _super);
    /**
     * Construct a new csv table widget.
     */
    function CSVToolbar(options) {
        if (options === void 0) { options = {}; }
        var _this = _super.call(this, { node: Private.createNode(options.selected) }) || this;
        _this._delimiterChanged = new signaling_1.Signal(_this);
        _this.addClass(CSV_TOOLBAR_CLASS);
        return _this;
    }
    Object.defineProperty(CSVToolbar.prototype, "delimiterChanged", {
        /**
         * A signal emitted when the delimiter selection has changed.
         */
        get: function () {
            return this._delimiterChanged;
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(CSVToolbar.prototype, "selectNode", {
        /**
         * The delimiter dropdown menu.
         */
        get: function () {
            return this.node.getElementsByTagName('select')[0];
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
     * called in response to events on the dock panel's node. It should
     * not be called directly by user code.
     */
    CSVToolbar.prototype.handleEvent = function (event) {
        switch (event.type) {
            case 'change':
                this._delimiterChanged.emit(this.selectNode.value);
                break;
            default:
                break;
        }
    };
    /**
     * Handle `after-attach` messages for the widget.
     */
    CSVToolbar.prototype.onAfterAttach = function (msg) {
        this.selectNode.addEventListener('change', this);
    };
    /**
     * Handle `before-detach` messages for the widget.
     */
    CSVToolbar.prototype.onBeforeDetach = function (msg) {
        this.selectNode.removeEventListener('change', this);
    };
    return CSVToolbar;
}(widgets_1.Widget));
exports.CSVToolbar = CSVToolbar;
/**
 * A namespace for private toolbar methods.
 */
var Private;
(function (Private) {
    /**
     * Create the node for the delimiter switcher.
     */
    function createNode(selected) {
        var div = document.createElement('div');
        var label = document.createElement('label');
        var select = document.createElement('select');
        select.className = CSV_TOOLBAR_DROPDOWN_CLASS;
        label.textContent = 'Delimiter: ';
        algorithm_1.each(algorithm_1.zip(exports.DELIMITERS, exports.LABELS), function (_a) {
            var delimiter = _a[0], label = _a[1];
            var option = document.createElement('option');
            option.value = delimiter;
            option.textContent = label;
            if (delimiter === selected) {
                option.selected = true;
            }
            select.appendChild(option);
        });
        label.appendChild(select);
        div.appendChild(label);
        return div;
    }
    Private.createNode = createNode;
})(Private || (Private = {}));

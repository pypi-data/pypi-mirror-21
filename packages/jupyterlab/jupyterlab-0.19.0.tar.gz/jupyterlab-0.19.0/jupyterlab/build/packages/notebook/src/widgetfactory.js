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
var default_toolbar_1 = require("./default-toolbar");
var panel_1 = require("./panel");
/**
 * A widget factory for notebook panels.
 */
var NotebookWidgetFactory = (function (_super) {
    __extends(NotebookWidgetFactory, _super);
    /**
     * Construct a new notebook widget factory.
     *
     * @param options - The options used to construct the factory.
     */
    function NotebookWidgetFactory(options) {
        var _this = _super.call(this, options) || this;
        _this.rendermime = options.rendermime;
        _this.contentFactory = options.contentFactory;
        _this.mimeTypeService = options.mimeTypeService;
        return _this;
    }
    /**
     * Create a new widget.
     *
     * #### Notes
     * The factory will start the appropriate kernel and populate
     * the default toolbar items using `ToolbarItems.populateDefaults`.
     */
    NotebookWidgetFactory.prototype.createNewWidget = function (context) {
        var rendermime = this.rendermime.clone();
        var panel = new panel_1.NotebookPanel({
            rendermime: rendermime,
            contentFactory: this.contentFactory,
            mimeTypeService: this.mimeTypeService
        });
        panel.context = context;
        default_toolbar_1.ToolbarItems.populateDefaults(panel);
        return panel;
    };
    return NotebookWidgetFactory;
}(docregistry_1.ABCWidgetFactory));
exports.NotebookWidgetFactory = NotebookWidgetFactory;

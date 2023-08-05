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
var apputils_1 = require("@jupyterlab/apputils");
/* tslint:disable */
/**
 * The notebook tracker token.
 */
exports.INotebookTracker = new coreutils_1.Token('jupyter.services.notebooks');
/* tslint:enable */
var NotebookTracker = (function (_super) {
    __extends(NotebookTracker, _super);
    function NotebookTracker() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this._activeCell = null;
        _this._activeCellChanged = new signaling_1.Signal(_this);
        _this._selectionChanged = new signaling_1.Signal(_this);
        return _this;
    }
    Object.defineProperty(NotebookTracker.prototype, "activeCell", {
        /**
         * The currently focused cell.
         *
         * #### Notes
         * This is a read-only property. If there is no cell with the focus, then this
         * value is `null`.
         */
        get: function () {
            var widget = this.currentWidget;
            if (!widget) {
                return null;
            }
            return widget.notebook.activeCell || null;
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(NotebookTracker.prototype, "activeCellChanged", {
        /**
         * A signal emitted when the current active cell changes.
         *
         * #### Notes
         * If there is no cell with the focus, then `null` will be emitted.
         */
        get: function () {
            return this._activeCellChanged;
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(NotebookTracker.prototype, "selectionChanged", {
        /**
         * A signal emitted when the selection state changes.
         */
        get: function () {
            return this._selectionChanged;
        },
        enumerable: true,
        configurable: true
    });
    /**
     * Add a new notebook panel to the tracker.
     *
     * @param panel - The notebook panel being added.
     */
    NotebookTracker.prototype.add = function (panel) {
        var promise = _super.prototype.add.call(this, panel);
        panel.notebook.activeCellChanged.connect(this._onActiveCellChanged, this);
        panel.notebook.selectionChanged.connect(this._onSelectionChanged, this);
        return promise;
    };
    /**
     * Dispose of the resources held by the tracker.
     */
    NotebookTracker.prototype.dispose = function () {
        this._activeCell = null;
        _super.prototype.dispose.call(this);
    };
    /**
     * Handle the current change event.
     */
    NotebookTracker.prototype.onCurrentChanged = function (widget) {
        // Store an internal reference to active cell to prevent false positives.
        var activeCell = this.activeCell;
        if (activeCell && activeCell === this._activeCell) {
            return;
        }
        this._activeCell = activeCell;
        if (!widget) {
            return;
        }
        // Since the notebook has changed, immediately signal an active cell change
        this._activeCellChanged.emit(widget.notebook.activeCell || null);
    };
    NotebookTracker.prototype._onActiveCellChanged = function (sender, cell) {
        // Check if the active cell change happened for the current notebook.
        if (this.currentWidget && this.currentWidget.notebook === sender) {
            this._activeCell = cell || null;
            this._activeCellChanged.emit(this._activeCell);
        }
    };
    NotebookTracker.prototype._onSelectionChanged = function (sender) {
        // Check if the selection change happened for the current notebook.
        if (this.currentWidget && this.currentWidget.notebook === sender) {
            this._selectionChanged.emit(void 0);
        }
    };
    return NotebookTracker;
}(apputils_1.InstanceTracker));
exports.NotebookTracker = NotebookTracker;

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
var actions_1 = require("./actions");
var apputils_1 = require("@jupyterlab/apputils");
/**
 * The class name added to toolbar save button.
 */
var TOOLBAR_SAVE_CLASS = 'jp-SaveIcon';
/**
 * The class name added to toolbar insert button.
 */
var TOOLBAR_INSERT_CLASS = 'jp-AddIcon';
/**
 * The class name added to toolbar cut button.
 */
var TOOLBAR_CUT_CLASS = 'jp-CutIcon';
/**
 * The class name added to toolbar copy button.
 */
var TOOLBAR_COPY_CLASS = 'jp-CopyIcon';
/**
 * The class name added to toolbar paste button.
 */
var TOOLBAR_PASTE_CLASS = 'jp-PasteIcon';
/**
 * The class name added to toolbar run button.
 */
var TOOLBAR_RUN_CLASS = 'jp-RunIcon';
/**
 * The class name added to toolbar cell type dropdown wrapper.
 */
var TOOLBAR_CELLTYPE_CLASS = 'jp-Notebook-toolbarCellType';
/**
 * The class name added to toolbar cell type dropdown.
 */
var TOOLBAR_CELLTYPE_DROPDOWN_CLASS = 'jp-Notebook-toolbarCellTypeDropdown';
/**
 * A namespace for the default toolbar items.
 */
var ToolbarItems;
(function (ToolbarItems) {
    /**
     * Create save button toolbar item.
     */
    function createSaveButton(panel) {
        return new apputils_1.ToolbarButton({
            className: TOOLBAR_SAVE_CLASS,
            onClick: function () {
                panel.context.save().then(function () {
                    if (!panel.isDisposed) {
                        return panel.context.createCheckpoint();
                    }
                });
            },
            tooltip: 'Save the notebook contents and create checkpoint'
        });
    }
    ToolbarItems.createSaveButton = createSaveButton;
    /**
     * Create an insert toolbar item.
     */
    function createInsertButton(panel) {
        return new apputils_1.ToolbarButton({
            className: TOOLBAR_INSERT_CLASS,
            onClick: function () {
                actions_1.NotebookActions.insertBelow(panel.notebook);
            },
            tooltip: 'Insert a cell below'
        });
    }
    ToolbarItems.createInsertButton = createInsertButton;
    /**
     * Create a cut toolbar item.
     */
    function createCutButton(panel) {
        return new apputils_1.ToolbarButton({
            className: TOOLBAR_CUT_CLASS,
            onClick: function () {
                actions_1.NotebookActions.cut(panel.notebook);
            },
            tooltip: 'Cut the selected cell(s)'
        });
    }
    ToolbarItems.createCutButton = createCutButton;
    /**
     * Create a copy toolbar item.
     */
    function createCopyButton(panel) {
        return new apputils_1.ToolbarButton({
            className: TOOLBAR_COPY_CLASS,
            onClick: function () {
                actions_1.NotebookActions.copy(panel.notebook);
            },
            tooltip: 'Copy the selected cell(s)'
        });
    }
    ToolbarItems.createCopyButton = createCopyButton;
    /**
     * Create a paste toolbar item.
     */
    function createPasteButton(panel) {
        return new apputils_1.ToolbarButton({
            className: TOOLBAR_PASTE_CLASS,
            onClick: function () {
                actions_1.NotebookActions.paste(panel.notebook);
            },
            tooltip: 'Paste cell(s) from the clipboard'
        });
    }
    ToolbarItems.createPasteButton = createPasteButton;
    /**
     * Create a run toolbar item.
     */
    function createRunButton(panel) {
        return new apputils_1.ToolbarButton({
            className: TOOLBAR_RUN_CLASS,
            onClick: function () {
                actions_1.NotebookActions.runAndAdvance(panel.notebook, panel.session);
            },
            tooltip: 'Run the selected cell(s) and advance'
        });
    }
    ToolbarItems.createRunButton = createRunButton;
    /**
     * Create a cell type switcher item.
     *
     * #### Notes
     * It will display the type of the current active cell.
     * If more than one cell is selected but are of different types,
     * it will display `'-'`.
     * When the user changes the cell type, it will change the
     * cell types of the selected cells.
     * It can handle a change to the context.
     */
    function createCellTypeItem(panel) {
        return new CellTypeSwitcher(panel.notebook);
    }
    ToolbarItems.createCellTypeItem = createCellTypeItem;
    /**
     * Add the default items to the panel toolbar.
     */
    function populateDefaults(panel) {
        var toolbar = panel.toolbar;
        toolbar.addItem('save', createSaveButton(panel));
        toolbar.addItem('insert', createInsertButton(panel));
        toolbar.addItem('cut', createCutButton(panel));
        toolbar.addItem('copy', createCopyButton(panel));
        toolbar.addItem('paste', createPasteButton(panel));
        toolbar.addItem('run', createRunButton(panel));
        toolbar.addItem('interrupt', apputils_1.Toolbar.createInterruptButton(panel.session));
        toolbar.addItem('restart', apputils_1.Toolbar.createRestartButton(panel.session));
        toolbar.addItem('cellType', createCellTypeItem(panel));
        toolbar.addItem('kernelName', apputils_1.Toolbar.createKernelNameItem(panel.session));
        toolbar.addItem('kernelStatus', apputils_1.Toolbar.createKernelStatusItem(panel.session));
    }
    ToolbarItems.populateDefaults = populateDefaults;
})(ToolbarItems = exports.ToolbarItems || (exports.ToolbarItems = {}));
/**
 * A toolbar widget that switches cell types.
 */
var CellTypeSwitcher = (function (_super) {
    __extends(CellTypeSwitcher, _super);
    /**
     * Construct a new cell type switcher.
     */
    function CellTypeSwitcher(widget) {
        var _this = _super.call(this, { node: createCellTypeSwitcherNode() }) || this;
        _this._changeGuard = false;
        _this._wildCard = null;
        _this._select = null;
        _this._notebook = null;
        _this.addClass(TOOLBAR_CELLTYPE_CLASS);
        _this._select = _this.node.firstChild;
        apputils_1.Styling.wrapSelect(_this._select);
        _this._wildCard = document.createElement('option');
        _this._wildCard.value = '-';
        _this._wildCard.textContent = '-';
        _this._notebook = widget;
        // Set the initial value.
        if (widget.model) {
            _this._updateValue();
        }
        // Follow the type of the active cell.
        widget.activeCellChanged.connect(_this._updateValue, _this);
        // Follow a change in the selection.
        widget.selectionChanged.connect(_this._updateValue, _this);
        return _this;
    }
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
    CellTypeSwitcher.prototype.handleEvent = function (event) {
        switch (event.type) {
            case 'change':
                this._evtChange(event);
                break;
            case 'keydown':
                this._evtKeyDown(event);
                break;
            default:
                break;
        }
    };
    /**
     * Handle `after-attach` messages for the widget.
     */
    CellTypeSwitcher.prototype.onAfterAttach = function (msg) {
        this._select.addEventListener('change', this);
        this._select.addEventListener('keydown', this);
    };
    /**
     * Handle `before-detach` messages for the widget.
     */
    CellTypeSwitcher.prototype.onBeforeDetach = function (msg) {
        this._select.removeEventListener('change', this);
        this._select.removeEventListener('keydown', this);
    };
    /**
     * Handle `changed` events for the widget.
     */
    CellTypeSwitcher.prototype._evtChange = function (event) {
        var select = this._select;
        var widget = this._notebook;
        if (select.value === '-') {
            return;
        }
        if (!this._changeGuard) {
            var value = select.value;
            actions_1.NotebookActions.changeCellType(widget, value);
            widget.activate();
        }
    };
    /**
     * Handle `keydown` events for the widget.
     */
    CellTypeSwitcher.prototype._evtKeyDown = function (event) {
        if (event.keyCode === 13) {
            this._notebook.activate();
        }
    };
    /**
     * Update the value of the dropdown from the widget state.
     */
    CellTypeSwitcher.prototype._updateValue = function () {
        var widget = this._notebook;
        var select = this._select;
        if (!widget.activeCell) {
            return;
        }
        var mType = widget.activeCell.model.type;
        for (var i = 0; i < widget.widgets.length; i++) {
            var child = widget.widgets[i];
            if (widget.isSelected(child)) {
                if (child.model.type !== mType) {
                    mType = '-';
                    select.appendChild(this._wildCard);
                    break;
                }
            }
        }
        if (mType !== '-') {
            select.remove(3);
        }
        this._changeGuard = true;
        select.value = mType;
        this._changeGuard = false;
    };
    return CellTypeSwitcher;
}(widgets_1.Widget));
/**
 * Create the node for the cell type switcher.
 */
function createCellTypeSwitcherNode() {
    var div = document.createElement('div');
    var select = document.createElement('select');
    for (var _i = 0, _a = ['Code', 'Markdown', 'Raw']; _i < _a.length; _i++) {
        var t = _a[_i];
        var option = document.createElement('option');
        option.value = t.toLowerCase();
        option.textContent = t;
        select.appendChild(option);
    }
    select.className = TOOLBAR_CELLTYPE_DROPDOWN_CLASS;
    div.appendChild(select);
    return div;
}

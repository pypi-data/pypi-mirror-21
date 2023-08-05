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
var coreutils_1 = require("@phosphor/coreutils");
var messaging_1 = require("@phosphor/messaging");
var virtualdom_1 = require("@phosphor/virtualdom");
var widgets_1 = require("@phosphor/widgets");
var apputils_1 = require("@jupyterlab/apputils");
var codeeditor_1 = require("@jupyterlab/codeeditor");
var coreutils_2 = require("@jupyterlab/coreutils");
/**
 * The class name added to a CellTools instance.
 */
var CELLTOOLS_CLASS = 'jp-CellTools';
/**
 * The class name added to a CellTools tool.
 */
var CHILD_CLASS = 'jp-CellTools-tool';
/**
 * The class name added to a CellTools active cell.
 */
var ACTIVE_CELL_CLASS = 'jp-ActiveCellTool';
/**
 * The class name added to the Metadata editor tool.
 */
var EDITOR_CLASS = 'jp-MetadataEditorTool';
/**
 * The class name added to an Editor instance.
 */
var EDITOR_TITLE_CLASS = 'jp-MetadataEditorTool-header';
/**
 * The class name added to the toggle button.
 */
var TOGGLE_CLASS = 'jp-MetadataEditorTool-toggleButton';
/**
 * The class name added to collapsed elements.
 */
var COLLAPSED_CLASS = 'jp-mod-collapsed';
/**
 * The class name added to a KeySelector instance.
 */
var KEYSELECTOR_CLASS = 'jp-KeySelector';
/* tslint:disable */
/**
 * The main menu token.
 */
exports.ICellTools = new coreutils_1.Token('jupyter.services.cell-tools');
;
/**
 * A widget that provides cell metadata tools.
 */
var CellTools = (function (_super) {
    __extends(CellTools, _super);
    /**
     * Construct a new CellTools object.
     */
    function CellTools(options) {
        var _this = _super.call(this) || this;
        _this._items = [];
        _this.addClass(CELLTOOLS_CLASS);
        _this.layout = new widgets_1.PanelLayout();
        _this._tracker = options.tracker;
        _this._tracker.activeCellChanged.connect(_this._onActiveCellChanged, _this);
        _this._tracker.selectionChanged.connect(_this._onSelectionChanged, _this);
        _this._onActiveCellChanged();
        _this._onSelectionChanged();
        return _this;
    }
    Object.defineProperty(CellTools.prototype, "activeCell", {
        /**
         * The active cell widget.
         */
        get: function () {
            return this._tracker.activeCell;
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(CellTools.prototype, "selectedCells", {
        /**
         * The currently selected cells.
         */
        get: function () {
            var selected = [];
            var panel = this._tracker.currentWidget;
            if (!panel) {
                return selected;
            }
            algorithm_1.each(panel.notebook.widgets, function (widget) {
                if (panel.notebook.isSelected(widget)) {
                    selected.push(widget);
                }
            });
            return selected;
        },
        enumerable: true,
        configurable: true
    });
    /**
     * Add a cell tool item.
     */
    CellTools.prototype.addItem = function (options) {
        var tool = options.tool;
        var rank = 'rank' in options ? options.rank : 100;
        var rankItem = { tool: tool, rank: rank };
        var index = algorithm_1.ArrayExt.upperBound(this._items, rankItem, Private.itemCmp);
        tool.addClass(CHILD_CLASS);
        // Add the tool.
        algorithm_1.ArrayExt.insert(this._items, index, rankItem);
        var layout = this.layout;
        layout.insertWidget(index, tool);
        // Trigger the tool to update its active cell.
        messaging_1.MessageLoop.sendMessage(tool, CellTools.ActiveCellMessage);
    };
    /**
     * Handle the removal of a child
     */
    CellTools.prototype.onChildRemoved = function (msg) {
        var index = algorithm_1.ArrayExt.findFirstIndex(this._items, function (item) { return item.tool === msg.child; });
        if (index !== -1) {
            algorithm_1.ArrayExt.removeAt(this._items, index);
        }
    };
    /**
     * Handle a change to the active cell.
     */
    CellTools.prototype._onActiveCellChanged = function () {
        if (this._prevActive) {
            this._prevActive.metadata.changed.disconnect(this._onMetadataChanged, this);
        }
        var activeCell = this._tracker.activeCell;
        this._prevActive = activeCell ? activeCell.model : null;
        if (activeCell) {
            activeCell.model.metadata.changed.connect(this._onMetadataChanged, this);
        }
        algorithm_1.each(this.children(), function (widget) {
            messaging_1.MessageLoop.sendMessage(widget, CellTools.ActiveCellMessage);
        });
    };
    /**
     * Handle a change in the selection.
     */
    CellTools.prototype._onSelectionChanged = function () {
        algorithm_1.each(this.children(), function (widget) {
            messaging_1.MessageLoop.sendMessage(widget, CellTools.SelectionMessage);
        });
    };
    /**
     * Handle a change in the metadata.
     */
    CellTools.prototype._onMetadataChanged = function (sender, args) {
        var message = new coreutils_2.ObservableJSON.ChangeMessage(args);
        algorithm_1.each(this.children(), function (widget) {
            messaging_1.MessageLoop.sendMessage(widget, message);
        });
    };
    return CellTools;
}(widgets_1.Widget));
exports.CellTools = CellTools;
/**
 * The namespace for CellTools class statics.
 */
(function (CellTools) {
    /**
     * A singleton conflatable `'activecell-changed'` message.
     */
    CellTools.ActiveCellMessage = new messaging_1.ConflatableMessage('activecell-changed');
    /**
     * A singleton conflatable `'selection-changed'` message.
     */
    CellTools.SelectionMessage = new messaging_1.ConflatableMessage('selection-changed');
    /**
     * The base cell tool, meant to be subclassed.
     */
    var Tool = (function (_super) {
        __extends(Tool, _super);
        function Tool() {
            return _super !== null && _super.apply(this, arguments) || this;
        }
        /**
         * Process a message sent to the widget.
         *
         * @param msg - The message sent to the widget.
         */
        Tool.prototype.processMessage = function (msg) {
            _super.prototype.processMessage.call(this, msg);
            switch (msg.type) {
                case 'activecell-changed':
                    this.onActiveCellChanged(msg);
                    break;
                case 'selection-changed':
                    this.onSelectionChanged(msg);
                    break;
                case 'jsonvalue-changed':
                    this.onMetadataChanged(msg);
                    break;
                default:
                    break;
            }
        };
        /**
         * Handle a change to the active cell.
         *
         * #### Notes
         * The default implemenatation is a no-op.
         */
        Tool.prototype.onActiveCellChanged = function (msg) { };
        /**
         * Handle a change to the selection.
         *
         * #### Notes
         * The default implementation is a no-op.
         */
        Tool.prototype.onSelectionChanged = function (msg) { };
        /**
         * Handle a change to the metadata of the active cell.
         *
         * #### Notes
         * The default implementation is a no-op.
         */
        Tool.prototype.onMetadataChanged = function (msg) { };
        return Tool;
    }(widgets_1.Widget));
    CellTools.Tool = Tool;
    /**
     * A cell tool displaying the active cell contents.
     */
    var ActiveCellTool = (function (_super) {
        __extends(ActiveCellTool, _super);
        /**
         * Construct a new active cell tool.
         */
        function ActiveCellTool() {
            var _this = _super.call(this) || this;
            _this._model = new codeeditor_1.CodeEditor.Model();
            _this.addClass(ACTIVE_CELL_CLASS);
            _this.addClass('jp-InputArea');
            _this.layout = new widgets_1.PanelLayout();
            return _this;
        }
        /**
         * Dispose of the resources used by the tool.
         */
        ActiveCellTool.prototype.dispose = function () {
            if (this._model === null) {
                return;
            }
            this._model.dispose();
            this._model = null;
            _super.prototype.dispose.call(this);
        };
        /**
         * Handle a change to the active cell.
         */
        ActiveCellTool.prototype.onActiveCellChanged = function () {
            var activeCell = this.parent.activeCell;
            var layout = this.layout;
            var count = layout.widgets.length;
            for (var i = 0; i < count; i++) {
                layout.widgets[0].dispose();
            }
            if (this._cellModel) {
                this._cellModel.value.changed.disconnect(this._onValueChanged, this);
                this._cellModel.mimeTypeChanged.disconnect(this._onMimeTypeChanged, this);
            }
            if (!activeCell) {
                var cell = new widgets_1.Widget();
                cell.addClass('jp-CellEditor');
                cell.addClass('jp-InputArea-editor');
                layout.addWidget(cell);
                this._cellModel = null;
                return;
            }
            var promptNode = activeCell.promptNode.cloneNode(true);
            var prompt = new widgets_1.Widget({ node: promptNode });
            var factory = activeCell.contentFactory.editorFactory;
            var cellModel = this._cellModel = activeCell.model;
            cellModel.value.changed.connect(this._onValueChanged, this);
            cellModel.mimeTypeChanged.connect(this._onMimeTypeChanged, this);
            this._model.value.text = cellModel.value.text.split('\n')[0];
            this._model.mimeType = cellModel.mimeType;
            var model = this._model;
            var editorWidget = new codeeditor_1.CodeEditorWidget({ model: model, factory: factory });
            editorWidget.addClass('jp-CellEditor');
            editorWidget.addClass('jp-InputArea-editor');
            editorWidget.editor.readOnly = true;
            layout.addWidget(prompt);
            layout.addWidget(editorWidget);
        };
        /**
         * Handle a change to the current editor value.
         */
        ActiveCellTool.prototype._onValueChanged = function () {
            this._model.value.text = this._cellModel.value.text.split('\n')[0];
        };
        /**
         * Handle a change to the current editor mimetype.
         */
        ActiveCellTool.prototype._onMimeTypeChanged = function () {
            this._model.mimeType = this._cellModel.mimeType;
        };
        return ActiveCellTool;
    }(Tool));
    CellTools.ActiveCellTool = ActiveCellTool;
    /**
     * A raw metadata editor.
     */
    var MetadataEditorTool = (function (_super) {
        __extends(MetadataEditorTool, _super);
        /**
         * Construct a new raw metadata tool.
         */
        function MetadataEditorTool(options) {
            var _this = _super.call(this) || this;
            var editorFactory = options.editorFactory;
            _this.addClass(EDITOR_CLASS);
            var layout = _this.layout = new widgets_1.PanelLayout();
            var header = Private.createMetadataHeader();
            layout.addWidget(header);
            _this.editor = new codeeditor_1.JSONEditorWidget({ editorFactory: editorFactory });
            layout.addWidget(_this.editor);
            header.addClass(COLLAPSED_CLASS);
            _this.editor.addClass(COLLAPSED_CLASS);
            _this.toggleNode.classList.add(COLLAPSED_CLASS);
            return _this;
        }
        Object.defineProperty(MetadataEditorTool.prototype, "toggleNode", {
            /**
             * Get the toggle node used by the editor.
             */
            get: function () {
                return this.node.getElementsByClassName(TOGGLE_CLASS)[0];
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
         * called in response to events on the notebook panel's node. It should
         * not be called directly by user code.
         */
        MetadataEditorTool.prototype.handleEvent = function (event) {
            if (event.type !== 'click') {
                return;
            }
            algorithm_1.each(this.children(), function (widget) {
                widget.toggleClass(COLLAPSED_CLASS);
            });
            var toggleNode = this.toggleNode;
            if (this.editor.hasClass(COLLAPSED_CLASS)) {
                toggleNode.classList.add(COLLAPSED_CLASS);
            }
            else {
                toggleNode.classList.remove(COLLAPSED_CLASS);
            }
            this.editor.editor.refresh();
        };
        /**
         * Handle `after-attach` messages for the widget.
         */
        MetadataEditorTool.prototype.onAfterAttach = function (msg) {
            this.toggleNode.addEventListener('click', this);
            var cell = this.parent.activeCell;
            this.editor.source = cell ? cell.model.metadata : null;
        };
        /**
         * Handle `before-detach` messages for the widget.
         */
        MetadataEditorTool.prototype.onBeforeDetach = function (msg) {
            this.toggleNode.removeEventListener('click', this);
        };
        /**
         * Handle a change to the active cell.
         */
        MetadataEditorTool.prototype.onActiveCellChanged = function (msg) {
            var cell = this.parent.activeCell;
            this.editor.source = cell ? cell.model.metadata : null;
        };
        return MetadataEditorTool;
    }(Tool));
    CellTools.MetadataEditorTool = MetadataEditorTool;
    /**
     * A cell tool that provides a selection for a given metadata key.
     */
    var KeySelector = (function (_super) {
        __extends(KeySelector, _super);
        /**
         * Construct a new KeySelector.
         */
        function KeySelector(options) {
            var _this = _super.call(this, { node: Private.createSelectorNode(options) }) || this;
            _this._changeGuard = false;
            _this.addClass(KEYSELECTOR_CLASS);
            _this.key = options.key;
            _this._validCellTypes = options.validCellTypes || [];
            return _this;
        }
        Object.defineProperty(KeySelector.prototype, "selectNode", {
            /**
             * The select node for the widget.
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
         * called in response to events on the notebook panel's node. It should
         * not be called directly by user code.
         */
        KeySelector.prototype.handleEvent = function (event) {
            switch (event.type) {
                case 'change':
                    this.onValueChanged();
                    break;
                default:
                    break;
            }
        };
        /**
         * Handle `after-attach` messages for the widget.
         */
        KeySelector.prototype.onAfterAttach = function (msg) {
            var node = this.selectNode;
            node.addEventListener('change', this);
        };
        /**
         * Handle `before-detach` messages for the widget.
         */
        KeySelector.prototype.onBeforeDetach = function (msg) {
            var node = this.selectNode;
            node.removeEventListener('change', this);
        };
        /**
         * Handle a change to the active cell.
         */
        KeySelector.prototype.onActiveCellChanged = function (msg) {
            var select = this.selectNode;
            var activeCell = this.parent.activeCell;
            if (!activeCell) {
                select.disabled = true;
                select.value = '';
                return;
            }
            var cellType = activeCell.model.type;
            if (this._validCellTypes.length &&
                this._validCellTypes.indexOf(cellType) === -1) {
                select.disabled = true;
                return;
            }
            select.disabled = false;
            var source = activeCell.model.metadata;
            select.value = JSON.stringify(source.get(this.key));
        };
        /**
         * Handle a change to the metadata of the active cell.
         */
        KeySelector.prototype.onMetadataChanged = function (msg) {
            if (this._changeGuard) {
                return;
            }
            var select = this.selectNode;
            if (msg.args.key === this.key) {
                this._changeGuard = true;
                select.value = JSON.stringify(msg.args.newValue);
                this._changeGuard = false;
            }
        };
        /**
         * Handle a change to the value.
         */
        KeySelector.prototype.onValueChanged = function () {
            var activeCell = this.parent.activeCell;
            if (!activeCell || this._changeGuard) {
                return;
            }
            this._changeGuard = true;
            var select = this.selectNode;
            var source = activeCell.model.metadata;
            source.set(this.key, JSON.parse(select.value));
            this._changeGuard = false;
        };
        return KeySelector;
    }(Tool));
    CellTools.KeySelector = KeySelector;
    /**
     * Create a slideshow selector.
     */
    function createSlideShowSelector() {
        var options = {
            key: 'slideshow',
            title: 'Slide Type',
            optionsMap: {
                '-': '-',
                'Slide': 'slide',
                'Sub-Slide': 'subslide',
                'Fragment': 'fragment',
                'Skip': 'skip',
                'Notes': 'notes'
            }
        };
        return new KeySelector(options);
    }
    CellTools.createSlideShowSelector = createSlideShowSelector;
    /**
     * Create an nbcovert selector.
     */
    function createNBConvertSelector() {
        return new KeySelector({
            key: 'raw_mimetype',
            title: 'Raw NBConvert Format',
            optionsMap: {
                'None': '-',
                'LaTeX': 'text/latex',
                'reST': 'text/restructuredtext',
                'HTML': 'text/html',
                'Markdown': 'text/markdown',
                'Python': 'text/x-python'
            },
            validCellTypes: ['raw']
        });
    }
    CellTools.createNBConvertSelector = createNBConvertSelector;
})(CellTools = exports.CellTools || (exports.CellTools = {}));
exports.CellTools = CellTools;
/**
 * A namespace for private data.
 */
var Private;
(function (Private) {
    /**
     * A comparator function for widget rank items.
     */
    function itemCmp(first, second) {
        return first.rank - second.rank;
    }
    Private.itemCmp = itemCmp;
    /**
     * Create the node for a KeySelector.
     */
    function createSelectorNode(options) {
        var name = options.key;
        var title = (options.title || name[0].toLocaleUpperCase() + name.slice(1));
        var optionNodes = [];
        for (var label in options.optionsMap) {
            var value = JSON.stringify(options.optionsMap[label]);
            optionNodes.push(virtualdom_1.h.option({ label: label, value: value }));
        }
        var node = virtualdom_1.VirtualDOM.realize(virtualdom_1.h.div({}, virtualdom_1.h.label(title), virtualdom_1.h.select({}, optionNodes)));
        apputils_1.Styling.styleNode(node);
        return node;
    }
    Private.createSelectorNode = createSelectorNode;
    /**
     * Create the metadata header widget.
     */
    function createMetadataHeader() {
        var node = virtualdom_1.VirtualDOM.realize(virtualdom_1.h.div({ className: EDITOR_TITLE_CLASS }, virtualdom_1.h.label({}, 'Edit Metadata'), virtualdom_1.h.span({ className: TOGGLE_CLASS })));
        return new widgets_1.Widget({ node: node });
    }
    Private.createMetadataHeader = createMetadataHeader;
})(Private || (Private = {}));

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
var properties_1 = require("@phosphor/properties");
var signaling_1 = require("@phosphor/signaling");
var dragdrop_1 = require("@phosphor/dragdrop");
var widgets_1 = require("@phosphor/widgets");
var widgets_2 = require("@phosphor/widgets");
var cells_1 = require("@jupyterlab/cells");
var outputarea_1 = require("@jupyterlab/outputarea");
/**
 * The class name added to notebook widgets.
 */
var NB_CLASS = 'jp-Notebook';
/**
 * The class name added to notebook widget cells.
 */
var NB_CELL_CLASS = 'jp-Notebook-cell';
/**
 * The class name added to a notebook in edit mode.
 */
var EDIT_CLASS = 'jp-mod-editMode';
/**
 * The class name added to a notebook in command mode.
 */
var COMMAND_CLASS = 'jp-mod-commandMode';
/**
 * The class name added to the active cell.
 */
var ACTIVE_CLASS = 'jp-mod-active';
/**
 * The class name added to selected cells.
 */
var SELECTED_CLASS = 'jp-mod-selected';
/**
 * The class name added to an active cell when there are other selected cells.
 */
var OTHER_SELECTED_CLASS = 'jp-mod-multiSelected';
/**
 * The class name added to unconfined images.
 */
var UNCONFINED_CLASS = 'jp-mod-unconfined';
/**
 * The class name added to a drop target.
 */
var DROP_TARGET_CLASS = 'jp-mod-dropTarget';
/**
 * The class name added to a drop source.
 */
var DROP_SOURCE_CLASS = 'jp-mod-dropSource';
/**
 * The class name added to drag images.
 */
var DRAG_IMAGE_CLASS = 'jp-dragImage';
/**
 * The class name added to a filled circle.
 */
var FILLED_CIRCLE_CLASS = 'jp-filledCircle';
/**
 * The mimetype used for Jupyter cell data.
 */
exports.JUPYTER_CELL_MIME = 'application/vnd.jupyter.cells';
/**
 * The threshold in pixels to start a drag event.
 */
var DRAG_THRESHOLD = 5;
/**
 * A widget which renders static non-interactive notebooks.
 *
 * #### Notes
 * The widget model must be set separately and can be changed
 * at any time.  Consumers of the widget must account for a
 * `null` model, and may want to listen to the `modelChanged`
 * signal.
 */
var StaticNotebook = (function (_super) {
    __extends(StaticNotebook, _super);
    /**
     * Construct a notebook widget.
     */
    function StaticNotebook(options) {
        var _this = _super.call(this) || this;
        _this._mimetype = 'text/plain';
        _this._model = null;
        _this._modelChanged = new signaling_1.Signal(_this);
        _this._modelContentChanged = new signaling_1.Signal(_this);
        _this.addClass(NB_CLASS);
        _this.rendermime = options.rendermime;
        _this.layout = new Private.NotebookPanelLayout();
        _this.contentFactory = options.contentFactory;
        _this._mimetypeService = options.mimeTypeService;
        return _this;
    }
    Object.defineProperty(StaticNotebook.prototype, "modelChanged", {
        /**
         * A signal emitted when the model of the notebook changes.
         */
        get: function () {
            return this._modelChanged;
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(StaticNotebook.prototype, "modelContentChanged", {
        /**
         * A signal emitted when the model content changes.
         *
         * #### Notes
         * This is a convenience signal that follows the current model.
         */
        get: function () {
            return this._modelContentChanged;
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(StaticNotebook.prototype, "model", {
        /**
         * The model for the widget.
         */
        get: function () {
            return this._model;
        },
        set: function (newValue) {
            newValue = newValue || null;
            if (this._model === newValue) {
                return;
            }
            var oldValue = this._model;
            this._model = newValue;
            // Trigger private, protected, and public changes.
            this._onModelChanged(oldValue, newValue);
            this.onModelChanged(oldValue, newValue);
            this._modelChanged.emit(void 0);
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(StaticNotebook.prototype, "codeMimetype", {
        /**
         * Get the mimetype for code cells.
         */
        get: function () {
            return this._mimetype;
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(StaticNotebook.prototype, "widgets", {
        /**
         * A read-only sequence of the widgets in the notebook.
         */
        get: function () {
            return this.layout.widgets;
        },
        enumerable: true,
        configurable: true
    });
    /**
     * Dispose of the resources held by the widget.
     */
    StaticNotebook.prototype.dispose = function () {
        // Do nothing if already disposed.
        if (this.isDisposed) {
            return;
        }
        this._model = null;
        _super.prototype.dispose.call(this);
    };
    /**
     * Handle a new model.
     *
     * #### Notes
     * This method is called after the model change has been handled
     * internally and before the `modelChanged` signal is emitted.
     * The default implementation is a no-op.
     */
    StaticNotebook.prototype.onModelChanged = function (oldValue, newValue) {
        // No-op.
    };
    /**
     * Handle changes to the notebook model content.
     *
     * #### Notes
     * The default implementation emits the `modelContentChanged` signal.
     */
    StaticNotebook.prototype.onModelContentChanged = function (model, args) {
        this._modelContentChanged.emit(void 0);
    };
    /**
     * Handle changes to the notebook model metadata.
     *
     * #### Notes
     * The default implementation updates the mimetypes of the code cells
     * when the `language_info` metadata changes.
     */
    StaticNotebook.prototype.onMetadataChanged = function (sender, args) {
        switch (args.key) {
            case 'language_info':
                this._updateMimetype();
                break;
            default:
                break;
        }
    };
    /**
     * Handle a cell being inserted.
     *
     * The default implementation is a no-op
     */
    StaticNotebook.prototype.onCellInserted = function (index, cell) {
        // This is a no-op.
    };
    /**
     * Handle a cell being moved.
     *
     * The default implementation is a no-op
     */
    StaticNotebook.prototype.onCellMoved = function (fromIndex, toIndex) {
        // This is a no-op.
    };
    /**
     * Handle a cell being removed.
     *
     * The default implementation is a no-op
     */
    StaticNotebook.prototype.onCellRemoved = function (cell) {
        // This is a no-op.
    };
    /**
     * Handle a new model on the widget.
     */
    StaticNotebook.prototype._onModelChanged = function (oldValue, newValue) {
        var _this = this;
        var layout = this.layout;
        if (oldValue) {
            oldValue.cells.changed.disconnect(this._onCellsChanged, this);
            oldValue.metadata.changed.disconnect(this.onMetadataChanged, this);
            oldValue.contentChanged.disconnect(this.onModelContentChanged, this);
            // TODO: reuse existing cell widgets if possible.
            while (layout.widgets.length) {
                this._removeCell(0);
            }
        }
        if (!newValue) {
            this._mimetype = 'text/plain';
            return;
        }
        this._updateMimetype();
        var cells = newValue.cells;
        algorithm_1.each(cells, function (cell, i) {
            _this._insertCell(i, cell);
        });
        cells.changed.connect(this._onCellsChanged, this);
        newValue.contentChanged.connect(this.onModelContentChanged, this);
        newValue.metadata.changed.connect(this.onMetadataChanged, this);
    };
    /**
     * Handle a change cells event.
     */
    StaticNotebook.prototype._onCellsChanged = function (sender, args) {
        var _this = this;
        var index = 0;
        switch (args.type) {
            case 'add':
                index = args.newIndex;
                algorithm_1.each(args.newValues, function (value) {
                    _this._insertCell(index++, value);
                });
                break;
            case 'move':
                this._moveCell(args.oldIndex, args.newIndex);
                break;
            case 'remove':
                algorithm_1.each(args.oldValues, function (value) {
                    _this._removeCell(args.oldIndex);
                });
                break;
            case 'set':
                // TODO: reuse existing widgets if possible.
                index = args.newIndex;
                algorithm_1.each(args.newValues, function (value) {
                    _this._removeCell(index);
                    _this._insertCell(index, value);
                    index++;
                });
                break;
            default:
                return;
        }
    };
    /**
     * Create a cell widget and insert into the notebook.
     */
    StaticNotebook.prototype._insertCell = function (index, cell) {
        var widget;
        switch (cell.type) {
            case 'code':
                widget = this._createCodeCell(cell);
                widget.model.mimeType = this._mimetype;
                break;
            case 'markdown':
                widget = this._createMarkdownCell(cell);
                break;
            default:
                widget = this._createRawCell(cell);
        }
        widget.addClass(NB_CELL_CLASS);
        var layout = this.layout;
        layout.insertWidget(index, widget);
        this.onCellInserted(index, widget);
    };
    /**
     * Create a code cell widget from a code cell model.
     */
    StaticNotebook.prototype._createCodeCell = function (model) {
        var factory = this.contentFactory;
        var contentFactory = factory.codeCellContentFactory;
        var rendermime = this.rendermime;
        var options = { model: model, rendermime: rendermime, contentFactory: contentFactory };
        return factory.createCodeCell(options, this);
    };
    /**
     * Create a markdown cell widget from a markdown cell model.
     */
    StaticNotebook.prototype._createMarkdownCell = function (model) {
        var factory = this.contentFactory;
        var contentFactory = factory.markdownCellContentFactory;
        var rendermime = this.rendermime;
        var options = { model: model, rendermime: rendermime, contentFactory: contentFactory };
        return factory.createMarkdownCell(options, this);
    };
    /**
     * Create a raw cell widget from a raw cell model.
     */
    StaticNotebook.prototype._createRawCell = function (model) {
        var factory = this.contentFactory;
        var contentFactory = factory.rawCellContentFactory;
        var options = { model: model, contentFactory: contentFactory };
        return factory.createRawCell(options, this);
    };
    /**
     * Move a cell widget.
     */
    StaticNotebook.prototype._moveCell = function (fromIndex, toIndex) {
        var layout = this.layout;
        layout.insertWidget(toIndex, layout.widgets[fromIndex]);
        this.onCellMoved(fromIndex, toIndex);
    };
    /**
     * Remove a cell widget.
     */
    StaticNotebook.prototype._removeCell = function (index) {
        var layout = this.layout;
        var widget = layout.widgets[index];
        widget.parent = null;
        this.onCellRemoved(widget);
        widget.dispose();
    };
    /**
     * Update the mimetype of the notebook.
     */
    StaticNotebook.prototype._updateMimetype = function () {
        var _this = this;
        var info = this._model.metadata.get('language_info');
        if (!info) {
            return;
        }
        this._mimetype = this._mimetypeService.getMimeTypeByLanguage(info);
        algorithm_1.each(this.widgets, function (widget) {
            if (widget.model.type === 'code') {
                widget.model.mimeType = _this._mimetype;
            }
        });
    };
    return StaticNotebook;
}(widgets_2.Widget));
exports.StaticNotebook = StaticNotebook;
/**
 * The namespace for the `StaticNotebook` class statics.
 */
(function (StaticNotebook) {
    /**
     * The default implementation of an `IContentFactory`.
     */
    var ContentFactory = (function () {
        /**
         * Creates a new renderer.
         */
        function ContentFactory(options) {
            var editorFactory = options.editorFactory;
            var outputAreaContentFactory = (options.outputAreaContentFactory ||
                outputarea_1.OutputAreaWidget.defaultContentFactory);
            this.codeCellContentFactory = (options.codeCellContentFactory ||
                new cells_1.CodeCellWidget.ContentFactory({
                    editorFactory: editorFactory,
                    outputAreaContentFactory: outputAreaContentFactory
                }));
            this.rawCellContentFactory = (options.rawCellContentFactory ||
                new cells_1.RawCellWidget.ContentFactory({ editorFactory: editorFactory }));
            this.markdownCellContentFactory = (options.markdownCellContentFactory ||
                new cells_1.MarkdownCellWidget.ContentFactory({ editorFactory: editorFactory }));
        }
        /**
         * Create a new code cell widget.
         */
        ContentFactory.prototype.createCodeCell = function (options, parent) {
            return new cells_1.CodeCellWidget(options);
        };
        /**
         * Create a new markdown cell widget.
         */
        ContentFactory.prototype.createMarkdownCell = function (options, parent) {
            return new cells_1.MarkdownCellWidget(options);
        };
        /**
         * Create a new raw cell widget.
         */
        ContentFactory.prototype.createRawCell = function (options, parent) {
            return new cells_1.RawCellWidget(options);
        };
        return ContentFactory;
    }());
    StaticNotebook.ContentFactory = ContentFactory;
})(StaticNotebook = exports.StaticNotebook || (exports.StaticNotebook = {}));
exports.StaticNotebook = StaticNotebook;
/**
 * A notebook widget that supports interactivity.
 */
var Notebook = (function (_super) {
    __extends(Notebook, _super);
    /**
     * Construct a notebook widget.
     */
    function Notebook(options) {
        var _this = _super.call(this, options) || this;
        _this._activeCellIndex = -1;
        _this._activeCell = null;
        _this._mode = 'command';
        _this._drag = null;
        _this._dragData = null;
        _this._activeCellChanged = new signaling_1.Signal(_this);
        _this._stateChanged = new signaling_1.Signal(_this);
        _this._selectionChanged = new signaling_1.Signal(_this);
        _this.node.tabIndex = -1; // Allow the widget to take focus.
        // Allow the node to scroll while dragging items.
        _this.node.setAttribute('data-p-dragscroll', 'true');
        return _this;
    }
    Object.defineProperty(Notebook.prototype, "activeCellChanged", {
        /**
         * A signal emitted when the active cell changes.
         *
         * #### Notes
         * This can be due to the active index changing or the
         * cell at the active index changing.
         */
        get: function () {
            return this._activeCellChanged;
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(Notebook.prototype, "stateChanged", {
        /**
         * A signal emitted when the state of the notebook changes.
         */
        get: function () {
            return this._stateChanged;
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(Notebook.prototype, "selectionChanged", {
        /**
         * A signal emitted when the selection state of the notebook changes.
         */
        get: function () {
            return this._selectionChanged;
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(Notebook.prototype, "mode", {
        /**
         * The interactivity mode of the notebook.
         */
        get: function () {
            return this._mode;
        },
        set: function (newValue) {
            var _this = this;
            var activeCell = this.activeCell;
            if (!activeCell) {
                newValue = 'command';
            }
            if (newValue === this._mode) {
                this._ensureFocus();
                return;
            }
            // Post an update request.
            this.update();
            var oldValue = this._mode;
            this._mode = newValue;
            if (newValue === 'edit') {
                var node = this.activeCell.editorWidget.node;
                this.scrollToPosition(node.getBoundingClientRect().top);
                // Edit mode deselects all cells.
                algorithm_1.each(this.widgets, function (widget) { _this.deselect(widget); });
                //  Edit mode unrenders an active markdown widget.
                if (activeCell instanceof cells_1.MarkdownCellWidget) {
                    activeCell.rendered = false;
                }
            }
            this._stateChanged.emit({ name: 'mode', oldValue: oldValue, newValue: newValue });
            this._ensureFocus();
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(Notebook.prototype, "activeCellIndex", {
        /**
         * The active cell index of the notebook.
         *
         * #### Notes
         * The index will be clamped to the bounds of the notebook cells.
         */
        get: function () {
            if (!this.model) {
                return -1;
            }
            return this.model.cells.length ? this._activeCellIndex : -1;
        },
        set: function (newValue) {
            var oldValue = this._activeCellIndex;
            if (!this.model || !this.model.cells.length) {
                newValue = -1;
            }
            else {
                newValue = Math.max(newValue, 0);
                newValue = Math.min(newValue, this.model.cells.length - 1);
            }
            this._activeCellIndex = newValue;
            var cell = this.widgets[newValue];
            if (cell !== this._activeCell) {
                // Post an update request.
                this.update();
                this._activeCell = cell;
                this._activeCellChanged.emit(cell);
            }
            if (this.mode === 'edit' && cell instanceof cells_1.MarkdownCellWidget) {
                cell.rendered = false;
            }
            this._ensureFocus();
            if (newValue === oldValue) {
                return;
            }
            this._stateChanged.emit({ name: 'activeCellIndex', oldValue: oldValue, newValue: newValue });
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(Notebook.prototype, "activeCell", {
        /**
         * Get the active cell widget.
         */
        get: function () {
            return this._activeCell;
        },
        enumerable: true,
        configurable: true
    });
    /**
     * Dispose of the resources held by the widget.
     */
    Notebook.prototype.dispose = function () {
        if (this._activeCell === null) {
            return;
        }
        this._activeCell = null;
        _super.prototype.dispose.call(this);
    };
    /**
     * Select a cell widget.
     *
     * #### Notes
     * It is a no-op if the value does not change.
     * It will emit the `selectionChanged` signal.
     */
    Notebook.prototype.select = function (widget) {
        if (Private.selectedProperty.get(widget)) {
            return;
        }
        Private.selectedProperty.set(widget, true);
        this._selectionChanged.emit(void 0);
        this.update();
    };
    /**
     * Deselect a cell widget.
     *
     * #### Notes
     * It is a no-op if the value does not change.
     * It will emit the `selectionChanged` signal.
     */
    Notebook.prototype.deselect = function (widget) {
        if (!Private.selectedProperty.get(widget)) {
            return;
        }
        Private.selectedProperty.set(widget, false);
        this._selectionChanged.emit(void 0);
        this.update();
    };
    /**
     * Whether a cell is selected or is the active cell.
     */
    Notebook.prototype.isSelected = function (widget) {
        if (widget === this._activeCell) {
            return true;
        }
        return Private.selectedProperty.get(widget);
    };
    /**
     * Deselect all of the cells.
     */
    Notebook.prototype.deselectAll = function () {
        var changed = false;
        algorithm_1.each(this.widgets, function (widget) {
            if (Private.selectedProperty.get(widget)) {
                changed = true;
            }
            Private.selectedProperty.set(widget, false);
        });
        if (changed) {
            this._selectionChanged.emit(void 0);
        }
        // Make sure we have a valid active cell.
        this.activeCellIndex = this.activeCellIndex;
    };
    /**
     * Scroll so that the given position is visible.
     *
     * @param position - The vertical position in the notebook widget.
     *
     * @param threshold - An optional threshold for the scroll.  Defaults to 25
     *   percent of the widget height.
     */
    Notebook.prototype.scrollToPosition = function (position, threshold) {
        if (threshold === void 0) { threshold = 25; }
        var node = this.node;
        var ar = node.getBoundingClientRect();
        var delta = position - ar.top - ar.height / 2;
        if (Math.abs(delta) > ar.height * threshold / 100) {
            node.scrollTop += delta;
        }
    };
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
    Notebook.prototype.handleEvent = function (event) {
        if (!this.model || this.model.readOnly) {
            return;
        }
        switch (event.type) {
            case 'mousedown':
                this._evtMouseDown(event);
                break;
            case 'mouseup':
                this._evtMouseup(event);
                break;
            case 'mousemove':
                this._evtMousemove(event);
                break;
            case 'keydown':
                this._ensureFocus(true);
                break;
            case 'dblclick':
                this._evtDblClick(event);
                break;
            case 'focus':
                this._evtFocus(event);
                break;
            case 'blur':
                this._evtBlur(event);
                break;
            case 'p-dragenter':
                this._evtDragEnter(event);
                break;
            case 'p-dragleave':
                this._evtDragLeave(event);
                break;
            case 'p-dragover':
                this._evtDragOver(event);
                break;
            case 'p-drop':
                this._evtDrop(event);
                break;
            default:
                break;
        }
    };
    /**
     * Handle `after-attach` messages for the widget.
     */
    Notebook.prototype.onAfterAttach = function (msg) {
        _super.prototype.onAfterAttach.call(this, msg);
        var node = this.node;
        node.addEventListener('mousedown', this);
        node.addEventListener('keydown', this);
        node.addEventListener('dblclick', this);
        node.addEventListener('focus', this, true);
        node.addEventListener('blur', this, true);
        node.addEventListener('p-dragenter', this);
        node.addEventListener('p-dragleave', this);
        node.addEventListener('p-dragover', this);
        node.addEventListener('p-drop', this);
    };
    /**
     * Handle `before-detach` messages for the widget.
     */
    Notebook.prototype.onBeforeDetach = function (msg) {
        var node = this.node;
        node.removeEventListener('mousedown', this);
        node.removeEventListener('keydown', this);
        node.removeEventListener('dblclick', this);
        node.removeEventListener('focus', this, true);
        node.removeEventListener('blur', this, true);
        node.removeEventListener('p-dragenter', this);
        node.removeEventListener('p-dragleave', this);
        node.removeEventListener('p-dragover', this);
        node.removeEventListener('p-drop', this);
        document.removeEventListener('mousemove', this, true);
        document.removeEventListener('mouseup', this, true);
    };
    /**
     * Handle `'activate-request'` messages.
     */
    Notebook.prototype.onActivateRequest = function (msg) {
        this._ensureFocus(true);
    };
    /**
     * Handle `update-request` messages sent to the widget.
     */
    Notebook.prototype.onUpdateRequest = function (msg) {
        var _this = this;
        var activeCell = this.activeCell;
        // Set the appropriate classes on the cells.
        if (this.mode === 'edit') {
            this.addClass(EDIT_CLASS);
            this.removeClass(COMMAND_CLASS);
        }
        else {
            this.addClass(COMMAND_CLASS);
            this.removeClass(EDIT_CLASS);
        }
        if (activeCell) {
            activeCell.addClass(ACTIVE_CLASS);
        }
        var count = 0;
        algorithm_1.each(this.widgets, function (widget) {
            if (widget !== activeCell) {
                widget.removeClass(ACTIVE_CLASS);
            }
            widget.removeClass(OTHER_SELECTED_CLASS);
            if (_this.isSelected(widget)) {
                widget.addClass(SELECTED_CLASS);
                count++;
            }
            else {
                widget.removeClass(SELECTED_CLASS);
            }
        });
        if (count > 1) {
            activeCell.addClass(OTHER_SELECTED_CLASS);
        }
    };
    /**
     * Handle a cell being inserted.
     */
    Notebook.prototype.onCellInserted = function (index, cell) {
        cell.editor.edgeRequested.connect(this._onEdgeRequest, this);
        // Trigger an update of the active cell.
        this.activeCellIndex = this.activeCellIndex;
    };
    /**
     * Handle a cell being moved.
     */
    Notebook.prototype.onCellMoved = function (fromIndex, toIndex) {
        if (fromIndex === this.activeCellIndex) {
            this.activeCellIndex = toIndex;
        }
    };
    /**
     * Handle a cell being removed.
     */
    Notebook.prototype.onCellRemoved = function (cell) {
        // Trigger an update of the active cell.
        this.activeCellIndex = this.activeCellIndex;
        if (this.isSelected(cell)) {
            this._selectionChanged.emit(void 0);
        }
    };
    /**
     * Handle a new model.
     */
    Notebook.prototype.onModelChanged = function (oldValue, newValue) {
        // Try to set the active cell index to 0.
        // It will be set to `-1` if there is no new model or the model is empty.
        this.activeCellIndex = 0;
    };
    /**
     * Handle edge request signals from cells.
     */
    Notebook.prototype._onEdgeRequest = function (editor, location) {
        var prev = this.activeCellIndex;
        if (location === 'top') {
            this.activeCellIndex--;
            // Move the cursor to the first position on the last line.
            if (this.activeCellIndex < prev) {
                var editor_1 = this.activeCell.editor;
                var lastLine = editor_1.lineCount - 1;
                editor_1.setCursorPosition({ line: lastLine, column: 0 });
            }
        }
        else {
            this.activeCellIndex++;
            // Move the cursor to the first character.
            if (this.activeCellIndex > prev) {
                var editor_2 = this.activeCell.editor;
                editor_2.setCursorPosition({ line: 0, column: 0 });
            }
        }
    };
    /**
     * Ensure that the notebook has proper focus.
     */
    Notebook.prototype._ensureFocus = function (force) {
        if (force === void 0) { force = false; }
        var activeCell = this.activeCell;
        if (this.mode === 'edit' && activeCell) {
            activeCell.editor.focus();
        }
        else if (activeCell) {
            activeCell.editor.blur();
        }
        if (force && !this.node.contains(document.activeElement)) {
            this.node.focus();
        }
    };
    /**
     * Find the cell index containing the target html element.
     *
     * #### Notes
     * Returns -1 if the cell is not found.
     */
    Notebook.prototype._findCell = function (node) {
        // Trace up the DOM hierarchy to find the root cell node.
        // Then find the corresponding child and select it.
        while (node && node !== this.node) {
            if (node.classList.contains(NB_CELL_CLASS)) {
                var i = algorithm_1.ArrayExt.findFirstIndex(this.widgets, function (widget) { return widget.node === node; });
                if (i !== -1) {
                    return i;
                }
                break;
            }
            node = node.parentElement;
        }
        return -1;
    };
    /**
     * Handle `mousedown` events for the widget.
     */
    Notebook.prototype._evtMouseDown = function (event) {
        var target = event.target;
        var i = this._findCell(target);
        var shouldDrag = false;
        if (i !== -1) {
            var widget = this.widgets[i];
            // Event is on a cell but not in its editor, switch to command mode.
            if (!widget.editorWidget.node.contains(target)) {
                this.mode = 'command';
                shouldDrag = widget.promptNode.contains(target);
            }
            if (event.shiftKey) {
                shouldDrag = false;
                this._extendSelectionTo(i);
                // Prevent text select behavior.
                event.preventDefault();
                event.stopPropagation();
            }
            else {
                if (!this.isSelected(widget)) {
                    this.deselectAll();
                }
            }
            // Set the cell as the active one.
            // This must be done *after* setting the mode above.
            this.activeCellIndex = i;
        }
        this._ensureFocus(true);
        // Left mouse press for drag start.
        if (event.button === 0 && shouldDrag) {
            this._dragData = { pressX: event.clientX, pressY: event.clientY, index: i };
            document.addEventListener('mouseup', this, true);
            document.addEventListener('mousemove', this, true);
            event.preventDefault();
        }
    };
    /**
     * Handle the `'mouseup'` event for the widget.
     */
    Notebook.prototype._evtMouseup = function (event) {
        if (event.button !== 0 || !this._drag) {
            document.removeEventListener('mousemove', this, true);
            document.removeEventListener('mouseup', this, true);
            return;
        }
        event.preventDefault();
        event.stopPropagation();
    };
    /**
     * Handle the `'mousemove'` event for the widget.
     */
    Notebook.prototype._evtMousemove = function (event) {
        event.preventDefault();
        event.stopPropagation();
        // Bail if we are the one dragging.
        if (this._drag) {
            return;
        }
        // Check for a drag initialization.
        var data = this._dragData;
        var dx = Math.abs(event.clientX - data.pressX);
        var dy = Math.abs(event.clientY - data.pressY);
        if (dx < DRAG_THRESHOLD && dy < DRAG_THRESHOLD) {
            return;
        }
        this._startDrag(data.index, event.clientX, event.clientY);
    };
    /**
     * Handle the `'p-dragenter'` event for the widget.
     */
    Notebook.prototype._evtDragEnter = function (event) {
        if (!event.mimeData.hasData(exports.JUPYTER_CELL_MIME)) {
            return;
        }
        event.preventDefault();
        event.stopPropagation();
        var target = event.target;
        var index = this._findCell(target);
        if (index === -1) {
            return;
        }
        var widget = this.layout.widgets[index];
        widget.node.classList.add(DROP_TARGET_CLASS);
    };
    /**
     * Handle the `'p-dragleave'` event for the widget.
     */
    Notebook.prototype._evtDragLeave = function (event) {
        if (!event.mimeData.hasData(exports.JUPYTER_CELL_MIME)) {
            return;
        }
        event.preventDefault();
        event.stopPropagation();
        var elements = this.node.getElementsByClassName(DROP_TARGET_CLASS);
        if (elements.length) {
            elements[0].classList.remove(DROP_TARGET_CLASS);
        }
    };
    /**
     * Handle the `'p-dragover'` event for the widget.
     */
    Notebook.prototype._evtDragOver = function (event) {
        if (!event.mimeData.hasData(exports.JUPYTER_CELL_MIME)) {
            return;
        }
        event.preventDefault();
        event.stopPropagation();
        event.dropAction = event.proposedAction;
        var elements = this.node.getElementsByClassName(DROP_TARGET_CLASS);
        if (elements.length) {
            elements[0].classList.remove(DROP_TARGET_CLASS);
        }
        var target = event.target;
        var index = this._findCell(target);
        if (index === -1) {
            return;
        }
        var widget = this.layout.widgets[index];
        widget.node.classList.add(DROP_TARGET_CLASS);
    };
    /**
     * Handle the `'p-drop'` event for the widget.
     */
    Notebook.prototype._evtDrop = function (event) {
        var _this = this;
        if (!event.mimeData.hasData(exports.JUPYTER_CELL_MIME)) {
            return;
        }
        event.preventDefault();
        event.stopPropagation();
        if (event.proposedAction === 'none') {
            event.dropAction = 'none';
            return;
        }
        var target = event.target;
        while (target && target.parentElement) {
            if (target.classList.contains(DROP_TARGET_CLASS)) {
                target.classList.remove(DROP_TARGET_CLASS);
                break;
            }
            target = target.parentElement;
        }
        var source = event.source;
        if (source === this) {
            // Handle the case where we are moving cells within
            // the same notebook.
            event.dropAction = 'move';
            var toMove = event.mimeData.getData('internal:cells');
            //Compute the to/from indices for the move.
            var fromIndex_1 = algorithm_1.ArrayExt.firstIndexOf(this.widgets, toMove[0]);
            var toIndex_1 = this._findCell(target);
            // This check is needed for consistency with the view.
            if (toIndex_1 !== -1 && toIndex_1 > fromIndex_1) {
                toIndex_1 -= 1;
            }
            else if (toIndex_1 === -1) {
                // If the drop is within the notebook but not on any cell,
                // most often this means it is past the cell areas, so
                // set it to move the cells to the end of the notebook.
                toIndex_1 = this.widgets.length - 1;
            }
            //Don't move if we are within the block of selected cells.
            if (toIndex_1 >= fromIndex_1 && toIndex_1 < fromIndex_1 + toMove.length) {
                return;
            }
            // Move the cells one by one
            this.model.cells.beginCompoundOperation();
            if (fromIndex_1 < toIndex_1) {
                algorithm_1.each(toMove, function (cellWidget) {
                    _this.model.cells.move(fromIndex_1, toIndex_1);
                });
            }
            else if (fromIndex_1 > toIndex_1) {
                algorithm_1.each(toMove, function (cellWidget) {
                    _this.model.cells.move(fromIndex_1++, toIndex_1++);
                });
            }
            this.model.cells.endCompoundOperation();
        }
        else {
            // Handle the case where we are copying cells between
            // notebooks.
            event.dropAction = 'copy';
            // Find the target cell and insert the copied cells.
            var index_1 = this._findCell(target);
            if (index_1 === -1) {
                index_1 = this.widgets.length;
            }
            var model_1 = this.model;
            var values = event.mimeData.getData(exports.JUPYTER_CELL_MIME);
            var factory_1 = model_1.contentFactory;
            // Insert the copies of the original cells.
            model_1.cells.beginCompoundOperation();
            algorithm_1.each(values, function (cell) {
                var value;
                switch (cell.cell_type) {
                    case 'code':
                        value = factory_1.createCodeCell({ cell: cell });
                        break;
                    case 'markdown':
                        value = factory_1.createMarkdownCell({ cell: cell });
                        break;
                    default:
                        value = factory_1.createRawCell({ cell: cell });
                        break;
                }
                model_1.cells.insert(index_1++, value);
            });
            model_1.cells.endCompoundOperation();
            // Activate the last cell.
            this.activeCellIndex = index_1 - 1;
        }
    };
    /**
     * Start a drag event.
     */
    Notebook.prototype._startDrag = function (index, clientX, clientY) {
        var _this = this;
        var cells = this.model.cells;
        var selected = [];
        var toMove = [];
        algorithm_1.each(this.widgets, function (widget, i) {
            var cell = cells.at(i);
            if (_this.isSelected(widget)) {
                widget.addClass(DROP_SOURCE_CLASS);
                selected.push(cell.toJSON());
                toMove.push(widget);
            }
        });
        // Create the drag image.
        var dragImage = Private.createDragImage(selected.length);
        // Set up the drag event.
        this._drag = new dragdrop_1.Drag({
            mimeData: new coreutils_1.MimeData(),
            dragImage: dragImage,
            supportedActions: 'copy-move',
            proposedAction: 'copy',
            source: this
        });
        this._drag.mimeData.setData(exports.JUPYTER_CELL_MIME, selected);
        // Add mimeData for the fully reified cell widgets, for the
        // case where the target is in the same notebook and we
        // can just move the cells.
        this._drag.mimeData.setData('internal:cells', toMove);
        // Remove mousemove and mouseup listeners and start the drag.
        document.removeEventListener('mousemove', this, true);
        document.removeEventListener('mouseup', this, true);
        this._drag.start(clientX, clientY).then(function (action) {
            if (_this.isDisposed) {
                return;
            }
            _this._drag = null;
            algorithm_1.each(toMove, function (widget) { widget.removeClass(DROP_SOURCE_CLASS); });
        });
    };
    /**
     * Handle `focus` events for the widget.
     */
    Notebook.prototype._evtFocus = function (event) {
        var target = event.target;
        var i = this._findCell(target);
        if (i !== -1) {
            var widget = this.widgets[i];
            // If the editor itself does not have focus, ensure command mode.
            if (!widget.editorWidget.node.contains(target)) {
                this.mode = 'command';
            }
            this.activeCellIndex = i;
            // If the editor has focus, ensure edit mode.
            var node = widget.editorWidget.node;
            if (node.contains(target)) {
                this.mode = 'edit';
                this.scrollToPosition(node.getBoundingClientRect().top);
            }
        }
        else {
            // No cell has focus, ensure command mode.
            this.mode = 'command';
        }
    };
    /**
     * Handle `blur` events for the notebook.
     */
    Notebook.prototype._evtBlur = function (event) {
        var relatedTarget = event.relatedTarget;
        // Bail if focus is leaving the notebook.
        if (!this.node.contains(relatedTarget)) {
            return;
        }
        this.mode = 'command';
    };
    /**
     * Handle `dblclick` events for the widget.
     */
    Notebook.prototype._evtDblClick = function (event) {
        var model = this.model;
        if (!model || model.readOnly) {
            return;
        }
        var target = event.target;
        var i = this._findCell(target);
        if (i === -1) {
            return;
        }
        this.activeCellIndex = i;
        if (model.cells.at(i).type === 'markdown') {
            var widget = this.widgets[i];
            widget.rendered = false;
        }
        else if (target.localName === 'img') {
            target.classList.toggle(UNCONFINED_CLASS);
        }
    };
    /**
     * Extend the selection to a given index.
     */
    Notebook.prototype._extendSelectionTo = function (index) {
        var activeIndex = this.activeCellIndex;
        var j = index;
        // extend the existing selection.
        if (j > activeIndex) {
            while (j > activeIndex) {
                Private.selectedProperty.set(this.widgets[j], true);
                j--;
            }
        }
        else if (j < activeIndex) {
            while (j < activeIndex) {
                Private.selectedProperty.set(this.widgets[j], true);
                j++;
            }
        }
        Private.selectedProperty.set(this.widgets[activeIndex], true);
        this._selectionChanged.emit(void 0);
    };
    return Notebook;
}(StaticNotebook));
exports.Notebook = Notebook;
/**
 * The namespace for the `Notebook` class statics.
 */
(function (Notebook) {
    /**
     * The default implementation of an `IFactory`.
     */
    var ContentFactory = (function (_super) {
        __extends(ContentFactory, _super);
        function ContentFactory() {
            return _super !== null && _super.apply(this, arguments) || this;
        }
        return ContentFactory;
    }(StaticNotebook.ContentFactory));
    Notebook.ContentFactory = ContentFactory;
})(Notebook = exports.Notebook || (exports.Notebook = {}));
exports.Notebook = Notebook;
/**
 * A namespace for private data.
 */
var Private;
(function (Private) {
    /**
     * An attached property for the selected state of a cell.
     */
    Private.selectedProperty = new properties_1.AttachedProperty({
        name: 'selected',
        create: function () { return false; }
    });
    /**
     * A custom panel layout for the notebook.
     */
    var NotebookPanelLayout = (function (_super) {
        __extends(NotebookPanelLayout, _super);
        function NotebookPanelLayout() {
            return _super !== null && _super.apply(this, arguments) || this;
        }
        /**
         * A message handler invoked on an `'update-request'` message.
         *
         * #### Notes
         * This is a reimplementation of the base class method,
         * and is a no-op.
         */
        NotebookPanelLayout.prototype.onUpdateRequest = function (msg) {
            // This is a no-op.
        };
        return NotebookPanelLayout;
    }(widgets_1.PanelLayout));
    Private.NotebookPanelLayout = NotebookPanelLayout;
    /**
     * Create a cell drag image.
     */
    function createDragImage(count) {
        var node = document.createElement('div');
        var span = document.createElement('span');
        span.textContent = "" + count;
        span.className = FILLED_CIRCLE_CLASS;
        node.appendChild(span);
        node.className = DRAG_IMAGE_CLASS;
        return node;
    }
    Private.createDragImage = createDragImage;
})(Private || (Private = {}));

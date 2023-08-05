// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var apputils_1 = require("@jupyterlab/apputils");
var cells_1 = require("@jupyterlab/cells");
var algorithm_1 = require("@phosphor/algorithm");
var domutils_1 = require("@phosphor/domutils");
var widget_1 = require("./widget");
/**
 * A namespace for handling actions on a notebook.
 *
 * #### Notes
 * All of the actions are a no-op if there is no model on the notebook.
 * The actions set the widget `mode` to `'command'` unless otherwise specified.
 * The actions will preserve the selection on the notebook widget unless
 * otherwise specified.
 */
var NotebookActions;
(function (NotebookActions) {
    /**
     * Split the active cell into two cells.
     *
     * @param widget - The target notebook widget.
     *
     * #### Notes
     * It will preserve the existing mode.
     * The second cell will be activated.
     * The existing selection will be cleared.
     * The leading whitespace in the second cell will be removed.
     * If there is no content, two empty cells will be created.
     * Both cells will have the same type as the original cell.
     * This action can be undone.
     */
    function splitCell(widget) {
        if (!widget.model || !widget.activeCell) {
            return;
        }
        var state = Private.getState(widget);
        widget.deselectAll();
        var nbModel = widget.model;
        var index = widget.activeCellIndex;
        var child = widget.widgets[index];
        var editor = child.editor;
        var position = editor.getCursorPosition();
        var offset = editor.getOffsetAt(position);
        var orig = child.model.value.text;
        // Create new models to preserve history.
        var clone0 = Private.cloneCell(nbModel, child.model);
        var clone1 = Private.cloneCell(nbModel, child.model);
        if (clone0.type === 'code') {
            clone0.outputs.clear();
        }
        clone0.value.text = orig.slice(0, offset).replace(/^\n+/, '').replace(/\n+$/, '');
        clone1.value.text = orig.slice(offset).replace(/^\n+/, '').replace(/\n+$/, '');
        // Make the changes while preserving history.
        var cells = nbModel.cells;
        cells.beginCompoundOperation();
        cells.set(index, clone0);
        cells.insert(index + 1, clone1);
        cells.endCompoundOperation();
        widget.activeCellIndex++;
        Private.handleState(widget, state);
    }
    NotebookActions.splitCell = splitCell;
    /**
     * Merge the selected cells.
     *
     * @param widget - The target notebook widget.
     *
     * #### Notes
     * The widget mode will be preserved.
     * If only one cell is selected, the next cell will be selected.
     * If the active cell is a code cell, its outputs will be cleared.
     * This action can be undone.
     * The final cell will have the same type as the active cell.
     * If the active cell is a markdown cell, it will be unrendered.
     */
    function mergeCells(widget) {
        if (!widget.model || !widget.activeCell) {
            return;
        }
        var state = Private.getState(widget);
        var toMerge = [];
        var toDelete = [];
        var model = widget.model;
        var cells = model.cells;
        var primary = widget.activeCell;
        var index = widget.activeCellIndex;
        var offset = 0;
        // Get the cells to merge.
        algorithm_1.each(widget.widgets, function (child, i) {
            if (widget.isSelected(child)) {
                toMerge.push(child.model.value.text);
                if (i !== index) {
                    toDelete.push(child.model);
                    if (i < index) {
                        offset += 1;
                    }
                }
            }
        });
        // Check for only a single cell selected.
        if (toMerge.length === 1) {
            // Bail if it is the last cell.
            if (index === cells.length - 1) {
                return;
            }
            // Otherwise merge with the next cell.
            var cellModel = cells.at(index + 1);
            toMerge.push(cellModel.value.text);
            toDelete.push(cellModel);
        }
        widget.deselectAll();
        // Create a new cell for the source to preserve history.
        var newModel = Private.cloneCell(model, primary.model);
        newModel.value.text = toMerge.join('\n\n');
        if (newModel.type === 'code') {
            newModel.outputs.clear();
        }
        // Make the changes while preserving history.
        cells.beginCompoundOperation();
        cells.set(index, newModel);
        algorithm_1.each(toDelete, function (cell) {
            cells.remove(cell);
        });
        cells.endCompoundOperation();
        // If the original cell is a markdown cell, make sure
        // the new cell is unrendered.
        if (primary instanceof cells_1.MarkdownCellWidget) {
            var cell = widget.activeCell;
            cell.rendered = false;
        }
        widget.activeCellIndex -= offset;
        Private.handleState(widget, state);
    }
    NotebookActions.mergeCells = mergeCells;
    /**
     * Delete the selected cells.
     *
     * @param widget - The target notebook widget.
     *
     * #### Notes
     * The cell after the last selected cell will be activated.
     * It will add a code cell if all cells are deleted.
     * This action can be undone.
     */
    function deleteCells(widget) {
        if (!widget.model || !widget.activeCell) {
            return;
        }
        var state = Private.getState(widget);
        Private.deleteCells(widget);
        Private.handleState(widget, state);
    }
    NotebookActions.deleteCells = deleteCells;
    /**
     * Insert a new code cell above the active cell.
     *
     * @param widget - The target notebook widget.
     *
     * #### Notes
     * The widget mode will be preserved.
     * This action can be undone.
     * The existing selection will be cleared.
     * The new cell will the active cell.
     */
    function insertAbove(widget) {
        if (!widget.model || !widget.activeCell) {
            return;
        }
        var state = Private.getState(widget);
        var model = widget.model;
        var cell = model.contentFactory.createCodeCell({});
        model.cells.insert(widget.activeCellIndex, cell);
        widget.deselectAll();
        Private.handleState(widget, state);
    }
    NotebookActions.insertAbove = insertAbove;
    /**
     * Insert a new code cell below the active cell.
     *
     * @param widget - The target notebook widget.
     *
     * #### Notes
     * The widget mode will be preserved.
     * This action can be undone.
     * The existing selection will be cleared.
     * The new cell will be the active cell.
     */
    function insertBelow(widget) {
        if (!widget.model || !widget.activeCell) {
            return;
        }
        var state = Private.getState(widget);
        var model = widget.model;
        var cell = model.contentFactory.createCodeCell({});
        model.cells.insert(widget.activeCellIndex + 1, cell);
        widget.activeCellIndex++;
        widget.deselectAll();
        Private.handleState(widget, state);
    }
    NotebookActions.insertBelow = insertBelow;
    /**
     * Move the selected cell(s) down.
     *
     * @param widget = The target notebook widget.
     */
    function moveDown(widget) {
        if (!widget.model || !widget.activeCell) {
            return;
        }
        var state = Private.getState(widget);
        var cells = widget.model.cells;
        var widgets = widget.widgets;
        cells.beginCompoundOperation();
        for (var i = cells.length - 2; i > -1; i--) {
            if (widget.isSelected(widgets[i])) {
                if (!widget.isSelected(widgets[i + 1])) {
                    cells.move(i, i + 1);
                    if (widget.activeCellIndex === i) {
                        widget.activeCellIndex++;
                    }
                    widget.select(widgets[i + 1]);
                    widget.deselect(widgets[i]);
                }
            }
        }
        cells.endCompoundOperation();
        Private.handleState(widget, state);
    }
    NotebookActions.moveDown = moveDown;
    /**
     * Move the selected cell(s) up.
     *
     * @param widget - The target notebook widget.
     */
    function moveUp(widget) {
        if (!widget.model || !widget.activeCell) {
            return;
        }
        var state = Private.getState(widget);
        var cells = widget.model.cells;
        var widgets = widget.widgets;
        cells.beginCompoundOperation();
        for (var i = 1; i < cells.length; i++) {
            if (widget.isSelected(widgets[i])) {
                if (!widget.isSelected(widgets[i - 1])) {
                    cells.move(i, i - 1);
                    if (widget.activeCellIndex === i) {
                        widget.activeCellIndex--;
                    }
                    widget.select(widgets[i - 1]);
                    widget.deselect(widgets[i]);
                }
            }
        }
        cells.endCompoundOperation();
        Private.handleState(widget, state);
    }
    NotebookActions.moveUp = moveUp;
    /**
     * Change the selected cell type(s).
     *
     * @param widget - The target notebook widget.
     *
     * @param value - The target cell type.
     *
     * #### Notes
     * It should preserve the widget mode.
     * This action can be undone.
     * The existing selection will be cleared.
     * Any cells converted to markdown will be unrendered.
     */
    function changeCellType(widget, value) {
        if (!widget.model || !widget.activeCell) {
            return;
        }
        var state = Private.getState(widget);
        Private.changeCellType(widget, value);
        Private.handleState(widget, state);
    }
    NotebookActions.changeCellType = changeCellType;
    /**
     * Run the selected cell(s).
     *
     * @param widget - The target notebook widget.
     *
     * @param session - The optional client session object.
     *
     * #### Notes
     * The last selected cell will be activated.
     * The existing selection will be cleared.
     * An execution error will prevent the remaining code cells from executing.
     * All markdown cells will be rendered.
     */
    function run(widget, session) {
        if (!widget.model || !widget.activeCell) {
            return Promise.resolve(false);
        }
        var state = Private.getState(widget);
        var promise = Private.runSelected(widget, session);
        Private.handleRunState(widget, state);
        return promise;
    }
    NotebookActions.run = run;
    /**
     * Run the selected cell(s) and advance to the next cell.
     *
     * @param widget - The target notebook widget.
     *
     * @param session - The optional client session object.
     *
     * #### Notes
     * The existing selection will be cleared.
     * The cell after the last selected cell will be activated.
     * An execution error will prevent the remaining code cells from executing.
     * All markdown cells will be rendered.
     * If the last selected cell is the last cell, a new code cell
     * will be created in `'edit'` mode.  The new cell creation can be undone.
     */
    function runAndAdvance(widget, session) {
        if (!widget.model || !widget.activeCell) {
            return Promise.resolve(false);
        }
        var state = Private.getState(widget);
        var promise = Private.runSelected(widget, session);
        var model = widget.model;
        if (widget.activeCellIndex === widget.widgets.length - 1) {
            var cell = model.contentFactory.createCodeCell({});
            model.cells.pushBack(cell);
            widget.activeCellIndex++;
            widget.mode = 'edit';
        }
        else {
            widget.activeCellIndex++;
        }
        Private.handleRunState(widget, state);
        return promise;
    }
    NotebookActions.runAndAdvance = runAndAdvance;
    /**
     * Run the selected cell(s) and insert a new code cell.
     *
     * @param widget - The target notebook widget.
     *
     * @param session - The optional client session object.
     *
     * #### Notes
     * An execution error will prevent the remaining code cells from executing.
     * All markdown cells will be rendered.
     * The widget mode will be set to `'edit'` after running.
     * The existing selection will be cleared.
     * The cell insert can be undone.
     */
    function runAndInsert(widget, session) {
        if (!widget.model || !widget.activeCell) {
            return Promise.resolve(false);
        }
        var state = Private.getState(widget);
        var promise = Private.runSelected(widget, session);
        var model = widget.model;
        var cell = model.contentFactory.createCodeCell({});
        model.cells.insert(widget.activeCellIndex + 1, cell);
        widget.activeCellIndex++;
        widget.mode = 'edit';
        Private.handleRunState(widget, state);
        return promise;
    }
    NotebookActions.runAndInsert = runAndInsert;
    /**
     * Run all of the cells in the notebook.
     *
     * @param widget - The target notebook widget.
     *
     * @param session - The optional client session object.
     *
     * #### Notes
     * The existing selection will be cleared.
     * An execution error will prevent the remaining code cells from executing.
     * All markdown cells will be rendered.
     * The last cell in the notebook will be activated.
     */
    function runAll(widget, session) {
        if (!widget.model || !widget.activeCell) {
            return Promise.resolve(false);
        }
        var state = Private.getState(widget);
        algorithm_1.each(widget.widgets, function (child) {
            widget.select(child);
        });
        var promise = Private.runSelected(widget, session);
        Private.handleRunState(widget, state);
        return promise;
    }
    NotebookActions.runAll = runAll;
    /**
     * Select the above the active cell.
     *
     * @param widget - The target notebook widget.
     *
     * #### Notes
     * The widget mode will be preserved.
     * This is a no-op if the first cell is the active cell.
     * The existing selection will be cleared.
     */
    function selectAbove(widget) {
        if (!widget.model || !widget.activeCell) {
            return;
        }
        if (widget.activeCellIndex === 0) {
            return;
        }
        var state = Private.getState(widget);
        widget.activeCellIndex -= 1;
        widget.deselectAll();
        Private.handleState(widget, state);
    }
    NotebookActions.selectAbove = selectAbove;
    /**
     * Select the cell below the active cell.
     *
     * @param widget - The target notebook widget.
     *
     * #### Notes
     * The widget mode will be preserved.
     * This is a no-op if the last cell is the active cell.
     * The existing selection will be cleared.
     */
    function selectBelow(widget) {
        if (!widget.model || !widget.activeCell) {
            return;
        }
        if (widget.activeCellIndex === widget.widgets.length - 1) {
            return;
        }
        var state = Private.getState(widget);
        widget.activeCellIndex += 1;
        widget.deselectAll();
        Private.handleState(widget, state);
    }
    NotebookActions.selectBelow = selectBelow;
    /**
     * Extend the selection to the cell above.
     *
     * @param widget - The target notebook widget.
     *
     * #### Notes
     * This is a no-op if the first cell is the active cell.
     * The new cell will be activated.
     */
    function extendSelectionAbove(widget) {
        if (!widget.model || !widget.activeCell) {
            return;
        }
        // Do not wrap around.
        if (widget.activeCellIndex === 0) {
            return;
        }
        var state = Private.getState(widget);
        widget.mode = 'command';
        var current = widget.activeCell;
        var prev = widget.widgets[widget.activeCellIndex - 1];
        if (widget.isSelected(prev)) {
            widget.deselect(current);
            if (widget.activeCellIndex > 1) {
                var prevPrev = widget.widgets[widget.activeCellIndex - 2];
                if (!widget.isSelected(prevPrev)) {
                    widget.deselect(prev);
                }
            }
        }
        else {
            widget.select(current);
        }
        widget.activeCellIndex -= 1;
        Private.handleState(widget, state);
    }
    NotebookActions.extendSelectionAbove = extendSelectionAbove;
    /**
     * Extend the selection to the cell below.
     *
     * @param widget - The target notebook widget.
     *
     * #### Notes
     * This is a no-op if the last cell is the active cell.
     * The new cell will be activated.
     */
    function extendSelectionBelow(widget) {
        if (!widget.model || !widget.activeCell) {
            return;
        }
        // Do not wrap around.
        if (widget.activeCellIndex === widget.widgets.length - 1) {
            return;
        }
        var state = Private.getState(widget);
        widget.mode = 'command';
        var current = widget.activeCell;
        var next = widget.widgets[widget.activeCellIndex + 1];
        if (widget.isSelected(next)) {
            widget.deselect(current);
            if (widget.activeCellIndex < widget.model.cells.length - 2) {
                var nextNext = widget.widgets[widget.activeCellIndex + 2];
                if (!widget.isSelected(nextNext)) {
                    widget.deselect(next);
                }
            }
        }
        else {
            widget.select(current);
        }
        widget.activeCellIndex += 1;
        Private.handleState(widget, state);
    }
    NotebookActions.extendSelectionBelow = extendSelectionBelow;
    /**
     * Copy the selected cell data to a clipboard.
     *
     * @param widget - The target notebook widget.
     */
    function copy(widget) {
        Private.copyOrCut(widget, false);
    }
    NotebookActions.copy = copy;
    /**
     * Cut the selected cell data to a clipboard.
     *
     * @param widget - The target notebook widget.
     *
     * #### Notes
     * This action can be undone.
     * A new code cell is added if all cells are cut.
     */
    function cut(widget) {
        Private.copyOrCut(widget, true);
    }
    NotebookActions.cut = cut;
    /**
     * Paste cells from the application clipboard.
     *
     * @param widget - The target notebook widget.
     *
     * #### Notes
     * The cells are pasted below the active cell.
     * The last pasted cell becomes the active cell.
     * This is a no-op if there is no cell data on the clipboard.
     * This action can be undone.
     */
    function paste(widget) {
        if (!widget.model || !widget.activeCell) {
            return;
        }
        var clipboard = apputils_1.Clipboard.getInstance();
        if (!clipboard.hasData(widget_1.JUPYTER_CELL_MIME)) {
            return;
        }
        var state = Private.getState(widget);
        var values = clipboard.getData(widget_1.JUPYTER_CELL_MIME);
        var model = widget.model;
        var newCells = [];
        widget.mode = 'command';
        algorithm_1.each(values, function (cell) {
            switch (cell.cell_type) {
                case 'code':
                    newCells.push(model.contentFactory.createCodeCell({ cell: cell }));
                    break;
                case 'markdown':
                    newCells.push(model.contentFactory.createMarkdownCell({ cell: cell }));
                    break;
                default:
                    newCells.push(model.contentFactory.createRawCell({ cell: cell }));
                    break;
            }
        });
        var index = widget.activeCellIndex;
        var cells = widget.model.cells;
        cells.beginCompoundOperation();
        algorithm_1.each(newCells, function (cell) {
            cells.insert(++index, cell);
        });
        cells.endCompoundOperation();
        widget.activeCellIndex += newCells.length;
        widget.deselectAll();
        Private.handleState(widget, state);
    }
    NotebookActions.paste = paste;
    /**
     * Undo a cell action.
     *
     * @param widget - The target notebook widget.
     *
     * #### Notes
     * This is a no-op if if there are no cell actions to undo.
     */
    function undo(widget) {
        if (!widget.model || !widget.activeCell) {
            return;
        }
        var state = Private.getState(widget);
        widget.mode = 'command';
        widget.model.cells.undo();
        widget.deselectAll();
        Private.handleState(widget, state);
    }
    NotebookActions.undo = undo;
    /**
     * Redo a cell action.
     *
     * @param widget - The target notebook widget.
     *
     * #### Notes
     * This is a no-op if there are no cell actions to redo.
     */
    function redo(widget) {
        if (!widget.model || !widget.activeCell) {
            return;
        }
        var state = Private.getState(widget);
        widget.mode = 'command';
        widget.model.cells.redo();
        widget.deselectAll();
        Private.handleState(widget, state);
    }
    NotebookActions.redo = redo;
    /**
     * Toggle line numbers on the selected cell(s).
     *
     * @param widget - The target notebook widget.
     *
     * #### Notes
     * The original state is based on the state of the active cell.
     * The `mode` of the widget will be preserved.
     */
    function toggleLineNumbers(widget) {
        if (!widget.model || !widget.activeCell) {
            return;
        }
        var state = Private.getState(widget);
        var lineNumbers = widget.activeCell.editor.lineNumbers;
        algorithm_1.each(widget.widgets, function (child) {
            if (widget.isSelected(child)) {
                child.editor.lineNumbers = !lineNumbers;
            }
        });
        Private.handleState(widget, state);
    }
    NotebookActions.toggleLineNumbers = toggleLineNumbers;
    /**
     * Toggle the line number of all cells.
     *
     * @param widget - The target notebook widget.
     *
     * #### Notes
     * The original state is based on the state of the active cell.
     * The `mode` of the widget will be preserved.
     */
    function toggleAllLineNumbers(widget) {
        if (!widget.model || !widget.activeCell) {
            return;
        }
        var state = Private.getState(widget);
        var lineNumbers = widget.activeCell.editor.lineNumbers;
        algorithm_1.each(widget.widgets, function (child) {
            child.editor.lineNumbers = !lineNumbers;
        });
        Private.handleState(widget, state);
    }
    NotebookActions.toggleAllLineNumbers = toggleAllLineNumbers;
    /**
     * Clear the code outputs of the selected cells.
     *
     * @param widget - The target notebook widget.
     *
     * #### Notes
     * The widget `mode` will be preserved.
     */
    function clearOutputs(widget) {
        if (!widget.model || !widget.activeCell) {
            return;
        }
        var state = Private.getState(widget);
        var cells = widget.model.cells;
        var i = 0;
        algorithm_1.each(cells, function (cell) {
            var child = widget.widgets[i];
            if (widget.isSelected(child) && cell.type === 'code') {
                cell.outputs.clear();
                cell.executionCount = null;
            }
            i++;
        });
        Private.handleState(widget, state);
    }
    NotebookActions.clearOutputs = clearOutputs;
    /**
     * Clear all the code outputs on the widget.
     *
     * @param widget - The target notebook widget.
     *
     * #### Notes
     * The widget `mode` will be preserved.
     */
    function clearAllOutputs(widget) {
        if (!widget.model || !widget.activeCell) {
            return;
        }
        var state = Private.getState(widget);
        algorithm_1.each(widget.model.cells, function (cell) {
            if (cell.type === 'code') {
                cell.outputs.clear();
                cell.executionCount = null;
            }
        });
        Private.handleState(widget, state);
    }
    NotebookActions.clearAllOutputs = clearAllOutputs;
    /**
     * Set the markdown header level.
     *
     * @param widget - The target notebook widget.
     *
     * @param level - The header level.
     *
     * #### Notes
     * All selected cells will be switched to markdown.
     * The level will be clamped between 1 and 6.
     * If there is an existing header, it will be replaced.
     * There will always be one blank space after the header.
     * The cells will be unrendered.
     */
    function setMarkdownHeader(widget, level) {
        if (!widget.model || !widget.activeCell) {
            return;
        }
        var state = Private.getState(widget);
        level = Math.min(Math.max(level, 1), 6);
        var cells = widget.model.cells;
        var i = 0;
        algorithm_1.each(widget.widgets, function (child) {
            if (widget.isSelected(child)) {
                Private.setMarkdownHeader(cells.at(i), level);
            }
            i++;
        });
        Private.changeCellType(widget, 'markdown');
        Private.handleState(widget, state);
    }
    NotebookActions.setMarkdownHeader = setMarkdownHeader;
})(NotebookActions = exports.NotebookActions || (exports.NotebookActions = {}));
/**
 * A namespace for private data.
 */
var Private;
(function (Private) {
    /**
     * Get the state of a widget before running an action.
     */
    function getState(widget) {
        return {
            wasFocused: widget.node.contains(document.activeElement),
            activeCell: widget.activeCell
        };
    }
    Private.getState = getState;
    /**
     * Handle the state of a widget after running an action.
     */
    function handleState(widget, state) {
        if (state.wasFocused || widget.mode === 'edit') {
            widget.activate();
        }
        domutils_1.ElementExt.scrollIntoViewIfNeeded(widget.node, widget.activeCell.node);
    }
    Private.handleState = handleState;
    /**
     * Handle the state of a widget after running a run action.
     */
    function handleRunState(widget, state) {
        if (state.wasFocused || widget.mode === 'edit') {
            widget.activate();
        }
        // Scroll to the top of the previous active cell output.
        var er = state.activeCell.editorWidget.node.getBoundingClientRect();
        widget.scrollToPosition(er.bottom);
    }
    Private.handleRunState = handleRunState;
    /**
     * Clone a cell model.
     */
    function cloneCell(model, cell) {
        switch (cell.type) {
            case 'code':
                return model.contentFactory.createCodeCell(cell.toJSON());
            case 'markdown':
                return model.contentFactory.createMarkdownCell(cell.toJSON());
            default:
                return model.contentFactory.createRawCell(cell.toJSON());
        }
    }
    Private.cloneCell = cloneCell;
    /**
     * Run the selected cells.
     */
    function runSelected(widget, session) {
        widget.mode = 'command';
        var selected = [];
        var lastIndex = widget.activeCellIndex;
        var i = 0;
        algorithm_1.each(widget.widgets, function (child) {
            if (widget.isSelected(child)) {
                selected.push(child);
                lastIndex = i;
            }
            i++;
        });
        widget.activeCellIndex = lastIndex;
        widget.deselectAll();
        var promises = [];
        algorithm_1.each(selected, function (child) {
            promises.push(runCell(widget, child, session));
        });
        return Promise.all(promises).then(function (results) {
            if (widget.isDisposed) {
                return false;
            }
            // Post an update request.
            widget.update();
            for (var _i = 0, results_1 = results; _i < results_1.length; _i++) {
                var result = results_1[_i];
                if (!result) {
                    return false;
                }
            }
            return true;
        });
    }
    Private.runSelected = runSelected;
    /**
     * Run a cell.
     */
    function runCell(parent, child, session) {
        switch (child.model.type) {
            case 'markdown':
                child.rendered = true;
                break;
            case 'code':
                if (session) {
                    return child.execute(session).then(function (reply) {
                        if (child.isDisposed) {
                            return false;
                        }
                        if (reply && reply.content.status === 'ok') {
                            var content = reply.content;
                            if (content.payload && content.payload.length) {
                                handlePayload(content, parent, child);
                            }
                        }
                        return reply ? reply.content.status === 'ok' : true;
                    });
                }
                child.model.executionCount = null;
                break;
            default:
                break;
        }
        return Promise.resolve(true);
    }
    /**
     * Handle payloads from an execute reply.
     *
     * #### Notes
     * Payloads are deprecated and there are no official interfaces for them in
     * the kernel type definitions.
     * See [Payloads (DEPRECATED)](https://jupyter-client.readthedocs.io/en/latest/messaging.html#payloads-deprecated).
     */
    function handlePayload(content, parent, child) {
        var setNextInput = content.payload.filter(function (i) {
            return i.source === 'set_next_input';
        })[0];
        if (!setNextInput) {
            return;
        }
        var text = setNextInput.text;
        var replace = setNextInput.replace;
        if (replace) {
            child.model.value.text = text;
            return;
        }
        // Create a new code cell and add as the next cell.
        var cell = parent.model.contentFactory.createCodeCell({});
        cell.value.text = text;
        var cells = parent.model.cells;
        var i = algorithm_1.ArrayExt.firstIndexOf(algorithm_1.toArray(cells), child.model);
        if (i === -1) {
            cells.pushBack(cell);
        }
        else {
            cells.insert(i + 1, cell);
        }
    }
    /**
     * Copy or cut the selected cell data to the application clipboard.
     *
     * @param widget - The target notebook widget.
     *
     * @param cut - Whether to copy or cut.
     */
    function copyOrCut(widget, cut) {
        if (!widget.model || !widget.activeCell) {
            return;
        }
        var state = getState(widget);
        widget.mode = 'command';
        var clipboard = apputils_1.Clipboard.getInstance();
        clipboard.clear();
        var data = [];
        algorithm_1.each(widget.widgets, function (child) {
            if (widget.isSelected(child)) {
                data.push(child.model.toJSON());
            }
        });
        clipboard.setData(widget_1.JUPYTER_CELL_MIME, data);
        if (cut) {
            deleteCells(widget);
        }
        else {
            widget.deselectAll();
        }
        handleState(widget, state);
    }
    Private.copyOrCut = copyOrCut;
    /**
     * Change the selected cell type(s).
     *
     * @param widget - The target notebook widget.
     *
     * @param value - The target cell type.
     *
     * #### Notes
     * It should preserve the widget mode.
     * This action can be undone.
     * The existing selection will be cleared.
     * Any cells converted to markdown will be unrendered.
     */
    function changeCellType(widget, value) {
        var model = widget.model;
        var cells = model.cells;
        cells.beginCompoundOperation();
        algorithm_1.each(widget.widgets, function (child, i) {
            if (!widget.isSelected(child)) {
                return;
            }
            if (child.model.type !== value) {
                var cell = child.model.toJSON();
                var newCell = void 0;
                switch (value) {
                    case 'code':
                        newCell = model.contentFactory.createCodeCell({ cell: cell });
                        break;
                    case 'markdown':
                        newCell = model.contentFactory.createMarkdownCell({ cell: cell });
                        if (child.model.type === 'code') {
                            newCell.trusted = false;
                        }
                        break;
                    default:
                        newCell = model.contentFactory.createRawCell({ cell: cell });
                        if (child.model.type === 'code') {
                            newCell.trusted = false;
                        }
                }
                cells.set(i, newCell);
            }
            if (value === 'markdown') {
                // Fetch the new widget and unrender it.
                child = widget.widgets[i];
                child.rendered = false;
            }
        });
        cells.endCompoundOperation();
        widget.deselectAll();
    }
    Private.changeCellType = changeCellType;
    /**
     * Delete the selected cells.
     *
     * @param widget - The target notebook widget.
     *
     * #### Notes
     * The cell after the last selected cell will be activated.
     * It will add a code cell if all cells are deleted.
     * This action can be undone.
     */
    function deleteCells(widget) {
        var model = widget.model;
        var cells = model.cells;
        var toDelete = [];
        widget.mode = 'command';
        // Find the cells to delete.
        algorithm_1.each(widget.widgets, function (child, i) {
            var deletable = child.model.metadata.get('deletable');
            if (widget.isSelected(child) && deletable !== false) {
                toDelete.push(i);
            }
        });
        // If cells are not deletable, we may not have anything to delete.
        if (toDelete.length > 0) {
            // Delete the cells as one undo event.
            cells.beginCompoundOperation();
            algorithm_1.each(toDelete.reverse(), function (i) {
                cells.removeAt(i);
            });
            // Add a new cell if the notebook is empty. This is done
            // within the compound operation to make the deletion of
            // a notebook's last cell undoable.
            if (!cells.length) {
                cells.pushBack(model.contentFactory.createCodeCell({}));
            }
            cells.endCompoundOperation();
            // Select the *first* interior cell not deleted or the cell
            // *after* the last selected cell.
            // Note: The activeCellIndex is clamped to the available cells,
            // so if the last cell is deleted the previous cell will be activated.
            widget.activeCellIndex = toDelete[0];
        }
        // Deselect any remaining, undeletable cells. Do this even if we don't
        // delete anything so that users are aware *something* happened.
        widget.deselectAll();
    }
    Private.deleteCells = deleteCells;
    /**
     * Set the markdown header level of a cell.
     */
    function setMarkdownHeader(cell, level) {
        var source = cell.value.text;
        var newHeader = Array(level + 1).join('#') + ' ';
        // Remove existing header or leading white space.
        var regex = /^(#+\s*)|^(\s*)/;
        var matches = regex.exec(source);
        if (matches) {
            source = source.slice(matches[0].length);
        }
        cell.value.text = newHeader + source;
    }
    Private.setMarkdownHeader = setMarkdownHeader;
})(Private || (Private = {}));

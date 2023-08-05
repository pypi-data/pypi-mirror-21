import { IClientSession } from '@jupyterlab/apputils';
import { nbformat } from '@jupyterlab/coreutils';
import { Notebook } from './widget';
/**
 * A namespace for handling actions on a notebook.
 *
 * #### Notes
 * All of the actions are a no-op if there is no model on the notebook.
 * The actions set the widget `mode` to `'command'` unless otherwise specified.
 * The actions will preserve the selection on the notebook widget unless
 * otherwise specified.
 */
export declare namespace NotebookActions {
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
    function splitCell(widget: Notebook): void;
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
    function mergeCells(widget: Notebook): void;
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
    function deleteCells(widget: Notebook): void;
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
    function insertAbove(widget: Notebook): void;
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
    function insertBelow(widget: Notebook): void;
    /**
     * Move the selected cell(s) down.
     *
     * @param widget = The target notebook widget.
     */
    function moveDown(widget: Notebook): void;
    /**
     * Move the selected cell(s) up.
     *
     * @param widget - The target notebook widget.
     */
    function moveUp(widget: Notebook): void;
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
    function changeCellType(widget: Notebook, value: nbformat.CellType): void;
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
    function run(widget: Notebook, session?: IClientSession): Promise<boolean>;
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
    function runAndAdvance(widget: Notebook, session?: IClientSession): Promise<boolean>;
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
    function runAndInsert(widget: Notebook, session: IClientSession): Promise<boolean>;
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
    function runAll(widget: Notebook, session?: IClientSession): Promise<boolean>;
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
    function selectAbove(widget: Notebook): void;
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
    function selectBelow(widget: Notebook): void;
    /**
     * Extend the selection to the cell above.
     *
     * @param widget - The target notebook widget.
     *
     * #### Notes
     * This is a no-op if the first cell is the active cell.
     * The new cell will be activated.
     */
    function extendSelectionAbove(widget: Notebook): void;
    /**
     * Extend the selection to the cell below.
     *
     * @param widget - The target notebook widget.
     *
     * #### Notes
     * This is a no-op if the last cell is the active cell.
     * The new cell will be activated.
     */
    function extendSelectionBelow(widget: Notebook): void;
    /**
     * Copy the selected cell data to a clipboard.
     *
     * @param widget - The target notebook widget.
     */
    function copy(widget: Notebook): void;
    /**
     * Cut the selected cell data to a clipboard.
     *
     * @param widget - The target notebook widget.
     *
     * #### Notes
     * This action can be undone.
     * A new code cell is added if all cells are cut.
     */
    function cut(widget: Notebook): void;
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
    function paste(widget: Notebook): void;
    /**
     * Undo a cell action.
     *
     * @param widget - The target notebook widget.
     *
     * #### Notes
     * This is a no-op if if there are no cell actions to undo.
     */
    function undo(widget: Notebook): void;
    /**
     * Redo a cell action.
     *
     * @param widget - The target notebook widget.
     *
     * #### Notes
     * This is a no-op if there are no cell actions to redo.
     */
    function redo(widget: Notebook): void;
    /**
     * Toggle line numbers on the selected cell(s).
     *
     * @param widget - The target notebook widget.
     *
     * #### Notes
     * The original state is based on the state of the active cell.
     * The `mode` of the widget will be preserved.
     */
    function toggleLineNumbers(widget: Notebook): void;
    /**
     * Toggle the line number of all cells.
     *
     * @param widget - The target notebook widget.
     *
     * #### Notes
     * The original state is based on the state of the active cell.
     * The `mode` of the widget will be preserved.
     */
    function toggleAllLineNumbers(widget: Notebook): void;
    /**
     * Clear the code outputs of the selected cells.
     *
     * @param widget - The target notebook widget.
     *
     * #### Notes
     * The widget `mode` will be preserved.
     */
    function clearOutputs(widget: Notebook): void;
    /**
     * Clear all the code outputs on the widget.
     *
     * @param widget - The target notebook widget.
     *
     * #### Notes
     * The widget `mode` will be preserved.
     */
    function clearAllOutputs(widget: Notebook): void;
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
    function setMarkdownHeader(widget: Notebook, level: number): void;
}

import { Widget } from '@phosphor/widgets';
import { ToolbarButton } from '@jupyterlab/apputils';
import { NotebookPanel } from './panel';
/**
 * A namespace for the default toolbar items.
 */
export declare namespace ToolbarItems {
    /**
     * Create save button toolbar item.
     */
    function createSaveButton(panel: NotebookPanel): ToolbarButton;
    /**
     * Create an insert toolbar item.
     */
    function createInsertButton(panel: NotebookPanel): ToolbarButton;
    /**
     * Create a cut toolbar item.
     */
    function createCutButton(panel: NotebookPanel): ToolbarButton;
    /**
     * Create a copy toolbar item.
     */
    function createCopyButton(panel: NotebookPanel): ToolbarButton;
    /**
     * Create a paste toolbar item.
     */
    function createPasteButton(panel: NotebookPanel): ToolbarButton;
    /**
     * Create a run toolbar item.
     */
    function createRunButton(panel: NotebookPanel): ToolbarButton;
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
    function createCellTypeItem(panel: NotebookPanel): Widget;
    /**
     * Add the default items to the panel toolbar.
     */
    function populateDefaults(panel: NotebookPanel): void;
}

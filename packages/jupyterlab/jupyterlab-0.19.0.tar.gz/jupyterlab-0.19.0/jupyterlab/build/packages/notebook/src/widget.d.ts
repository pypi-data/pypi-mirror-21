import { JSONValue } from '@phosphor/coreutils';
import { Message } from '@phosphor/messaging';
import { ISignal } from '@phosphor/signaling';
import { Widget } from '@phosphor/widgets';
import { BaseCellWidget, CodeCellWidget, MarkdownCellWidget, RawCellWidget } from '@jupyterlab/cells';
import { IEditorMimeTypeService, CodeEditor } from '@jupyterlab/codeeditor';
import { IChangedArgs, IObservableMap, ObservableMap } from '@jupyterlab/coreutils';
import { RenderMime } from '@jupyterlab/rendermime';
import { OutputAreaWidget } from '@jupyterlab/outputarea';
import { INotebookModel } from './model';
/**
 * The mimetype used for Jupyter cell data.
 */
export declare const JUPYTER_CELL_MIME: string;
/**
 * The interactivity modes for the notebook.
 */
export declare type NotebookMode = 'command' | 'edit';
/**
 * A widget which renders static non-interactive notebooks.
 *
 * #### Notes
 * The widget model must be set separately and can be changed
 * at any time.  Consumers of the widget must account for a
 * `null` model, and may want to listen to the `modelChanged`
 * signal.
 */
export declare class StaticNotebook extends Widget {
    /**
     * Construct a notebook widget.
     */
    constructor(options: StaticNotebook.IOptions);
    /**
     * A signal emitted when the model of the notebook changes.
     */
    readonly modelChanged: ISignal<this, void>;
    /**
     * A signal emitted when the model content changes.
     *
     * #### Notes
     * This is a convenience signal that follows the current model.
     */
    readonly modelContentChanged: ISignal<this, void>;
    /**
     * The cell factory used by the widget.
     */
    readonly contentFactory: StaticNotebook.IContentFactory;
    /**
     * The Rendermime instance used by the widget.
     */
    readonly rendermime: RenderMime;
    /**
     * The model for the widget.
     */
    model: INotebookModel;
    /**
     * Get the mimetype for code cells.
     */
    readonly codeMimetype: string;
    /**
     * A read-only sequence of the widgets in the notebook.
     */
    readonly widgets: ReadonlyArray<BaseCellWidget>;
    /**
     * Dispose of the resources held by the widget.
     */
    dispose(): void;
    /**
     * Handle a new model.
     *
     * #### Notes
     * This method is called after the model change has been handled
     * internally and before the `modelChanged` signal is emitted.
     * The default implementation is a no-op.
     */
    protected onModelChanged(oldValue: INotebookModel, newValue: INotebookModel): void;
    /**
     * Handle changes to the notebook model content.
     *
     * #### Notes
     * The default implementation emits the `modelContentChanged` signal.
     */
    protected onModelContentChanged(model: INotebookModel, args: void): void;
    /**
     * Handle changes to the notebook model metadata.
     *
     * #### Notes
     * The default implementation updates the mimetypes of the code cells
     * when the `language_info` metadata changes.
     */
    protected onMetadataChanged(sender: IObservableMap<JSONValue>, args: ObservableMap.IChangedArgs<JSONValue>): void;
    /**
     * Handle a cell being inserted.
     *
     * The default implementation is a no-op
     */
    protected onCellInserted(index: number, cell: BaseCellWidget): void;
    /**
     * Handle a cell being moved.
     *
     * The default implementation is a no-op
     */
    protected onCellMoved(fromIndex: number, toIndex: number): void;
    /**
     * Handle a cell being removed.
     *
     * The default implementation is a no-op
     */
    protected onCellRemoved(cell: BaseCellWidget): void;
    /**
     * Handle a new model on the widget.
     */
    private _onModelChanged(oldValue, newValue);
    /**
     * Handle a change cells event.
     */
    private _onCellsChanged(sender, args);
    /**
     * Create a cell widget and insert into the notebook.
     */
    private _insertCell(index, cell);
    /**
     * Create a code cell widget from a code cell model.
     */
    private _createCodeCell(model);
    /**
     * Create a markdown cell widget from a markdown cell model.
     */
    private _createMarkdownCell(model);
    /**
     * Create a raw cell widget from a raw cell model.
     */
    private _createRawCell(model);
    /**
     * Move a cell widget.
     */
    private _moveCell(fromIndex, toIndex);
    /**
     * Remove a cell widget.
     */
    private _removeCell(index);
    /**
     * Update the mimetype of the notebook.
     */
    private _updateMimetype();
    private _mimetype;
    private _model;
    private _mimetypeService;
    private _modelChanged;
    private _modelContentChanged;
}
/**
 * The namespace for the `StaticNotebook` class statics.
 */
export declare namespace StaticNotebook {
    /**
     * An options object for initializing a static notebook.
     */
    interface IOptions {
        /**
         * The rendermime instance used by the widget.
         */
        rendermime: RenderMime;
        /**
         * The language preference for the model.
         */
        languagePreference?: string;
        /**
         * A factory for creating content.
         */
        contentFactory: IContentFactory;
        /**
         * The service used to look up mime types.
         */
        mimeTypeService: IEditorMimeTypeService;
    }
    /**
     * A factory for creating notebook content.
     */
    interface IContentFactory {
        /**
         * The editor factory.
         */
        readonly editorFactory: CodeEditor.Factory;
        /**
         * The factory for code cell widget content.
         */
        readonly codeCellContentFactory?: CodeCellWidget.IContentFactory;
        /**
         * The factory for raw cell widget content.
         */
        readonly rawCellContentFactory?: BaseCellWidget.IContentFactory;
        /**
         * The factory for markdown cell widget content.
         */
        readonly markdownCellContentFactory?: BaseCellWidget.IContentFactory;
        /**
         * Create a new code cell widget.
         */
        createCodeCell(options: CodeCellWidget.IOptions, parent: StaticNotebook): CodeCellWidget;
        /**
         * Create a new markdown cell widget.
         */
        createMarkdownCell(options: MarkdownCellWidget.IOptions, parent: StaticNotebook): MarkdownCellWidget;
        /**
         * Create a new raw cell widget.
         */
        createRawCell(options: RawCellWidget.IOptions, parent: StaticNotebook): RawCellWidget;
    }
    /**
     * The default implementation of an `IContentFactory`.
     */
    class ContentFactory implements IContentFactory {
        /**
         * Creates a new renderer.
         */
        constructor(options: IContentFactoryOptions);
        /**
         * The editor factory.
         */
        readonly editorFactory: CodeEditor.Factory;
        /**
         * The factory for code cell widget content.
         */
        readonly codeCellContentFactory: CodeCellWidget.IContentFactory;
        /**
         * The factory for raw cell widget content.
         */
        readonly rawCellContentFactory: BaseCellWidget.IContentFactory;
        /**
         * The factory for markdown cell widget content.
         */
        readonly markdownCellContentFactory: BaseCellWidget.IContentFactory;
        /**
         * Create a new code cell widget.
         */
        createCodeCell(options: CodeCellWidget.IOptions, parent: StaticNotebook): CodeCellWidget;
        /**
         * Create a new markdown cell widget.
         */
        createMarkdownCell(options: MarkdownCellWidget.IOptions, parent: StaticNotebook): MarkdownCellWidget;
        /**
         * Create a new raw cell widget.
         */
        createRawCell(options: RawCellWidget.IOptions, parent: StaticNotebook): RawCellWidget;
    }
    /**
     * An options object for initializing a notebook content factory.
     */
    interface IContentFactoryOptions {
        /**
         * The editor factory.
         */
        editorFactory: CodeEditor.Factory;
        /**
         * The factory for output area content.
         */
        outputAreaContentFactory?: OutputAreaWidget.IContentFactory;
        /**
         * The factory for code cell widget content.  If given, this will
         * take precedence over the `outputAreaContentFactory`.
         */
        codeCellContentFactory?: CodeCellWidget.IContentFactory;
        /**
         * The factory for raw cell widget content.
         */
        rawCellContentFactory?: BaseCellWidget.IContentFactory;
        /**
         * The factory for markdown cell widget content.
         */
        markdownCellContentFactory?: BaseCellWidget.IContentFactory;
    }
}
/**
 * A notebook widget that supports interactivity.
 */
export declare class Notebook extends StaticNotebook {
    /**
     * Construct a notebook widget.
     */
    constructor(options: StaticNotebook.IOptions);
    /**
     * A signal emitted when the active cell changes.
     *
     * #### Notes
     * This can be due to the active index changing or the
     * cell at the active index changing.
     */
    readonly activeCellChanged: ISignal<this, BaseCellWidget>;
    /**
     * A signal emitted when the state of the notebook changes.
     */
    readonly stateChanged: ISignal<this, IChangedArgs<any>>;
    /**
     * A signal emitted when the selection state of the notebook changes.
     */
    readonly selectionChanged: ISignal<this, void>;
    /**
     * The interactivity mode of the notebook.
     */
    mode: NotebookMode;
    /**
     * The active cell index of the notebook.
     *
     * #### Notes
     * The index will be clamped to the bounds of the notebook cells.
     */
    activeCellIndex: number;
    /**
     * Get the active cell widget.
     */
    readonly activeCell: BaseCellWidget;
    /**
     * Dispose of the resources held by the widget.
     */
    dispose(): void;
    /**
     * Select a cell widget.
     *
     * #### Notes
     * It is a no-op if the value does not change.
     * It will emit the `selectionChanged` signal.
     */
    select(widget: BaseCellWidget): void;
    /**
     * Deselect a cell widget.
     *
     * #### Notes
     * It is a no-op if the value does not change.
     * It will emit the `selectionChanged` signal.
     */
    deselect(widget: BaseCellWidget): void;
    /**
     * Whether a cell is selected or is the active cell.
     */
    isSelected(widget: BaseCellWidget): boolean;
    /**
     * Deselect all of the cells.
     */
    deselectAll(): void;
    /**
     * Scroll so that the given position is visible.
     *
     * @param position - The vertical position in the notebook widget.
     *
     * @param threshold - An optional threshold for the scroll.  Defaults to 25
     *   percent of the widget height.
     */
    scrollToPosition(position: number, threshold?: number): void;
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
    handleEvent(event: Event): void;
    /**
     * Handle `after-attach` messages for the widget.
     */
    protected onAfterAttach(msg: Message): void;
    /**
     * Handle `before-detach` messages for the widget.
     */
    protected onBeforeDetach(msg: Message): void;
    /**
     * Handle `'activate-request'` messages.
     */
    protected onActivateRequest(msg: Message): void;
    /**
     * Handle `update-request` messages sent to the widget.
     */
    protected onUpdateRequest(msg: Message): void;
    /**
     * Handle a cell being inserted.
     */
    protected onCellInserted(index: number, cell: BaseCellWidget): void;
    /**
     * Handle a cell being moved.
     */
    protected onCellMoved(fromIndex: number, toIndex: number): void;
    /**
     * Handle a cell being removed.
     */
    protected onCellRemoved(cell: BaseCellWidget): void;
    /**
     * Handle a new model.
     */
    protected onModelChanged(oldValue: INotebookModel, newValue: INotebookModel): void;
    /**
     * Handle edge request signals from cells.
     */
    private _onEdgeRequest(editor, location);
    /**
     * Ensure that the notebook has proper focus.
     */
    private _ensureFocus(force?);
    /**
     * Find the cell index containing the target html element.
     *
     * #### Notes
     * Returns -1 if the cell is not found.
     */
    private _findCell(node);
    /**
     * Handle `mousedown` events for the widget.
     */
    private _evtMouseDown(event);
    /**
     * Handle the `'mouseup'` event for the widget.
     */
    private _evtMouseup(event);
    /**
     * Handle the `'mousemove'` event for the widget.
     */
    private _evtMousemove(event);
    /**
     * Handle the `'p-dragenter'` event for the widget.
     */
    private _evtDragEnter(event);
    /**
     * Handle the `'p-dragleave'` event for the widget.
     */
    private _evtDragLeave(event);
    /**
     * Handle the `'p-dragover'` event for the widget.
     */
    private _evtDragOver(event);
    /**
     * Handle the `'p-drop'` event for the widget.
     */
    private _evtDrop(event);
    /**
     * Start a drag event.
     */
    private _startDrag(index, clientX, clientY);
    /**
     * Handle `focus` events for the widget.
     */
    private _evtFocus(event);
    /**
     * Handle `blur` events for the notebook.
     */
    private _evtBlur(event);
    /**
     * Handle `dblclick` events for the widget.
     */
    private _evtDblClick(event);
    /**
     * Extend the selection to a given index.
     */
    private _extendSelectionTo(index);
    private _activeCellIndex;
    private _activeCell;
    private _mode;
    private _drag;
    private _dragData;
    private _activeCellChanged;
    private _stateChanged;
    private _selectionChanged;
}
/**
 * The namespace for the `Notebook` class statics.
 */
export declare namespace Notebook {
    /**
     * An options object for initializing a notebook.
     */
    interface IOptions extends StaticNotebook.IOptions {
    }
    /**
     * The cell factory for the notebook
     */
    interface IContentFactory extends StaticNotebook.IContentFactory {
    }
    /**
     * The default implementation of an `IFactory`.
     */
    class ContentFactory extends StaticNotebook.ContentFactory {
    }
}

import { Message } from '@phosphor/messaging';
import { ISignal } from '@phosphor/signaling';
import { Widget } from '@phosphor/widgets';
import { IClientSession } from '@jupyterlab/apputils';
import { IEditorMimeTypeService, CodeEditor } from '@jupyterlab/codeeditor';
import { BaseCellWidget, CodeCellWidget, RawCellWidget, ICodeCellModel, IRawCellModel, CellModel, CodeCellModel } from '@jupyterlab/cells';
import { nbformat, IObservableVector } from '@jupyterlab/coreutils';
import { OutputAreaWidget } from '@jupyterlab/outputarea';
import { IRenderMime } from '@jupyterlab/rendermime';
import { ForeignHandler } from './foreign';
import { ConsoleHistory, IConsoleHistory } from './history';
/**
 * A widget containing a Jupyter console.
 *
 * #### Notes
 * The CodeConsole class is intended to be used within a ConsolePanel
 * instance. Under most circumstances, it is not instantiated by user code.
 */
export declare class CodeConsole extends Widget {
    /**
     * Construct a console widget.
     */
    constructor(options: CodeConsole.IOptions);
    /**
     * A signal emitted when the console finished executing its prompt.
     */
    readonly executed: ISignal<this, Date>;
    /**
     * A signal emitted when a new prompt is created.
     */
    readonly promptCreated: ISignal<this, CodeCellWidget>;
    /**
     * The content factory used by the console.
     */
    readonly contentFactory: CodeConsole.IContentFactory;
    /**
     * The model factory for the console widget.
     */
    readonly modelFactory: CodeConsole.IModelFactory;
    /**
     * The rendermime instance used by the console.
     */
    readonly rendermime: IRenderMime;
    /**
     * The client session used by the console.
     */
    readonly session: IClientSession;
    /**
     * The console banner widget.
     */
    readonly banner: RawCellWidget;
    /**
     * The list of content cells in the console.
     *
     * #### Notes
     * This list does not include the banner or the prompt for a console.
     */
    readonly cells: IObservableVector<BaseCellWidget>;
    readonly prompt: CodeCellWidget | null;
    /**
     * Add a new cell to the content panel.
     *
     * @param cell - The cell widget being added to the content panel.
     *
     * #### Notes
     * This method is meant for use by outside classes that want to inject content
     * into a console. It is distinct from the `inject` method in that it requires
     * rendered code cell widgets and does not execute them.
     */
    addCell(cell: BaseCellWidget): void;
    /**
     * Clear the code cells.
     */
    clear(): void;
    /**
     * Dispose of the resources held by the widget.
     */
    dispose(): void;
    /**
     * Execute the current prompt.
     *
     * @param force - Whether to force execution without checking code
     * completeness.
     *
     * @param timeout - The length of time, in milliseconds, that the execution
     * should wait for the API to determine whether code being submitted is
     * incomplete before attempting submission anyway. The default value is `250`.
     */
    execute(force?: boolean, timeout?: number): Promise<void>;
    /**
     * Inject arbitrary code for the console to execute immediately.
     *
     * @param code - The code contents of the cell being injected.
     *
     * @returns A promise that indicates when the injected cell's execution ends.
     */
    inject(code: string): Promise<void>;
    /**
     * Insert a line break in the prompt.
     */
    insertLinebreak(): void;
    /**
     * Serialize the output.
     */
    serialize(): nbformat.ICodeCell[];
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
     * Handle `after_attach` messages for the widget.
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
     * Make a new prompt.
     */
    protected newPrompt(): void;
    /**
     * Handle `update-request` messages.
     */
    protected onUpdateRequest(msg: Message): void;
    /**
     * Handle the `'keydown'` event for the widget.
     */
    private _evtKeyDown(event);
    /**
     * Execute the code in the current prompt.
     */
    private _execute(cell);
    /**
     * Update the console based on the kernel info.
     */
    private _handleInfo(info);
    /**
     * Create a new foreign cell.
     */
    private _createForeignCell();
    /**
     * Create the options used to initialize a code cell widget.
     */
    private _createCodeCellOptions();
    /**
     * Handle cell disposed signals.
     */
    private _onCellDisposed(sender, args);
    /**
     * Test whether we should execute the prompt.
     */
    private _shouldExecute(timeout);
    /**
     * Handle a keydown event on an editor.
     */
    private _onEditorKeydown(editor, event);
    /**
     * Handle a change to the kernel.
     */
    private _onKernelChanged();
    private _mimeTypeService;
    private _cells;
    private _content;
    private _foreignHandler;
    private _history;
    private _input;
    private _mimetype;
    private _executed;
    private _promptCreated;
}
/**
 * A namespace for CodeConsole statics.
 */
export declare namespace CodeConsole {
    /**
     * The initialization options for a console widget.
     */
    interface IOptions {
        /**
         * The content factory for the console widget.
         */
        contentFactory: IContentFactory;
        /**
         * The model factory for the console widget.
         */
        modelFactory?: IModelFactory;
        /**
         * The mime renderer for the console widget.
         */
        rendermime: IRenderMime;
        /**
         * The client session for the console widget.
         */
        session: IClientSession;
        /**
         * The service used to look up mime types.
         */
        mimeTypeService: IEditorMimeTypeService;
    }
    /**
     * A content factory for console children.
     */
    interface IContentFactory {
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
         * The history manager for a console widget.
         */
        createConsoleHistory(options: ConsoleHistory.IOptions): IConsoleHistory;
        /**
         * The foreign handler for a console widget.
         */
        createForeignHandler(options: ForeignHandler.IOptions): ForeignHandler;
        /**
         * Create a new banner widget.
         */
        createBanner(options: RawCellWidget.IOptions, parent: CodeConsole): RawCellWidget;
        /**
         * Create a new prompt widget.
         */
        createPrompt(options: CodeCellWidget.IOptions, parent: CodeConsole): CodeCellWidget;
        /**
         * Create a code cell whose input originated from a foreign session.
         */
        createForeignCell(options: CodeCellWidget.IOptions, parent: CodeConsole): CodeCellWidget;
    }
    /**
     * Default implementation of `IContentFactory`.
     */
    class ContentFactory implements IContentFactory {
        /**
         * Create a new content factory.
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
         * The history manager for a console widget.
         */
        createConsoleHistory(options: ConsoleHistory.IOptions): IConsoleHistory;
        /**
         * The foreign handler for a console widget.
         */
        createForeignHandler(options: ForeignHandler.IOptions): ForeignHandler;
        /**
         * Create a new banner widget.
         */
        createBanner(options: RawCellWidget.IOptions, parent: CodeConsole): RawCellWidget;
        /**
         * Create a new prompt widget.
         */
        createPrompt(options: CodeCellWidget.IOptions, parent: CodeConsole): CodeCellWidget;
        /**
         * Create a new code cell widget for an input from a foreign session.
         */
        createForeignCell(options: CodeCellWidget.IOptions, parent: CodeConsole): CodeCellWidget;
    }
    /**
     * An initialize options for `ContentFactory`.
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
    }
    /**
     * A model factory for a console widget.
     */
    interface IModelFactory {
        /**
         * The factory for code cell content.
         */
        readonly codeCellContentFactory: CodeCellModel.IContentFactory;
        /**
         * Create a new code cell.
         *
         * @param options - The options used to create the cell.
         *
         * @returns A new code cell. If a source cell is provided, the
         *   new cell will be intialized with the data from the source.
         */
        createCodeCell(options: CodeCellModel.IOptions): ICodeCellModel;
        /**
         * Create a new raw cell.
         *
         * @param options - The options used to create the cell.
         *
         * @returns A new raw cell. If a source cell is provided, the
         *   new cell will be intialized with the data from the source.
         */
        createRawCell(options: CellModel.IOptions): IRawCellModel;
    }
    /**
     * The default implementation of an `IModelFactory`.
     */
    class ModelFactory {
        /**
         * Create a new cell model factory.
         */
        constructor(options: IModelFactoryOptions);
        /**
         * The factory for output area models.
         */
        readonly codeCellContentFactory: CodeCellModel.IContentFactory;
        /**
         * Create a new code cell.
         *
         * @param source - The data to use for the original source data.
         *
         * @returns A new code cell. If a source cell is provided, the
         *   new cell will be intialized with the data from the source.
         *   If the contentFactory is not provided, the instance
         *   `codeCellContentFactory` will be used.
         */
        createCodeCell(options: CodeCellModel.IOptions): ICodeCellModel;
        /**
         * Create a new raw cell.
         *
         * @param source - The data to use for the original source data.
         *
         * @returns A new raw cell. If a source cell is provided, the
         *   new cell will be intialized with the data from the source.
         */
        createRawCell(options: CellModel.IOptions): IRawCellModel;
    }
    /**
     * The options used to initialize a `ModelFactory`.
     */
    interface IModelFactoryOptions {
        /**
         * The factory for output area models.
         */
        codeCellContentFactory?: CodeCellModel.IContentFactory;
    }
    /**
     * The default `ModelFactory` instance.
     */
    const defaultModelFactory: ModelFactory;
}

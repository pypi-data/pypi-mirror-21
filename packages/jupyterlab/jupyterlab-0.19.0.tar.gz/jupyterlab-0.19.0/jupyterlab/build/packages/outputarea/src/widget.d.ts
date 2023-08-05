import { Kernel, KernelMessage } from '@jupyterlab/services';
import { IDisposable } from '@phosphor/disposable';
import { ISignal } from '@phosphor/signaling';
import { Message } from '@phosphor/messaging';
import { Widget } from '@phosphor/widgets';
import { IClientSession } from '@jupyterlab/apputils';
import { ObservableVector, nbformat } from '@jupyterlab/coreutils';
import { IOutputModel, RenderMime } from '@jupyterlab/rendermime';
/**
 * An output area widget.
 *
 * #### Notes
 * The widget model must be set separately and can be changed
 * at any time.  Consumers of the widget must account for a
 * `null` model, and may want to listen to the `modelChanged`
 * signal.
 */
export declare class OutputAreaWidget extends Widget {
    /**
     * Construct an output area widget.
     */
    constructor(options: OutputAreaWidget.IOptions);
    /**
     * Create a mirrored output area widget.
     */
    mirror(): OutputAreaWidget;
    /**
     * The model used by the widget.
     */
    readonly model: IOutputAreaModel;
    /**
     * Te rendermime instance used by the widget.
     */
    readonly rendermime: RenderMime;
    /**
     * The content factory used by the widget.
     */
    readonly contentFactory: OutputAreaWidget.IContentFactory;
    /**
     * A read-only sequence of the widgets in the output area.
     */
    readonly widgets: ReadonlyArray<Widget>;
    /**
     * The collapsed state of the widget.
     */
    collapsed: boolean;
    /**
     * The fixed height state of the widget.
     */
    fixedHeight: boolean;
    /**
     * Execute code on a client session and handle response messages.
     */
    execute(code: string, session: IClientSession): Promise<KernelMessage.IExecuteReplyMsg>;
    /**
     * Handle `update-request` messages.
     */
    protected onUpdateRequest(msg: Message): void;
    /**
     * Follow changes on the model state.
     */
    protected onModelChanged(sender: IOutputAreaModel, args: IOutputAreaModel.ChangedArgs): void;
    /**
     * Clear the widget inputs and outputs.
     */
    private _clear();
    /**
     * Handle an iopub message.
     */
    private _onIOPub(msg);
    /**
     * Handle an execute reply message.
     */
    private _onExecuteReply(msg);
    /**
     * Handle an input request from a kernel.
     */
    private _onInputRequest(msg, session);
    /**
     * Insert an output to the layout.
     */
    private _insertOutput(index, model);
    /**
     * Update an output in place.
     */
    private _setOutput(index, model);
    /**
     * Create an output.
     */
    private _createOutput(model);
    private _fixedHeight;
    private _collapsed;
    private _minHeightTimeout;
}
/**
 * A namespace for OutputAreaWidget statics.
 */
export declare namespace OutputAreaWidget {
    /**
     * The options to pass to an `OutputAreaWidget`.
     */
    interface IOptions {
        /**
         * The rendermime instance used by the widget.
         */
        rendermime: RenderMime;
        /**
         * The model used by the widget.
         */
        model: IOutputAreaModel;
        /**
         * The output widget content factory.
         *
         * Defaults to a shared `IContentFactory` instance.
         */
        contentFactory?: IContentFactory;
    }
    /**
     * The interface for a gutter widget.
     */
    interface IGutterWidget extends Widget {
        /**
         * The execution count for the widget.
         */
        executionCount: nbformat.ExecutionCount;
    }
    /**
     * The options to create a stdin widget.
     */
    interface IStdinOptions {
        /**
         * The prompt text.
         */
        prompt: string;
        /**
         * Whether the input is a password.
         */
        password: boolean;
        /**
         * The kernel associated with the request.
         */
        kernel: Kernel.IKernelConnection;
    }
    /**
     * An output widget content factory.
     */
    interface IContentFactory {
        /**
         * Create a gutter for an output or input.
         *
         */
        createGutter(): IGutterWidget;
        /**
         * Create an stdin widget.
         */
        createStdin(options: IStdinOptions): Widget;
    }
    /**
     * The default implementation of `IContentFactory`.
     */
    class ContentFactory implements IContentFactory {
        /**
         * Create the gutter for the widget.
         */
        createGutter(): IGutterWidget;
        /**
         * Create an stdin widget.
         */
        createStdin(options: IStdinOptions): Widget;
    }
    /**
     * The default `ContentFactory` instance.
     */
    const defaultContentFactory: ContentFactory;
    /**
     * The default stdin widget.
     */
    class StdinWidget extends Widget {
        /**
         * Construct a new input widget.
         */
        constructor(options: IStdinOptions);
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
        handleEvent(event: Event): void;
        /**
         * Handle `after-attach` messages sent to the widget.
         */
        protected onAfterAttach(msg: Message): void;
        /**
         * Handle `update-request` messages sent to the widget.
         */
        protected onUpdateRequest(msg: Message): void;
        /**
         * Handle `before-detach` messages sent to the widget.
         */
        protected onBeforeDetach(msg: Message): void;
        private _kernel;
        private _input;
    }
    /**
     * The default output gutter.
     */
    class GutterWidget extends Widget {
        /**
         * The execution count for the widget.
         */
        executionCount: nbformat.ExecutionCount;
        /**
         * Handle the DOM events for the output gutter widget.
         *
         * @param event - The DOM event sent to the widget.
         *
         * #### Notes
         * This method implements the DOM `EventListener` interface and is
         * called in response to events on the panel's DOM node. It should
         * not be called directly by user code.
         */
        handleEvent(event: Event): void;
        /**
         * A message handler invoked on an `'after-attach'` message.
         */
        protected onAfterAttach(msg: Message): void;
        /**
         * A message handler invoked on a `'before-detach'` message.
         */
        protected onBeforeDetach(msg: Message): void;
        /**
         * Handle the `'mousedown'` event for the widget.
         */
        private _evtMousedown(event);
        /**
         * Handle the `'mouseup'` event for the widget.
         */
        private _evtMouseup(event);
        /**
         * Handle the `'mousemove'` event for the widget.
         */
        private _evtMousemove(event);
        /**
         * Start a drag event.
         */
        private _startDrag(clientX, clientY);
        /**
         * Dispose of the resources held by the widget.
         */
        dispose(): void;
        private _drag;
        private _dragData;
        private _executionCount;
    }
}
/**
 * The model for an output area.
 */
export interface IOutputAreaModel extends IDisposable {
    /**
     * A signal emitted when the model state changes.
     */
    readonly stateChanged: ISignal<IOutputAreaModel, void>;
    /**
     * A signal emitted when the model changes.
     */
    readonly changed: ISignal<IOutputAreaModel, IOutputAreaModel.ChangedArgs>;
    /**
     * The length of the items in the model.
     */
    readonly length: number;
    /**
     * Whether the output area is trusted.
     */
    trusted: boolean;
    /**
     * The output content factory used by the model.
     */
    readonly contentFactory: IOutputAreaModel.IContentFactory;
    /**
     * Get an item at the specified index.
     */
    get(index: number): IOutputModel;
    /**
     * Add an output, which may be combined with previous output.
     *
     * #### Notes
     * The output bundle is copied.
     * Contiguous stream outputs of the same `name` are combined.
     */
    add(output: nbformat.IOutput): number;
    /**
     * Clear all of the output.
     *
     * @param wait - Delay clearing the output until the next message is added.
     */
    clear(wait?: boolean): void;
    /**
     * Deserialize the model from JSON.
     *
     * #### Notes
     * This will clear any existing data.
     */
    fromJSON(values: nbformat.IOutput[]): void;
    /**
     * Serialize the model to JSON.
     */
    toJSON(): nbformat.IOutput[];
}
/**
 * The namespace for IOutputAreaModel interfaces.
 */
export declare namespace IOutputAreaModel {
    /**
     * The options used to create a output area model.
     */
    interface IOptions {
        /**
         * The initial values for the model.
         */
        values?: nbformat.IOutput[];
        /**
         * Whether the output is trusted.  The default is false.
         */
        trusted?: boolean;
        /**
         * The output content factory used by the model.
         *
         * If not given, a default factory will be used.
         */
        contentFactory?: IContentFactory;
    }
    /**
     * A type alias for changed args.
     */
    type ChangedArgs = ObservableVector.IChangedArgs<IOutputModel>;
    /**
     * The interface for an output content factory.
     */
    interface IContentFactory {
        /**
         * Create an output model.
         */
        createOutputModel(options: IOutputModel.IOptions): IOutputModel;
    }
}

import { KernelMessage } from '@jupyterlab/services';
import { IDisposable } from '@phosphor/disposable';
import { Message } from '@phosphor/messaging';
import { IClientSession } from '@jupyterlab/apputils';
import { CodeEditor } from '@jupyterlab/codeeditor';
import { CompleterWidget } from './widget';
/**
 * A completion handler for editors.
 */
export declare class CompletionHandler implements IDisposable {
    /**
     * Construct a new completion handler for a widget.
     */
    constructor(options: CompletionHandler.IOptions);
    /**
     * The completer widget managed by the handler.
     */
    readonly completer: CompleterWidget;
    /**
     * The editor used by the completion handler.
     */
    editor: CodeEditor.IEditor;
    /**
     * The session used by the completion handler.
     */
    readonly session: IClientSession;
    /**
     * Get whether the completion handler is disposed.
     */
    readonly isDisposed: boolean;
    /**
     * Dispose of the resources used by the handler.
     */
    dispose(): void;
    /**
     * Invoke the handler and launch a completer.
     */
    invoke(): void;
    /**
     * Process a message sent to the completion handler.
     */
    processMessage(msg: Message): void;
    /**
     * Get the state of the text editor at the given position.
     */
    protected getState(position: CodeEditor.IPosition): CompleterWidget.ITextState;
    /**
     * Make a complete request using the session.
     */
    protected makeRequest(position: CodeEditor.IPosition): Promise<void>;
    /**
     * Handle a completion selected signal from the completion widget.
     */
    protected onCompletionSelected(completer: CompleterWidget, value: string): void;
    /**
     * Handle `invoke-request` messages.
     */
    protected onInvokeRequest(msg: Message): void;
    /**
     * Receive a completion reply from the kernel.
     *
     * @param state - The state of the editor when completion request was made.
     *
     * @param reply - The API response returned for a completion request.
     */
    protected onReply(state: CompleterWidget.ITextState, reply: KernelMessage.ICompleteReplyMsg): void;
    /**
     * Handle selection changed signal from an editor.
     *
     * #### Notes
     * If a sub-class reimplements this method, then that class must either call
     * its super method or it must take responsibility for adding and removing
     * the completer completable class to the editor host node.
     *
     * Despite the fact that the editor widget adds a class whenever there is a
     * primary selection, this method checks indepenently for two reasons:
     *
     * 1. The editor widget connects to the same signal to add that class, so
     *    there is no guarantee that the class will be added before this method
     *    is invoked so simply checking for the CSS class's existence is not an
     *    option. Secondarily, checking the editor state should be faster than
     *    querying the DOM in either case.
     * 2. Because this method adds a class that indicates whether completer
     *    functionality ought to be enabled, relying on the behavior of the
     *    `jp-mod-has-primary-selection` to filter out any editors that have
     *    a selection means the semantic meaning of `jp-mod-completer-enabled`
     *    is obscured because there may be cases where the enabled class is added
     *    even though the completer is not available.
     */
    protected onSelectionsChanged(): void;
    /**
     * Handle a text changed signal from an editor.
     */
    protected onTextChanged(): void;
    /**
     * Handle a visiblity change signal from a completer widget.
     */
    protected onVisibilityChanged(completer: CompleterWidget): void;
    private _editor;
    private _enabled;
    private _completer;
    private _pending;
}
/**
 * A namespace for cell completion handler statics.
 */
export declare namespace CompletionHandler {
    /**
     * The instantiation options for cell completion handlers.
     */
    interface IOptions {
        /**
         * The completion widget the handler will connect to.
         */
        completer: CompleterWidget;
        /**
         * The session for the completion handler.
         */
        session: IClientSession;
    }
    /**
     * A namespace for completion handler messages.
     */
    namespace Msg {
        /**
         * A singleton `'invoke-request'` message.
         */
        const InvokeRequest: Message;
    }
}

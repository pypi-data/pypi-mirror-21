import { IDisposable } from '@phosphor/disposable';
import { IMessageHandler, Message } from '@phosphor/messaging';
import { ISignal } from '@phosphor/signaling';
import { Widget } from '@phosphor/widgets';
import { DocumentRegistry } from '@jupyterlab/docregistry';
/**
 * A class that maintains the lifecyle of file-backed widgets.
 */
export declare class DocumentWidgetManager implements IDisposable {
    /**
     * Construct a new document widget manager.
     */
    constructor(options: DocumentWidgetManager.IOptions);
    /**
     * A signal emitted when one of the documents is activated.
     */
    readonly activateRequested: ISignal<this, string>;
    /**
     * Test whether the document widget manager is disposed.
     */
    readonly isDisposed: boolean;
    /**
     * Dispose of the resources used by the widget manager.
     */
    dispose(): void;
    /**
     * Create a widget for a document and handle its lifecycle.
     *
     * @param name - The name of the widget factory.
     *
     * @param context - The document context object.
     *
     * @returns A widget created by the factory.
     *
     * @throws If the factory is not registered.
     */
    createWidget(name: string, context: DocumentRegistry.Context): Widget;
    /**
     * Install the message hook for the widget and add to list
     * of known widgets.
     *
     * @param context - The document context object.
     *
     * @param widget - The widget to adopt.
     */
    adoptWidget(context: DocumentRegistry.Context, widget: Widget): void;
    /**
     * See if a widget already exists for the given context and widget name.
     *
     * @param context - The document context object.
     *
     * @returns The found widget, or `undefined`.
     *
     * #### Notes
     * This can be used to use an existing widget instead of opening
     * a new widget.
     */
    findWidget(context: DocumentRegistry.Context, widgetName: string): Widget;
    /**
     * Get the document context for a widget.
     *
     * @param widget - The widget of interest.
     *
     * @returns The context associated with the widget, or `undefined`.
     */
    contextForWidget(widget: Widget): DocumentRegistry.Context;
    /**
     * Clone a widget.
     *
     * @param widget - The source widget.
     *
     * @returns A new widget or `undefined`.
     *
     * #### Notes
     *  Uses the same widget factory and context as the source, or returns
     *  `undefined` if the source widget is not managed by this manager.
     */
    cloneWidget(widget: Widget): Widget;
    /**
     * Close the widgets associated with a given context.
     *
     * @param context - The document context object.
     */
    closeWidgets(context: DocumentRegistry.Context): Promise<void>;
    /**
     * Filter a message sent to a message handler.
     *
     * @param handler - The target handler of the message.
     *
     * @param msg - The message dispatched to the handler.
     *
     * @returns `false` if the message should be filtered, of `true`
     *   if the message should be dispatched to the handler as normal.
     */
    protected filterMessage(handler: IMessageHandler, msg: Message): boolean;
    /**
     * Set the caption for widget title.
     *
     * @param widget - The target widget.
     */
    protected setCaption(widget: Widget): void;
    /**
     * Handle `'close-request'` messages.
     *
     * @param widget - The target widget.
     *
     * @returns A promise that resolves with whether the widget was closed.
     */
    protected onClose(widget: Widget): Promise<boolean>;
    /**
     * Ask the user whether to close an unsaved file.
     */
    private _maybeClose(widget);
    /**
     * Handle the disposal of a widget.
     */
    private _widgetDisposed(widget);
    /**
     * Handle the disposal of a widget.
     */
    private _onWidgetDisposed(widget);
    /**
     * Handle a file changed signal for a context.
     */
    private _onFileChanged(context);
    /**
     * Handle a path changed signal for a context.
     */
    private _onPathChanged(context);
    private _closeGuard;
    private _registry;
    private _activateRequested;
}
/**
 * A namespace for document widget manager statics.
 */
export declare namespace DocumentWidgetManager {
    /**
     * The options used to initialize a document widget manager.
     */
    interface IOptions {
        /**
         * A document registry instance.
         */
        registry: DocumentRegistry;
    }
}

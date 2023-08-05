import { ServiceManager, Session, TerminalSession } from '@jupyterlab/services';
import { Message } from '@phosphor/messaging';
import { ISignal } from '@phosphor/signaling';
import { Widget } from '@phosphor/widgets';
/**
 * A regex for console names.
 */
export declare const CONSOLE_REGEX: RegExp;
/**
 * A class that exposes the running terminal and kernel sessions.
 */
export declare class RunningSessions extends Widget {
    /**
     * Construct a new running widget.
     */
    constructor(options: RunningSessions.IOptions);
    /**
     * A signal emitted when a kernel session open is requested.
     */
    readonly sessionOpenRequested: ISignal<this, Session.IModel>;
    /**
     * A signal emitted when a terminal session open is requested.
     */
    readonly terminalOpenRequested: ISignal<this, TerminalSession.IModel>;
    /**
     * The renderer used by the running sessions widget.
     */
    readonly renderer: RunningSessions.IRenderer;
    /**
     * Dispose of the resources used by the widget.
     */
    dispose(): void;
    /**
     * Refresh the widget.
     */
    refresh(): Promise<void>;
    /**
     * Handle the DOM events for the widget.
     *
     * @param event - The DOM event sent to the widget.
     *
     * #### Notes
     * This method implements the DOM `EventListener` interface and is
     * called in response to events on the widget's DOM nodes. It should
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
     * A message handler invoked on an `'update-request'` message.
     */
    protected onUpdateRequest(msg: Message): void;
    /**
     * Handle the `'click'` event for the widget.
     *
     * #### Notes
     * This listener is attached to the document node.
     */
    private _evtClick(event);
    /**
     * Handle a change to the running sessions.
     */
    private _onSessionsChanged(sender, models);
    /**
     * Handle a change to the running terminals.
     */
    private _onTerminalsChanged(sender, models);
    private _manager;
    private _renderer;
    private _runningSessions;
    private _runningTerminals;
    private _refreshId;
    private _sessionOpenRequested;
    private _terminalOpenRequested;
}
/**
 * The namespace for the `RunningSessions` class statics.
 */
export declare namespace RunningSessions {
    /**
     * An options object for creating a running sessions widget.
     */
    interface IOptions {
        /**
         * A service manager instance.
         */
        manager: ServiceManager.IManager;
        /**
         * The renderer for the running sessions widget.
         *
         * The default is a shared renderer instance.
         */
        renderer?: IRenderer;
    }
    /**
     * A renderer for use with a running sessions widget.
     */
    interface IRenderer {
        /**
         * Create the root node for the running sessions widget.
         */
        createNode(): HTMLElement;
        /**
         * Create a fully populated header node for the terminals section.
         *
         * @returns A new node for a running terminal session header.
         */
        createTerminalHeaderNode(): HTMLElement;
        /**
         * Create a fully populated header node for the sessions section.
         *
         * @returns A new node for a running kernel session header.
         */
        createSessionHeaderNode(): HTMLElement;
        /**
         * Create a node for a running terminal session item.
         *
         * @returns A new node for a running terminal session item.
         *
         * #### Notes
         * The data in the node should be uninitialized.
         *
         * The `updateTerminalNode` method will be called for initialization.
         */
        createTerminalNode(): HTMLLIElement;
        /**
         * Create a node for a running kernel session item.
         *
         * @returns A new node for a running kernel session item.
         *
         * #### Notes
         * The data in the node should be uninitialized.
         *
         * The `updateSessionNode` method will be called for initialization.
         */
        createSessionNode(): HTMLLIElement;
        /**
         * Get the shutdown node for a terminal node.
         *
         * @param node - A node created by a call to `createTerminalNode`.
         *
         * @returns The node representing the shutdown option.
         *
         * #### Notes
         * A click on this node is considered a shutdown request.
         * A click anywhere else on the node is considered an open request.
         */
        getTerminalShutdown(node: HTMLLIElement): HTMLElement;
        /**
         * Get the shutdown node for a session node.
         *
         * @param node - A node created by a call to `createSessionNode`.
         *
         * @returns The node representing the shutdown option.
         *
         * #### Notes
         * A click on this node is considered a shutdown request.
         * A click anywhere else on the node is considered an open request.
         */
        getSessionShutdown(node: HTMLLIElement): HTMLElement;
        /**
         * Populate a node with running terminal session data.
         *
         * @param node - A node created by a call to `createTerminalNode`.
         *
         * @param models - The list of terminal session models.
         *
         * #### Notes
         * This method should completely reset the state of the node to
         * reflect the data for the session models.
         */
        updateTerminalNode(node: HTMLLIElement, model: TerminalSession.IModel): void;
        /**
         * Populate a node with running kernel session data.
         *
         * @param node - A node created by a call to `createSessionNode`.
         *
         * @param models - The list of kernel session models.
         *
         * @param kernelName - The kernel display name.
         *
         * #### Notes
         * This method should completely reset the state of the node to
         * reflect the data for the session models.
         */
        updateSessionNode(node: HTMLLIElement, model: Session.IModel, kernelName: string): void;
    }
    /**
     * The default implementation of `IRenderer`.
     */
    class Renderer implements IRenderer {
        /**
         * Create the root node for the running sessions widget.
         */
        createNode(): HTMLElement;
        /**
         * Create a fully populated header node for the terminals section.
         *
         * @returns A new node for a running terminal session header.
         */
        createTerminalHeaderNode(): HTMLElement;
        /**
         * Create a fully populated header node for the sessions section.
         *
         * @returns A new node for a running kernel session header.
         */
        createSessionHeaderNode(): HTMLElement;
        /**
         * Create a node for a running terminal session item.
         *
         * @returns A new node for a running terminal session item.
         *
         * #### Notes
         * The data in the node should be uninitialized.
         *
         * The `updateTerminalNode` method will be called for initialization.
         */
        createTerminalNode(): HTMLLIElement;
        /**
         * Create a node for a running kernel session item.
         *
         * @returns A new node for a running kernel session item.
         *
         * #### Notes
         * The data in the node should be uninitialized.
         *
         * The `updateSessionNode` method will be called for initialization.
         */
        createSessionNode(): HTMLLIElement;
        /**
         * Get the shutdown node for a terminal node.
         *
         * @param node - A node created by a call to `createTerminalNode`.
         *
         * @returns The node representing the shutdown option.
         *
         * #### Notes
         * A click on this node is considered a shutdown request.
         * A click anywhere else on the node is considered an open request.
         */
        getTerminalShutdown(node: HTMLLIElement): HTMLElement;
        /**
         * Get the shutdown node for a session node.
         *
         * @param node - A node created by a call to `createSessionNode`.
         *
         * @returns The node representing the shutdown option.
         *
         * #### Notes
         * A click on this node is considered a shutdown request.
         * A click anywhere else on the node is considered an open request.
         */
        getSessionShutdown(node: HTMLLIElement): HTMLElement;
        /**
         * Populate a node with running terminal session data.
         *
         * @param node - A node created by a call to `createTerminalNode`.
         *
         * @param models - The list of terminal session models.
         *
         * #### Notes
         * This method should completely reset the state of the node to
         * reflect the data for the session models.
         */
        updateTerminalNode(node: HTMLLIElement, model: TerminalSession.IModel): void;
        /**
         * Populate a node with running kernel session data.
         *
         * @param node - A node created by a call to `createSessionNode`.
         *
         * @param models - The list of kernel session models.
         *
         * @param kernelName - The kernel display name.
         *
         * #### Notes
         * This method should completely reset the state of the node to
         * reflect the data for the session models.
         */
        updateSessionNode(node: HTMLLIElement, model: Session.IModel, kernelName: string): void;
    }
    /**
     * The default `Renderer` instance.
     */
    const defaultRenderer: Renderer;
}

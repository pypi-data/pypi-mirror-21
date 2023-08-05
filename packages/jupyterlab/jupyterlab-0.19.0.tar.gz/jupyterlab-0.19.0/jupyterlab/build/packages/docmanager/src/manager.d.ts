import { Kernel, ServiceManager } from '@jupyterlab/services';
import { Token } from '@phosphor/coreutils';
import { IDisposable } from '@phosphor/disposable';
import { ISignal } from '@phosphor/signaling';
import { Widget } from '@phosphor/widgets';
import { DocumentRegistry } from '@jupyterlab/docregistry';
/**
 * The document registry token.
 */
export declare const IDocumentManager: Token<IDocumentManager>;
/**
 * The interface for a document manager.
 */
export interface IDocumentManager extends DocumentManager {
}
/**
 * The document manager.
 *
 * #### Notes
 * The document manager is used to register model and widget creators,
 * and the file browser uses the document manager to create widgets. The
 * document manager maintains a context for each path and model type that is
 * open, and a list of widgets for each context. The document manager is in
 * control of the proper closing and disposal of the widgets and contexts.
 */
export declare class DocumentManager implements IDisposable {
    /**
     * Construct a new document manager.
     */
    constructor(options: DocumentManager.IOptions);
    /**
     * A signal emitted when one of the documents is activated.
     */
    readonly activateRequested: ISignal<this, string>;
    /**
     * Get the registry used by the manager.
     */
    readonly registry: DocumentRegistry;
    /**
     * Get the service manager used by the manager.
     */
    readonly services: ServiceManager.IManager;
    /**
     * Get whether the document manager has been disposed.
     */
    readonly isDisposed: boolean;
    /**
     * Dispose of the resources held by the document manager.
     */
    dispose(): void;
    /**
     * Open a file and return the widget used to view it.
     * Reveals an already existing editor.
     *
     * @param path - The file path to open.
     *
     * @param widgetName - The name of the widget factory to use. 'default' will use the default widget.
     *
     * @param kernel - An optional kernel name/id to override the default.
     *
     * @returns The created widget, or `undefined`.
     *
     * #### Notes
     * This function will return `undefined` if a valid widget factory
     * cannot be found.
     */
    openOrReveal(path: string, widgetName?: string, kernel?: Kernel.IModel): Widget;
    /**
     * Open a file and return the widget used to view it.
     *
     * @param path - The file path to open.
     *
     * @param widgetName - The name of the widget factory to use. 'default' will use the default widget.
     *
     * @param kernel - An optional kernel name/id to override the default.
     *
     * @returns The created widget, or `undefined`.
     *
     * #### Notes
     * This function will return `undefined` if a valid widget factory
     * cannot be found.
     */
    open(path: string, widgetName?: string, kernel?: Kernel.IModel): Widget;
    /**
     * Create a new file and return the widget used to view it.
     *
     * @param path - The file path to create.
     *
     * @param widgetName - The name of the widget factory to use. 'default' will use the default widget.
     *
     * @param kernel - An optional kernel name/id to override the default.
     *
     * @returns The created widget, or `undefined`.
     *
     * #### Notes
     * This function will return `undefined` if a valid widget factory
     * cannot be found.
     */
    createNew(path: string, widgetName?: string, kernel?: Kernel.IModel): Widget;
    /**
     * See if a widget already exists for the given path and widget name.
     *
     * @param path - The file path to use.
     *
     * @param widgetName - The name of the widget factory to use. 'default' will use the default widget.
     *
     * @returns The found widget, or `undefined`.
     *
     * #### Notes
     * This can be used to use an existing widget instead of opening
     * a new widget.
     */
    findWidget(path: string, widgetName?: string): Widget;
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
     * Close the widgets associated with a given path.
     *
     * @param path - The target path.
     */
    closeFile(path: string): Promise<void>;
    /**
     * Close all of the open documents.
     */
    closeAll(): Promise<void>;
    /**
     * Find a context for a given path and factory name.
     */
    private _findContext(path, factoryName);
    /**
     * Get a context for a given path.
     */
    private _contextForPath(path);
    /**
     * Create a context from a path and a model factory.
     */
    private _createContext(path, factory, kernelPreference);
    /**
     * Handle a context disposal.
     */
    private _onContextDisposed(context);
    /**
     * Get the model factory for a given widget name.
     */
    private _widgetFactoryFor(path, widgetName);
    /**
     * Creates a new document, or loads one from disk, depending on the `which` argument.
     * If `which==='create'`, then it creates a new document. If `which==='open'`,
     * then it loads the document from disk.
     *
     * The two cases differ in how the document context is handled, but the creation
     * of the widget and launching of the kernel are identical.
     */
    private _createOrOpenDocument(which, path, widgetName?, kernel?);
    /**
     * Handle an activateRequested signal from the widget manager.
     */
    private _onActivateRequested(sender, args);
    private _serviceManager;
    private _widgetManager;
    private _registry;
    private _contexts;
    private _opener;
    private _activateRequested;
}
/**
 * A namespace for document manager statics.
 */
export declare namespace DocumentManager {
    /**
     * The options used to initialize a document manager.
     */
    interface IOptions {
        /**
         * A document registry instance.
         */
        registry: DocumentRegistry;
        /**
         * A service manager instance.
         */
        manager: ServiceManager.IManager;
        /**
         * A widget opener for sibling widgets.
         */
        opener: IWidgetOpener;
    }
    /**
     * An interface for a widget opener.
     */
    interface IWidgetOpener {
        /**
         * Open the given widget.
         */
        open(widget: Widget): void;
    }
}

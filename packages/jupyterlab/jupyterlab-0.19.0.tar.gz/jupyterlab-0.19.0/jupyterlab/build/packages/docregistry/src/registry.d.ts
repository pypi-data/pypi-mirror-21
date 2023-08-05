import { Contents, Kernel } from '@jupyterlab/services';
import { IIterator } from '@phosphor/algorithm';
import { Token } from '@phosphor/coreutils';
import { IDisposable } from '@phosphor/disposable';
import { ISignal } from '@phosphor/signaling';
import { Widget } from '@phosphor/widgets';
import { IClientSession } from '@jupyterlab/apputils';
import { CodeEditor } from '@jupyterlab/codeeditor';
import { IChangedArgs as IChangedArgsGeneric } from '@jupyterlab/coreutils';
/**
 * The document registry token.
 */
export declare const IDocumentRegistry: Token<IDocumentRegistry>;
/**
 * The interface for a document registry.
 */
export interface IDocumentRegistry extends DocumentRegistry {
}
/**
 * The document registry.
 */
export declare class DocumentRegistry implements IDisposable {
    /**
     * A signal emitted when the registry has changed.
     */
    readonly changed: ISignal<this, DocumentRegistry.IChangedArgs>;
    /**
     * Get whether the document registry has been disposed.
     */
    readonly isDisposed: boolean;
    /**
     * Dispose of the resources held by the document registery.
     */
    dispose(): void;
    /**
     * Add a widget factory to the registry.
     *
     * @param factory - The factory instance to register.
     *
     * @returns A disposable which will unregister the factory.
     *
     * #### Notes
     * If a factory with the given `'displayName'` is already registered,
     * a warning will be logged, and this will be a no-op.
     * If `'*'` is given as a default extension, the factory will be registered
     * as the global default.
     * If an extension or global default is already registered, this factory
     * will override the existing default.
     */
    addWidgetFactory(factory: DocumentRegistry.WidgetFactory): IDisposable;
    /**
     * Add a model factory to the registry.
     *
     * @param factory - The factory instance.
     *
     * @returns A disposable which will unregister the factory.
     *
     * #### Notes
     * If a factory with the given `name` is already registered, or
     * the given factory is already registered, a warning will be logged
     * and this will be a no-op.
     */
    addModelFactory(factory: DocumentRegistry.ModelFactory): IDisposable;
    /**
     * Add a widget extension to the registry.
     *
     * @param widgetName - The name of the widget factory.
     *
     * @param extension - A widget extension.
     *
     * @returns A disposable which will unregister the extension.
     *
     * #### Notes
     * If the extension is already registered for the given
     * widget name, a warning will be logged and this will be a no-op.
     */
    addWidgetExtension(widgetName: string, extension: DocumentRegistry.WidgetExtension): IDisposable;
    /**
     * Add a file type to the document registry.
     *
     * @params fileType - The file type object to register.
     *
     * @returns A disposable which will unregister the command.
     *
     * #### Notes
     * These are used to populate the "Create New" dialog.
     */
    addFileType(fileType: DocumentRegistry.IFileType): IDisposable;
    /**
     * Add a creator to the registry.
     *
     * @params creator - The file creator object to register.
     *
     * @returns A disposable which will unregister the creator.
     */
    addCreator(creator: DocumentRegistry.IFileCreator): IDisposable;
    /**
     * Get a list of the preferred widget factories.
     *
     * @param ext - An optional file extension to filter the results.
     *
     * @returns A new array of widget factories.
     *
     * #### Notes
     * Only the widget factories whose associated model factory have
     * been registered will be returned.
     * The first item is considered the default. The returned iterator
     * has widget factories in the following order:
     * - extension-specific default factory
     * - global default factory
     * - all other extension-specific factories
     * - all other global factories
     */
    preferredWidgetFactories(ext?: string): DocumentRegistry.WidgetFactory[];
    /**
     * Get the default widget factory for an extension.
     *
     * @param ext - An optional file extension to filter the results.
     *
     * @returns The default widget factory for an extension.
     *
     * #### Notes
     * This is equivalent to the first value in [[preferredWidgetFactories]].
     */
    defaultWidgetFactory(ext?: string): DocumentRegistry.WidgetFactory;
    /**
     * Create an iterator over the widget factories that have been registered.
     *
     * @returns A new iterator of widget factories.
     */
    widgetFactories(): IIterator<DocumentRegistry.WidgetFactory>;
    /**
     * Create an iterator over the model factories that have been registered.
     *
     * @returns A new iterator of model factories.
     */
    modelFactories(): IIterator<DocumentRegistry.ModelFactory>;
    /**
     * Create an iterator over the registered extensions for a given widget.
     *
     * @param widgetName - The name of the widget factory.
     *
     * @returns A new iterator over the widget extensions.
     */
    widgetExtensions(widgetName: string): IIterator<DocumentRegistry.WidgetExtension>;
    /**
     * Create an iterator over the file types that have been registered.
     *
     * @returns A new iterator of file types.
     */
    fileTypes(): IIterator<DocumentRegistry.IFileType>;
    /**
     * Create an iterator over the file creators that have been registered.
     *
     * @returns A new iterator of file creatores.
     */
    creators(): IIterator<DocumentRegistry.IFileCreator>;
    /**
     * Get a widget factory by name.
     *
     * @param widgetName - The name of the widget factory.
     *
     * @returns A widget factory instance.
     */
    getWidgetFactory(widgetName: string): DocumentRegistry.WidgetFactory;
    /**
     * Get a model factory by name.
     *
     * @param name - The name of the model factory.
     *
     * @returns A model factory instance.
     */
    getModelFactory(name: string): DocumentRegistry.ModelFactory;
    /**
     * Get a file type by name.
     */
    getFileType(name: string): DocumentRegistry.IFileType;
    /**
     * Get a creator by name.
     */
    getCreator(name: string): DocumentRegistry.IFileCreator;
    /**
     * Get a kernel preference.
     *
     * @param ext - The file extension.
     *
     * @param widgetName - The name of the widget factory.
     *
     * @param kernel - An optional existing kernel model.
     *
     * @returns A kernel preference.
     */
    getKernelPreference(ext: string, widgetName: string, kernel?: Kernel.IModel): IClientSession.IKernelPreference;
    private _modelFactories;
    private _widgetFactories;
    private _defaultWidgetFactory;
    private _defaultWidgetFactories;
    private _widgetFactoryExtensions;
    private _fileTypes;
    private _creators;
    private _extenders;
    private _changed;
}
/**
 * The namespace for the `DocumentRegistry` class statics.
 */
export declare namespace DocumentRegistry {
    /**
     * The interface for a document model.
     */
    interface IModel extends IDisposable {
        /**
         * A signal emitted when the document content changes.
         */
        contentChanged: ISignal<this, void>;
        /**
         * A signal emitted when the model state changes.
         */
        stateChanged: ISignal<this, IChangedArgsGeneric<any>>;
        /**
         * The dirty state of the model.
         *
         * #### Notes
         * This should be cleared when the document is loaded from
         * or saved to disk.
         */
        dirty: boolean;
        /**
         * The read-only state of the model.
         */
        readOnly: boolean;
        /**
         * The default kernel name of the document.
         */
        readonly defaultKernelName: string;
        /**
         * The default kernel language of the document.
         */
        readonly defaultKernelLanguage: string;
        /**
         * Serialize the model to a string.
         */
        toString(): string;
        /**
         * Deserialize the model from a string.
         *
         * #### Notes
         * Should emit a [contentChanged] signal.
         */
        fromString(value: string): void;
        /**
         * Serialize the model to JSON.
         */
        toJSON(): any;
        /**
         * Deserialize the model from JSON.
         *
         * #### Notes
         * Should emit a [contentChanged] signal.
         */
        fromJSON(value: any): void;
    }
    /**
     * The interface for a document model that represents code.
     */
    interface ICodeModel extends IModel, CodeEditor.IModel {
    }
    /**
     * The document context object.
     */
    interface IContext<T extends IModel> extends IDisposable {
        /**
         * A signal emitted when the path changes.
         */
        pathChanged: ISignal<this, string>;
        /**
         * A signal emitted when the contentsModel changes.
         */
        fileChanged: ISignal<this, Contents.IModel>;
        /**
         * A signal emitted when the context is disposed.
         */
        disposed: ISignal<this, void>;
        /**
         * Get the model associated with the document.
         */
        readonly model: T;
        /**
         * The client session object associated with the context.
         */
        readonly session: IClientSession;
        /**
         * The current path associated with the document.
         */
        readonly path: string;
        /**
         * The current contents model associated with the document
         *
         * #### Notes
         * The model will have an empty `contents` field.
         * It will be `null` until the context is ready.
         */
        readonly contentsModel: Contents.IModel;
        /**
         * Whether the context is ready.
         */
        readonly isReady: boolean;
        /**
         * A promise that is fulfilled when the context is ready.
         */
        readonly ready: Promise<void>;
        /**
         * Save the document contents to disk.
         */
        save(): Promise<void>;
        /**
         * Save the document to a different path chosen by the user.
         */
        saveAs(): Promise<void>;
        /**
         * Revert the document contents to disk contents.
         */
        revert(): Promise<void>;
        /**
         * Create a checkpoint for the file.
         *
         * @returns A promise which resolves with the new checkpoint model when the
         *   checkpoint is created.
         */
        createCheckpoint(): Promise<Contents.ICheckpointModel>;
        /**
         * Delete a checkpoint for the file.
         *
         * @param checkpointID - The id of the checkpoint to delete.
         *
         * @returns A promise which resolves when the checkpoint is deleted.
         */
        deleteCheckpoint(checkpointID: string): Promise<void>;
        /**
         * Restore the file to a known checkpoint state.
         *
         * @param checkpointID - The optional id of the checkpoint to restore,
         *   defaults to the most recent checkpoint.
         *
         * @returns A promise which resolves when the checkpoint is restored.
         */
        restoreCheckpoint(checkpointID?: string): Promise<void>;
        /**
         * List available checkpoints for the file.
         *
         * @returns A promise which resolves with a list of checkpoint models for
         *    the file.
         */
        listCheckpoints(): Promise<Contents.ICheckpointModel[]>;
        /**
         * Resolve a relative url to a correct server path.
         */
        resolveUrl(url: string): Promise<string>;
        /**
         * Get the download url of a given absolute server path.
         */
        getDownloadUrl(path: string): Promise<string>;
        /**
         * Add a sibling widget to the document manager.
         *
         * @param widget - The widget to add to the document manager.
         *
         * @returns A disposable used to remove the sibling if desired.
         *
         * #### Notes
         * It is assumed that the widget has the same model and context
         * as the original widget.
         */
        addSibling(widget: Widget): IDisposable;
    }
    /**
     * A type alias for a context.
     */
    type Context = IContext<IModel>;
    /**
     * A type alias for a code context.
     */
    type CodeContext = IContext<ICodeModel>;
    /**
     * The options used to initialize a widget factory.
     */
    interface IWidgetFactoryOptions {
        /**
         * The file extensions the widget can view.
         *
         * #### Notes
         * Use "*" to denote all files. Specific file extensions must be preceded
         * with '.', like '.png', '.txt', etc.  They may themselves contain a
         * period (e.g. .table.json).
         */
        readonly fileExtensions: string[];
        /**
         * The name of the widget to display in dialogs.
         */
        readonly name: string;
        /**
         * The file extensions for which the factory should be the default.
         *
         * #### Notes
         * Use "*" to denote all files. Specific file extensions must be preceded
         * with '.', like '.png', '.txt', etc. Entries in this attribute must also
         * be included in the fileExtensions attribute.
         * The default is an empty array.
         *
         * **See also:** [[fileExtensions]].
         */
        readonly defaultFor?: string[];
        /**
         * The registered name of the model type used to create the widgets.
         */
        readonly modelName?: string;
        /**
         * Whether the widgets prefer having a kernel started.
         */
        readonly preferKernel?: boolean;
        /**
         * Whether the widgets can start a kernel when opened.
         */
        readonly canStartKernel?: boolean;
    }
    /**
     * The interface for a widget factory.
     */
    interface IWidgetFactory<T extends Widget, U extends IModel> extends IDisposable, IWidgetFactoryOptions {
        /**
         * A signal emitted when a widget is created.
         */
        widgetCreated: ISignal<IWidgetFactory<T, U>, T>;
        /**
         * Create a new widget given a context.
         *
         * #### Notes
         * It should emit the [widgetCreated] signal with the new widget.
         */
        createNew(context: IContext<U>): T;
    }
    /**
     * A type alias for a standard widget factory.
     */
    type WidgetFactory = IWidgetFactory<Widget, IModel>;
    /**
     * An interface for a widget extension.
     */
    interface IWidgetExtension<T extends Widget, U extends IModel> {
        /**
         * Create a new extension for a given widget.
         */
        createNew(widget: T, context: IContext<U>): IDisposable;
    }
    /**
     * A type alias for a standard widget extension.
     */
    type WidgetExtension = IWidgetExtension<Widget, IModel>;
    /**
     * The interface for a model factory.
     */
    interface IModelFactory<T extends IModel> extends IDisposable {
        /**
         * The name of the model.
         */
        readonly name: string;
        /**
         * The content type of the file (defaults to `"file"`).
         */
        readonly contentType: Contents.ContentType;
        /**
         * The format of the file (defaults to `"text"`).
         */
        readonly fileFormat: Contents.FileFormat;
        /**
         * Create a new model for a given path.
         *
         * @param languagePreference - An optional kernel language preference.
         *
         * @returns A new document model.
         */
        createNew(languagePreference?: string): T;
        /**
         * Get the preferred kernel language given an extension.
         */
        preferredLanguage(ext: string): string;
    }
    /**
     * A type alias for a standard model factory.
     */
    type ModelFactory = IModelFactory<IModel>;
    /**
     * A type alias for a code model factory.
     */
    type CodeModelFactory = IModelFactory<ICodeModel>;
    /**
     * An interface for a file type.
     */
    interface IFileType {
        /**
         * The name of the file type.
         */
        readonly name: string;
        /**
         * The extension of the file type (e.g. `".txt"`).  Can be a compound
         * extension (e.g. `".table.json:`).
         */
        readonly extension: string;
        /**
         * The optional mimetype of the file type.
         */
        readonly mimetype?: string;
        /**
         * The optional icon class to use for the file type.
         */
        readonly icon?: string;
        /**
         * The content type of the new file (defaults to `"file"`).
         */
        readonly contentType?: Contents.ContentType;
        /**
         * The format of the new file (default to `"text"`).
         */
        readonly fileFormat?: Contents.FileFormat;
    }
    /**
     * An interface for a "Create New" item.
     */
    interface IFileCreator {
        /**
         * The name of the file creator.
         */
        readonly name: string;
        /**
         * The filetype name associated with the creator.
         */
        readonly fileType: string;
        /**
         * The optional widget name.
         */
        readonly widgetName?: string;
        /**
         * The optional kernel name.
         */
        readonly kernelName?: string;
    }
    /**
     * An arguments object for the `changed` signal.
     */
    interface IChangedArgs {
        /**
         * The type of the changed item.
         */
        readonly type: 'widgetFactory' | 'modelFactory' | 'widgetExtension' | 'fileCreator' | 'fileType';
        /**
         * The name of the item.
         */
        readonly name: string;
        /**
         * Whether the item was added or removed.
         */
        readonly change: 'added' | 'removed';
    }
    /**
     * Get the extension name of a path.
     *
     * @param file - string.
     *
     * #### Notes
     * Dotted filenames (e.g. `".table.json"` are allowed.
     */
    function extname(path: string): string;
}

import { Contents } from '@jupyterlab/services';
import { ISignal } from '@phosphor/signaling';
import { Widget } from '@phosphor/widgets';
import { CodeEditor } from '@jupyterlab/codeeditor';
import { IChangedArgs } from '@jupyterlab/coreutils';
import { DocumentRegistry } from './index';
/**
 * The default implementation of a document model.
 */
export declare class DocumentModel extends CodeEditor.Model implements DocumentRegistry.ICodeModel {
    /**
     * Construct a new document model.
     */
    constructor(languagePreference?: string);
    /**
     * A signal emitted when the document content changes.
     */
    readonly contentChanged: ISignal<this, void>;
    /**
     * A signal emitted when the document state changes.
     */
    readonly stateChanged: ISignal<this, IChangedArgs<any>>;
    /**
     * The dirty state of the document.
     */
    dirty: boolean;
    /**
     * The read only state of the document.
     */
    readOnly: boolean;
    /**
     * The default kernel name of the document.
     *
     * #### Notes
     * This is a read-only property.
     */
    readonly defaultKernelName: string;
    /**
     * The default kernel language of the document.
     *
     * #### Notes
     * This is a read-only property.
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
    /**
     * Trigger a state change signal.
     */
    protected triggerStateChange(args: IChangedArgs<any>): void;
    /**
     * Trigger a content changed signal.
     */
    protected triggerContentChange(): void;
    private _defaultLang;
    private _dirty;
    private _readOnly;
    private _contentChanged;
    private _stateChanged;
}
/**
 * An implementation of a model factory for text files.
 */
export declare class TextModelFactory implements DocumentRegistry.CodeModelFactory {
    /**
     * The name of the model type.
     *
     * #### Notes
     * This is a read-only property.
     */
    readonly name: string;
    /**
     * The type of the file.
     *
     * #### Notes
     * This is a read-only property.
     */
    readonly contentType: Contents.ContentType;
    /**
     * The format of the file.
     *
     * This is a read-only property.
     */
    readonly fileFormat: Contents.FileFormat;
    /**
     * Get whether the model factory has been disposed.
     */
    readonly isDisposed: boolean;
    /**
     * Dispose of the resources held by the model factory.
     */
    dispose(): void;
    /**
     * Create a new model.
     *
     * @param languagePreference - An optional kernel language preference.
     *
     * @returns A new document model.
     */
    createNew(languagePreference?: string): DocumentRegistry.ICodeModel;
    /**
     * Get the preferred kernel language given an extension.
     */
    preferredLanguage(ext: string): string;
    private _isDisposed;
}
/**
 * An implementation of a model factory for base64 files.
 */
export declare class Base64ModelFactory extends TextModelFactory {
    /**
     * The name of the model type.
     *
     * #### Notes
     * This is a read-only property.
     */
    readonly name: string;
    /**
     * The type of the file.
     *
     * #### Notes
     * This is a read-only property.
     */
    readonly contentType: Contents.ContentType;
    /**
     * The format of the file.
     *
     * This is a read-only property.
     */
    readonly fileFormat: Contents.FileFormat;
}
/**
 * The default implemetation of a widget factory.
 */
export declare abstract class ABCWidgetFactory<T extends Widget, U extends DocumentRegistry.IModel> implements DocumentRegistry.IWidgetFactory<T, U> {
    /**
     * Construct a new `ABCWidgetFactory`.
     */
    constructor(options: DocumentRegistry.IWidgetFactoryOptions);
    /**
     * A signal emitted when a widget is created.
     */
    readonly widgetCreated: ISignal<DocumentRegistry.IWidgetFactory<T, U>, T>;
    /**
     * Get whether the model factory has been disposed.
     */
    readonly isDisposed: boolean;
    /**
     * Dispose of the resources held by the document manager.
     */
    dispose(): void;
    /**
     * The name of the widget to display in dialogs.
     */
    readonly name: string;
    /**
     * The file extensions the widget can view.
     */
    readonly fileExtensions: string[];
    /**
     * The registered name of the model type used to create the widgets.
     */
    readonly modelName: string;
    /**
     * The file extensions for which the factory should be the default.
     */
    readonly defaultFor: string[];
    /**
     * Whether the widgets prefer having a kernel started.
     */
    readonly preferKernel: boolean;
    /**
     * Whether the widgets can start a kernel when opened.
     */
    readonly canStartKernel: boolean;
    /**
     * Create a new widget given a document model and a context.
     *
     * #### Notes
     * It should emit the [widgetCreated] signal with the new widget.
     */
    createNew(context: DocumentRegistry.IContext<U>): T;
    /**
     * Create a widget for a context.
     */
    protected abstract createNewWidget(context: DocumentRegistry.IContext<U>): T;
    private _isDisposed;
    private _name;
    private _canStartKernel;
    private _preferKernel;
    private _modelName;
    private _fileExtensions;
    private _defaultFor;
    private _widgetCreated;
}

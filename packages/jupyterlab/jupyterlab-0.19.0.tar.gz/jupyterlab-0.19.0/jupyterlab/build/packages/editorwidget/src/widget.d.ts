import { ABCWidgetFactory, DocumentRegistry } from '@jupyterlab/docregistry';
import { CodeEditor, IEditorServices, IEditorMimeTypeService, CodeEditorWidget } from '@jupyterlab/codeeditor';
/**
 * A document widget for editors.
 */
export declare class EditorWidget extends CodeEditorWidget {
    /**
     * Construct a new editor widget.
     */
    constructor(options: EditorWidget.IOptions);
    /**
     * Get the context for the editor widget.
     */
    readonly context: DocumentRegistry.Context;
    /**
     * Handle actions that should be taken when the context is ready.
     */
    private _onContextReady();
    /**
     * Handle a change to the context model state.
     */
    private _onModelStateChanged(sender, args);
    /**
     * Handle the dirty state of the context model.
     */
    private _handleDirtyState();
    /**
     * Handle a change in context model content.
     */
    private _onContentChanged();
    /**
     * Handle a change to the path.
     */
    private _onPathChanged();
    protected _context: DocumentRegistry.Context;
    private _mimeTypeService;
}
/**
 * The namespace for editor widget statics.
 */
export declare namespace EditorWidget {
    /**
     * The options used to create an editor widget.
     */
    interface IOptions {
        /**
         * A code editor factory.
         */
        factory: CodeEditor.Factory;
        /**
         * The mime type service for the editor.
         */
        mimeTypeService: IEditorMimeTypeService;
        /**
         * The document context associated with the editor.
         */
        context: DocumentRegistry.CodeContext;
    }
}
/**
 * A widget factory for editors.
 */
export declare class EditorWidgetFactory extends ABCWidgetFactory<EditorWidget, DocumentRegistry.ICodeModel> {
    /**
     * Construct a new editor widget factory.
     */
    constructor(options: EditorWidgetFactory.IOptions);
    /**
     * Create a new widget given a context.
     */
    protected createNewWidget(context: DocumentRegistry.CodeContext): EditorWidget;
    private _services;
}
/**
 * The namespace for `EditorWidgetFactory` class statics.
 */
export declare namespace EditorWidgetFactory {
    /**
     * The options used to create an editor widget factory.
     */
    interface IOptions {
        /**
         * The editor services used by the factory.
         */
        editorServices: IEditorServices;
        /**
         * The factory options associated with the factory.
         */
        factoryOptions: DocumentRegistry.IWidgetFactoryOptions;
    }
}

import { IClientSession } from '@jupyterlab/apputils';
import { BaseCellWidget, CodeCellWidget } from '@jupyterlab/cells';
import { IEditorMimeTypeService, CodeEditor } from '@jupyterlab/codeeditor';
import { OutputAreaWidget } from '@jupyterlab/outputarea';
import { IRenderMime } from '@jupyterlab/rendermime';
import { ServiceManager } from '@jupyterlab/services';
import { Token } from '@phosphor/coreutils';
import { Message } from '@phosphor/messaging';
import { Panel } from '@phosphor/widgets';
import { CodeConsole } from './widget';
/**
 * A panel which contains a console and the ability to add other children.
 */
export declare class ConsolePanel extends Panel {
    /**
     * Construct a console panel.
     */
    constructor(options: ConsolePanel.IOptions);
    /**
     * The console widget used by the panel.
     */
    readonly console: CodeConsole;
    /**
     * The session used by the panel.
     */
    readonly session: IClientSession;
    /**
     * Dispose of the resources held by the widget.
     */
    dispose(): void;
    /**
     * Handle `'after-attach'` messages.
     */
    protected onAfterAttach(msg: Message): void;
    /**
     * Handle `'activate-request'` messages.
     */
    protected onActivateRequest(msg: Message): void;
    /**
     * Handle `'close-request'` messages.
     */
    protected onCloseRequest(msg: Message): void;
    /**
     * Handle a console execution.
     */
    private _onExecuted(sender, args);
    /**
     * Update the console panel title.
     */
    private _updateTitle();
    private _manager;
    private _executed;
    private _connected;
    private _session;
}
/**
 * A namespace for ConsolePanel statics.
 */
export declare namespace ConsolePanel {
    /**
     * The initialization options for a console panel.
     */
    interface IOptions {
        /**
         * The rendermime instance used by the panel.
         */
        rendermime: IRenderMime;
        /**
         * The content factory for the panel.
         */
        contentFactory: IContentFactory;
        /**
         * The service manager used by the panel.
         */
        manager: ServiceManager.IManager;
        /**
         * The path of an existing console.
         */
        path?: string;
        /**
         * The base path for a new console.
         */
        basePath?: string;
        /**
         * The name of the console.
         */
        name?: string;
        /**
         * A kernel preference.
         */
        kernelPreference?: IClientSession.IKernelPreference;
        /**
         * The model factory for the console widget.
         */
        modelFactory?: CodeConsole.IModelFactory;
        /**
         * The service used to look up mime types.
         */
        mimeTypeService: IEditorMimeTypeService;
    }
    /**
     * The console panel renderer.
     */
    interface IContentFactory {
        /**
         * The editor factory used by the content factory.
         */
        readonly editorFactory: CodeEditor.Factory;
        /**
         * The factory for code console content.
         */
        readonly consoleContentFactory: CodeConsole.IContentFactory;
        /**
         * Create a new console panel.
         */
        createConsole(options: CodeConsole.IOptions): CodeConsole;
    }
    /**
     * Default implementation of `IContentFactory`.
     */
    class ContentFactory implements IContentFactory {
        /**
         * Create a new content factory.
         */
        constructor(options: ContentFactory.IOptions);
        /**
         * The editor factory used by the content factory.
         */
        readonly editorFactory: CodeEditor.Factory;
        /**
         * The factory for code console content.
         */
        readonly consoleContentFactory: CodeConsole.IContentFactory;
        /**
         * Create a new console panel.
         */
        createConsole(options: CodeConsole.IOptions): CodeConsole;
    }
    /**
     * The namespace for `ContentFactory`.
     */
    namespace ContentFactory {
        /**
         * An initialization options for a console panel factory.
         */
        interface IOptions {
            /**
             * The editor factory.  This will be used to create a
             * consoleContentFactory if none is given.
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
             * The factory for console widget content.  If given, this will
             * take precedence over the output area and cell factories.
             */
            consoleContentFactory?: CodeConsole.IContentFactory;
        }
    }
    /**
     * The console renderer token.
     */
    const IContentFactory: Token<IContentFactory>;
}

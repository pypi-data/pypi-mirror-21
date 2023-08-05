import { Message } from '@phosphor/messaging';
import { Widget } from '@phosphor/widgets';
import { DocumentRegistry, ABCWidgetFactory } from '@jupyterlab/docregistry';
import { RenderMime } from '@jupyterlab/rendermime';
/**
 * A widget for rendered markdown.
 */
export declare class MarkdownWidget extends Widget {
    /**
     * Construct a new markdown widget.
     */
    constructor(context: DocumentRegistry.Context, rendermime: RenderMime);
    /**
     * The markdown widget's context.
     */
    readonly context: DocumentRegistry.Context;
    /**
     * Dispose of the resources held by the widget.
     */
    dispose(): void;
    /**
     * Handle `'activate-request'` messages.
     */
    protected onActivateRequest(msg: Message): void;
    /**
     * Handle an `after-attach` message to the widget.
     */
    protected onAfterAttach(msg: Message): void;
    /**
     * Handle an `update-request` message to the widget.
     */
    protected onUpdateRequest(msg: Message): void;
    /**
     * Handle a path change.
     */
    private _onPathChanged();
    private _context;
    private _monitor;
    private _rendermime;
}
/**
 * A widget factory for Markdown.
 */
export declare class MarkdownWidgetFactory extends ABCWidgetFactory<MarkdownWidget, DocumentRegistry.IModel> {
    /**
     * Construct a new markdown widget factory.
     */
    constructor(options: MarkdownWidgetFactory.IOptions);
    /**
     * Create a new widget given a context.
     */
    protected createNewWidget(context: DocumentRegistry.Context): MarkdownWidget;
    private _rendermime;
}
/**
 * A namespace for `MarkdownWidgetFactory` statics.
 */
export declare namespace MarkdownWidgetFactory {
    /**
     * The options used to create a markdown widget factory.
     */
    interface IOptions extends DocumentRegistry.IWidgetFactoryOptions {
        /**
         * A rendermime instance.
         */
        rendermime: RenderMime;
    }
}

import { Message } from '@phosphor/messaging';
import { Widget } from '@phosphor/widgets';
import { ABCWidgetFactory, DocumentRegistry } from '@jupyterlab/docregistry';
/**
 * A widget for images.
 */
export declare class ImageWidget extends Widget {
    /**
     * Construct a new image widget.
     */
    constructor(context: DocumentRegistry.Context);
    /**
     * The image widget's context.
     */
    readonly context: DocumentRegistry.Context;
    /**
     * The scale factor for the image.
     */
    scale: number;
    /**
     * Dispose of the resources used by the widget.
     */
    dispose(): void;
    /**
     * Handle `update-request` messages for the widget.
     */
    protected onUpdateRequest(msg: Message): void;
    /**
     * Handle `'activate-request'` messages.
     */
    protected onActivateRequest(msg: Message): void;
    /**
     * Handle a change to the title.
     */
    private _onTitleChanged();
    private _context;
    private _scale;
}
/**
 * A widget factory for images.
 */
export declare class ImageWidgetFactory extends ABCWidgetFactory<ImageWidget, DocumentRegistry.IModel> {
    /**
     * Create a new widget given a context.
     */
    protected createNewWidget(context: DocumentRegistry.IContext<DocumentRegistry.IModel>): ImageWidget;
}

import { Message } from '@phosphor/messaging';
import { Widget } from '@phosphor/widgets';
import { ABCWidgetFactory, DocumentRegistry } from '@jupyterlab/docregistry';
import { CSVModel } from './table';
/**
 * A widget for CSV tables.
 */
export declare class CSVWidget extends Widget {
    /**
     * Construct a new CSV widget.
     */
    constructor(options: CSVWidget.IOptions);
    /**
     * The CSV widget's context.
     */
    readonly context: DocumentRegistry.Context;
    /**
     * The CSV data model.
     */
    readonly model: CSVModel;
    /**
     * Dispose of the resources used by the widget.
     */
    dispose(): void;
    /**
     * Handle `'activate-request'` messages.
     */
    protected onActivateRequest(msg: Message): void;
    /**
     * Handle a max exceeded in a csv widget.
     */
    private _onMaxExceeded(sender, overflow);
    /**
     * Handle a change in delimiter.
     */
    private _onDelimiterChanged(sender, delimiter);
    /**
     * Handle a change in content.
     */
    private _onContentChanged();
    /**
     * Handle a change in path.
     */
    private _onPathChanged();
    private _context;
    private _model;
    private _table;
    private _toolbar;
    private _warning;
}
/**
 * A namespace for `CSVWidget` statics.
 */
export declare namespace CSVWidget {
    /**
     * Instantiation options for CSV widgets.
     */
    interface IOptions {
        /**
         * The document context for the CSV being rendered by the widget.
         */
        context: DocumentRegistry.Context;
    }
}
/**
 * A widget factory for CSV widgets.
 */
export declare class CSVWidgetFactory extends ABCWidgetFactory<CSVWidget, DocumentRegistry.IModel> {
    /**
     * Create a new widget given a context.
     */
    protected createNewWidget(context: DocumentRegistry.Context): CSVWidget;
}

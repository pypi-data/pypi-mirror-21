import * as dsv from 'd3-dsv';
import { ISignal } from '@phosphor/signaling';
import { VirtualNode } from '@phosphor/virtualdom';
import { VDomModel, VDomWidget } from '@jupyterlab/apputils';
/**
 * The hard limit on the number of rows to display.
 */
export declare const DISPLAY_LIMIT: number;
/**
 * A CSV table content model.
 */
export declare class CSVModel extends VDomModel {
    /**
     * Instantiate a CSV model.
     */
    constructor(options?: CSVModel.IOptions);
    /**
     * A signal emitted when the parsed value's rows exceed the display limit. It
     * emits the length of the parsed value.
     */
    readonly maxExceeded: ISignal<this, CSVModel.IOverflow>;
    /**
     * The raw model content.
     */
    content: string;
    /**
     * The CSV delimiter value.
     */
    delimiter: string;
    /**
     * Parse the content using the model's delimiter.
     *
     * #### Notes
     * This method will always return parsed content that has at most the display
     * limit worth of rows, currently maxing out at 1000 rows.
     */
    parse(): dsv.DSVParsedArray<dsv.DSVRowString>;
    private _content;
    private _delimiter;
    private _maxExceeded;
}
/**
 * A namespace for `CSVModel` statics.
 */
export declare namespace CSVModel {
    /**
     * The value emitted when there are more data rows than what can be displayed.
     */
    interface IOverflow {
        /**
         * The actual number of rows in the data.
         */
        available: number;
        /**
         * The maximum number of items that can be displayed.
         */
        maximum: number;
    }
    /**
     * Instantiation options for CSV models.
     */
    interface IOptions {
        /**
         * The raw model content.
         */
        content?: string;
        /**
         * The CSV delimiter value.
         *
         * #### Notes
         * If this value is not set, it defaults to `','`.
         */
        delimiter?: string;
    }
}
/**
 * A CSV table content widget.
 */
export declare class CSVTable extends VDomWidget<CSVModel> {
    /**
     * Instantiate a new CSV table widget.
     */
    constructor();
    /**
     * Render the content as virtual DOM nodes.
     */
    protected render(): VirtualNode | VirtualNode[];
}

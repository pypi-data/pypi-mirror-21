import { ISignal } from '@phosphor/signaling';
import { IObservableVector, nbformat } from '@jupyterlab/coreutils';
import { IOutputModel } from '@jupyterlab/rendermime';
import { IOutputAreaModel } from './widget';
/**
 * The default implementation of the IOutputAreaModel.
 */
export declare class OutputAreaModel implements IOutputAreaModel {
    /**
     * Construct a new observable outputs instance.
     */
    constructor(options?: IOutputAreaModel.IOptions);
    /**
     * A signal emitted when the model state changes.
     */
    readonly stateChanged: ISignal<IOutputAreaModel, void>;
    /**
     * A signal emitted when the model changes.
     */
    readonly changed: ISignal<this, IOutputAreaModel.ChangedArgs>;
    /**
     * Get the length of the items in the model.
     */
    readonly length: number;
    /**
     * Get whether the model is trusted.
     */
    /**
     * Set whether the model is trusted.
     *
     * #### Notes
     * Changing the value will cause all of the models to re-set.
     */
    trusted: boolean;
    /**
     * The output content factory used by the model.
     */
    readonly contentFactory: IOutputAreaModel.IContentFactory;
    /**
     * Test whether the model is disposed.
     */
    readonly isDisposed: boolean;
    /**
     * Dispose of the resources used by the model.
     */
    dispose(): void;
    /**
     * Get an item at the specified index.
     */
    get(index: number): IOutputModel;
    /**
     * Add an output, which may be combined with previous output.
     *
     * #### Notes
     * The output bundle is copied.
     * Contiguous stream outputs of the same `name` are combined.
     */
    add(output: nbformat.IOutput): number;
    /**
     * Clear all of the output.
     *
     * @param wait Delay clearing the output until the next message is added.
     */
    clear(wait?: boolean): void;
    /**
     * Deserialize the model from JSON.
     *
     * #### Notes
     * This will clear any existing data.
     */
    fromJSON(values: nbformat.IOutput[]): void;
    /**
     * Serialize the model to JSON.
     */
    toJSON(): nbformat.IOutput[];
    /**
     * Add an item to the list.
     */
    private _add(value);
    protected clearNext: boolean;
    protected list: IObservableVector<IOutputModel>;
    /**
     * Create an output item and hook up its signals.
     */
    private _createItem(options);
    /**
     * Handle a change to the list.
     */
    private _onListChanged(sender, args);
    /**
     * Handle a change to an item.
     */
    private _onGenericChange();
    private _lastStream;
    private _lastName;
    private _trusted;
    private _isDisposed;
    private _stateChanged;
    private _changed;
}
/**
 * The namespace for OutputAreaModel class statics.
 */
export declare namespace OutputAreaModel {
    /**
     * The default implementation of a `IModelOutputFactory`.
     */
    class ContentFactory implements IOutputAreaModel.IContentFactory {
        /**
         * Create an output model.
         */
        createOutputModel(options: IOutputModel.IOptions): IOutputModel;
    }
    /**
     * The default output model factory.
     */
    const defaultContentFactory: ContentFactory;
}

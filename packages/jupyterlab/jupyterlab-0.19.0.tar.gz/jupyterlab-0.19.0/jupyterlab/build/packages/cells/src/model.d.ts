import { ISignal, Signal } from '@phosphor/signaling';
import { CodeEditor } from '@jupyterlab/codeeditor';
import { IChangedArgs, nbformat } from '@jupyterlab/coreutils';
import { IObservableJSON } from '@jupyterlab/coreutils';
import { IOutputAreaModel } from '@jupyterlab/outputarea';
/**
 * The definition of a model object for a cell.
 */
export interface ICellModel extends CodeEditor.IModel {
    /**
     * The type of the cell.
     */
    readonly type: nbformat.CellType;
    /**
     * A signal emitted when the content of the model changes.
     */
    readonly contentChanged: ISignal<ICellModel, void>;
    /**
     * A signal emitted when a model state changes.
     */
    readonly stateChanged: ISignal<ICellModel, IChangedArgs<any>>;
    /**
     * Whether the cell is trusted.
     */
    trusted: boolean;
    /**
     * The metadata associated with the cell.
     */
    readonly metadata: IObservableJSON;
    /**
     * Serialize the model to JSON.
     */
    toJSON(): nbformat.ICell;
}
/**
 * The definition of a code cell.
 */
export interface ICodeCellModel extends ICellModel {
    /**
     * The type of the cell.
     *
     * #### Notes
     * This is a read-only property.
     */
    type: 'code';
    /**
     * The code cell's prompt number. Will be null if the cell has not been run.
     */
    executionCount: nbformat.ExecutionCount;
    /**
     * The cell outputs.
     */
    outputs: IOutputAreaModel;
}
/**
 * The definition of a markdown cell.
 */
export interface IMarkdownCellModel extends ICellModel {
    /**
     * The type of the cell.
     */
    type: 'markdown';
}
/**
 * The definition of a raw cell.
 */
export interface IRawCellModel extends ICellModel {
    /**
     * The type of the cell.
     */
    type: 'raw';
}
/**
 * An implementation of the cell model.
 */
export declare class CellModel extends CodeEditor.Model implements ICellModel {
    /**
     * Construct a cell model from optional cell content.
     */
    constructor(options: CellModel.IOptions);
    /**
     * The type of cell.
     */
    readonly type: nbformat.CellType;
    /**
     * A signal emitted when the state of the model changes.
     */
    readonly contentChanged: Signal<this, void>;
    /**
     * A signal emitted when a model state changes.
     */
    readonly stateChanged: Signal<this, IChangedArgs<any>>;
    /**
     * The metadata associated with the cell.
     */
    readonly metadata: IObservableJSON;
    /**
     * Get the trusted state of the model.
     */
    /**
     * Set the trusted state of the model.
     */
    trusted: boolean;
    /**
     * Dispose of the resources held by the model.
     */
    dispose(): void;
    /**
     * Serialize the model to JSON.
     */
    toJSON(): nbformat.ICell;
    /**
     * Handle a change to the trusted state.
     *
     * The default implementation is a no-op.
     */
    onTrustedChanged(value: boolean): void;
    /**
     * Handle a change to the observable value.
     */
    protected onGenericChange(): void;
    private _metadata;
    private _trusted;
}
/**
 * The namespace for `CellModel` statics.
 */
export declare namespace CellModel {
    /**
     * The options used to initialize a `CellModel`.
     */
    interface IOptions {
        /**
         * The source cell data.
         */
        cell?: nbformat.IBaseCell;
    }
}
/**
 * An implementation of a raw cell model.
 */
export declare class RawCellModel extends CellModel {
    /**
     * The type of the cell.
     */
    readonly type: 'raw';
}
/**
 * An implementation of a markdown cell model.
 */
export declare class MarkdownCellModel extends CellModel {
    /**
     * Construct a markdown cell model from optional cell content.
     */
    constructor(options: CellModel.IOptions);
    /**
     * The type of the cell.
     */
    readonly type: 'markdown';
}
/**
 * An implementation of a code cell Model.
 */
export declare class CodeCellModel extends CellModel implements ICodeCellModel {
    /**
     * Construct a new code cell with optional original cell content.
     */
    constructor(options: CodeCellModel.IOptions);
    /**
     * The type of the cell.
     */
    readonly type: 'code';
    /**
     * The execution count of the cell.
     */
    executionCount: nbformat.ExecutionCount;
    /**
     * The cell outputs.
     */
    readonly outputs: IOutputAreaModel;
    /**
     * Dispose of the resources held by the model.
     */
    dispose(): void;
    /**
     * Serialize the model to JSON.
     */
    toJSON(): nbformat.ICodeCell;
    /**
     * Handle a change to the trusted state.
     *
     * The default implementation is a no-op.
     */
    onTrustedChanged(value: boolean): void;
    private _outputs;
    private _executionCount;
}
/**
 * The namespace for `CodeCellModel` statics.
 */
export declare namespace CodeCellModel {
    /**
     * The options used to initialize a `CodeCellModel`.
     */
    interface IOptions {
        /**
         * The source cell data.
         */
        cell?: nbformat.IBaseCell;
        /**
         * The factory for output area model creation.
         */
        contentFactory?: IContentFactory;
    }
    /**
     * A factory for creating code cell model content.
     */
    interface IContentFactory {
        /**
         * Create an output area.
         */
        createOutputArea(options: IOutputAreaModel.IOptions): IOutputAreaModel;
    }
    /**
     * The default implementation of an `IContentFactory`.
     */
    class ContentFactory {
        /**
         * Create an output area.
         */
        createOutputArea(options: IOutputAreaModel.IOptions): IOutputAreaModel;
    }
    /**
     * The shared `ConetntFactory` instance.
     */
    const defaultContentFactory: ContentFactory;
}

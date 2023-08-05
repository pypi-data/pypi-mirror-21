import { IIterator, IterableOrArrayLike } from '@phosphor/algorithm';
import { ISignal } from '@phosphor/signaling';
import { CompleterWidget } from './widget';
/**
 * An implementation of a completer model.
 */
export declare class CompleterModel implements CompleterWidget.IModel {
    /**
     * A signal emitted when state of the completer menu changes.
     */
    readonly stateChanged: ISignal<this, void>;
    /**
     * The original completion request details.
     */
    original: CompleterWidget.ITextState;
    /**
     * The current text change details.
     */
    current: CompleterWidget.ITextState;
    /**
     * The cursor details that the API has used to return matching options.
     */
    cursor: CompleterWidget.ICursorSpan;
    /**
     * The query against which items are filtered.
     */
    query: string;
    /**
     * A flag that is true when the model value was modified by a subset match.
     */
    subsetMatch: boolean;
    /**
     * Get whether the model is disposed.
     */
    readonly isDisposed: boolean;
    /**
     * Dispose of the resources held by the model.
     */
    dispose(): void;
    /**
     * The list of visible items in the completer menu.
     *
     * #### Notes
     * This is a read-only property.
     */
    items(): IIterator<CompleterWidget.IItem>;
    /**
     * The unfiltered list of all available options in a completer menu.
     */
    options(): IIterator<string>;
    /**
     * Set the avilable options in the completer menu.
     */
    setOptions(newValue: IterableOrArrayLike<string>): void;
    /**
     * Handle a cursor change.
     */
    handleCursorChange(change: CompleterWidget.ITextState): void;
    /**
     * Handle a text change.
     */
    handleTextChange(change: CompleterWidget.ITextState): void;
    /**
     * Create a resolved patch between the original state and a patch string.
     *
     * @param patch - The patch string to apply to the original value.
     *
     * @returns A patched text change or null if original value did not exist.
     */
    createPatch(patch: string): CompleterWidget.IPatch;
    /**
     * Reset the state of the model and emit a state change signal.
     *
     * @param hard - Reset even if a subset match is in progress.
     */
    reset(hard?: boolean): void;
    /**
     * Apply the query to the complete options list to return the matching subset.
     */
    private _filter();
    /**
     * Reset the state of the model.
     */
    private _reset();
    private _current;
    private _cursor;
    private _isDisposed;
    private _options;
    private _original;
    private _query;
    private _subsetMatch;
    private _stateChanged;
}

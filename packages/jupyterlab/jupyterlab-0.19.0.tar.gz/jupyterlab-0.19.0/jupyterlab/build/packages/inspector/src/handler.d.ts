import { IDisposable } from '@phosphor/disposable';
import { ISignal } from '@phosphor/signaling';
import { IClientSession } from '@jupyterlab/apputils';
import { CodeEditor } from '@jupyterlab/codeeditor';
import { RenderMime } from '@jupyterlab/rendermime';
import { IInspector } from './';
/**
 * An object that handles code inspection.
 */
export declare class InspectionHandler implements IDisposable, IInspector.IInspectable {
    /**
     * Construct a new inspection handler for a widget.
     */
    constructor(options: InspectionHandler.IOptions);
    /**
     * A signal emitted when the handler is disposed.
     */
    readonly disposed: ISignal<InspectionHandler, void>;
    /**
     * A signal emitted when inspector should clear all items with no history.
     */
    readonly ephemeralCleared: ISignal<InspectionHandler, void>;
    /**
     * A signal emitted when an inspector value is generated.
     */
    readonly inspected: ISignal<InspectionHandler, IInspector.IInspectorUpdate>;
    /**
     * The client session used by the inspection handler.
     */
    readonly session: IClientSession;
    /**
     * The editor widget used by the inspection handler.
     */
    editor: CodeEditor.IEditor;
    /**
     * Indicates whether the handler makes API inspection requests or stands by.
     *
     * #### Notes
     * The use case for this attribute is to limit the API traffic when no
     * inspector is visible.
     */
    standby: boolean;
    /**
     * Get whether the inspection handler is disposed.
     *
     * #### Notes
     * This is a read-only property.
     */
    readonly isDisposed: boolean;
    /**
     * Dispose of the resources used by the handler.
     */
    dispose(): void;
    /**
     * Handle a text changed signal from an editor.
     *
     * #### Notes
     * Update the hints inspector based on a text change.
     */
    protected onTextChanged(): void;
    private _disposed;
    private _editor;
    private _ephemeralCleared;
    private _inspected;
    private _pending;
    private _rendermime;
    private _standby;
}
/**
 * A namespace for inspection handler statics.
 */
export declare namespace InspectionHandler {
    /**
     * The instantiation options for an inspection handler.
     */
    interface IOptions {
        /**
         * The client session for the inspection handler.
         */
        session: IClientSession;
        /**
         * The mime renderer for the inspection handler.
         */
        rendermime: RenderMime;
    }
}

import { Kernel } from '@jupyterlab/services';
import { CommandRegistry } from '@phosphor/commands';
import { Widget } from '@phosphor/widgets';
import { DocumentManager } from '@jupyterlab/docmanager';
import { FileBrowserModel } from './model';
/**
 * A widget which hosts the file browser buttons.
 */
export declare class FileButtons extends Widget {
    /**
     * Construct a new file browser buttons widget.
     */
    constructor(options: FileButtons.IOptions);
    /**
     * Dispose of the resources held by the widget.
     */
    dispose(): void;
    /**
     * Get the model used by the widget.
     */
    readonly model: FileBrowserModel;
    /**
     * Get the document manager used by the widget.
     */
    readonly manager: DocumentManager;
    /**
     * Get the create button node.
     */
    readonly createNode: HTMLButtonElement;
    /**
     * Get the upload button node.
     */
    readonly uploadNode: HTMLButtonElement;
    /**
     * Get the refresh button node.
     */
    readonly refreshNode: HTMLButtonElement;
    /**
     * Create a file from a creator.
     *
     * @param creatorName - The name of the file creator.
     *
     * @returns A promise that resolves with the created widget.
     */
    createFrom(creatorName: string): Promise<Widget>;
    /**
     * Open a file by path.
     *
     * @param path - The path of the file.
     *
     * @param widgetName - The name of the widget factory to use.
     *
     * @param kernel - The kernel model to use.
     *
     * @return The widget for the path.
     */
    open(path: string, widgetName?: string, kernel?: Kernel.IModel): Widget;
    /**
     * Create a new file by path.
     *
     * @param path - The path of the file.
     *
     * @param widgetName - The name of the widget factory to use.
     *
     * @param kernel - The kernel model to use.
     *
     * @return The widget for the path.
     */
    createNew(path: string, widgetName?: string, kernel?: Kernel.IModel): Widget;
    /**
     * The 'mousedown' handler for the create button.
     */
    private _onCreateButtonPressed(event);
    /**
     * Handle a dropdwon about to close.
     */
    private _onDropDownAboutToClose(sender);
    /**
     * Handle a dropdown disposal.
     */
    private _onDropDownDisposed(sender);
    /**
     * The 'click' handler for the upload button.
     */
    private _onUploadButtonClicked(event);
    /**
     * The 'click' handler for the refresh button.
     */
    private _onRefreshButtonClicked(event);
    /**
     * The 'change' handler for the input field.
     */
    private _onInputChanged();
    private _buttons;
    private _commands;
    private _input;
    private _manager;
    private _model;
}
/**
 * The namespace for the `FileButtons` class statics.
 */
export declare namespace FileButtons {
    /**
     * An options object for initializing a file buttons widget.
     */
    interface IOptions {
        /**
         * The command registry for use with the file buttons.
         */
        commands: CommandRegistry;
        /**
         * A file browser model instance.
         */
        model: FileBrowserModel;
        /**
         * A document manager instance.
         */
        manager: DocumentManager;
    }
}

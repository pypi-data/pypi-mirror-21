import { Contents } from '@jupyterlab/services';
import { CommandRegistry } from '@phosphor/commands';
import { Widget } from '@phosphor/widgets';
import { DocumentManager } from '@jupyterlab/docmanager';
import { DirListing } from './listing';
import { FileBrowserModel } from './model';
/**
 * A widget which hosts a file browser.
 *
 * The widget uses the Jupyter Contents API to retreive contents,
 * and presents itself as a flat list of files and directories with
 * breadcrumbs.
 */
export declare class FileBrowser extends Widget {
    /**
     * Construct a new file browser.
     *
     * @param model - The file browser view model.
     */
    constructor(options: FileBrowser.IOptions);
    /**
     * Get the command registry used by the file browser.
     */
    readonly commands: CommandRegistry;
    /**
     * Get the model used by the file browser.
     */
    readonly model: FileBrowserModel;
    /**
     * Dispose of the resources held by the file browser.
     */
    dispose(): void;
    /**
     * Open the currently selected item(s).
     *
     * Changes to the first directory encountered.
     */
    open(): void;
    /**
     * Open a file by path.
     *
     * @param path - The path to of the file to open.
     *
     * @param widgetName - The name of the widget factory to use.
     *
     * @returns The widget for the file.
     */
    openPath(path: string, widgetName?: string): Widget;
    /**
     * Create a file from a creator.
     *
     * @param creatorName - The name of the widget creator.
     *
     * @returns A promise that resolves with the created widget.
     */
    createFrom(creatorName: string): Promise<Widget>;
    /**
     * Create a new untitled file in the current directory.
     *
     * @param options - The options used to create the file.
     *
     * @returns A promise that resolves with the created widget.
     */
    createNew(options: Contents.ICreateOptions): Promise<Widget>;
    /**
     * Rename the first currently selected item.
     *
     * @returns A promise that resolves with the new name of the item.
     */
    rename(): Promise<string>;
    /**
     * Cut the selected items.
     */
    cut(): void;
    /**
     * Copy the selected items.
     */
    copy(): void;
    /**
     * Paste the items from the clipboard.
     *
     * @returns A promise that resolves when the operation is complete.
     */
    paste(): Promise<void>;
    /**
     * Delete the currently selected item(s).
     *
     * @returns A promise that resolves when the operation is complete.
     */
    delete(): Promise<void>;
    /**
     * Duplicate the currently selected item(s).
     *
     * @returns A promise that resolves when the operation is complete.
     */
    duplicate(): Promise<void>;
    /**
     * Download the currently selected item(s).
     */
    download(): void;
    /**
     * Shut down kernels on the applicable currently selected items.
     *
     * @returns A promise that resolves when the operation is complete.
     */
    shutdownKernels(): Promise<void>;
    /**
     * Select next item.
     */
    selectNext(): void;
    /**
     * Select previous item.
     */
    selectPrevious(): void;
    /**
     * Find a path given a click.
     *
     * @param event - The mouse event.
     *
     * @returns The path to the selected file.
     */
    pathForClick(event: MouseEvent): string;
    /**
     * Handle a connection lost signal from the model.
     */
    private _onConnectionFailure(sender, args);
    private _buttons;
    private _commands;
    private _crumbs;
    private _listing;
    private _manager;
    private _model;
    private _showingError;
}
/**
 * The namespace for the `FileBrowser` class statics.
 */
export declare namespace FileBrowser {
    /**
     * An options object for initializing a file browser widget.
     */
    interface IOptions {
        /**
         * The command registry for use with the file browser.
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
        /**
         * An optional renderer for the directory listing area.
         *
         * The default is a shared instance of `DirListing.Renderer`.
         */
        renderer?: DirListing.IRenderer;
    }
}

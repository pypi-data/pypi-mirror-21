import { Contents, Kernel, ServiceManager, Session } from '@jupyterlab/services';
import { IIterator } from '@phosphor/algorithm';
import { IDisposable } from '@phosphor/disposable';
import { ISignal } from '@phosphor/signaling';
import { IChangedArgs } from '@jupyterlab/coreutils';
import { IPathTracker } from './tracker';
/**
 * An implementation of a file browser model.
 *
 * #### Notes
 * All paths parameters without a leading `'/'` are interpreted as relative to
 * the current directory.  Supports `'../'` syntax.
 */
export declare class FileBrowserModel implements IDisposable, IPathTracker {
    /**
     * Construct a new file browser model.
     */
    constructor(options: FileBrowserModel.IOptions);
    /**
     * A signal emitted when the path changes.
     */
    readonly pathChanged: ISignal<this, IChangedArgs<string>>;
    /**
     * A signal emitted when the directory listing is refreshed.
     */
    readonly refreshed: ISignal<this, void>;
    /**
     * A signal emitted when the running sessions in the directory changes.
     */
    readonly sessionsChanged: ISignal<this, void>;
    /**
     * Get the file path changed signal.
     */
    readonly fileChanged: ISignal<this, Contents.IChangedArgs>;
    /**
     * A signal emitted when the file browser model loses connection.
     */
    readonly connectionFailure: ISignal<this, Error>;
    /**
     * Get the current path.
     */
    readonly path: string;
    /**
     * Get the kernel spec models.
     */
    readonly specs: Kernel.ISpecModels | null;
    /**
     * Get whether the model is disposed.
     */
    readonly isDisposed: boolean;
    /**
     * Dispose of the resources held by the model.
     */
    dispose(): void;
    /**
     * Create an iterator over the model's items.
     *
     * @returns A new iterator over the model's items.
     */
    items(): IIterator<Contents.IModel>;
    /**
     * Create an iterator over the active sessions in the directory.
     *
     * @returns A new iterator over the model's active sessions.
     */
    sessions(): IIterator<Session.IModel>;
    /**
     * Force a refresh of the directory contents.
     */
    refresh(): Promise<void>;
    /**
     * Change directory.
     *
     * @param path - The path to the file or directory.
     *
     * @returns A promise with the contents of the directory.
     */
    cd(newValue?: string): Promise<void>;
    /**
     * Copy a file.
     *
     * @param fromFile - The path of the original file.
     *
     * @param toDir - The path to the target directory.
     *
     * @returns A promise which resolves to the contents of the file.
     */
    copy(fromFile: string, toDir: string): Promise<Contents.IModel>;
    /**
     * Delete a file.
     *
     * @param: path - The path to the file to be deleted.
     *
     * @returns A promise which resolves when the file is deleted.
     *
     * #### Notes
     * If there is a running session associated with the file and no other
     * sessions are using the kernel, the session will be shut down.
     */
    deleteFile(path: string): Promise<void>;
    /**
     * Download a file.
     *
     * @param - path - The path of the file to be downloaded.
     *
     * @returns A promise which resolves when the file has begun
     *   downloading.
     */
    download(path: string): Promise<void>;
    /**
     * Create a new untitled file or directory in the current directory.
     *
     * @param type - The type of file object to create. One of
     *  `['file', 'notebook', 'directory']`.
     *
     * @param ext - Optional extension for `'file'` types (defaults to `'.txt'`).
     *
     * @returns A promise containing the new file contents model.
     */
    newUntitled(options: Contents.ICreateOptions): Promise<Contents.IModel>;
    /**
     * Rename a file or directory.
     *
     * @param path - The path to the original file.
     *
     * @param newPath - The path to the new file.
     *
     * @returns A promise containing the new file contents model.  The promise
     *   will reject if the newPath already exists.  Use [[overwrite]] to
     *   overwrite a file.
     */
    rename(path: string, newPath: string): Promise<Contents.IModel>;
    /**
     * Overwrite a file.
     *
     * @param path - The path to the original file.
     *
     * @param newPath - The path to the new file.
     *
     * @returns A promise containing the new file contents model.
     */
    overwrite(path: string, newPath: string): Promise<Contents.IModel>;
    /**
     * Upload a `File` object.
     *
     * @param file - The `File` object to upload.
     *
     * @param overwrite - Whether to overwrite an existing file.
     *
     * @returns A promise containing the new file contents model.
     *
     * #### Notes
     * This will fail to upload files that are too big to be sent in one
     * request to the server.
     */
    upload(file: File, overwrite?: boolean): Promise<Contents.IModel>;
    /**
     * Shut down a session by session id.
     *
     * @param id - The id of the session.
     *
     * @returns A promise that resolves when the action is complete.
     */
    shutdown(id: string): Promise<void>;
    /**
     * Find a session associated with a path and stop it is the only
     * session using that kernel.
     */
    protected stopIfNeeded(path: string): Promise<void>;
    /**
     * Perform the actual upload.
     */
    private _upload(file);
    /**
     * Handle an updated contents model.
     */
    private _handleContents(contents);
    /**
     * Handle a change to the running sessions.
     */
    private _onRunningChanged(sender, models);
    /**
     * Handle a change on the contents manager.
     */
    private _onFileChanged(sender, change);
    /**
     * Handle internal model refresh logic.
     */
    private _scheduleUpdate();
    private _maxUploadSizeMb;
    private _manager;
    private _sessions;
    private _items;
    private _paths;
    private _model;
    private _pendingPath;
    private _pending;
    private _timeoutId;
    private _refreshId;
    private _blackoutId;
    private _requested;
    private _pathChanged;
    private _refreshed;
    private _sessionsChanged;
    private _fileChanged;
    private _connectionFailure;
}
/**
 * The namespace for the `FileBrowserModel` class statics.
 */
export declare namespace FileBrowserModel {
    /**
     * An options object for initializing a file browser.
     */
    interface IOptions {
        /**
         * A service manager instance.
         */
        manager: ServiceManager.IManager;
    }
}

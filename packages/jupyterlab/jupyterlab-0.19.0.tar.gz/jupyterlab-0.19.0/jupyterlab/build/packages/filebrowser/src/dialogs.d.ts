import { Contents } from '@jupyterlab/services';
import { Widget } from '@phosphor/widgets';
import { DocumentManager } from '@jupyterlab/docmanager';
import { FileBrowserModel } from './model';
/**
 * Create a file using a file creator.
 */
export declare function createFromDialog(model: FileBrowserModel, manager: DocumentManager, creatorName: string): Promise<Widget>;
/**
 * Open a file using a dialog.
 */
export declare function openWithDialog(path: string, manager: DocumentManager, host?: HTMLElement): Promise<Widget>;
/**
 * Create a new file using a dialog.
 */
export declare function createNewDialog(model: FileBrowserModel, manager: DocumentManager, host?: HTMLElement): Promise<Widget>;
/**
 * Rename a file with optional dialog.
 */
export declare function renameFile(model: FileBrowserModel, oldPath: string, newPath: string): Promise<Contents.IModel>;

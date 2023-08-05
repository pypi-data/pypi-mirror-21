/**
 * The class name added to FileBrowser instances.
 */
export declare const FILE_BROWSER_CLASS = "jp-FileBrowser";
/**
 * The class name added to drop targets.
 */
export declare const DROP_TARGET_CLASS = "jp-mod-dropTarget";
/**
 * The class name added to selected rows.
 */
export declare const SELECTED_CLASS = "jp-mod-selected";
/**
 * The mime type for a contents drag object.
 */
export declare const CONTENTS_MIME = "application/x-jupyter-icontents";
/**
 * An error message dialog to show in the filebrowser widget.
 */
export declare function showErrorMessage(title: string, error: Error): Promise<void>;

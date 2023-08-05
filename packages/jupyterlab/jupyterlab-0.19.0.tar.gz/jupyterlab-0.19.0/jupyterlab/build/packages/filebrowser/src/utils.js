// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var apputils_1 = require("@jupyterlab/apputils");
/**
 * The class name added to FileBrowser instances.
 */
exports.FILE_BROWSER_CLASS = 'jp-FileBrowser';
/**
 * The class name added to drop targets.
 */
exports.DROP_TARGET_CLASS = 'jp-mod-dropTarget';
/**
 * The class name added to selected rows.
 */
exports.SELECTED_CLASS = 'jp-mod-selected';
/**
 * The mime type for a contents drag object.
 */
exports.CONTENTS_MIME = 'application/x-jupyter-icontents';
/**
 * An error message dialog to show in the filebrowser widget.
 */
function showErrorMessage(title, error) {
    console.error(error);
    var options = {
        title: title,
        body: error.message || "File " + title,
        buttons: [apputils_1.Dialog.okButton()],
        okText: 'DISMISS'
    };
    return apputils_1.showDialog(options).then(function () { });
}
exports.showErrorMessage = showErrorMessage;

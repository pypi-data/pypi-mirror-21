// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var apputils_1 = require("@jupyterlab/apputils");
// The message to display to the user when prompting to trust the notebook.
var TRUST_MESSAGE = '<p>A trusted Jupyter notebook may execute hidden malicious code when you open it.<br>Selecting trust will re-render this notebook in a trusted state.<br>For more information, see the <a href="http://ipython.org/ipython-doc/2/notebook/security.html">Jupyter security documentation</a>.</p>';
/**
 * Trust the notebook after prompting the user.
 *
 * @param model - The notebook model.
 *
 * @param host - The host node for the confirmation dialog (defaults to body).
 *
 * @returns a promise that resolves when the transaction is finished.
 *
 * #### Notes
 * No dialog will be presented if the notebook is already trusted.
 */
function trustNotebook(model, host) {
    if (!model) {
        return Promise.resolve(void 0);
    }
    // Do nothing if already trusted.
    var cells = model.cells;
    var trusted = true;
    for (var i = 0; i < cells.length; i++) {
        var cell = cells.at(i);
        if (!cell.trusted) {
            trusted = false;
        }
    }
    if (trusted) {
        return apputils_1.showDialog({
            body: 'Notebook is already trusted',
            buttons: [apputils_1.Dialog.okButton()]
        }).then(function () { return void 0; });
    }
    return apputils_1.showDialog({
        body: TRUST_MESSAGE,
        title: 'Trust this notebook?',
        buttons: [apputils_1.Dialog.cancelButton(), apputils_1.Dialog.warnButton()]
    }).then(function (result) {
        if (result.accept) {
            for (var i = 0; i < cells.length; i++) {
                var cell = cells.at(i);
                cell.trusted = true;
            }
        }
    });
}
exports.trustNotebook = trustNotebook;

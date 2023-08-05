// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var apputils_1 = require("@jupyterlab/apputils");
/**
 * The command IDs used by the application plugin.
 */
var CommandIDs;
(function (CommandIDs) {
    CommandIDs.closeAll = 'main-jupyterlab:close-all';
    CommandIDs.activateNextTab = 'main-jupyterlab:activate-next-tab';
    CommandIDs.activatePreviousTab = 'main-jupyterlab:activate-previous-tab';
})(CommandIDs || (CommandIDs = {}));
;
/**
 * The main extension.
 */
var plugin = {
    id: 'jupyter.extensions.main',
    requires: [apputils_1.ICommandPalette],
    activate: function (app, palette) {
        var command = CommandIDs.closeAll;
        app.commands.addCommand(command, {
            label: 'Close All Widgets',
            execute: function () { app.shell.closeAll(); }
        });
        palette.addItem({ command: command, category: 'Main Area' });
        command = CommandIDs.activateNextTab;
        app.commands.addCommand(command, {
            label: 'Activate Next Tab',
            execute: function () { app.shell.activateNextTab(); }
        });
        palette.addItem({ command: command, category: 'Main Area' });
        command = CommandIDs.activatePreviousTab;
        app.commands.addCommand(command, {
            label: 'Activate Previous Tab',
            execute: function () { app.shell.activatePreviousTab(); }
        });
        palette.addItem({ command: command, category: 'Main Area' });
        var message = 'Are you sure you want to exit JupyterLab?\n' +
            'Any unsaved changes will be lost.';
        // The spec for the `beforeunload` event is implemented differently by
        // the different browser vendors. Consequently, the `event.returnValue`
        // attribute needs to set in addition to a return value being returned.
        // For more information, see:
        // https://developer.mozilla.org/en/docs/Web/Events/beforeunload
        window.addEventListener('beforeunload', function (event) {
            return event.returnValue = message;
        });
    },
    autoStart: true
};
/**
 * Export the plugin as default.
 */
exports.default = plugin;

// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var services_1 = require("@jupyterlab/services");
var apputils_1 = require("@jupyterlab/apputils");
var filebrowser_1 = require("@jupyterlab/filebrowser");
var launcher_1 = require("@jupyterlab/launcher");
/**
 * The command IDs used by the launcher plugin.
 */
var CommandIDs;
(function (CommandIDs) {
    CommandIDs.show = 'launcher-jupyterlab:show';
})(CommandIDs || (CommandIDs = {}));
;
/**
 * A service providing an interface to the the launcher.
 */
var plugin = {
    activate: activate,
    id: 'jupyter.services.launcher',
    requires: [
        services_1.IServiceManager,
        filebrowser_1.IPathTracker,
        apputils_1.ICommandPalette,
        apputils_1.ICommandLinker,
        apputils_1.ILayoutRestorer
    ],
    provides: launcher_1.ILauncher,
    autoStart: true
};
/**
 * Export the plugin as default.
 */
exports.default = plugin;
/**
 * Activate the launcher.
 */
function activate(app, services, pathTracker, palette, linker, restorer) {
    var commands = app.commands, shell = app.shell;
    var model = new launcher_1.LauncherModel();
    // Set launcher path and track the path as it changes.
    model.path = pathTracker.path;
    pathTracker.pathChanged.connect(function () { model.path = pathTracker.path; });
    var widget = new launcher_1.LauncherWidget({ linker: linker });
    widget.model = model;
    widget.id = 'launcher';
    widget.title.label = 'Launcher';
    // Let the application restorer track the launcher for restoration of
    // application state (e.g. setting the launcher as the current side bar
    // widget).
    restorer.add(widget, 'launcher');
    commands.addCommand(CommandIDs.show, {
        label: 'Show Launcher',
        execute: function () {
            if (!widget.isAttached) {
                shell.addToLeftArea(widget);
            }
            shell.activateById(widget.id);
        }
    });
    palette.addItem({ command: CommandIDs.show, category: 'Help' });
    shell.addToLeftArea(widget);
    return model;
}

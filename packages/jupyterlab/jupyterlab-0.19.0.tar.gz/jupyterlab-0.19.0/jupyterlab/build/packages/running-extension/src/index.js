// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var apputils_1 = require("@jupyterlab/apputils");
var services_1 = require("@jupyterlab/services");
var running_1 = require("@jupyterlab/running");
/**
 * The default running sessions extension.
 */
var plugin = {
    activate: activate,
    id: 'jupyter.extensions.running-sessions',
    requires: [services_1.IServiceManager, apputils_1.ILayoutRestorer],
    autoStart: true
};
/**
 * Export the plugin as default.
 */
exports.default = plugin;
/**
 * Activate the running plugin.
 */
function activate(app, services, restorer) {
    var running = new running_1.RunningSessions({ manager: services });
    running.id = 'jp-running-sessions';
    running.title.label = 'Running';
    // Let the application restorer track the running panel for restoration of
    // application state (e.g. setting the running panel as the current side bar
    // widget).
    restorer.add(running, 'running-sessions');
    running.sessionOpenRequested.connect(function (sender, model) {
        var path = model.notebook.path;
        var name = path.split('/').pop();
        if (running_1.CONSOLE_REGEX.test(name)) {
            app.commands.execute('console:open', { id: model.id });
        }
        else {
            app.commands.execute('file-operations:open', { path: path });
        }
    });
    running.terminalOpenRequested.connect(function (sender, model) {
        app.commands.execute('terminal:open', { name: model.name });
    });
    // Rank has been chosen somewhat arbitrarily to give priority to the running
    // sessions widget in the sidebar.
    app.shell.addToLeftArea(running, { rank: 50 });
}

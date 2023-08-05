// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var services_1 = require("@jupyterlab/services");
var apputils_1 = require("@jupyterlab/apputils");
var filebrowser_1 = require("@jupyterlab/filebrowser");
var widget_1 = require("./widget");
/**
 * The command IDs used by the landing plugin.
 */
var CommandIDs;
(function (CommandIDs) {
    CommandIDs.open = 'landing-jupyterlab:open';
})(CommandIDs || (CommandIDs = {}));
;
/**
 * The class name added to the landing plugin.
 */
var LANDING_CLASS = 'jp-Landing';
/**
 * The landing page extension.
 */
var plugin = {
    activate: activate,
    id: 'jupyter.extensions.landing',
    requires: [filebrowser_1.IPathTracker, apputils_1.ICommandPalette, services_1.IServiceManager, apputils_1.ILayoutRestorer],
    autoStart: true
};
/**
 * Export the plugin as default.
 */
exports.default = plugin;
/**
 * Activate the landing plugin.
 */
function activate(app, pathTracker, palette, services, restorer) {
    var commands = app.commands, shell = app.shell;
    var category = 'Help';
    var command = CommandIDs.open;
    var model = new widget_1.LandingModel(services.terminals.isAvailable());
    var tracker = new apputils_1.InstanceTracker({
        namespace: 'landing',
        shell: shell
    });
    // Handle state restoration.
    restorer.restore(tracker, {
        command: command,
        args: function () { return null; },
        name: function () { return 'landing'; }
    });
    var widget;
    function newWidget() {
        var widget = new widget_1.LandingWidget(app);
        widget.model = model;
        widget.id = 'landing-jupyterlab';
        widget.title.label = 'Landing';
        widget.title.closable = true;
        widget.addClass(LANDING_CLASS);
        tracker.add(widget);
        return widget;
    }
    commands.addCommand(command, {
        label: 'Open Landing',
        execute: function () {
            if (!widget || widget.isDisposed) {
                widget = newWidget();
                shell.addToMainArea(widget);
            }
            tracker.activate(widget);
        }
    });
    pathTracker.pathChanged.connect(function () {
        if (pathTracker.path.length) {
            model.path = 'home > ' + pathTracker.path.replace('/', ' > ');
        }
        else {
            model.path = 'home';
        }
    });
    palette.addItem({ category: category, command: command });
    // Only create a landing page if there are no other tabs open.
    app.restored.then(function () {
        if (shell.isEmpty('main')) {
            commands.execute(command, void 0);
        }
    });
}

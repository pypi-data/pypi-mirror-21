// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var apputils_1 = require("@jupyterlab/apputils");
var widget_1 = require("./widget");
/**
 * The command IDs used by the about plugin.
 */
var CommandIDs;
(function (CommandIDs) {
    CommandIDs.open = 'about-jupyterlab:open';
})(CommandIDs || (CommandIDs = {}));
/**
 * The about page extension.
 */
var plugin = {
    activate: activate,
    id: 'jupyter.extensions.about',
    autoStart: true,
    requires: [apputils_1.ICommandPalette, apputils_1.ILayoutRestorer]
};
/**
 * Export the plugin as default.
 */
exports.default = plugin;
function activate(app, palette, restorer) {
    var namespace = 'about-jupyterlab';
    var model = new widget_1.AboutModel({ version: app.info.version });
    var command = CommandIDs.open;
    var category = 'Help';
    var shell = app.shell, commands = app.commands;
    var tracker = new apputils_1.InstanceTracker({ namespace: namespace, shell: shell });
    restorer.restore(tracker, {
        command: command,
        args: function () { return null; },
        name: function () { return 'about'; }
    });
    var widget;
    function newWidget() {
        var widget = new widget_1.AboutWidget();
        widget.model = model;
        widget.id = 'about';
        widget.title.label = 'About';
        widget.title.closable = true;
        tracker.add(widget);
        return widget;
    }
    commands.addCommand(command, {
        label: 'About JupyterLab',
        execute: function () {
            if (!widget || widget.isDisposed) {
                widget = newWidget();
                shell.addToMainArea(widget);
            }
            tracker.activate(widget);
        }
    });
    palette.addItem({ command: command, category: category });
}

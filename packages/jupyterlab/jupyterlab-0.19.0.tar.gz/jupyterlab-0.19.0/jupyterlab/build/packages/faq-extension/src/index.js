// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var apputils_1 = require("@jupyterlab/apputils");
var widget_1 = require("./widget");
/**
 * The command IDs used by the FAQ plugin.
 */
var CommandIDs;
(function (CommandIDs) {
    CommandIDs.open = 'faq-jupyterlab:open';
})(CommandIDs || (CommandIDs = {}));
;
/**
 * The FAQ page extension.
 */
var plugin = {
    activate: activate,
    id: 'jupyter.extensions.faq',
    requires: [apputils_1.ICommandPalette, apputils_1.ICommandLinker, apputils_1.ILayoutRestorer],
    autoStart: true
};
/**
 * Export the plugin as default.
 */
exports.default = plugin;
/**
 * Activate the FAQ plugin.
 */
function activate(app, palette, linker, restorer) {
    var category = 'Help';
    var command = CommandIDs.open;
    var model = new widget_1.FaqModel();
    var commands = app.commands, shell = app.shell;
    var tracker = new apputils_1.InstanceTracker({ namespace: 'faq', shell: shell });
    // Handle state restoration.
    restorer.restore(tracker, {
        command: command,
        args: function () { return null; },
        name: function () { return 'faq'; }
    });
    var widget;
    function newWidget() {
        var widget = new widget_1.FaqWidget({ linker: linker });
        widget.model = model;
        widget.id = 'faq';
        widget.title.label = 'FAQ';
        widget.title.closable = true;
        tracker.add(widget);
        return widget;
    }
    commands.addCommand(command, {
        label: 'Open FAQ',
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

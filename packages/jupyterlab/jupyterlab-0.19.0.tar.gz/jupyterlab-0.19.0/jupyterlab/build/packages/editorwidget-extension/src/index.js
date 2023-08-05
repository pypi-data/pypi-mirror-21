// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var apputils_1 = require("@jupyterlab/apputils");
var codeeditor_1 = require("@jupyterlab/codeeditor");
var docregistry_1 = require("@jupyterlab/docregistry");
var editorwidget_1 = require("@jupyterlab/editorwidget");
var launcher_1 = require("@jupyterlab/launcher");
/**
 * The class name for the text editor icon from the default theme.
 */
var EDITOR_ICON_CLASS = 'jp-ImageTextEditor';
/**
 * The name of the factory that creates editor widgets.
 */
var FACTORY = 'Editor';
/**
 * The editor tracker extension.
 */
var plugin = {
    activate: activate,
    id: 'jupyter.services.editor-tracker',
    requires: [docregistry_1.IDocumentRegistry, apputils_1.ILayoutRestorer, codeeditor_1.IEditorServices],
    optional: [launcher_1.ILauncher],
    provides: editorwidget_1.IEditorTracker,
    autoStart: true
};
/**
 * Export the plugins as default.
 */
exports.default = plugin;
/**
 * Activate the editor tracker plugin.
 */
function activate(app, registry, restorer, editorServices, launcher) {
    var factory = new editorwidget_1.EditorWidgetFactory({
        editorServices: editorServices,
        factoryOptions: {
            name: FACTORY,
            fileExtensions: ['*'],
            defaultFor: ['*']
        }
    });
    var shell = app.shell;
    var tracker = new apputils_1.InstanceTracker({
        namespace: 'editor',
        shell: shell
    });
    // Handle state restoration.
    restorer.restore(tracker, {
        command: 'file-operations:open',
        args: function (widget) { return ({ path: widget.context.path, factory: FACTORY }); },
        name: function (widget) { return widget.context.path; }
    });
    factory.widgetCreated.connect(function (sender, widget) {
        widget.title.icon = EDITOR_ICON_CLASS;
        // Notify the instance tracker if restore data needs to update.
        widget.context.pathChanged.connect(function () { tracker.save(widget); });
        tracker.add(widget);
    });
    registry.addWidgetFactory(factory);
    editorwidget_1.addDefaultCommands(tracker, app.commands);
    // Add a launcher item if the launcher is available.
    if (launcher) {
        launcher.add({
            name: 'Text Editor',
            command: 'file-operations:new-text-file'
        });
    }
    return tracker;
}

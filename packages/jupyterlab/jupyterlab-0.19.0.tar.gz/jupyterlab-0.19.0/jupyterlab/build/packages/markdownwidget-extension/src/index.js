// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var apputils_1 = require("@jupyterlab/apputils");
var docregistry_1 = require("@jupyterlab/docregistry");
var rendermime_1 = require("@jupyterlab/rendermime");
var markdownwidget_1 = require("@jupyterlab/markdownwidget");
/**
 * The class name for the text editor icon from the default theme.
 */
var TEXTEDITOR_ICON_CLASS = 'jp-ImageTextEditor';
/**
 * The name of the factory that creates markdown widgets.
 */
var FACTORY = 'Rendered Markdown';
/**
 * The markdown handler extension.
 */
var plugin = {
    activate: activate,
    id: 'jupyter.extensions.rendered-markdown',
    requires: [docregistry_1.IDocumentRegistry, rendermime_1.IRenderMime, apputils_1.ILayoutRestorer],
    autoStart: true
};
/**
 * Activate the markdown plugin.
 */
function activate(app, registry, rendermime, restorer) {
    var factory = new markdownwidget_1.MarkdownWidgetFactory({
        name: FACTORY,
        fileExtensions: ['.md'],
        rendermime: rendermime
    });
    var shell = app.shell;
    var namespace = 'rendered-markdown';
    var tracker = new apputils_1.InstanceTracker({ namespace: namespace, shell: shell });
    // Handle state restoration.
    restorer.restore(tracker, {
        command: 'file-operations:open',
        args: function (widget) { return ({ path: widget.context.path, factory: FACTORY }); },
        name: function (widget) { return widget.context.path; }
    });
    factory.widgetCreated.connect(function (sender, widget) {
        widget.title.icon = TEXTEDITOR_ICON_CLASS;
        // Notify the instance tracker if restore data needs to update.
        widget.context.pathChanged.connect(function () { tracker.save(widget); });
        tracker.add(widget);
    });
    registry.addWidgetFactory(factory);
}
/**
 * Export the plugin as default.
 */
exports.default = plugin;

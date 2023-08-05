// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var apputils_1 = require("@jupyterlab/apputils");
var csvwidget_1 = require("@jupyterlab/csvwidget");
var docregistry_1 = require("@jupyterlab/docregistry");
/**
 * The name of the factory that creates CSV widgets.
 */
var FACTORY = 'Table';
/**
 * The table file handler extension.
 */
var plugin = {
    activate: activate,
    id: 'jupyter.extensions.csv-handler',
    requires: [docregistry_1.IDocumentRegistry, apputils_1.ILayoutRestorer],
    autoStart: true
};
/**
 * Export the plugin as default.
 */
exports.default = plugin;
/**
 * Activate the table widget extension.
 */
function activate(app, registry, restorer) {
    var factory = new csvwidget_1.CSVWidgetFactory({
        name: FACTORY,
        fileExtensions: ['.csv'],
        defaultFor: ['.csv']
    });
    var tracker = new apputils_1.InstanceTracker({
        namespace: 'csvwidget',
        shell: app.shell
    });
    // Handle state restoration.
    restorer.restore(tracker, {
        command: 'file-operations:open',
        args: function (widget) { return ({ path: widget.context.path, factory: FACTORY }); },
        name: function (widget) { return widget.context.path; }
    });
    registry.addWidgetFactory(factory);
    factory.widgetCreated.connect(function (sender, widget) {
        // Track the widget.
        tracker.add(widget);
        // Notify the instance tracker if restore data needs to update.
        widget.context.pathChanged.connect(function () { tracker.save(widget); });
    });
}

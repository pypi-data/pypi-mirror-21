// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var apputils_1 = require("@jupyterlab/apputils");
var docregistry_1 = require("@jupyterlab/docregistry");
var imagewidget_1 = require("@jupyterlab/imagewidget");
/**
 * The command IDs used by the image widget plugin.
 */
var CommandIDs;
(function (CommandIDs) {
    CommandIDs.zoomIn = 'imagewidget:zoom-in';
    CommandIDs.zoomOut = 'imagewidget:zoom-out';
    CommandIDs.resetZoom = 'imagewidget:reset-zoom';
})(CommandIDs || (CommandIDs = {}));
;
/**
 * The list of file extensions for images.
 */
var EXTENSIONS = ['.png', '.gif', '.jpeg', '.jpg', '.svg', '.bmp', '.ico',
    '.xbm', '.tiff', '.tif'];
/**
 * The name of the factory that creates image widgets.
 */
var FACTORY = 'Image';
/**
 * The image file handler extension.
 */
var plugin = {
    activate: activate,
    id: 'jupyter.extensions.image-handler',
    provides: imagewidget_1.IImageTracker,
    requires: [docregistry_1.IDocumentRegistry, apputils_1.ICommandPalette, apputils_1.ILayoutRestorer],
    autoStart: true
};
/**
 * Export the plugin as default.
 */
exports.default = plugin;
/**
 * Activate the image widget extension.
 */
function activate(app, registry, palette, restorer) {
    var namespace = 'image-widget';
    var factory = new imagewidget_1.ImageWidgetFactory({
        name: FACTORY,
        modelName: 'base64',
        fileExtensions: EXTENSIONS,
        defaultFor: EXTENSIONS
    });
    var shell = app.shell;
    var tracker = new apputils_1.InstanceTracker({ namespace: namespace, shell: shell });
    // Handle state restoration.
    restorer.restore(tracker, {
        command: 'file-operations:open',
        args: function (widget) { return ({ path: widget.context.path, factory: FACTORY }); },
        name: function (widget) { return widget.context.path; }
    });
    registry.addWidgetFactory(factory);
    factory.widgetCreated.connect(function (sender, widget) {
        // Notify the instance tracker if restore data needs to update.
        widget.context.pathChanged.connect(function () { tracker.save(widget); });
        tracker.add(widget);
    });
    var category = 'Image Widget';
    [CommandIDs.zoomIn, CommandIDs.zoomOut, CommandIDs.resetZoom]
        .forEach(function (command) { palette.addItem({ command: command, category: category }); });
    return tracker;
}

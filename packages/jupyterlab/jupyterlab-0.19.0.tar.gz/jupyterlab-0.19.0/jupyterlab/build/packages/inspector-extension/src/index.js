// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var apputils_1 = require("@jupyterlab/apputils");
var console_1 = require("@jupyterlab/console");
var inspector_1 = require("@jupyterlab/inspector");
var notebook_1 = require("@jupyterlab/notebook");
var manager_1 = require("./manager");
/**
 * The command IDs used by the inspector plugin.
 */
var CommandIDs;
(function (CommandIDs) {
    CommandIDs.open = 'inspector:open';
})(CommandIDs || (CommandIDs = {}));
;
/**
 * A service providing code introspection.
 */
var service = {
    id: 'jupyter.services.inspector',
    requires: [apputils_1.ICommandPalette, apputils_1.ILayoutRestorer],
    provides: inspector_1.IInspector,
    autoStart: true,
    activate: function (app, palette, restorer) {
        var commands = app.commands, shell = app.shell;
        var manager = new manager_1.InspectorManager();
        var category = 'Inspector';
        var command = CommandIDs.open;
        var label = 'Open Inspector';
        var tracker = new apputils_1.InstanceTracker({
            namespace: 'inspector',
            shell: shell
        });
        /**
         * Create and track a new inspector.
         */
        function newInspectorPanel() {
            var inspector = new inspector_1.InspectorPanel();
            inspector.id = 'jp-inspector';
            inspector.title.label = 'Inspector';
            inspector.title.closable = true;
            inspector.disposed.connect(function () {
                if (manager.inspector === inspector) {
                    manager.inspector = null;
                }
            });
            // Track the inspector.
            tracker.add(inspector);
            // Add the default inspector child items.
            Private.defaultInspectorItems.forEach(function (item) { inspector.add(item); });
            return inspector;
        }
        // Handle state restoration.
        restorer.restore(tracker, {
            command: command,
            args: function () { return null; },
            name: function () { return 'inspector'; }
        });
        // Add command to registry and palette.
        commands.addCommand(command, {
            label: label,
            execute: function () {
                if (!manager.inspector || manager.inspector.isDisposed) {
                    manager.inspector = newInspectorPanel();
                    shell.addToMainArea(manager.inspector);
                }
                if (manager.inspector.isAttached) {
                    tracker.activate(manager.inspector);
                }
            }
        });
        palette.addItem({ command: command, category: category });
        return manager;
    }
};
/**
 * An extension that registers consoles for inspection.
 */
var consolePlugin = {
    id: 'jupyter.extensions.console-inspector',
    requires: [inspector_1.IInspector, console_1.IConsoleTracker],
    autoStart: true,
    activate: function (app, manager, consoles) {
        // Maintain association of new consoles with their respective handlers.
        var handlers = {};
        // Create a handler for each console that is created.
        consoles.widgetAdded.connect(function (sender, parent) {
            var session = parent.console.session;
            var rendermime = parent.console.rendermime;
            var handler = new inspector_1.InspectionHandler({ session: session, rendermime: rendermime });
            // Associate the handler to the widget.
            handlers[parent.id] = handler;
            // Set the initial editor.
            var cell = parent.console.prompt;
            handler.editor = cell && cell.editor;
            // Listen for prompt creation.
            parent.console.promptCreated.connect(function (sender, cell) {
                handler.editor = cell && cell.editor;
            });
            // Listen for parent disposal.
            parent.disposed.connect(function () {
                delete handlers[parent.id];
                handler.dispose();
            });
        });
        // Keep track of console instances and set inspector source.
        app.shell.currentChanged.connect(function (sender, args) {
            var widget = args.newValue;
            if (!widget || !consoles.has(widget)) {
                return;
            }
            var source = handlers[widget.id];
            if (source) {
                manager.source = source;
            }
        });
    }
};
/**
 * An extension that registers notebooks for inspection.
 */
var notebookPlugin = {
    id: 'jupyter.extensions.notebook-inspector',
    requires: [inspector_1.IInspector, notebook_1.INotebookTracker],
    autoStart: true,
    activate: function (app, manager, notebooks) {
        // Maintain association of new notebooks with their respective handlers.
        var handlers = {};
        // Create a handler for each notebook that is created.
        notebooks.widgetAdded.connect(function (sender, parent) {
            var session = parent.session;
            var rendermime = parent.rendermime;
            var handler = new inspector_1.InspectionHandler({ session: session, rendermime: rendermime });
            // Associate the handler to the widget.
            handlers[parent.id] = handler;
            // Set the initial editor.
            var cell = parent.notebook.activeCell;
            handler.editor = cell && cell.editor;
            // Listen for active cell changes.
            parent.notebook.activeCellChanged.connect(function (sender, cell) {
                handler.editor = cell && cell.editor;
            });
            // Listen for parent disposal.
            parent.disposed.connect(function () {
                delete handlers[parent.id];
                handler.dispose();
            });
        });
        // Keep track of notebook instances and set inspector source.
        app.shell.currentChanged.connect(function (sender, args) {
            var widget = args.newValue;
            if (!widget || !notebooks.has(widget)) {
                return;
            }
            var source = handlers[widget.id];
            if (source) {
                manager.source = source;
            }
        });
    }
};
/**
 * Export the plugins as default.
 */
var plugins = [
    service, consolePlugin, notebookPlugin
];
exports.default = plugins;
/**
 * A namespace for private data.
 */
var Private;
(function (Private) {
    /**
     * The default set of inspector items added to the inspector panel.
     */
    Private.defaultInspectorItems = [
        {
            className: 'jp-HintsInspectorItem',
            name: 'Hints',
            rank: 20,
            type: 'hints'
        }
    ];
})(Private || (Private = {}));

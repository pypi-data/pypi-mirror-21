// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var widgets_1 = require("@phosphor/widgets");
var completer_1 = require("@jupyterlab/completer");
var console_1 = require("@jupyterlab/console");
var notebook_1 = require("@jupyterlab/notebook");
/**
 * The command IDs used by the completer plugin.
 */
var CommandIDs;
(function (CommandIDs) {
    CommandIDs.invoke = 'completer:invoke';
    CommandIDs.invokeConsole = 'completer:invoke-console';
    CommandIDs.invokeNotebook = 'completer:invoke-notebook';
    CommandIDs.select = 'completer:select';
    CommandIDs.selectConsole = 'completer:select-console';
    CommandIDs.selectNotebook = 'completer:select-notebook';
})(CommandIDs || (CommandIDs = {}));
/**
 * A service providing code completion for editors.
 */
var service = {
    id: 'jupyter.services.completer',
    autoStart: true,
    provides: completer_1.ICompletionManager,
    activate: function (app) {
        var handlers = {};
        app.commands.addCommand(CommandIDs.invoke, {
            execute: function (args) {
                var id = args && args['id'];
                if (!id) {
                    return;
                }
                var handler = handlers[id];
                if (handler) {
                    handler.invoke();
                }
            }
        });
        app.commands.addCommand(CommandIDs.select, {
            execute: function (args) {
                var id = args && args['id'];
                if (!id) {
                    return;
                }
                var handler = handlers[id];
                if (handler) {
                    handler.completer.selectActive();
                }
            }
        });
        return {
            register: function (completable) {
                var editor = completable.editor, session = completable.session, parent = completable.parent;
                var model = new completer_1.CompleterModel();
                var completer = new completer_1.CompleterWidget({ editor: editor, model: model });
                var handler = new completer_1.CompletionHandler({ completer: completer, session: session });
                var id = parent.id;
                // Hide the widget when it first loads.
                completer.hide();
                // Associate the handler with the parent widget.
                handlers[id] = handler;
                // Set the handler's editor.
                handler.editor = editor;
                // Attach the completer widget.
                widgets_1.Widget.attach(completer, document.body);
                // Listen for parent disposal.
                parent.disposed.connect(function () {
                    delete handlers[id];
                    model.dispose();
                    completer.dispose();
                    handler.dispose();
                });
                return handler;
            }
        };
    }
};
/**
 * An extension that registers consoles for code completion.
 */
var consolePlugin = {
    id: 'jupyter.extensions.console-completer',
    requires: [completer_1.ICompletionManager, console_1.IConsoleTracker],
    autoStart: true,
    activate: function (app, manager, consoles) {
        // Create a handler for each console that is created.
        consoles.widgetAdded.connect(function (sender, panel) {
            var anchor = panel.console;
            var cell = anchor.prompt;
            var editor = cell && cell.editor;
            var session = anchor.session;
            var parent = panel;
            var handler = manager.register({ editor: editor, session: session, parent: parent });
            // Listen for prompt creation.
            anchor.promptCreated.connect(function (sender, cell) {
                handler.editor = cell && cell.editor;
            });
        });
        // Add console completer invoke command.
        app.commands.addCommand(CommandIDs.invokeConsole, {
            execute: function () {
                var id = consoles.currentWidget && consoles.currentWidget.id;
                if (!id) {
                    return;
                }
                return app.commands.execute(CommandIDs.invoke, { id: id });
            }
        });
        // Add console completer select command.
        app.commands.addCommand(CommandIDs.selectConsole, {
            execute: function () {
                var id = consoles.currentWidget && consoles.currentWidget.id;
                if (!id) {
                    return;
                }
                return app.commands.execute(CommandIDs.select, { id: id });
            }
        });
        // Set enter key for console completer select command.
        app.commands.addKeyBinding({
            command: CommandIDs.selectConsole,
            keys: ['Enter'],
            selector: ".jp-ConsolePanel .jp-mod-completer-active"
        });
    }
};
/**
 * An extension that registers notebooks for code completion.
 */
var notebookPlugin = {
    id: 'jupyter.extensions.notebook-completer',
    requires: [completer_1.ICompletionManager, notebook_1.INotebookTracker],
    autoStart: true,
    activate: function (app, manager, notebooks) {
        // Create a handler for each notebook that is created.
        notebooks.widgetAdded.connect(function (sender, panel) {
            var cell = panel.notebook.activeCell;
            var editor = cell && cell.editor;
            var session = panel.session;
            var parent = panel;
            var handler = manager.register({ editor: editor, session: session, parent: parent });
            // Listen for active cell changes.
            panel.notebook.activeCellChanged.connect(function (sender, cell) {
                handler.editor = cell && cell.editor;
            });
        });
        // Add notebook completer command.
        app.commands.addCommand(CommandIDs.invokeNotebook, {
            execute: function () {
                var id = notebooks.currentWidget && notebooks.currentWidget.id;
                return app.commands.execute(CommandIDs.invoke, { id: id });
            }
        });
        // Add notebook completer select command.
        app.commands.addCommand(CommandIDs.selectNotebook, {
            execute: function () {
                var id = notebooks.currentWidget && notebooks.currentWidget.id;
                if (!id) {
                    return;
                }
                return app.commands.execute(CommandIDs.select, { id: id });
            }
        });
        // Set enter key for notebook completer select command.
        app.commands.addKeyBinding({
            command: CommandIDs.selectNotebook,
            keys: ['Enter'],
            selector: ".jp-Notebook .jp-mod-completer-active"
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

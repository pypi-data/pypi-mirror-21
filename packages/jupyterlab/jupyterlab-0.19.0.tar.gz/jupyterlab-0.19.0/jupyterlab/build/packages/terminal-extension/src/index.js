// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var services_1 = require("@jupyterlab/services");
var widgets_1 = require("@phosphor/widgets");
var apputils_1 = require("@jupyterlab/apputils");
var launcher_1 = require("@jupyterlab/launcher");
var terminal_1 = require("@jupyterlab/terminal");
/**
 * The command IDs used by the terminal plugin.
 */
var CommandIDs;
(function (CommandIDs) {
    CommandIDs.createNew = 'terminal:create-new';
    CommandIDs.open = 'terminal:open';
    CommandIDs.refresh = 'terminal:refresh';
    CommandIDs.increaseFont = 'terminal:increase-font';
    CommandIDs.decreaseFont = 'terminal:decrease-font';
    CommandIDs.toggleTheme = 'terminal:toggle-theme';
})(CommandIDs || (CommandIDs = {}));
;
/**
 * The class name for the terminal icon in the default theme.
 */
var TERMINAL_ICON_CLASS = 'jp-ImageTerminal';
/**
 * The default terminal extension.
 */
var plugin = {
    activate: activate,
    id: 'jupyter.extensions.terminal',
    provides: terminal_1.ITerminalTracker,
    requires: [
        services_1.IServiceManager, apputils_1.IMainMenu, apputils_1.ICommandPalette, apputils_1.ILayoutRestorer
    ],
    optional: [launcher_1.ILauncher],
    autoStart: true
};
/**
 * Export the plugin as default.
 */
exports.default = plugin;
/**
 * Activate the terminal plugin.
 */
function activate(app, services, mainMenu, palette, restorer, launcher) {
    // Bail if there are no terminals available.
    if (!services.terminals.isAvailable()) {
        console.log('Disabling terminals plugin because they are not available on the server');
        return;
    }
    var commands = app.commands, shell = app.shell;
    var category = 'Terminal';
    var namespace = 'terminal';
    var tracker = new apputils_1.InstanceTracker({ namespace: namespace, shell: shell });
    // Handle state restoration.
    restorer.restore(tracker, {
        command: CommandIDs.createNew,
        args: function (widget) { return ({ name: widget.session.name }); },
        name: function (widget) { return widget.session && widget.session.name; }
    });
    terminal_1.addDefaultCommands(tracker, commands);
    // Add terminal commands.
    commands.addCommand(CommandIDs.createNew, {
        label: 'New Terminal',
        caption: 'Start a new terminal session',
        execute: function (args) {
            var name = args ? args['name'] : '';
            var term = new terminal_1.TerminalWidget();
            term.title.closable = true;
            term.title.icon = TERMINAL_ICON_CLASS;
            term.title.label = '...';
            shell.addToMainArea(term);
            var promise = name ?
                services.terminals.connectTo(name)
                : services.terminals.startNew();
            return promise.then(function (session) {
                term.session = session;
                tracker.add(term);
                tracker.activate(term);
            }).catch(function () { term.dispose(); });
        }
    });
    commands.addCommand(CommandIDs.open, {
        execute: function (args) {
            var name = args['name'];
            // Check for a running terminal with the given name.
            var widget = tracker.find(function (value) { return value.session.name === name; });
            if (widget) {
                tracker.activate(widget);
            }
            else {
                // Otherwise, create a new terminal with a given name.
                return commands.execute(CommandIDs.createNew, { name: name });
            }
        }
    });
    commands.addCommand(CommandIDs.refresh, {
        label: 'Refresh Terminal',
        caption: 'Refresh the current terminal session',
        execute: function () {
            var current = tracker.currentWidget;
            if (!current) {
                return;
            }
            tracker.activate(current);
            return current.refresh().then(function () {
                current.activate();
            });
        }
    });
    // Add command palette and menu items.
    var menu = new widgets_1.Menu({ commands: commands });
    menu.title.label = category;
    [
        CommandIDs.createNew,
        CommandIDs.refresh,
        CommandIDs.increaseFont,
        CommandIDs.decreaseFont,
        CommandIDs.toggleTheme
    ].forEach(function (command) {
        palette.addItem({ command: command, category: category });
        menu.addItem({ command: command });
    });
    mainMenu.addMenu(menu, { rank: 40 });
    // Add a launcher item if the launcher is available.
    if (launcher) {
        launcher.add({
            name: 'Terminal',
            command: CommandIDs.createNew
        });
    }
    return tracker;
}

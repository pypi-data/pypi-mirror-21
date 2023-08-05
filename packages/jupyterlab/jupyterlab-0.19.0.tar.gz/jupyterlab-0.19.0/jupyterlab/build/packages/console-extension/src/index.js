// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
"use strict";
var __assign = (this && this.__assign) || Object.assign || function(t) {
    for (var s, i = 1, n = arguments.length; i < n; i++) {
        s = arguments[i];
        for (var p in s) if (Object.prototype.hasOwnProperty.call(s, p))
            t[p] = s[p];
    }
    return t;
};
Object.defineProperty(exports, "__esModule", { value: true });
var services_1 = require("@jupyterlab/services");
var algorithm_1 = require("@phosphor/algorithm");
var widgets_1 = require("@phosphor/widgets");
var apputils_1 = require("@jupyterlab/apputils");
var codeeditor_1 = require("@jupyterlab/codeeditor");
var console_1 = require("@jupyterlab/console");
var filebrowser_1 = require("@jupyterlab/filebrowser");
var launcher_1 = require("@jupyterlab/launcher");
var rendermime_1 = require("@jupyterlab/rendermime");
/**
 * The command IDs used by the console plugin.
 */
var CommandIDs;
(function (CommandIDs) {
    CommandIDs.create = 'console:create';
    CommandIDs.clear = 'console:clear';
    CommandIDs.run = 'console:run';
    CommandIDs.runForced = 'console:run-forced';
    CommandIDs.linebreak = 'console:linebreak';
    CommandIDs.interrupt = 'console:interrupt-kernel';
    CommandIDs.restart = 'console:restart-kernel';
    CommandIDs.closeAndShutdown = 'console:close-and-shutdown';
    CommandIDs.open = 'console:open';
    CommandIDs.inject = 'console:inject';
    CommandIDs.switchKernel = 'console:switch-kernel';
})(CommandIDs || (CommandIDs = {}));
;
/**
 * The console widget tracker provider.
 */
exports.trackerPlugin = {
    id: 'jupyter.services.console-tracker',
    provides: console_1.IConsoleTracker,
    requires: [
        services_1.IServiceManager,
        rendermime_1.IRenderMime,
        apputils_1.IMainMenu,
        apputils_1.ICommandPalette,
        filebrowser_1.IPathTracker,
        console_1.ConsolePanel.IContentFactory,
        codeeditor_1.IEditorServices,
        apputils_1.ILayoutRestorer
    ],
    optional: [launcher_1.ILauncher],
    activate: activateConsole,
    autoStart: true
};
/**
 * The console widget content factory.
 */
exports.contentFactoryPlugin = {
    id: 'jupyter.services.console-renderer',
    provides: console_1.ConsolePanel.IContentFactory,
    requires: [codeeditor_1.IEditorServices],
    autoStart: true,
    activate: function (app, editorServices) {
        var editorFactory = editorServices.factoryService.newInlineEditor.bind(editorServices.factoryService);
        return new console_1.ConsolePanel.ContentFactory({ editorFactory: editorFactory });
    }
};
/**
 * Export the plugins as the default.
 */
var plugins = [exports.contentFactoryPlugin, exports.trackerPlugin];
exports.default = plugins;
/**
 * Activate the console extension.
 */
function activateConsole(app, manager, rendermime, mainMenu, palette, pathTracker, contentFactory, editorServices, restorer, launcher) {
    var commands = app.commands, shell = app.shell;
    var category = 'Console';
    var command;
    var menu = new widgets_1.Menu({ commands: commands });
    // Create an instance tracker for all console panels.
    var tracker = new apputils_1.InstanceTracker({
        namespace: 'console',
        shell: shell
    });
    // Handle state restoration.
    restorer.restore(tracker, {
        command: CommandIDs.open,
        args: function (panel) { return ({
            path: panel.console.session.path,
            name: panel.console.session.name
        }); },
        name: function (panel) { return panel.console.session.path; },
        when: manager.ready
    });
    // Add a launcher item if the launcher is available.
    if (launcher) {
        launcher.add({
            name: 'Code Console',
            command: CommandIDs.create
        });
    }
    // Set the main menu title.
    menu.title.label = category;
    /**
     * Create a console for a given path.
     */
    function createConsole(options) {
        return manager.ready.then(function () {
            var panel = new console_1.ConsolePanel(__assign({ manager: manager, rendermime: rendermime.clone(), contentFactory: contentFactory, mimeTypeService: editorServices.mimeTypeService }, options));
            // Add the console panel to the tracker.
            tracker.add(panel);
            shell.addToMainArea(panel);
            tracker.activate(panel);
        });
    }
    command = CommandIDs.open;
    commands.addCommand(command, {
        execute: function (args) {
            var path = args['path'];
            var widget = tracker.find(function (value) {
                if (value.console.session.path === path) {
                    return true;
                }
            });
            if (widget) {
                tracker.activate(widget);
            }
            else {
                return manager.ready.then(function () {
                    var model = algorithm_1.find(manager.sessions.running(), function (item) {
                        return item.path === path;
                    });
                    if (model) {
                        return createConsole(args);
                    }
                });
            }
        }
    });
    command = CommandIDs.create;
    commands.addCommand(command, {
        label: 'Start New Console',
        execute: function (args) {
            args.basePath = args.basePath || pathTracker.path;
            return createConsole(args);
        }
    });
    palette.addItem({ command: command, category: category });
    // Get the current widget and activate unless the args specify otherwise.
    function getCurrent(args) {
        var widget = tracker.currentWidget;
        var activate = args['activate'] !== false;
        if (activate && widget) {
            tracker.activate(widget);
        }
        return widget;
    }
    command = CommandIDs.clear;
    commands.addCommand(command, {
        label: 'Clear Cells',
        execute: function (args) {
            var current = getCurrent(args);
            if (!current) {
                return;
            }
            current.console.clear();
        }
    });
    palette.addItem({ command: command, category: category });
    command = CommandIDs.run;
    commands.addCommand(command, {
        label: 'Run Cell',
        execute: function (args) {
            var current = getCurrent(args);
            if (!current) {
                return;
            }
            return current.console.execute();
        }
    });
    palette.addItem({ command: command, category: category });
    command = CommandIDs.runForced;
    commands.addCommand(command, {
        label: 'Run Cell (forced)',
        execute: function (args) {
            var current = getCurrent(args);
            if (!current) {
                return;
            }
            current.console.execute(true);
        }
    });
    palette.addItem({ command: command, category: category });
    command = CommandIDs.linebreak;
    commands.addCommand(command, {
        label: 'Insert Line Break',
        execute: function (args) {
            var current = getCurrent(args);
            if (!current) {
                return;
            }
            current.console.insertLinebreak();
        }
    });
    palette.addItem({ command: command, category: category });
    command = CommandIDs.interrupt;
    commands.addCommand(command, {
        label: 'Interrupt Kernel',
        execute: function (args) {
            var current = getCurrent(args);
            if (!current) {
                return;
            }
            var kernel = current.console.session.kernel;
            if (kernel) {
                return kernel.interrupt();
            }
        }
    });
    palette.addItem({ command: command, category: category });
    command = CommandIDs.restart;
    commands.addCommand(command, {
        label: 'Restart Kernel',
        execute: function (args) {
            var current = getCurrent(args);
            if (!current) {
                return;
            }
            return current.console.session.restart();
        }
    });
    palette.addItem({ command: command, category: category });
    command = CommandIDs.closeAndShutdown;
    commands.addCommand(command, {
        label: 'Close and Shutdown',
        execute: function (args) {
            var current = getCurrent(args);
            if (!current) {
                return;
            }
            return apputils_1.showDialog({
                title: 'Shutdown the console?',
                body: "Are you sure you want to close \"" + current.title.label + "\"?",
                buttons: [apputils_1.Dialog.cancelButton(), apputils_1.Dialog.warnButton()]
            }).then(function (result) {
                if (result.accept) {
                    current.console.session.shutdown().then(function () {
                        current.dispose();
                    });
                }
                else {
                    return false;
                }
            });
        }
    });
    command = CommandIDs.inject;
    commands.addCommand(command, {
        execute: function (args) {
            var path = args['path'];
            tracker.find(function (widget) {
                if (widget.console.session.path === path) {
                    if (args['activate'] !== false) {
                        tracker.activate(widget);
                    }
                    widget.console.inject(args['code']);
                    return true;
                }
            });
        }
    });
    command = CommandIDs.switchKernel;
    commands.addCommand(command, {
        label: 'Switch Kernel',
        execute: function (args) {
            var current = getCurrent(args);
            if (!current) {
                return;
            }
            return current.console.session.selectKernel();
        }
    });
    palette.addItem({ command: command, category: category });
    menu.addItem({ command: CommandIDs.run });
    menu.addItem({ command: CommandIDs.runForced });
    menu.addItem({ command: CommandIDs.linebreak });
    menu.addItem({ type: 'separator' });
    menu.addItem({ command: CommandIDs.clear });
    menu.addItem({ type: 'separator' });
    menu.addItem({ command: CommandIDs.interrupt });
    menu.addItem({ command: CommandIDs.restart });
    menu.addItem({ command: CommandIDs.switchKernel });
    menu.addItem({ type: 'separator' });
    menu.addItem({ command: CommandIDs.closeAndShutdown });
    mainMenu.addMenu(menu, { rank: 50 });
    return tracker;
}

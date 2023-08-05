// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var algorithm_1 = require("@phosphor/algorithm");
var disposable_1 = require("@phosphor/disposable");
var widgets_1 = require("@phosphor/widgets");
var apputils_1 = require("@jupyterlab/apputils");
var docmanager_1 = require("@jupyterlab/docmanager");
var docregistry_1 = require("@jupyterlab/docregistry");
var filebrowser_1 = require("@jupyterlab/filebrowser");
var services_1 = require("@jupyterlab/services");
/**
 * The command IDs used by the file browser plugin.
 */
var CommandIDs;
(function (CommandIDs) {
    CommandIDs.save = 'file-operations:save';
    CommandIDs.restoreCheckpoint = 'file-operations:restore-checkpoint';
    CommandIDs.saveAs = 'file-operations:save-as';
    CommandIDs.close = 'file-operations:close';
    CommandIDs.closeAllFiles = 'file-operations:close-all-files';
    CommandIDs.open = 'file-operations:open';
    CommandIDs.newTextFile = 'file-operations:new-text-file';
    CommandIDs.newNotebook = 'file-operations:new-notebook';
    CommandIDs.showBrowser = 'file-browser:activate';
    CommandIDs.hideBrowser = 'file-browser:hide';
    CommandIDs.toggleBrowser = 'file-browser:toggle';
})(CommandIDs || (CommandIDs = {}));
;
/**
 * The default file browser provider.
 */
var plugin = {
    activate: activate,
    id: 'jupyter.services.file-browser',
    provides: filebrowser_1.IPathTracker,
    requires: [
        services_1.IServiceManager,
        docmanager_1.IDocumentManager,
        docregistry_1.IDocumentRegistry,
        apputils_1.IMainMenu,
        apputils_1.ICommandPalette,
        apputils_1.ILayoutRestorer,
        apputils_1.IStateDB
    ],
    autoStart: true
};
/**
 * Export the plugin as default.
 */
exports.default = plugin;
/**
 * The filebrowser plugin state namespace.
 */
var NAMESPACE = 'filebrowser';
/**
 * Activate the file browser.
 */
function activate(app, manager, documentManager, registry, mainMenu, palette, restorer, state) {
    var commands = app.commands;
    var fbModel = new filebrowser_1.FileBrowserModel({ manager: manager });
    var fbWidget = new filebrowser_1.FileBrowser({
        commands: commands,
        manager: documentManager,
        model: fbModel
    });
    // Let the application restorer track the file browser for restoration of
    // application state (e.g. setting the file browser as the current side bar
    // widget).
    restorer.add(fbWidget, NAMESPACE);
    var category = 'File Operations';
    var creatorCmds = Object.create(null);
    var addCreator = function (name) {
        var disposables = creatorCmds[name] = new disposable_1.DisposableSet();
        var command = Private.commandForName(name);
        disposables.add(commands.addCommand(command, {
            execute: function () { return fbWidget.createFrom(name); },
            label: "New " + name
        }));
        disposables.add(palette.addItem({ command: command, category: category }));
    };
    // Restore the state of the file browser on reload.
    var key = NAMESPACE + ":cwd";
    var connect = function () {
        // Save the subsequent state of the file browser in the state database.
        fbModel.pathChanged.connect(function (sender, args) {
            state.save(key, { path: args.newValue });
        });
    };
    Promise.all([state.fetch(key), app.started, manager.ready]).then(function (_a) {
        var cwd = _a[0];
        if (!cwd) {
            return;
        }
        var path = cwd['path'];
        return manager.contents.get(path)
            .then(function () { return fbModel.cd(path); })
            .catch(function () { return state.remove(key); });
    }).then(connect)
        .catch(function () { return state.remove(key).then(connect); });
    algorithm_1.each(registry.creators(), function (creator) { addCreator(creator.name); });
    // Add a context menu to the dir listing.
    var node = fbWidget.node.getElementsByClassName('jp-DirListing-content')[0];
    node.addEventListener('contextmenu', function (event) {
        event.preventDefault();
        var path = fbWidget.pathForClick(event) || '';
        var ext = docregistry_1.DocumentRegistry.extname(path);
        var factories = registry.preferredWidgetFactories(ext);
        var widgetNames = algorithm_1.toArray(algorithm_1.map(factories, function (factory) { return factory.name; }));
        var prefix = "file-browser-contextmenu-" + ++Private.id;
        var openWith = null;
        if (path && widgetNames.length > 1) {
            var disposables_1 = new disposable_1.DisposableSet();
            var command = void 0;
            openWith = new widgets_1.Menu({ commands: commands });
            openWith.title.label = 'Open With...';
            openWith.disposed.connect(function () { disposables_1.dispose(); });
            var _loop_1 = function (widgetName) {
                command = prefix + ":" + widgetName;
                disposables_1.add(commands.addCommand(command, {
                    execute: function () { return fbWidget.openPath(path, widgetName); },
                    label: widgetName
                }));
                openWith.addItem({ command: command });
            };
            for (var _i = 0, widgetNames_1 = widgetNames; _i < widgetNames_1.length; _i++) {
                var widgetName = widgetNames_1[_i];
                _loop_1(widgetName);
            }
        }
        var menu = createContextMenu(fbWidget, openWith);
        menu.open(event.clientX, event.clientY);
    });
    addCommands(app, fbWidget, documentManager);
    [
        CommandIDs.save,
        CommandIDs.restoreCheckpoint,
        CommandIDs.saveAs,
        CommandIDs.close,
        CommandIDs.closeAllFiles
    ].forEach(function (command) { palette.addItem({ command: command, category: category }); });
    var menu = createMenu(app, Object.keys(creatorCmds));
    mainMenu.addMenu(menu, { rank: 1 });
    fbWidget.title.label = 'Files';
    fbWidget.id = 'file-browser';
    app.shell.addToLeftArea(fbWidget, { rank: 40 });
    // If the layout is a fresh session without saved data, open file browser.
    app.restored.then(function (layout) {
        if (layout.fresh) {
            app.commands.execute(CommandIDs.showBrowser, void 0);
        }
    });
    // Handle fileCreator items as they are added.
    registry.changed.connect(function (sender, args) {
        if (args.type === 'fileCreator') {
            menu.dispose();
            var name_1 = args.name;
            if (args.change === 'added') {
                addCreator(name_1);
            }
            else {
                creatorCmds[name_1].dispose();
                delete creatorCmds[name_1];
            }
            menu = createMenu(app, Object.keys(creatorCmds));
            mainMenu.addMenu(menu, { rank: 1 });
        }
    });
    return fbModel;
}
/**
 * Add the filebrowser commands to the application's command registry.
 */
function addCommands(app, fbWidget, docManager) {
    var commands = app.commands;
    var isEnabled = function () {
        var currentWidget = app.shell.currentWidget;
        return !!(currentWidget && docManager.contextForWidget(currentWidget));
    };
    commands.addCommand(CommandIDs.save, {
        label: 'Save',
        caption: 'Save and create checkpoint',
        isEnabled: isEnabled,
        execute: function () {
            if (isEnabled()) {
                var context_1 = docManager.contextForWidget(app.shell.currentWidget);
                return context_1.save().then(function () { return context_1.createCheckpoint(); });
            }
        }
    });
    commands.addCommand(CommandIDs.restoreCheckpoint, {
        label: 'Revert to Checkpoint',
        caption: 'Revert contents to previous checkpoint',
        isEnabled: isEnabled,
        execute: function () {
            if (isEnabled()) {
                var context_2 = docManager.contextForWidget(app.shell.currentWidget);
                return context_2.restoreCheckpoint().then(function () { return context_2.revert(); });
            }
        }
    });
    commands.addCommand(CommandIDs.saveAs, {
        label: 'Save As...',
        caption: 'Save with new path and create checkpoint',
        isEnabled: isEnabled,
        execute: function () {
            if (isEnabled()) {
                var context_3 = docManager.contextForWidget(app.shell.currentWidget);
                return context_3.saveAs().then(function () {
                    return context_3.createCheckpoint();
                });
            }
        }
    });
    commands.addCommand(CommandIDs.open, {
        execute: function (args) {
            var path = args['path'];
            var factory = args['factory'] || void 0;
            return docManager.services.contents.get(path)
                .then(function () { return fbWidget.openPath(path, factory); });
        }
    });
    commands.addCommand(CommandIDs.close, {
        label: 'Close',
        execute: function () {
            if (app.shell.currentWidget) {
                app.shell.currentWidget.close();
            }
        }
    });
    commands.addCommand(CommandIDs.closeAllFiles, {
        label: 'Close All',
        execute: function () { app.shell.closeAll(); }
    });
    commands.addCommand(CommandIDs.showBrowser, {
        execute: function () { app.shell.activateById(fbWidget.id); }
    });
    commands.addCommand(CommandIDs.hideBrowser, {
        execute: function () {
            if (!fbWidget.isHidden) {
                app.shell.collapseLeft();
            }
        }
    });
    commands.addCommand(CommandIDs.toggleBrowser, {
        execute: function () {
            if (fbWidget.isHidden) {
                return commands.execute(CommandIDs.showBrowser, void 0);
            }
            else {
                return commands.execute(CommandIDs.hideBrowser, void 0);
            }
        }
    });
}
/**
 * Create a top level menu for the file browser.
 */
function createMenu(app, creatorCmds) {
    var commands = app.commands;
    var menu = new widgets_1.Menu({ commands: commands });
    menu.title.label = 'File';
    creatorCmds.forEach(function (name) {
        menu.addItem({ command: Private.commandForName(name) });
    });
    [
        CommandIDs.save,
        CommandIDs.restoreCheckpoint,
        CommandIDs.saveAs,
        CommandIDs.close,
        CommandIDs.closeAllFiles
    ].forEach(function (command) { menu.addItem({ command: command }); });
    return menu;
}
/**
 * Create a context menu for the file browser listing.
 *
 * #### Notes
 * This function generates temporary commands with an incremented name. These
 * commands are disposed when the menu itself is disposed.
 */
function createContextMenu(fbWidget, openWith) {
    var commands = fbWidget.commands;
    var menu = new widgets_1.Menu({ commands: commands });
    var prefix = "file-browser-" + ++Private.id;
    var disposables = new disposable_1.DisposableSet();
    var command;
    // Remove all the commands associated with this menu upon disposal.
    menu.disposed.connect(function () { disposables.dispose(); });
    command = prefix + ":open";
    disposables.add(commands.addCommand(command, {
        execute: function () { fbWidget.open(); },
        icon: 'jp-MaterialIcon jp-OpenFolderIcon',
        label: 'Open',
        mnemonic: 0
    }));
    menu.addItem({ command: command });
    if (openWith) {
        menu.addItem({ type: 'submenu', submenu: openWith });
    }
    command = prefix + ":rename";
    disposables.add(commands.addCommand(command, {
        execute: function () { return fbWidget.rename(); },
        icon: 'jp-MaterialIcon jp-EditIcon',
        label: 'Rename',
        mnemonic: 0
    }));
    menu.addItem({ command: command });
    command = prefix + ":delete";
    disposables.add(commands.addCommand(command, {
        execute: function () { return fbWidget.delete(); },
        icon: 'jp-MaterialIcon jp-CloseIcon',
        label: 'Delete',
        mnemonic: 0
    }));
    menu.addItem({ command: command });
    command = prefix + ":duplicate";
    disposables.add(commands.addCommand(command, {
        execute: function () { return fbWidget.duplicate(); },
        icon: 'jp-MaterialIcon jp-CopyIcon',
        label: 'Duplicate'
    }));
    menu.addItem({ command: command });
    command = prefix + ":cut";
    disposables.add(commands.addCommand(command, {
        execute: function () { fbWidget.cut(); },
        icon: 'jp-MaterialIcon jp-CutIcon',
        label: 'Cut'
    }));
    menu.addItem({ command: command });
    command = prefix + ":copy";
    disposables.add(commands.addCommand(command, {
        execute: function () { fbWidget.copy(); },
        icon: 'jp-MaterialIcon jp-CopyIcon',
        label: 'Copy',
        mnemonic: 0
    }));
    menu.addItem({ command: command });
    command = prefix + ":paste";
    disposables.add(commands.addCommand(command, {
        execute: function () { return fbWidget.paste(); },
        icon: 'jp-MaterialIcon jp-PasteIcon',
        label: 'Paste',
        mnemonic: 0
    }));
    menu.addItem({ command: command });
    command = prefix + ":download";
    disposables.add(commands.addCommand(command, {
        execute: function () { fbWidget.download(); },
        icon: 'jp-MaterialIcon jp-DownloadIcon',
        label: 'Download'
    }));
    menu.addItem({ command: command });
    command = prefix + ":shutdown";
    disposables.add(commands.addCommand(command, {
        execute: function () { return fbWidget.shutdownKernels(); },
        icon: 'jp-MaterialIcon jp-StopIcon',
        label: 'Shutdown Kernel'
    }));
    menu.addItem({ command: command });
    menu.disposed.connect(function () { disposables.dispose(); });
    return menu;
}
/**
 * A namespace for private data.
 */
var Private;
(function (Private) {
    /**
     * The ID counter prefix for new commands.
     *
     * #### Notes
     * Even though the commands are disposed when the menus are disposed,
     * in order to guarantee there are no race conditions, each set of commands
     * is prefixed.
     */
    Private.id = 0;
    /**
     * Get the command for a name.
     */
    function commandForName(name) {
        name = name.split(' ').join('-').toLocaleLowerCase();
        return "file-operations:new-" + name;
    }
    Private.commandForName = commandForName;
})(Private || (Private = {}));

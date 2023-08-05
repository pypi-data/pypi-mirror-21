// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var apputils_1 = require("@jupyterlab/apputils");
var codeeditor_1 = require("@jupyterlab/codeeditor");
var docregistry_1 = require("@jupyterlab/docregistry");
var launcher_1 = require("@jupyterlab/launcher");
var notebook_1 = require("@jupyterlab/notebook");
var rendermime_1 = require("@jupyterlab/rendermime");
var services_1 = require("@jupyterlab/services");
var messaging_1 = require("@phosphor/messaging");
var widgets_1 = require("@phosphor/widgets");
/**
 * The command IDs used by the notebook plugin.
 */
var CommandIDs;
(function (CommandIDs) {
    CommandIDs.interrupt = 'notebook:interrupt-kernel';
    CommandIDs.restart = 'notebook:restart-kernel';
    CommandIDs.restartClear = 'notebook:restart-clear';
    CommandIDs.restartRunAll = 'notebook:restart-runAll';
    CommandIDs.switchKernel = 'notebook:switch-kernel';
    CommandIDs.clearAllOutputs = 'notebook:clear-outputs';
    CommandIDs.closeAndShutdown = 'notebook:close-and-shutdown';
    CommandIDs.trust = 'notebook:trust';
    CommandIDs.run = 'notebook-cells:run';
    CommandIDs.runAndAdvance = 'notebook-cells:run-and-advance';
    CommandIDs.runAndInsert = 'notebook-cells:run-and-insert';
    CommandIDs.runAll = 'notebook:run-all';
    CommandIDs.toCode = 'notebook-cells:to-code';
    CommandIDs.toMarkdown = 'notebook-cells:to-markdown';
    CommandIDs.toRaw = 'notebook-cells:to-raw';
    CommandIDs.cut = 'notebook-cells:cut';
    CommandIDs.copy = 'notebook-cells:copy';
    CommandIDs.paste = 'notebook-cells:paste';
    CommandIDs.moveUp = 'notebook-cells:move-up';
    CommandIDs.moveDown = 'notebook-cells:move-down';
    CommandIDs.clearOutputs = 'notebook-cells:clear-output';
    CommandIDs.deleteCell = 'notebook-cells:delete';
    CommandIDs.insertAbove = 'notebook-cells:insert-above';
    CommandIDs.insertBelow = 'notebook-cells:insert-below';
    CommandIDs.selectAbove = 'notebook-cells:select-above';
    CommandIDs.selectBelow = 'notebook-cells:select-below';
    CommandIDs.extendAbove = 'notebook-cells:extend-above';
    CommandIDs.extendBelow = 'notebook-cells:extend-below';
    CommandIDs.editMode = 'notebook:edit-mode';
    CommandIDs.merge = 'notebook-cells:merge';
    CommandIDs.split = 'notebook-cells:split';
    CommandIDs.commandMode = 'notebook:command-mode';
    CommandIDs.toggleLines = 'notebook-cells:toggle-line-numbers';
    CommandIDs.toggleAllLines = 'notebook-cells:toggle-all-line-numbers';
    CommandIDs.undo = 'notebook-cells:undo';
    CommandIDs.redo = 'notebook-cells:redo';
    CommandIDs.markdown1 = 'notebook-cells:markdown-header1';
    CommandIDs.markdown2 = 'notebook-cells:markdown-header2';
    CommandIDs.markdown3 = 'notebook-cells:markdown-header3';
    CommandIDs.markdown4 = 'notebook-cells:markdown-header4';
    CommandIDs.markdown5 = 'notebook-cells:markdown-header5';
    CommandIDs.markdown6 = 'notebook-cells:markdown-header6';
})(CommandIDs || (CommandIDs = {}));
;
/**
 * The class name for the notebook icon from the default theme.
 */
var NOTEBOOK_ICON_CLASS = 'jp-ImageNotebook';
/**
 * The name of the factory that creates notebooks.
 */
var FACTORY = 'Notebook';
/**
 * The notebook widget tracker provider.
 */
exports.trackerPlugin = {
    id: 'jupyter.services.notebook-tracker',
    provides: notebook_1.INotebookTracker,
    requires: [
        docregistry_1.IDocumentRegistry,
        services_1.IServiceManager,
        rendermime_1.IRenderMime,
        apputils_1.IMainMenu,
        apputils_1.ICommandPalette,
        notebook_1.NotebookPanel.IContentFactory,
        codeeditor_1.IEditorServices,
        apputils_1.ILayoutRestorer
    ],
    optional: [launcher_1.ILauncher],
    activate: activateNotebookHandler,
    autoStart: true
};
/**
 * The notebook cell factory provider.
 */
exports.contentFactoryPlugin = {
    id: 'jupyter.services.notebook-renderer',
    provides: notebook_1.NotebookPanel.IContentFactory,
    requires: [codeeditor_1.IEditorServices],
    autoStart: true,
    activate: function (app, editorServices) {
        var editorFactory = editorServices.factoryService.newInlineEditor.bind(editorServices.factoryService);
        return new notebook_1.NotebookPanel.ContentFactory({ editorFactory: editorFactory });
    }
};
/**
 * The cell tools extension.
 */
var cellToolsPlugin = {
    activate: activateCellTools,
    provides: notebook_1.ICellTools,
    id: 'jupyter.extensions.cell-tools',
    autoStart: true,
    requires: [notebook_1.INotebookTracker, codeeditor_1.IEditorServices, apputils_1.IStateDB]
};
/**
 * Export the plugins as default.
 */
var plugins = [exports.contentFactoryPlugin, exports.trackerPlugin, cellToolsPlugin];
exports.default = plugins;
/**
 * Activate the cell tools extension.
 */
function activateCellTools(app, tracker, editorServices, state) {
    var id = 'cell-tools';
    var celltools = new notebook_1.CellTools({ tracker: tracker });
    var activeCellTool = new notebook_1.CellTools.ActiveCellTool();
    var slideShow = notebook_1.CellTools.createSlideShowSelector();
    var nbConvert = notebook_1.CellTools.createNBConvertSelector();
    var editorFactory = editorServices.factoryService.newInlineEditor
        .bind(editorServices.factoryService);
    var metadataEditor = new notebook_1.CellTools.MetadataEditorTool({ editorFactory: editorFactory });
    // Create message hook for triggers to save to the database.
    var hook = function (sender, message) {
        switch (message) {
            case widgets_1.Widget.Msg.ActivateRequest:
                state.save(id, { open: true });
                break;
            case widgets_1.Widget.Msg.CloseRequest:
                state.remove(celltools.id);
                break;
            default:
                break;
        }
        return true;
    };
    celltools.title.label = 'Cell Tools';
    celltools.id = id;
    celltools.addItem({ tool: activeCellTool, rank: 1 });
    celltools.addItem({ tool: slideShow, rank: 2 });
    celltools.addItem({ tool: nbConvert, rank: 3 });
    celltools.addItem({ tool: metadataEditor, rank: 4 });
    messaging_1.MessageLoop.installMessageHook(celltools, hook);
    // Wait until the application has finished restoring before rendering.
    Promise.all([state.fetch(id), app.restored]).then(function (_a) {
        var args = _a[0];
        var open = (args && args['open']) || false;
        // After initial restoration, check if the cell tools should render.
        if (tracker.size) {
            app.shell.addToLeftArea(celltools);
            if (open) {
                app.shell.activateById(celltools.id);
            }
        }
        // For all subsequent widget changes, check if the cell tools should render.
        app.shell.currentChanged.connect(function (sender, args) {
            // If there are any open notebooks, add cell tools to the side panel if
            // it is not already there.
            if (tracker.size) {
                if (!celltools.isAttached) {
                    app.shell.addToLeftArea(celltools);
                }
                return;
            }
            // If there are no notebooks, close cell tools.
            celltools.close();
        });
    });
    return Promise.resolve(celltools);
}
/**
 * Activate the notebook handler extension.
 */
function activateNotebookHandler(app, registry, services, rendermime, mainMenu, palette, contentFactory, editorServices, restorer, launcher) {
    var factory = new notebook_1.NotebookWidgetFactory({
        name: FACTORY,
        fileExtensions: ['.ipynb'],
        modelName: 'notebook',
        defaultFor: ['.ipynb'],
        preferKernel: true,
        canStartKernel: true,
        rendermime: rendermime,
        contentFactory: contentFactory,
        mimeTypeService: editorServices.mimeTypeService
    });
    var shell = app.shell;
    var tracker = new notebook_1.NotebookTracker({ namespace: 'notebook', shell: shell });
    // Handle state restoration.
    restorer.restore(tracker, {
        command: 'file-operations:open',
        args: function (panel) { return ({ path: panel.context.path, factory: FACTORY }); },
        name: function (panel) { return panel.context.path; },
        when: services.ready
    });
    registry.addModelFactory(new notebook_1.NotebookModelFactory({}));
    registry.addWidgetFactory(factory);
    registry.addFileType({
        name: 'Notebook',
        extension: '.ipynb',
        contentType: 'notebook',
        fileFormat: 'json'
    });
    registry.addCreator({
        name: 'Notebook',
        fileType: 'Notebook',
        widgetName: 'Notebook'
    });
    addCommands(app, services, tracker);
    populatePalette(palette);
    var id = 0; // The ID counter for notebook panels.
    factory.widgetCreated.connect(function (sender, widget) {
        // If the notebook panel does not have an ID, assign it one.
        widget.id = widget.id || "notebook-" + ++id;
        widget.title.icon = NOTEBOOK_ICON_CLASS;
        // Notify the instance tracker if restore data needs to update.
        widget.context.pathChanged.connect(function () { tracker.save(widget); });
        // Add the notebook panel to the tracker.
        tracker.add(widget);
    });
    // Add main menu notebook menu.
    mainMenu.addMenu(createMenu(app), { rank: 20 });
    // Add a launcher item if the launcher is available.
    if (launcher) {
        launcher.add({
            name: 'Notebook',
            command: 'file-operations:new-notebook'
        });
    }
    return tracker;
}
/**
 * Add the notebook commands to the application's command registry.
 */
function addCommands(app, services, tracker) {
    var commands = app.commands;
    // Get the current widget and activate unless the args specify otherwise.
    function getCurrent(args) {
        var widget = tracker.currentWidget;
        var activate = args['activate'] !== false;
        if (activate && widget) {
            tracker.activate(widget);
        }
        return widget;
    }
    commands.addCommand(CommandIDs.runAndAdvance, {
        label: 'Run Cell(s) and Advance',
        execute: function (args) {
            var current = getCurrent(args);
            if (!current) {
                return;
            }
            var content = current.notebook;
            return notebook_1.NotebookActions.runAndAdvance(content, current.context.session);
        }
    });
    commands.addCommand(CommandIDs.run, {
        label: 'Run Cell(s)',
        execute: function (args) {
            var current = getCurrent(args);
            if (!current) {
                return;
            }
            return notebook_1.NotebookActions.run(current.notebook, current.context.session);
        }
    });
    commands.addCommand(CommandIDs.runAndInsert, {
        label: 'Run Cell(s) and Insert',
        execute: function (args) {
            var current = getCurrent(args);
            if (!current) {
                return;
            }
            return notebook_1.NotebookActions.runAndInsert(current.notebook, current.context.session);
        }
    });
    commands.addCommand(CommandIDs.runAll, {
        label: 'Run All Cells',
        execute: function (args) {
            var current = getCurrent(args);
            if (!current) {
                return;
            }
            return notebook_1.NotebookActions.runAll(current.notebook, current.context.session);
        }
    });
    commands.addCommand(CommandIDs.restart, {
        label: 'Restart Kernel',
        execute: function (args) {
            var current = getCurrent(args);
            if (!current) {
                return;
            }
            current.session.restart();
        }
    });
    commands.addCommand(CommandIDs.closeAndShutdown, {
        label: 'Close and Shutdown',
        execute: function (args) {
            var current = getCurrent(args);
            if (!current) {
                return;
            }
            var fileName = current.title.label;
            return apputils_1.showDialog({
                title: 'Shutdown the notebook?',
                body: "Are you sure you want to close \"" + fileName + "\"?",
                buttons: [apputils_1.Dialog.cancelButton(), apputils_1.Dialog.warnButton()]
            }).then(function (result) {
                if (result.accept) {
                    return current.context.session.shutdown().then(function () {
                        current.dispose();
                    });
                }
                else {
                    return;
                }
            });
        }
    });
    commands.addCommand(CommandIDs.trust, {
        label: 'Trust Notebook',
        execute: function (args) {
            var current = getCurrent(args);
            if (!current) {
                return;
            }
            return notebook_1.trustNotebook(current.context.model).then(function () {
                return current.context.save();
            });
        }
    });
    commands.addCommand(CommandIDs.restartClear, {
        label: 'Restart Kernel & Clear Outputs',
        execute: function (args) {
            var current = getCurrent(args);
            if (!current) {
                return;
            }
            return current.session.restart().then(function () {
                notebook_1.NotebookActions.clearAllOutputs(current.notebook);
            });
        }
    });
    commands.addCommand(CommandIDs.restartRunAll, {
        label: 'Restart Kernel & Run All',
        execute: function (args) {
            var current = getCurrent(args);
            if (!current) {
                return;
            }
            return current.session.restart().then(function () {
                notebook_1.NotebookActions.runAll(current.notebook, current.context.session);
            });
        }
    });
    commands.addCommand(CommandIDs.clearAllOutputs, {
        label: 'Clear All Outputs',
        execute: function (args) {
            var current = getCurrent(args);
            if (!current) {
                return;
            }
            return notebook_1.NotebookActions.clearAllOutputs(current.notebook);
        }
    });
    commands.addCommand(CommandIDs.clearOutputs, {
        label: 'Clear Output(s)',
        execute: function (args) {
            var current = getCurrent(args);
            if (!current) {
                return;
            }
            return notebook_1.NotebookActions.clearOutputs(current.notebook);
        }
    });
    commands.addCommand(CommandIDs.interrupt, {
        label: 'Interrupt Kernel',
        execute: function (args) {
            var current = getCurrent(args);
            if (!current) {
                return;
            }
            var kernel = current.context.session.kernel;
            if (kernel) {
                return kernel.interrupt();
            }
        }
    });
    commands.addCommand(CommandIDs.toCode, {
        label: 'Convert to Code',
        execute: function (args) {
            var current = getCurrent(args);
            if (!current) {
                return;
            }
            return notebook_1.NotebookActions.changeCellType(current.notebook, 'code');
        }
    });
    commands.addCommand(CommandIDs.toMarkdown, {
        label: 'Convert to Markdown',
        execute: function (args) {
            var current = getCurrent(args);
            if (!current) {
                return;
            }
            return notebook_1.NotebookActions.changeCellType(current.notebook, 'markdown');
        }
    });
    commands.addCommand(CommandIDs.toRaw, {
        label: 'Convert to Raw',
        execute: function (args) {
            var current = getCurrent(args);
            if (!current) {
                return;
            }
            return notebook_1.NotebookActions.changeCellType(current.notebook, 'raw');
        }
    });
    commands.addCommand(CommandIDs.cut, {
        label: 'Cut Cell(s)',
        execute: function (args) {
            var current = getCurrent(args);
            if (!current) {
                return;
            }
            return notebook_1.NotebookActions.cut(current.notebook);
        }
    });
    commands.addCommand(CommandIDs.copy, {
        label: 'Copy Cell(s)',
        execute: function (args) {
            var current = getCurrent(args);
            if (!current) {
                return;
            }
            return notebook_1.NotebookActions.copy(current.notebook);
        }
    });
    commands.addCommand(CommandIDs.paste, {
        label: 'Paste Cell(s)',
        execute: function (args) {
            var current = getCurrent(args);
            if (!current) {
                return;
            }
            return notebook_1.NotebookActions.paste(current.notebook);
        }
    });
    commands.addCommand(CommandIDs.deleteCell, {
        label: 'Delete Cell(s)',
        execute: function (args) {
            var current = getCurrent(args);
            if (!current) {
                return;
            }
            return notebook_1.NotebookActions.deleteCells(current.notebook);
        }
    });
    commands.addCommand(CommandIDs.split, {
        label: 'Split Cell',
        execute: function (args) {
            var current = getCurrent(args);
            if (!current) {
                return;
            }
            return notebook_1.NotebookActions.splitCell(current.notebook);
        }
    });
    commands.addCommand(CommandIDs.merge, {
        label: 'Merge Selected Cell(s)',
        execute: function (args) {
            var current = getCurrent(args);
            if (!current) {
                return;
            }
            return notebook_1.NotebookActions.mergeCells(current.notebook);
        }
    });
    commands.addCommand(CommandIDs.insertAbove, {
        label: 'Insert Cell Above',
        execute: function (args) {
            var current = getCurrent(args);
            if (!current) {
                return;
            }
            return notebook_1.NotebookActions.insertAbove(current.notebook);
        }
    });
    commands.addCommand(CommandIDs.insertBelow, {
        label: 'Insert Cell Below',
        execute: function (args) {
            var current = getCurrent(args);
            if (!current) {
                return;
            }
            return notebook_1.NotebookActions.insertBelow(current.notebook);
        }
    });
    commands.addCommand(CommandIDs.selectAbove, {
        label: 'Select Cell Above',
        execute: function (args) {
            var current = getCurrent(args);
            if (!current) {
                return;
            }
            return notebook_1.NotebookActions.selectAbove(current.notebook);
        }
    });
    commands.addCommand(CommandIDs.selectBelow, {
        label: 'Select Cell Below',
        execute: function (args) {
            var current = getCurrent(args);
            if (!current) {
                return;
            }
            return notebook_1.NotebookActions.selectBelow(current.notebook);
        }
    });
    commands.addCommand(CommandIDs.extendAbove, {
        label: 'Extend Selection Above',
        execute: function (args) {
            var current = getCurrent(args);
            if (!current) {
                return;
            }
            return notebook_1.NotebookActions.extendSelectionAbove(current.notebook);
        }
    });
    commands.addCommand(CommandIDs.extendBelow, {
        label: 'Extend Selection Below',
        execute: function (args) {
            var current = getCurrent(args);
            if (!current) {
                return;
            }
            return notebook_1.NotebookActions.extendSelectionBelow(current.notebook);
        }
    });
    commands.addCommand(CommandIDs.moveUp, {
        label: 'Move Cell(s) Up',
        execute: function (args) {
            var current = getCurrent(args);
            if (!current) {
                return;
            }
            return notebook_1.NotebookActions.moveUp(current.notebook);
        }
    });
    commands.addCommand(CommandIDs.moveDown, {
        label: 'Move Cell(s) Down',
        execute: function (args) {
            var current = getCurrent(args);
            if (!current) {
                return;
            }
            return notebook_1.NotebookActions.moveDown(current.notebook);
        }
    });
    commands.addCommand(CommandIDs.toggleLines, {
        label: 'Toggle Line Numbers',
        execute: function (args) {
            var current = getCurrent(args);
            if (!current) {
                return;
            }
            return notebook_1.NotebookActions.toggleLineNumbers(current.notebook);
        }
    });
    commands.addCommand(CommandIDs.toggleAllLines, {
        label: 'Toggle All Line Numbers',
        execute: function (args) {
            var current = getCurrent(args);
            if (!current) {
                return;
            }
            return notebook_1.NotebookActions.toggleAllLineNumbers(current.notebook);
        }
    });
    commands.addCommand(CommandIDs.commandMode, {
        label: 'To Command Mode',
        execute: function (args) {
            var current = getCurrent(args);
            if (!current) {
                return;
            }
            return current.notebook.mode = 'command';
        }
    });
    commands.addCommand(CommandIDs.editMode, {
        label: 'To Edit Mode',
        execute: function (args) {
            var current = getCurrent(args);
            if (!current) {
                return;
            }
            current.notebook.mode = 'edit';
        }
    });
    commands.addCommand(CommandIDs.undo, {
        label: 'Undo Cell Operation',
        execute: function (args) {
            var current = getCurrent(args);
            if (!current) {
                return;
            }
            return notebook_1.NotebookActions.undo(current.notebook);
        }
    });
    commands.addCommand(CommandIDs.redo, {
        label: 'Redo Cell Operation',
        execute: function (args) {
            var current = getCurrent(args);
            if (!current) {
                return;
            }
            return notebook_1.NotebookActions.redo(current.notebook);
        }
    });
    commands.addCommand(CommandIDs.switchKernel, {
        label: 'Switch Kernel',
        execute: function (args) {
            var current = getCurrent(args);
            if (!current) {
                return;
            }
            return current.context.session.selectKernel();
        }
    });
    commands.addCommand(CommandIDs.markdown1, {
        label: 'Markdown Header 1',
        execute: function (args) {
            var current = getCurrent(args);
            if (!current) {
                return;
            }
            return notebook_1.NotebookActions.setMarkdownHeader(current.notebook, 1);
        }
    });
    commands.addCommand(CommandIDs.markdown2, {
        label: 'Markdown Header 2',
        execute: function (args) {
            var current = getCurrent(args);
            if (!current) {
                return;
            }
            return notebook_1.NotebookActions.setMarkdownHeader(current.notebook, 2);
        }
    });
    commands.addCommand(CommandIDs.markdown3, {
        label: 'Markdown Header 3',
        execute: function (args) {
            var current = getCurrent(args);
            if (!current) {
                return;
            }
            return notebook_1.NotebookActions.setMarkdownHeader(current.notebook, 3);
        }
    });
    commands.addCommand(CommandIDs.markdown4, {
        label: 'Markdown Header 4',
        execute: function (args) {
            var current = getCurrent(args);
            if (!current) {
                return;
            }
            return notebook_1.NotebookActions.setMarkdownHeader(current.notebook, 4);
        }
    });
    commands.addCommand(CommandIDs.markdown5, {
        label: 'Markdown Header 5',
        execute: function (args) {
            var current = getCurrent(args);
            if (!current) {
                return;
            }
            return notebook_1.NotebookActions.setMarkdownHeader(current.notebook, 5);
        }
    });
    commands.addCommand(CommandIDs.markdown6, {
        label: 'Markdown Header 6',
        execute: function (args) {
            var current = getCurrent(args);
            if (!current) {
                return;
            }
            return notebook_1.NotebookActions.setMarkdownHeader(current.notebook, 6);
        }
    });
}
/**
 * Populate the application's command palette with notebook commands.
 */
function populatePalette(palette) {
    var category = 'Notebook Operations';
    [
        CommandIDs.interrupt,
        CommandIDs.restart,
        CommandIDs.restartClear,
        CommandIDs.restartRunAll,
        CommandIDs.runAll,
        CommandIDs.clearAllOutputs,
        CommandIDs.toggleAllLines,
        CommandIDs.editMode,
        CommandIDs.commandMode,
        CommandIDs.switchKernel,
        CommandIDs.closeAndShutdown,
        CommandIDs.trust
    ].forEach(function (command) { palette.addItem({ command: command, category: category }); });
    category = 'Notebook Cell Operations';
    [
        CommandIDs.run,
        CommandIDs.runAndAdvance,
        CommandIDs.runAndInsert,
        CommandIDs.clearOutputs,
        CommandIDs.toCode,
        CommandIDs.toMarkdown,
        CommandIDs.toRaw,
        CommandIDs.cut,
        CommandIDs.copy,
        CommandIDs.paste,
        CommandIDs.deleteCell,
        CommandIDs.split,
        CommandIDs.merge,
        CommandIDs.insertAbove,
        CommandIDs.insertBelow,
        CommandIDs.selectAbove,
        CommandIDs.selectBelow,
        CommandIDs.extendAbove,
        CommandIDs.extendBelow,
        CommandIDs.moveDown,
        CommandIDs.moveUp,
        CommandIDs.toggleLines,
        CommandIDs.undo,
        CommandIDs.redo,
        CommandIDs.markdown1,
        CommandIDs.markdown2,
        CommandIDs.markdown3,
        CommandIDs.markdown4,
        CommandIDs.markdown5,
        CommandIDs.markdown6
    ].forEach(function (command) { palette.addItem({ command: command, category: category }); });
}
/**
 * Creates a menu for the notebook.
 */
function createMenu(app) {
    var commands = app.commands;
    var menu = new widgets_1.Menu({ commands: commands });
    var settings = new widgets_1.Menu({ commands: commands });
    menu.title.label = 'Notebook';
    settings.title.label = 'Settings';
    settings.addItem({ command: CommandIDs.toggleAllLines });
    menu.addItem({ command: CommandIDs.undo });
    menu.addItem({ command: CommandIDs.redo });
    menu.addItem({ type: 'separator' });
    menu.addItem({ command: CommandIDs.cut });
    menu.addItem({ command: CommandIDs.copy });
    menu.addItem({ command: CommandIDs.paste });
    menu.addItem({ command: CommandIDs.deleteCell });
    menu.addItem({ type: 'separator' });
    menu.addItem({ command: CommandIDs.split });
    menu.addItem({ command: CommandIDs.merge });
    menu.addItem({ type: 'separator' });
    menu.addItem({ command: CommandIDs.clearAllOutputs });
    menu.addItem({ type: 'separator' });
    menu.addItem({ command: CommandIDs.runAll });
    menu.addItem({ command: CommandIDs.interrupt });
    menu.addItem({ command: CommandIDs.restart });
    menu.addItem({ command: CommandIDs.switchKernel });
    menu.addItem({ type: 'separator' });
    menu.addItem({ command: CommandIDs.closeAndShutdown });
    menu.addItem({ command: CommandIDs.trust });
    menu.addItem({ type: 'separator' });
    menu.addItem({ type: 'submenu', submenu: settings });
    return menu;
}

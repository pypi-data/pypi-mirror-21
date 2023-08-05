// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var widgets_1 = require("@phosphor/widgets");
var apputils_1 = require("@jupyterlab/apputils");
var codeeditor_1 = require("@jupyterlab/codeeditor");
var codemirror_1 = require("@jupyterlab/codemirror");
var editorwidget_1 = require("@jupyterlab/editorwidget");
/**
 * The command IDs used by the codemirror plugin.
 */
var CommandIDs;
(function (CommandIDs) {
    CommandIDs.matchBrackets = 'codemirror:match-brackets';
    CommandIDs.vimMode = 'codemirror:vim-mode';
    CommandIDs.changeTheme = 'codemirror:change-theme';
})(CommandIDs || (CommandIDs = {}));
;
/**
 * The editor services.
 */
exports.servicesPlugin = {
    id: codeeditor_1.IEditorServices.name,
    provides: codeeditor_1.IEditorServices,
    activate: function () { return codemirror_1.editorServices; }
};
/**
 * The editor commands.
 */
exports.commandsPlugin = {
    id: 'jupyter.services.codemirror-commands',
    requires: [editorwidget_1.IEditorTracker, apputils_1.IMainMenu, apputils_1.ICommandPalette],
    activate: activateEditorCommands,
    autoStart: true
};
/**
 * Export the plugins as default.
 */
var plugins = [exports.commandsPlugin, exports.servicesPlugin];
exports.default = plugins;
/**
 * Set up the editor widget menu and commands.
 */
function activateEditorCommands(app, tracker, mainMenu, palette) {
    var commands = app.commands;
    /**
     * Toggle editor matching brackets
     */
    function toggleMatchBrackets() {
        if (tracker.currentWidget) {
            var editor = tracker.currentWidget.editor;
            if (editor instanceof codemirror_1.CodeMirrorEditor) {
                var cm = editor.editor;
                cm.setOption('matchBrackets', !cm.getOption('matchBrackets'));
            }
        }
    }
    /**
     * Toggle the editor's vim mode
     */
    function toggleVim() {
        tracker.forEach(function (widget) {
            if (widget.editor instanceof codemirror_1.CodeMirrorEditor) {
                var cm = widget.editor.editor;
                var keymap = cm.getOption('keyMap') === 'vim' ? 'default'
                    : 'vim';
                cm.setOption('keyMap', keymap);
            }
        });
    }
    /**
     * Create a menu for the editor.
     */
    function createMenu() {
        var theme = new widgets_1.Menu({ commands: commands });
        var menu = new widgets_1.Menu({ commands: commands });
        menu.title.label = 'Editor';
        theme.title.label = 'Theme';
        commands.addCommand(CommandIDs.changeTheme, {
            label: function (args) { return args['theme']; },
            execute: function (args) {
                var name = args['theme'] || codemirror_1.CodeMirrorEditor.DEFAULT_THEME;
                tracker.forEach(function (widget) {
                    if (widget.editor instanceof codemirror_1.CodeMirrorEditor) {
                        var cm = widget.editor.editor;
                        cm.setOption('theme', name);
                    }
                });
            }
        });
        [
            'jupyter', 'default', 'abcdef', 'base16-dark', 'base16-light',
            'hopscotch', 'material', 'mbo', 'mdn-like', 'seti', 'the-matrix',
            'xq-light', 'zenburn'
        ].forEach(function (name) { return theme.addItem({
            command: 'codemirror:change-theme',
            args: { theme: name }
        }); });
        menu.addItem({ command: 'editor:line-numbers' });
        menu.addItem({ command: 'editor:line-wrap' });
        menu.addItem({ command: CommandIDs.matchBrackets });
        menu.addItem({ command: CommandIDs.vimMode });
        menu.addItem({ type: 'separator' });
        menu.addItem({ type: 'submenu', submenu: theme });
        return menu;
    }
    mainMenu.addMenu(createMenu(), { rank: 30 });
    commands.addCommand(CommandIDs.matchBrackets, {
        execute: function () { toggleMatchBrackets(); },
        label: 'Toggle Match Brackets',
    });
    commands.addCommand(CommandIDs.vimMode, {
        execute: function () { toggleVim(); },
        label: 'Toggle Vim Mode'
    });
    [
        'editor:line-numbers',
        'editor:line-wrap',
        CommandIDs.matchBrackets,
        CommandIDs.vimMode,
        'editor-create-console',
        'editor:run-code'
    ].forEach(function (command) { return palette.addItem({ command: command, category: 'Editor' }); });
}

/*-----------------------------------------------------------------------------
| Copyright (c) Jupyter Development Team.
| Distributed under the terms of the Modified BSD License.
|----------------------------------------------------------------------------*/
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var disposable_1 = require("@phosphor/disposable");
var widgets_1 = require("@phosphor/widgets");
/**
 * The command IDs used by the apputils extension.
 */
var CommandIDs;
(function (CommandIDs) {
    CommandIDs.activate = 'command-palette:activate';
    CommandIDs.hide = 'command-palette:hide';
    CommandIDs.toggle = 'command-palette:toggle';
})(CommandIDs = exports.CommandIDs || (exports.CommandIDs = {}));
;
/**
 * A thin wrapper around the `CommandPalette` class to conform with the
 * JupyterLab interface for the application-wide command palette.
 */
var Palette = (function () {
    /**
     * Create a palette instance.
     */
    function Palette(palette) {
        this._palette = null;
        this._palette = palette;
    }
    Object.defineProperty(Palette.prototype, "placeholder", {
        get: function () {
            return this._palette.inputNode.placeholder;
        },
        /**
         * The placeholder text of the command palette's search input.
         */
        set: function (placeholder) {
            this._palette.inputNode.placeholder = placeholder;
        },
        enumerable: true,
        configurable: true
    });
    /**
     * Activate the command palette for user input.
     */
    Palette.prototype.activate = function () {
        this._palette.activate();
    };
    /**
     * Add a command item to the command palette.
     *
     * @param options - The options for creating the command item.
     *
     * @returns A disposable that will remove the item from the palette.
     */
    Palette.prototype.addItem = function (options) {
        var _this = this;
        var item = this._palette.addItem(options);
        return new disposable_1.DisposableDelegate(function () { return _this._palette.removeItem(item); });
    };
    return Palette;
}());
/**
 * Activate the command palette.
 */
function activatePalette(app, restorer) {
    var commands = app.commands, shell = app.shell;
    var palette = new widgets_1.CommandPalette({ commands: commands });
    // Let the application restorer track the command palette for restoration of
    // application state (e.g. setting the command palette as the current side bar
    // widget).
    restorer.add(palette, 'command-palette');
    palette.id = 'command-palette';
    palette.title.label = 'Commands';
    commands.addCommand(CommandIDs.activate, {
        execute: function () { shell.activateById(palette.id); },
        label: 'Activate Command Palette'
    });
    commands.addCommand(CommandIDs.hide, {
        execute: function () {
            if (!palette.isHidden) {
                shell.collapseLeft();
            }
        },
        label: 'Hide Command Palette'
    });
    commands.addCommand(CommandIDs.toggle, {
        execute: function () {
            if (palette.isHidden) {
                return commands.execute(CommandIDs.activate, void 0);
            }
            return commands.execute(CommandIDs.hide, void 0);
        },
        label: 'Toggle Command Palette'
    });
    palette.inputNode.placeholder = 'SEARCH';
    shell.addToLeftArea(palette);
    return new Palette(palette);
}
exports.activatePalette = activatePalette;

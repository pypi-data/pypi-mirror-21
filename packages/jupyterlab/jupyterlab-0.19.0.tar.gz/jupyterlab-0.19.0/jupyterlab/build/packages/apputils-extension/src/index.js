/*-----------------------------------------------------------------------------
| Copyright (c) Jupyter Development Team.
| Distributed under the terms of the Modified BSD License.
|----------------------------------------------------------------------------*/
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var widgets_1 = require("@phosphor/widgets");
var apputils_1 = require("@jupyterlab/apputils");
var palette_1 = require("./palette");
/**
 * The command IDs used by the apputils plugin.
 */
var CommandIDs;
(function (CommandIDs) {
    CommandIDs.clearStateDB = 'statedb:clear';
})(CommandIDs || (CommandIDs = {}));
;
/**
 * The default commmand linker provider.
 */
var linkerPlugin = {
    id: 'jupyter.services.command-linker',
    provides: apputils_1.ICommandLinker,
    activate: function (app) { return new apputils_1.CommandLinker({ commands: app.commands }); },
    autoStart: true
};
/**
 * The default layout restorer provider.
 */
var layoutPlugin = {
    id: 'jupyter.services.layout-restorer',
    requires: [apputils_1.IStateDB],
    activate: function (app, state) {
        var first = app.started;
        var registry = app.commands;
        var shell = app.shell;
        var restorer = new apputils_1.LayoutRestorer({ first: first, registry: registry, state: state });
        // Use the restorer as the application shell's layout database.
        shell.setLayoutDB(restorer);
        return restorer;
    },
    autoStart: true,
    provides: apputils_1.ILayoutRestorer
};
/**
 * A service providing an interface to the main menu.
 */
var mainMenuPlugin = {
    id: 'jupyter.services.main-menu',
    provides: apputils_1.IMainMenu,
    activate: function (app) {
        var menu = new apputils_1.MainMenu();
        menu.id = 'jp-MainMenu';
        var logo = new widgets_1.Widget();
        logo.node.className = 'jp-MainAreaPortraitIcon jp-JupyterIcon';
        logo.id = 'jp-MainLogo';
        app.shell.addToTopArea(logo);
        app.shell.addToTopArea(menu);
        return menu;
    }
};
/**
 * The default commmand palette extension.
 */
var palettePlugin = {
    activate: palette_1.activatePalette,
    id: 'jupyter.services.commandpalette',
    provides: apputils_1.ICommandPalette,
    requires: [apputils_1.ILayoutRestorer],
    autoStart: true
};
/**
 * The default state database for storing application state.
 */
var stateDBPlugin = {
    id: 'jupyter.services.statedb',
    autoStart: true,
    provides: apputils_1.IStateDB,
    activate: function (app) {
        var state = new apputils_1.StateDB({ namespace: app.info.namespace });
        var version = app.info.version;
        var key = 'statedb:version';
        var fetch = state.fetch(key);
        var save = function () { return state.save(key, { version: version }); };
        var reset = function () { return state.clear().then(save); };
        var check = function (value) {
            var old = value && value['version'];
            if (!old || old !== version) {
                console.log("Upgraded: " + (old || 'unknown') + " to " + version + "; Resetting DB.");
                return reset();
            }
        };
        app.commands.addCommand(CommandIDs.clearStateDB, {
            label: 'Clear Application Restore State',
            execute: function () { return state.clear(); }
        });
        return fetch.then(check, reset).then(function () { return state; });
    }
};
/**
 * Export the plugins as default.
 */
var plugins = [
    linkerPlugin, layoutPlugin, palettePlugin, mainMenuPlugin, stateDBPlugin
];
exports.default = plugins;

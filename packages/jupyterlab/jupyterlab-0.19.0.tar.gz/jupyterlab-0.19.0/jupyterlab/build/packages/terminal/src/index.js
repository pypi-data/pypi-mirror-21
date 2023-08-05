// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
"use strict";
function __export(m) {
    for (var p in m) if (!exports.hasOwnProperty(p)) exports[p] = m[p];
}
Object.defineProperty(exports, "__esModule", { value: true });
var coreutils_1 = require("@phosphor/coreutils");
var widget_1 = require("./widget");
__export(require("./widget"));
/* tslint:disable */
/**
 * The editor tracker token.
 */
exports.ITerminalTracker = new coreutils_1.Token('jupyter.services.terminal-tracker');
/* tslint:enable */
/**
 * Add the default commands for the editor.
 */
function addDefaultCommands(tracker, commands) {
    commands.addCommand('terminal:increase-font', {
        label: 'Increase Terminal Font Size',
        execute: function () {
            var options = widget_1.TerminalWidget.defaultOptions;
            if (options.fontSize < 72) {
                options.fontSize++;
                tracker.forEach(function (widget) { widget.fontSize = options.fontSize; });
            }
        }
    });
    commands.addCommand('terminal:decrease-font', {
        label: 'Decrease Terminal Font Size',
        execute: function () {
            var options = widget_1.TerminalWidget.defaultOptions;
            if (options.fontSize > 9) {
                options.fontSize--;
                tracker.forEach(function (widget) { widget.fontSize = options.fontSize; });
            }
        }
    });
    commands.addCommand('terminal:toggle-theme', {
        label: 'Toggle Terminal Theme',
        caption: 'Switch Terminal Background and Font Colors',
        execute: function () {
            var options = widget_1.TerminalWidget.defaultOptions;
            if (options.background === 'black') {
                options.background = 'white';
                options.color = 'black';
            }
            else {
                options.background = 'black';
                options.color = 'white';
            }
            tracker.forEach(function (widget) {
                widget.background = options.background;
                widget.color = options.color;
            });
        }
    });
}
exports.addDefaultCommands = addDefaultCommands;

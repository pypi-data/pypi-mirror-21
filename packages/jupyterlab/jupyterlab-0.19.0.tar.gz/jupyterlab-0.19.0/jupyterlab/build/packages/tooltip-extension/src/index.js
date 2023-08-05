// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var widgets_1 = require("@phosphor/widgets");
var console_1 = require("@jupyterlab/console");
var notebook_1 = require("@jupyterlab/notebook");
var tooltip_1 = require("@jupyterlab/tooltip");
/**
 * The command IDs used by the tooltip plugin.
 */
var CommandIDs;
(function (CommandIDs) {
    CommandIDs.launchConsole = 'tooltip:launch-console';
    CommandIDs.launchNotebook = 'tooltip:launch-notebook';
})(CommandIDs || (CommandIDs = {}));
;
/**
 * The main tooltip service.
 */
var service = {
    id: 'jupyter.services.tooltip',
    autoStart: true,
    provides: tooltip_1.ITooltipManager,
    activate: function (app) {
        var tooltip = null;
        return {
            invoke: function (options) {
                var detail = 0;
                var anchor = options.anchor, editor = options.editor, kernel = options.kernel, rendermime = options.rendermime;
                if (tooltip) {
                    tooltip.dispose();
                    tooltip = null;
                }
                return Private.fetch({ detail: detail, editor: editor, kernel: kernel }).then(function (bundle) {
                    tooltip = new tooltip_1.TooltipWidget({ anchor: anchor, bundle: bundle, editor: editor, rendermime: rendermime });
                    widgets_1.Widget.attach(tooltip, document.body);
                }).catch(function () { });
            }
        };
    }
};
/**
 * The console tooltip plugin.
 */
var consolePlugin = {
    id: 'jupyter.extensions.tooltip-console',
    autoStart: true,
    requires: [tooltip_1.ITooltipManager, console_1.IConsoleTracker],
    activate: function (app, manager, consoles) {
        // Add tooltip launch command.
        app.commands.addCommand(CommandIDs.launchConsole, {
            execute: function () {
                var parent = consoles.currentWidget;
                if (!parent) {
                    return;
                }
                var anchor = parent.console;
                var editor = anchor.prompt.editor;
                var kernel = anchor.session.kernel;
                var rendermime = anchor.rendermime;
                // If all components necessary for rendering exist, create a tooltip.
                if (!!editor && !!kernel && !!rendermime) {
                    return manager.invoke({ anchor: anchor, editor: editor, kernel: kernel, rendermime: rendermime });
                }
            }
        });
    }
};
/**
 * The notebook tooltip plugin.
 */
var notebookPlugin = {
    id: 'jupyter.extensions.tooltip-notebook',
    autoStart: true,
    requires: [tooltip_1.ITooltipManager, notebook_1.INotebookTracker],
    activate: function (app, manager, notebooks) {
        // Add tooltip launch command.
        app.commands.addCommand(CommandIDs.launchNotebook, {
            execute: function () {
                var parent = notebooks.currentWidget;
                if (!parent) {
                    return;
                }
                var anchor = parent.notebook;
                var editor = anchor.activeCell.editor;
                var kernel = parent.session.kernel;
                var rendermime = parent.rendermime;
                // If all components necessary for rendering exist, create a tooltip.
                if (!!editor && !!kernel && !!rendermime) {
                    return manager.invoke({ anchor: anchor, editor: editor, kernel: kernel, rendermime: rendermime });
                }
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
     * A counter for outstanding requests.
     */
    var pending = 0;
    /**
     * Fetch a tooltip's content from the API server.
     */
    function fetch(options) {
        var detail = options.detail, editor = options.editor, kernel = options.kernel;
        var code = editor.model.value.text;
        var position = editor.getCursorPosition();
        var offset = editor.getOffsetAt(position);
        // Clear hints if the new text value is empty or kernel is unavailable.
        if (!code || !kernel) {
            return Promise.reject(void 0);
        }
        var contents = {
            code: code,
            cursor_pos: offset,
            detail_level: detail || 0
        };
        var current = ++pending;
        return kernel.requestInspect(contents).then(function (msg) {
            var value = msg.content;
            // If a newer request is pending, bail.
            if (current !== pending) {
                return Promise.reject(void 0);
            }
            // If request fails or returns negative results, bail.
            if (value.status !== 'ok' || !value.found) {
                return Promise.reject(void 0);
            }
            return Promise.resolve(value.data);
        });
    }
    Private.fetch = fetch;
})(Private || (Private = {}));

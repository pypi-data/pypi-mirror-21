// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
"use strict";
function __export(m) {
    for (var p in m) if (!exports.hasOwnProperty(p)) exports[p] = m[p];
}
Object.defineProperty(exports, "__esModule", { value: true });
var coreutils_1 = require("@phosphor/coreutils");
var properties_1 = require("@phosphor/properties");
__export(require("./widget"));
/* tslint:disable */
/**
 * The editor tracker token.
 */
exports.IEditorTracker = new coreutils_1.Token('jupyter.services.editor-tracker');
/* tslint:enable */
/**
 * Add the default commands for the editor.
 */
function addDefaultCommands(tracker, commands) {
    /**
     * Toggle editor line numbers
     */
    function toggleLineNums(args) {
        var widget = tracker.currentWidget;
        if (!widget) {
            return;
        }
        widget.editor.lineNumbers = !widget.editor.lineNumbers;
        if (args['activate'] !== false) {
            widget.activate();
        }
    }
    /**
     * Toggle editor line wrap
     */
    function toggleLineWrap(args) {
        var widget = tracker.currentWidget;
        if (!widget) {
            return;
        }
        widget.editor.wordWrap = !widget.editor.wordWrap;
        if (args['activate'] !== false) {
            widget.activate();
        }
    }
    /**
     * An attached property for the session id associated with an editor widget.
     */
    var sessionIdProperty = new properties_1.AttachedProperty({
        name: 'sessionId',
        create: function () { return ''; }
    });
    commands.addCommand('editor:line-numbers', {
        execute: function (args) { toggleLineNums(args); },
        label: 'Toggle Line Numbers'
    });
    commands.addCommand('editor:line-wrap', {
        execute: function (args) { toggleLineWrap(args); },
        label: 'Toggle Line Wrap'
    });
    commands.addCommand('editor:create-console', {
        execute: function (args) {
            var widget = tracker.currentWidget;
            if (!widget) {
                return;
            }
            var options = {
                path: widget.context.path,
                preferredLanguage: widget.context.model.defaultKernelLanguage,
                activate: args['activate']
            };
            return commands.execute('console:create', options)
                .then(function (id) { sessionIdProperty.set(widget, id); });
        },
        label: 'Create Console for Editor'
    });
    commands.addCommand('editor:run-code', {
        execute: function (args) {
            var widget = tracker.currentWidget;
            if (!widget) {
                return;
            }
            // Get the session id.
            var id = sessionIdProperty.get(widget);
            if (!id) {
                return;
            }
            // Get the selected code from the editor.
            var editor = widget.editor;
            var selection = editor.getSelection();
            var start = editor.getOffsetAt(selection.start);
            var end = editor.getOffsetAt(selection.end);
            var options = {
                id: id,
                code: editor.model.value.text.substring(start, end),
                activate: args['activate']
            };
            return commands.execute('console:inject', options);
        },
        label: 'Run Code'
    });
}
exports.addDefaultCommands = addDefaultCommands;

// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var editor_1 = require("./editor");
/**
 * CodeMirror editor factory.
 */
var CodeMirrorEditorFactory = (function () {
    /**
     * Construct an IEditorFactoryService for CodeMirrorEditors.
     */
    function CodeMirrorEditorFactory(codeMirrorOptions) {
        this.inlineCodeMirrorOptions = {
            extraKeys: {
                'Cmd-Right': 'goLineRight',
                'End': 'goLineRight',
                'Cmd-Left': 'goLineLeft',
                'Tab': 'indentMore',
                'Shift-Tab': 'indentLess',
                'Cmd-Alt-[': 'indentAuto',
                'Ctrl-Alt-[': 'indentAuto',
                'Cmd-/': 'toggleComment',
                'Ctrl-/': 'toggleComment',
            }
        };
        this.documentCodeMirrorOptions = {
            extraKeys: {
                'Tab': 'indentMore',
                'Shift-Enter': function () { }
            },
            lineNumbers: true,
            lineWrapping: true
        };
        if (codeMirrorOptions !== undefined) {
            // Note: If codeMirrorOptions include `extraKeys`,
            // existing option will be overwritten.
            Private.assign(this.inlineCodeMirrorOptions, codeMirrorOptions);
            Private.assign(this.documentCodeMirrorOptions, codeMirrorOptions);
        }
    }
    /**
     * Create a new editor for inline code.
     */
    CodeMirrorEditorFactory.prototype.newInlineEditor = function (options) {
        return new editor_1.CodeMirrorEditor(options, this.inlineCodeMirrorOptions);
    };
    /**
     * Create a new editor for a full document.
     */
    CodeMirrorEditorFactory.prototype.newDocumentEditor = function (options) {
        return new editor_1.CodeMirrorEditor(options, this.documentCodeMirrorOptions);
    };
    return CodeMirrorEditorFactory;
}());
exports.CodeMirrorEditorFactory = CodeMirrorEditorFactory;
var Private;
(function (Private) {
    // Replace with Object.assign when available.
    function assign(target) {
        var configs = [];
        for (var _i = 1; _i < arguments.length; _i++) {
            configs[_i - 1] = arguments[_i];
        }
        var _loop_1 = function (source) {
            if (source) {
                Object.keys(source).forEach(function (key) {
                    target[key] = source[key];
                });
            }
        };
        for (var _a = 0, configs_1 = configs; _a < configs_1.length; _a++) {
            var source = configs_1[_a];
            _loop_1(source);
        }
        return target;
    }
    Private.assign = assign;
})(Private || (Private = {}));

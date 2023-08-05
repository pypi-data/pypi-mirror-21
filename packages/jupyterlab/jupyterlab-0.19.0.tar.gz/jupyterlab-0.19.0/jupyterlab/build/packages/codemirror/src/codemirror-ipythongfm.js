// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var CodeMirror = require("codemirror");
require("codemirror/mode/stex/stex");
require("codemirror/mode/gfm/gfm");
require("codemirror/addon/mode/multiplex");
/**
 * Define an IPython GFM (GitHub Flavored Markdown) mode.
 *
 * Is just a slightly altered GFM Mode with support for latex.
 * Latex support was supported by Codemirror GFM as of
 *   https://github.com/codemirror/CodeMirror/pull/567
 *  But was later removed in
 *   https://github.com/codemirror/CodeMirror/commit/d9c9f1b1ffe984aee41307f3e927f80d1f23590c
 */
CodeMirror.defineMode('ipythongfm', function (config, modeOptions) {
    var gfmMode = CodeMirror.getMode(config, 'gfm');
    var texMode = CodeMirror.getMode(config, 'stex');
    return CodeMirror.multiplexingMode(gfmMode, {
        open: '$', close: '$',
        mode: texMode,
        delimStyle: 'delimit'
    }, {
        // not sure this works as $$ is interpreted at (opening $, closing $, as defined just above)
        open: '$$', close: '$$',
        mode: texMode,
        delimStyle: 'delimit'
    }, {
        open: '\\(', close: '\\)',
        mode: texMode,
        delimStyle: 'delimit'
    }, {
        open: '\\[', close: '\\]',
        mode: texMode,
        delimStyle: 'delimit'
    }
    // .. more multiplexed styles can follow here
    );
}, 'gfm');
CodeMirror.defineMIME('text/x-ipythongfm', 'ipythongfm');
CodeMirror.modeInfo.push({
    ext: [],
    mime: 'text/x-ipythongfm',
    mode: 'ipythongfm',
    name: 'ipythongfm'
});

// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var CodeMirror = require("codemirror");
require("codemirror/mode/meta");
require("codemirror/mode/python/python");
/**
 * Define an IPython codemirror mode.
 *
 * It is a slightly altered Python Mode with a `?` operator.
 */
CodeMirror.defineMode('ipython', function (config, modeOptions) {
    var pythonConf = {};
    for (var prop in modeOptions) {
        if (modeOptions.hasOwnProperty(prop)) {
            pythonConf[prop] = modeOptions[prop];
        }
    }
    pythonConf.name = 'python';
    pythonConf.singleOperators = new RegExp('^[\\+\\-\\*/%&|@\\^~<>!\\?]');
    pythonConf.identifiers = new RegExp('^[_A-Za-z\u00A1-\uFFFF][_A-Za-z0-9\u00A1-\uFFFF]*');
    return CodeMirror.getMode(config, pythonConf);
}, 'python');
CodeMirror.defineMIME('text/x-ipython', 'ipython');
CodeMirror.modeInfo.push({
    ext: [],
    mime: 'text/x-ipython',
    mode: 'ipython',
    name: 'ipython'
});

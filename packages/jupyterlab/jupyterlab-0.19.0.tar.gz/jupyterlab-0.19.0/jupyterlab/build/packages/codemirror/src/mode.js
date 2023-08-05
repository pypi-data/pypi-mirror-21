// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var CodeMirror = require("codemirror");
require("codemirror/mode/meta");
require("codemirror/addon/runmode/runmode");
require("./codemirror-ipython");
require("./codemirror-ipythongfm");
// Bundle other common modes
require("codemirror/mode/javascript/javascript");
require("codemirror/mode/css/css");
require("codemirror/mode/julia/julia");
require("codemirror/mode/r/r");
require("codemirror/mode/markdown/markdown");
/**
 * Running a CodeMirror mode outside of an editor.
 */
function runMode(code, mode, el) {
    CodeMirror.runMode(code, mode, el);
}
exports.runMode = runMode;
/**
 * Find a mode name by extension.
 */
function findModeByExtension(ext) {
    var mode = CodeMirror.findModeByExtension(ext);
    return mode && mode.mode;
}
exports.findModeByExtension = findModeByExtension;
/**
 * Load a codemirror mode by file name.
 */
function loadModeByFileName(editor, filename) {
    loadInfo(editor, CodeMirror.findModeByFileName(filename));
}
exports.loadModeByFileName = loadModeByFileName;
/**
 * Load a codemirror mode by mime type.
 */
function loadModeByMIME(editor, mimetype) {
    loadInfo(editor, CodeMirror.findModeByMIME(mimetype));
}
exports.loadModeByMIME = loadModeByMIME;
/**
 * Load a codemirror mode by mode name.
 */
function loadModeByName(editor, mode) {
    loadInfo(editor, CodeMirror.findModeByName(mode));
}
exports.loadModeByName = loadModeByName;
/**
 * Find a codemirror mode by name or CodeMirror spec.
 */
function findMode(mode) {
    var modename = (typeof mode === 'string') ? mode :
        mode.mode || mode.name;
    var mimetype = (typeof mode !== 'string') ? mode.mime : '';
    return (CodeMirror.findModeByName(modename) ||
        CodeMirror.findModeByMIME(mimetype) ||
        CodeMirror.modes['null']);
}
exports.findMode = findMode;
/**
 * Require a codemirror mode by name or Codemirror spec.
 */
function requireMode(mode) {
    var info = findMode(mode);
    // Simplest, cheapest check by mode name.
    if (CodeMirror.modes.hasOwnProperty(info.mode)) {
        return Promise.resolve(info);
    }
    // Fetch the mode asynchronously.
    return new Promise(function (resolve, reject) {
        require(["codemirror/mode/" + info.mode + "/" + info.mode + ".js"], function () {
            resolve(info);
        });
    });
}
exports.requireMode = requireMode;
/**
 * Load a CodeMirror mode based on a mode spec.
 */
function loadInfo(editor, info) {
    if (!info) {
        editor.setOption('mode', 'null');
        return;
    }
    requireMode(info).then(function () {
        editor.setOption('mode', info.mime);
    });
}

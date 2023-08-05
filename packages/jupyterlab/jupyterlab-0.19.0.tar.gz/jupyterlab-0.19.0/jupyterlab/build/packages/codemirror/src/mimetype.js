// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var CodeMirror = require("codemirror");
var codeeditor_1 = require("@jupyterlab/codeeditor");
var _1 = require(".");
/**
 * The mime type service for CodeMirror.
 */
var CodeMirrorMimeTypeService = (function () {
    function CodeMirrorMimeTypeService() {
    }
    /**
     * Returns a mime type for the given language info.
     *
     * #### Notes
     * If a mime type cannot be found returns the defaul mime type `text/plain`, never `null`.
     */
    CodeMirrorMimeTypeService.prototype.getMimeTypeByLanguage = function (info) {
        if (info.codemirror_mode) {
            return _1.findMode(info.codemirror_mode).mime;
        }
        var mode = CodeMirror.findModeByMIME(info.mimetype || '');
        if (mode) {
            return info.mimetype;
        }
        var ext = info.file_extension || '';
        ext = ext.split('.').slice(-1)[0];
        mode = CodeMirror.findModeByExtension(ext || '');
        if (mode) {
            return mode.mime;
        }
        mode = CodeMirror.findModeByName(info.name || '');
        return mode ? mode.mime : codeeditor_1.IEditorMimeTypeService.defaultMimeType;
    };
    /**
     * Returns a mime type for the given file path.
     *
     * #### Notes
     * If a mime type cannot be found returns the defaul mime type `text/plain`, never `null`.
     */
    CodeMirrorMimeTypeService.prototype.getMimeTypeByFilePath = function (path) {
        var mode = CodeMirror.findModeByFileName(path);
        return mode ? mode.mime : codeeditor_1.IEditorMimeTypeService.defaultMimeType;
    };
    return CodeMirrorMimeTypeService;
}());
exports.CodeMirrorMimeTypeService = CodeMirrorMimeTypeService;

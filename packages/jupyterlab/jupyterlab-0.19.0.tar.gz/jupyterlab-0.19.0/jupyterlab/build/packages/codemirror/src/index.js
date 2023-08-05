// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
"use strict";
function __export(m) {
    for (var p in m) if (!exports.hasOwnProperty(p)) exports[p] = m[p];
}
Object.defineProperty(exports, "__esModule", { value: true });
var factory_1 = require("./factory");
var mimetype_1 = require("./mimetype");
__export(require("./mode"));
__export(require("./editor"));
__export(require("./factory"));
__export(require("./mimetype"));
/**
 * The default editor services.
 */
exports.editorServices = {
    factoryService: new factory_1.CodeMirrorEditorFactory(),
    mimeTypeService: new mimetype_1.CodeMirrorMimeTypeService()
};

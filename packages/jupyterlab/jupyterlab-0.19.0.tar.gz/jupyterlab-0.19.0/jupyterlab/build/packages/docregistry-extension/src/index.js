// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var docregistry_1 = require("@jupyterlab/docregistry");
/**
 * The default document registry provider.
 */
var plugin = {
    id: 'jupyter.services.document-registry',
    provides: docregistry_1.IDocumentRegistry,
    activate: function () {
        var registry = new docregistry_1.DocumentRegistry();
        registry.addModelFactory(new docregistry_1.TextModelFactory());
        registry.addModelFactory(new docregistry_1.Base64ModelFactory());
        registry.addFileType({
            name: 'Text',
            extension: '.txt',
            contentType: 'file',
            fileFormat: 'text'
        });
        registry.addCreator({ name: 'Text File', fileType: 'Text', });
        return registry;
    }
};
/**
 * Export the plugin as default.
 */
exports.default = plugin;

// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var docmanager_1 = require("@jupyterlab/docmanager");
var docregistry_1 = require("@jupyterlab/docregistry");
var services_1 = require("@jupyterlab/services");
/**
 * The default document manager provider.
 */
var plugin = {
    id: 'jupyter.services.document-manager',
    provides: docmanager_1.IDocumentManager,
    requires: [services_1.IServiceManager, docregistry_1.IDocumentRegistry],
    activate: function (app, manager, registry) {
        var id = 1;
        var opener = {
            open: function (widget) {
                if (!widget.id) {
                    widget.id = "document-manager-" + ++id;
                }
                if (!widget.isAttached) {
                    app.shell.addToMainArea(widget);
                }
                app.shell.activateById(widget.id);
            }
        };
        return new docmanager_1.DocumentManager({ registry: registry, manager: manager, opener: opener });
    }
};
/**
 * Export the plugin as default.
 */
exports.default = plugin;

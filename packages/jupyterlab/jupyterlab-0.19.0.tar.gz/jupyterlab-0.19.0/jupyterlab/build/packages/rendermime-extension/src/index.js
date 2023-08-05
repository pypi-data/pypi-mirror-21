// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var apputils_1 = require("@jupyterlab/apputils");
var coreutils_1 = require("@jupyterlab/coreutils");
var rendermime_1 = require("@jupyterlab/rendermime");
/**
 * The default rendermime provider.
 */
var plugin = {
    id: 'jupyter.services.rendermime',
    requires: [apputils_1.ICommandLinker],
    provides: rendermime_1.IRenderMime,
    activate: activate,
    autoStart: true
};
/**
 * Export the plugin as default.
 */
exports.default = plugin;
/**
 * Activate the rendermine plugin.
 */
function activate(app, linker) {
    var linkHandler = {
        handleLink: function (node, path) {
            if (!coreutils_1.URLExt.parse(path).protocol && path.indexOf('//') !== 0) {
                linker.connectNode(node, 'file-operations:open', { path: path });
            }
        }
    };
    var items = rendermime_1.RenderMime.getDefaultItems();
    return new rendermime_1.RenderMime({ items: items, linkHandler: linkHandler });
}
;

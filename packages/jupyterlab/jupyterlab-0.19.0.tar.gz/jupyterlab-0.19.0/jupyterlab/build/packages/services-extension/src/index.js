// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var services_1 = require("@jupyterlab/services");
/**
 * The default services provider.
 */
var plugin = {
    id: 'jupyter.services.services',
    provides: services_1.IServiceManager,
    activate: function () { return new services_1.ServiceManager(); }
};
/**
 * Export the plugin as default.
 */
exports.default = plugin;

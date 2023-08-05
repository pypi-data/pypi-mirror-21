// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
"use strict";
var __extends = (this && this.__extends) || (function () {
    var extendStatics = Object.setPrototypeOf ||
        ({ __proto__: [] } instanceof Array && function (d, b) { d.__proto__ = b; }) ||
        function (d, b) { for (var p in b) if (b.hasOwnProperty(p)) d[p] = b[p]; };
    return function (d, b) {
        extendStatics(d, b);
        function __() { this.constructor = d; }
        d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
var application_1 = require("@phosphor/application");
var shell_1 = require("./shell");
var loader_1 = require("./loader");
exports.ModuleLoader = loader_1.ModuleLoader;
var shell_2 = require("./shell");
exports.ApplicationShell = shell_2.ApplicationShell;
/**
 * JupyterLab is the main application class. It is instantiated once and shared.
 */
var JupyterLab = (function (_super) {
    __extends(JupyterLab, _super);
    /**
     * Construct a new JupyterLab object.
     */
    function JupyterLab(options) {
        if (options === void 0) { options = {}; }
        var _this = _super.call(this, { shell: new shell_1.ApplicationShell() }) || this;
        _this._info = {
            gitDescription: options.gitDescription || 'unknown',
            namespace: options.namespace || 'jupyterlab',
            version: options.version || 'unknown'
        };
        _this._loader = options.loader || null;
        return _this;
    }
    Object.defineProperty(JupyterLab.prototype, "info", {
        /**
         * The information about the application.
         */
        get: function () {
            return this._info;
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(JupyterLab.prototype, "loader", {
        /**
         * The module loader used by the application.
         */
        get: function () {
            return this._loader;
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(JupyterLab.prototype, "restored", {
        /**
         * Promise that resolves when state is restored, returning layout description.
         *
         * #### Notes
         * This is just a reference to `shell.restored`.
         */
        get: function () {
            return this.shell.restored;
        },
        enumerable: true,
        configurable: true
    });
    /**
     * Register plugins from a plugin module.
     *
     * @param mod - The plugin module to register.
     */
    JupyterLab.prototype.registerPluginModule = function (mod) {
        var _this = this;
        var data = mod.default;
        if (!Array.isArray(data)) {
            data = [data];
        }
        data.forEach(function (item) { _this.registerPlugin(item); });
    };
    /**
     * Register the plugins from multiple plugin modules.
     *
     * @param mods - The plugin modules to register.
     */
    JupyterLab.prototype.registerPluginModules = function (mods) {
        var _this = this;
        mods.forEach(function (mod) { _this.registerPluginModule(mod); });
    };
    return JupyterLab;
}(application_1.Application));
exports.JupyterLab = JupyterLab;

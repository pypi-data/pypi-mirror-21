// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var algorithm_1 = require("@phosphor/algorithm");
var coreutils_1 = require("@phosphor/coreutils");
var disposable_1 = require("@phosphor/disposable");
var signaling_1 = require("@phosphor/signaling");
var coreutils_2 = require("@jupyterlab/coreutils");
/* tslint:disable */
/**
 * The document registry token.
 */
exports.IDocumentRegistry = new coreutils_1.Token('jupyter.services.document-registry');
/**
 * The document registry.
 */
var DocumentRegistry = (function () {
    function DocumentRegistry() {
        this._modelFactories = Object.create(null);
        this._widgetFactories = Object.create(null);
        this._defaultWidgetFactory = '';
        this._defaultWidgetFactories = Object.create(null);
        this._widgetFactoryExtensions = Object.create(null);
        this._fileTypes = [];
        this._creators = [];
        this._extenders = Object.create(null);
        this._changed = new signaling_1.Signal(this);
    }
    Object.defineProperty(DocumentRegistry.prototype, "changed", {
        /**
         * A signal emitted when the registry has changed.
         */
        get: function () {
            return this._changed;
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(DocumentRegistry.prototype, "isDisposed", {
        /**
         * Get whether the document registry has been disposed.
         */
        get: function () {
            return this._widgetFactories === null;
        },
        enumerable: true,
        configurable: true
    });
    /**
     * Dispose of the resources held by the document registery.
     */
    DocumentRegistry.prototype.dispose = function () {
        if (this._widgetFactories === null) {
            return;
        }
        var widgetFactories = this._widgetFactories;
        var modelFactories = this._modelFactories;
        var extenders = this._extenders;
        this._widgetFactories = null;
        this._modelFactories = null;
        this._extenders = null;
        for (var modelName in modelFactories) {
            modelFactories[modelName].dispose();
        }
        for (var widgetName in widgetFactories) {
            widgetFactories[widgetName].dispose();
        }
        for (var widgetName in extenders) {
            extenders[widgetName].length = 0;
        }
        this._fileTypes.length = 0;
        this._creators.length = 0;
        signaling_1.Signal.clearData(this);
    };
    /**
     * Add a widget factory to the registry.
     *
     * @param factory - The factory instance to register.
     *
     * @returns A disposable which will unregister the factory.
     *
     * #### Notes
     * If a factory with the given `'displayName'` is already registered,
     * a warning will be logged, and this will be a no-op.
     * If `'*'` is given as a default extension, the factory will be registered
     * as the global default.
     * If an extension or global default is already registered, this factory
     * will override the existing default.
     */
    DocumentRegistry.prototype.addWidgetFactory = function (factory) {
        var _this = this;
        var name = factory.name.toLowerCase();
        if (this._widgetFactories[name]) {
            console.warn("Duplicate registered factory " + name);
            return new disposable_1.DisposableDelegate(null);
        }
        this._widgetFactories[name] = factory;
        for (var _i = 0, _a = factory.defaultFor; _i < _a.length; _i++) {
            var ext = _a[_i];
            if (factory.fileExtensions.indexOf(ext) === -1) {
                continue;
            }
            if (ext === '*') {
                this._defaultWidgetFactory = name;
            }
            else {
                this._defaultWidgetFactories[ext] = name;
            }
        }
        // For convenience, store a mapping of ext -> name
        for (var _b = 0, _c = factory.fileExtensions; _b < _c.length; _b++) {
            var ext = _c[_b];
            if (!this._widgetFactoryExtensions[ext]) {
                this._widgetFactoryExtensions[ext] = [];
            }
            this._widgetFactoryExtensions[ext].push(name);
        }
        this._changed.emit({
            type: 'widgetFactory',
            name: name,
            change: 'added'
        });
        return new disposable_1.DisposableDelegate(function () {
            delete _this._widgetFactories[name];
            if (_this._defaultWidgetFactory === name) {
                _this._defaultWidgetFactory = '';
            }
            for (var _i = 0, _a = Object.keys(_this._defaultWidgetFactories); _i < _a.length; _i++) {
                var ext = _a[_i];
                if (_this._defaultWidgetFactories[ext] === name) {
                    delete _this._defaultWidgetFactories[ext];
                }
            }
            for (var _b = 0, _c = Object.keys(_this._widgetFactoryExtensions); _b < _c.length; _b++) {
                var ext = _c[_b];
                algorithm_1.ArrayExt.removeFirstOf(_this._widgetFactoryExtensions[ext], name);
                if (_this._widgetFactoryExtensions[ext].length === 0) {
                    delete _this._widgetFactoryExtensions[ext];
                }
            }
            _this._changed.emit({
                type: 'widgetFactory',
                name: name,
                change: 'removed'
            });
        });
    };
    /**
     * Add a model factory to the registry.
     *
     * @param factory - The factory instance.
     *
     * @returns A disposable which will unregister the factory.
     *
     * #### Notes
     * If a factory with the given `name` is already registered, or
     * the given factory is already registered, a warning will be logged
     * and this will be a no-op.
     */
    DocumentRegistry.prototype.addModelFactory = function (factory) {
        var _this = this;
        var name = factory.name.toLowerCase();
        if (this._modelFactories[name]) {
            console.warn("Duplicate registered factory " + name);
            return new disposable_1.DisposableDelegate(null);
        }
        this._modelFactories[name] = factory;
        this._changed.emit({
            type: 'modelFactory',
            name: name,
            change: 'added'
        });
        return new disposable_1.DisposableDelegate(function () {
            delete _this._modelFactories[name];
            _this._changed.emit({
                type: 'modelFactory',
                name: name,
                change: 'removed'
            });
        });
    };
    /**
     * Add a widget extension to the registry.
     *
     * @param widgetName - The name of the widget factory.
     *
     * @param extension - A widget extension.
     *
     * @returns A disposable which will unregister the extension.
     *
     * #### Notes
     * If the extension is already registered for the given
     * widget name, a warning will be logged and this will be a no-op.
     */
    DocumentRegistry.prototype.addWidgetExtension = function (widgetName, extension) {
        var _this = this;
        widgetName = widgetName.toLowerCase();
        if (!(widgetName in this._extenders)) {
            this._extenders[widgetName] = [];
        }
        var extenders = this._extenders[widgetName];
        var index = algorithm_1.ArrayExt.firstIndexOf(extenders, extension);
        if (index !== -1) {
            console.warn("Duplicate registered extension for " + widgetName);
            return new disposable_1.DisposableDelegate(null);
        }
        this._extenders[widgetName].push(extension);
        this._changed.emit({
            type: 'widgetExtension',
            name: null,
            change: 'added'
        });
        return new disposable_1.DisposableDelegate(function () {
            algorithm_1.ArrayExt.removeFirstOf(_this._extenders[widgetName], extension);
            _this._changed.emit({
                type: 'widgetExtension',
                name: null,
                change: 'removed'
            });
        });
    };
    /**
     * Add a file type to the document registry.
     *
     * @params fileType - The file type object to register.
     *
     * @returns A disposable which will unregister the command.
     *
     * #### Notes
     * These are used to populate the "Create New" dialog.
     */
    DocumentRegistry.prototype.addFileType = function (fileType) {
        var _this = this;
        this._fileTypes.push(fileType);
        this._changed.emit({
            type: 'fileType',
            name: fileType.name,
            change: 'added'
        });
        return new disposable_1.DisposableDelegate(function () {
            algorithm_1.ArrayExt.removeFirstOf(_this._fileTypes, fileType);
            _this._changed.emit({
                type: 'fileType',
                name: fileType.name,
                change: 'removed'
            });
        });
    };
    /**
     * Add a creator to the registry.
     *
     * @params creator - The file creator object to register.
     *
     * @returns A disposable which will unregister the creator.
     */
    DocumentRegistry.prototype.addCreator = function (creator) {
        var _this = this;
        var index = algorithm_1.ArrayExt.findFirstIndex(this._creators, function (value) {
            return value.name.localeCompare(creator.name) > 0;
        });
        if (index !== -1) {
            algorithm_1.ArrayExt.insert(this._creators, index, creator);
        }
        else {
            this._creators.push(creator);
        }
        this._changed.emit({
            type: 'fileCreator',
            name: creator.name,
            change: 'added'
        });
        return new disposable_1.DisposableDelegate(function () {
            algorithm_1.ArrayExt.removeFirstOf(_this._creators, creator);
            _this._changed.emit({
                type: 'fileCreator',
                name: creator.name,
                change: 'removed'
            });
        });
    };
    /**
     * Get a list of the preferred widget factories.
     *
     * @param ext - An optional file extension to filter the results.
     *
     * @returns A new array of widget factories.
     *
     * #### Notes
     * Only the widget factories whose associated model factory have
     * been registered will be returned.
     * The first item is considered the default. The returned iterator
     * has widget factories in the following order:
     * - extension-specific default factory
     * - global default factory
     * - all other extension-specific factories
     * - all other global factories
     */
    DocumentRegistry.prototype.preferredWidgetFactories = function (ext) {
        var _this = this;
        if (ext === void 0) { ext = '*'; }
        var factories = new Set();
        ext = Private.normalizeExtension(ext);
        var last = '.' + ext.split('.').pop();
        // Start with the extension-specific default factory.
        if (ext.length > 1) {
            if (ext in this._defaultWidgetFactories) {
                factories.add(this._defaultWidgetFactories[ext]);
            }
        }
        // Handle multi-part extension default factories.
        if (last !== ext) {
            if (last in this._defaultWidgetFactories) {
                factories.add(this._defaultWidgetFactories[last]);
            }
        }
        // Add the global default factory.
        if (this._defaultWidgetFactory) {
            factories.add(this._defaultWidgetFactory);
        }
        // Add the extension-specific factories in registration order.
        if (ext.length > 1) {
            if (ext in this._widgetFactoryExtensions) {
                algorithm_1.each(this._widgetFactoryExtensions[ext], function (n) {
                    factories.add(n);
                });
            }
        }
        // Handle multi-part extension-specific factories.
        if (last !== ext) {
            if (last in this._widgetFactoryExtensions) {
                algorithm_1.each(this._widgetFactoryExtensions[last], function (n) {
                    factories.add(n);
                });
            }
        }
        // Add the rest of the global factories, in registration order.
        if ('*' in this._widgetFactoryExtensions) {
            algorithm_1.each(this._widgetFactoryExtensions['*'], function (n) {
                factories.add(n);
            });
        }
        // Construct the return list, checking to make sure the corresponding
        // model factories are registered.
        var factoryList = [];
        factories.forEach(function (name) {
            if (_this._widgetFactories[name].modelName in _this._modelFactories) {
                factoryList.push(_this._widgetFactories[name]);
            }
        });
        return factoryList;
    };
    /**
     * Get the default widget factory for an extension.
     *
     * @param ext - An optional file extension to filter the results.
     *
     * @returns The default widget factory for an extension.
     *
     * #### Notes
     * This is equivalent to the first value in [[preferredWidgetFactories]].
     */
    DocumentRegistry.prototype.defaultWidgetFactory = function (ext) {
        if (ext === void 0) { ext = '*'; }
        return this.preferredWidgetFactories(ext)[0];
    };
    /**
     * Create an iterator over the widget factories that have been registered.
     *
     * @returns A new iterator of widget factories.
     */
    DocumentRegistry.prototype.widgetFactories = function () {
        var _this = this;
        return algorithm_1.map(Object.keys(this._widgetFactories), function (name) {
            return _this._widgetFactories[name];
        });
    };
    /**
     * Create an iterator over the model factories that have been registered.
     *
     * @returns A new iterator of model factories.
     */
    DocumentRegistry.prototype.modelFactories = function () {
        var _this = this;
        return algorithm_1.map(Object.keys(this._modelFactories), function (name) {
            return _this._modelFactories[name];
        });
    };
    /**
     * Create an iterator over the registered extensions for a given widget.
     *
     * @param widgetName - The name of the widget factory.
     *
     * @returns A new iterator over the widget extensions.
     */
    DocumentRegistry.prototype.widgetExtensions = function (widgetName) {
        widgetName = widgetName.toLowerCase();
        if (!(widgetName in this._extenders)) {
            return algorithm_1.empty();
        }
        return new algorithm_1.ArrayIterator(this._extenders[widgetName]);
    };
    /**
     * Create an iterator over the file types that have been registered.
     *
     * @returns A new iterator of file types.
     */
    DocumentRegistry.prototype.fileTypes = function () {
        return new algorithm_1.ArrayIterator(this._fileTypes);
    };
    /**
     * Create an iterator over the file creators that have been registered.
     *
     * @returns A new iterator of file creatores.
     */
    DocumentRegistry.prototype.creators = function () {
        return new algorithm_1.ArrayIterator(this._creators);
    };
    /**
     * Get a widget factory by name.
     *
     * @param widgetName - The name of the widget factory.
     *
     * @returns A widget factory instance.
     */
    DocumentRegistry.prototype.getWidgetFactory = function (widgetName) {
        return this._widgetFactories[widgetName.toLowerCase()];
    };
    /**
     * Get a model factory by name.
     *
     * @param name - The name of the model factory.
     *
     * @returns A model factory instance.
     */
    DocumentRegistry.prototype.getModelFactory = function (name) {
        return this._modelFactories[name.toLowerCase()];
    };
    /**
     * Get a file type by name.
     */
    DocumentRegistry.prototype.getFileType = function (name) {
        name = name.toLowerCase();
        return algorithm_1.find(this._fileTypes, function (fileType) {
            return fileType.name.toLowerCase() === name;
        });
    };
    /**
     * Get a creator by name.
     */
    DocumentRegistry.prototype.getCreator = function (name) {
        name = name.toLowerCase();
        return algorithm_1.find(this._creators, function (creator) {
            return creator.name.toLowerCase() === name;
        });
    };
    /**
     * Get a kernel preference.
     *
     * @param ext - The file extension.
     *
     * @param widgetName - The name of the widget factory.
     *
     * @param kernel - An optional existing kernel model.
     *
     * @returns A kernel preference.
     */
    DocumentRegistry.prototype.getKernelPreference = function (ext, widgetName, kernel) {
        ext = Private.normalizeExtension(ext);
        widgetName = widgetName.toLowerCase();
        var widgetFactory = this._widgetFactories[widgetName];
        if (!widgetFactory) {
            return void 0;
        }
        var modelFactory = this.getModelFactory(widgetFactory.modelName);
        if (!modelFactory) {
            return void 0;
        }
        var language = modelFactory.preferredLanguage(ext);
        var name = kernel && kernel.name;
        var id = kernel && kernel.id;
        return {
            id: id,
            name: name,
            language: language,
            shouldStart: widgetFactory.preferKernel,
            canStart: widgetFactory.canStartKernel
        };
    };
    return DocumentRegistry;
}());
exports.DocumentRegistry = DocumentRegistry;
/**
 * The namespace for the `DocumentRegistry` class statics.
 */
(function (DocumentRegistry) {
    /**
     * Get the extension name of a path.
     *
     * @param file - string.
     *
     * #### Notes
     * Dotted filenames (e.g. `".table.json"` are allowed.
     */
    function extname(path) {
        var parts = coreutils_2.PathExt.basename(path).split('.');
        parts.shift();
        return '.' + parts.join('.');
    }
    DocumentRegistry.extname = extname;
})(DocumentRegistry = exports.DocumentRegistry || (exports.DocumentRegistry = {}));
exports.DocumentRegistry = DocumentRegistry;
/**
 * A private namespace for DocumentRegistry data.
 */
var Private;
(function (Private) {
    /**
     * Normalize a file extension to be of the type `'.foo'`.
     *
     * Adds a leading dot if not present and converts to lower case.
     */
    function normalizeExtension(extension) {
        if (extension === '*') {
            return extension;
        }
        if (extension === '.*') {
            return '*';
        }
        if (extension.indexOf('.') !== 0) {
            extension = "." + extension;
        }
        return extension.toLowerCase();
    }
    Private.normalizeExtension = normalizeExtension;
})(Private || (Private = {}));

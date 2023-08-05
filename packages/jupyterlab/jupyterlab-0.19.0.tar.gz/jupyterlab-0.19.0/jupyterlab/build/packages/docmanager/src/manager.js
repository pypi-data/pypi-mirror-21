// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var algorithm_1 = require("@phosphor/algorithm");
var coreutils_1 = require("@phosphor/coreutils");
var properties_1 = require("@phosphor/properties");
var signaling_1 = require("@phosphor/signaling");
var docregistry_1 = require("@jupyterlab/docregistry");
var savehandler_1 = require("./savehandler");
var widgetmanager_1 = require("./widgetmanager");
/* tslint:disable */
/**
 * The document registry token.
 */
exports.IDocumentManager = new coreutils_1.Token('jupyter.services.document-manager');
/**
 * The document manager.
 *
 * #### Notes
 * The document manager is used to register model and widget creators,
 * and the file browser uses the document manager to create widgets. The
 * document manager maintains a context for each path and model type that is
 * open, and a list of widgets for each context. The document manager is in
 * control of the proper closing and disposal of the widgets and contexts.
 */
var DocumentManager = (function () {
    /**
     * Construct a new document manager.
     */
    function DocumentManager(options) {
        this._serviceManager = null;
        this._widgetManager = null;
        this._registry = null;
        this._contexts = [];
        this._opener = null;
        this._activateRequested = new signaling_1.Signal(this);
        this._registry = options.registry;
        this._serviceManager = options.manager;
        this._opener = options.opener;
        this._widgetManager = new widgetmanager_1.DocumentWidgetManager({
            registry: this._registry
        });
        this._widgetManager.activateRequested.connect(this._onActivateRequested, this);
    }
    Object.defineProperty(DocumentManager.prototype, "activateRequested", {
        /**
         * A signal emitted when one of the documents is activated.
         */
        get: function () {
            return this._activateRequested;
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(DocumentManager.prototype, "registry", {
        /**
         * Get the registry used by the manager.
         */
        get: function () {
            return this._registry;
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(DocumentManager.prototype, "services", {
        /**
         * Get the service manager used by the manager.
         */
        get: function () {
            return this._serviceManager;
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(DocumentManager.prototype, "isDisposed", {
        /**
         * Get whether the document manager has been disposed.
         */
        get: function () {
            return this._serviceManager === null;
        },
        enumerable: true,
        configurable: true
    });
    /**
     * Dispose of the resources held by the document manager.
     */
    DocumentManager.prototype.dispose = function () {
        if (this._serviceManager === null) {
            return;
        }
        var widgetManager = this._widgetManager;
        this._serviceManager = null;
        this._widgetManager = null;
        signaling_1.Signal.clearData(this);
        algorithm_1.each(algorithm_1.toArray(this._contexts), function (context) {
            widgetManager.closeWidgets(context);
        });
        widgetManager.dispose();
        this._contexts.length = 0;
    };
    /**
     * Open a file and return the widget used to view it.
     * Reveals an already existing editor.
     *
     * @param path - The file path to open.
     *
     * @param widgetName - The name of the widget factory to use. 'default' will use the default widget.
     *
     * @param kernel - An optional kernel name/id to override the default.
     *
     * @returns The created widget, or `undefined`.
     *
     * #### Notes
     * This function will return `undefined` if a valid widget factory
     * cannot be found.
     */
    DocumentManager.prototype.openOrReveal = function (path, widgetName, kernel) {
        if (widgetName === void 0) { widgetName = 'default'; }
        var widget = this.findWidget(path, widgetName);
        if (!widget) {
            widget = this.open(path, widgetName, kernel);
        }
        else {
            this._opener.open(widget);
        }
        return widget;
    };
    /**
     * Open a file and return the widget used to view it.
     *
     * @param path - The file path to open.
     *
     * @param widgetName - The name of the widget factory to use. 'default' will use the default widget.
     *
     * @param kernel - An optional kernel name/id to override the default.
     *
     * @returns The created widget, or `undefined`.
     *
     * #### Notes
     * This function will return `undefined` if a valid widget factory
     * cannot be found.
     */
    DocumentManager.prototype.open = function (path, widgetName, kernel) {
        if (widgetName === void 0) { widgetName = 'default'; }
        return this._createOrOpenDocument('open', path, widgetName, kernel);
    };
    /**
     * Create a new file and return the widget used to view it.
     *
     * @param path - The file path to create.
     *
     * @param widgetName - The name of the widget factory to use. 'default' will use the default widget.
     *
     * @param kernel - An optional kernel name/id to override the default.
     *
     * @returns The created widget, or `undefined`.
     *
     * #### Notes
     * This function will return `undefined` if a valid widget factory
     * cannot be found.
     */
    DocumentManager.prototype.createNew = function (path, widgetName, kernel) {
        if (widgetName === void 0) { widgetName = 'default'; }
        return this._createOrOpenDocument('create', path, widgetName, kernel);
    };
    /**
     * See if a widget already exists for the given path and widget name.
     *
     * @param path - The file path to use.
     *
     * @param widgetName - The name of the widget factory to use. 'default' will use the default widget.
     *
     * @returns The found widget, or `undefined`.
     *
     * #### Notes
     * This can be used to use an existing widget instead of opening
     * a new widget.
     */
    DocumentManager.prototype.findWidget = function (path, widgetName) {
        if (widgetName === void 0) { widgetName = 'default'; }
        if (widgetName === 'default') {
            var extname = docregistry_1.DocumentRegistry.extname(path);
            var factory = this._registry.defaultWidgetFactory(extname);
            if (!factory) {
                return;
            }
            widgetName = factory.name;
        }
        var context = this._contextForPath(path);
        if (context) {
            return this._widgetManager.findWidget(context, widgetName);
        }
    };
    /**
     * Get the document context for a widget.
     *
     * @param widget - The widget of interest.
     *
     * @returns The context associated with the widget, or `undefined`.
     */
    DocumentManager.prototype.contextForWidget = function (widget) {
        return this._widgetManager.contextForWidget(widget);
    };
    /**
     * Clone a widget.
     *
     * @param widget - The source widget.
     *
     * @returns A new widget or `undefined`.
     *
     * #### Notes
     *  Uses the same widget factory and context as the source, or returns
     *  `undefined` if the source widget is not managed by this manager.
     */
    DocumentManager.prototype.cloneWidget = function (widget) {
        return this._widgetManager.cloneWidget(widget);
    };
    /**
     * Close the widgets associated with a given path.
     *
     * @param path - The target path.
     */
    DocumentManager.prototype.closeFile = function (path) {
        var context = this._contextForPath(path);
        if (context) {
            return this._widgetManager.closeWidgets(context);
        }
        return Promise.resolve(void 0);
    };
    /**
     * Close all of the open documents.
     */
    DocumentManager.prototype.closeAll = function () {
        var _this = this;
        return Promise.all(algorithm_1.toArray(algorithm_1.map(this._contexts, function (context) {
            return _this._widgetManager.closeWidgets(context);
        }))).then(function () { return undefined; });
    };
    /**
     * Find a context for a given path and factory name.
     */
    DocumentManager.prototype._findContext = function (path, factoryName) {
        return algorithm_1.find(this._contexts, function (context) {
            return (context.factoryName === factoryName &&
                context.path === path);
        });
    };
    /**
     * Get a context for a given path.
     */
    DocumentManager.prototype._contextForPath = function (path) {
        return algorithm_1.find(this._contexts, function (context) {
            return context.path === path;
        });
    };
    /**
     * Create a context from a path and a model factory.
     */
    DocumentManager.prototype._createContext = function (path, factory, kernelPreference) {
        var _this = this;
        var adopter = function (widget) {
            _this._widgetManager.adoptWidget(context, widget);
            _this._opener.open(widget);
        };
        var context = new docregistry_1.Context({
            opener: adopter,
            manager: this._serviceManager,
            factory: factory,
            path: path,
            kernelPreference: kernelPreference
        });
        var handler = new savehandler_1.SaveHandler({
            context: context,
            manager: this._serviceManager
        });
        Private.saveHandlerProperty.set(context, handler);
        context.ready.then(function () {
            handler.start();
        });
        context.disposed.connect(this._onContextDisposed, this);
        this._contexts.push(context);
        return context;
    };
    /**
     * Handle a context disposal.
     */
    DocumentManager.prototype._onContextDisposed = function (context) {
        algorithm_1.ArrayExt.removeFirstOf(this._contexts, context);
    };
    /**
     * Get the model factory for a given widget name.
     */
    DocumentManager.prototype._widgetFactoryFor = function (path, widgetName) {
        var registry = this._registry;
        if (widgetName === 'default') {
            var extname = docregistry_1.DocumentRegistry.extname(path);
            var factory = registry.defaultWidgetFactory(extname);
            if (!factory) {
                return;
            }
            widgetName = factory.name;
        }
        return registry.getWidgetFactory(widgetName);
    };
    /**
     * Creates a new document, or loads one from disk, depending on the `which` argument.
     * If `which==='create'`, then it creates a new document. If `which==='open'`,
     * then it loads the document from disk.
     *
     * The two cases differ in how the document context is handled, but the creation
     * of the widget and launching of the kernel are identical.
     */
    DocumentManager.prototype._createOrOpenDocument = function (which, path, widgetName, kernel) {
        if (widgetName === void 0) { widgetName = 'default'; }
        var widgetFactory = this._widgetFactoryFor(path, widgetName);
        if (!widgetFactory) {
            return;
        }
        var factory = this._registry.getModelFactory(widgetFactory.modelName);
        if (!factory) {
            return;
        }
        // Handle the kernel pereference.
        var ext = docregistry_1.DocumentRegistry.extname(path);
        var preference = this._registry.getKernelPreference(ext, widgetFactory.name, kernel);
        var context = null;
        // Handle the load-from-disk case
        if (which === 'open') {
            // Use an existing context if available.
            context = this._findContext(path, factory.name);
            if (!context) {
                context = this._createContext(path, factory, preference);
                // Load the contents from disk.
                context.revert();
            }
        }
        else if (which === 'create') {
            context = this._createContext(path, factory, preference);
            // Immediately save the contents to disk.
            context.save();
        }
        var widget = this._widgetManager.createWidget(widgetFactory.name, context);
        this._opener.open(widget);
        return widget;
    };
    /**
     * Handle an activateRequested signal from the widget manager.
     */
    DocumentManager.prototype._onActivateRequested = function (sender, args) {
        this._activateRequested.emit(args);
    };
    return DocumentManager;
}());
exports.DocumentManager = DocumentManager;
/**
 * A namespace for private data.
 */
var Private;
(function (Private) {
    /**
     * An attached property for a context save handler.
     */
    Private.saveHandlerProperty = new properties_1.AttachedProperty({
        name: 'saveHandler',
        create: function () { return null; }
    });
    ;
})(Private || (Private = {}));

// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var algorithm_1 = require("@phosphor/algorithm");
var disposable_1 = require("@phosphor/disposable");
var messaging_1 = require("@phosphor/messaging");
var properties_1 = require("@phosphor/properties");
var signaling_1 = require("@phosphor/signaling");
var coreutils_1 = require("@jupyterlab/coreutils");
var apputils_1 = require("@jupyterlab/apputils");
/**
 * The class name added to document widgets.
 */
var DOCUMENT_CLASS = 'jp-Document';
/**
 * A class that maintains the lifecyle of file-backed widgets.
 */
var DocumentWidgetManager = (function () {
    /**
     * Construct a new document widget manager.
     */
    function DocumentWidgetManager(options) {
        this._closeGuard = false;
        this._registry = null;
        this._activateRequested = new signaling_1.Signal(this);
        this._registry = options.registry;
    }
    Object.defineProperty(DocumentWidgetManager.prototype, "activateRequested", {
        /**
         * A signal emitted when one of the documents is activated.
         */
        get: function () {
            return this._activateRequested;
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(DocumentWidgetManager.prototype, "isDisposed", {
        /**
         * Test whether the document widget manager is disposed.
         */
        get: function () {
            return this._registry === null;
        },
        enumerable: true,
        configurable: true
    });
    /**
     * Dispose of the resources used by the widget manager.
     */
    DocumentWidgetManager.prototype.dispose = function () {
        if (this._registry == null) {
            return;
        }
        this._registry = null;
        signaling_1.Signal.disconnectReceiver(this);
    };
    /**
     * Create a widget for a document and handle its lifecycle.
     *
     * @param name - The name of the widget factory.
     *
     * @param context - The document context object.
     *
     * @returns A widget created by the factory.
     *
     * @throws If the factory is not registered.
     */
    DocumentWidgetManager.prototype.createWidget = function (name, context) {
        var _this = this;
        var factory = this._registry.getWidgetFactory(name);
        if (!factory) {
            throw new Error("Factory is not registered: " + name);
        }
        var widget = factory.createNew(context);
        Private.nameProperty.set(widget, name);
        // Handle widget extensions.
        var disposables = new disposable_1.DisposableSet();
        algorithm_1.each(this._registry.widgetExtensions(name), function (extender) {
            disposables.add(extender.createNew(widget, context));
        });
        Private.disposablesProperty.set(widget, disposables);
        widget.disposed.connect(this._onWidgetDisposed, this);
        this.adoptWidget(context, widget);
        context.fileChanged.connect(this._onFileChanged, this);
        context.pathChanged.connect(this._onPathChanged, this);
        context.ready.then(function () {
            _this.setCaption(widget);
        });
        return widget;
    };
    /**
     * Install the message hook for the widget and add to list
     * of known widgets.
     *
     * @param context - The document context object.
     *
     * @param widget - The widget to adopt.
     */
    DocumentWidgetManager.prototype.adoptWidget = function (context, widget) {
        var _this = this;
        var widgets = Private.widgetsProperty.get(context);
        widgets.push(widget);
        messaging_1.MessageLoop.installMessageHook(widget, function (handler, msg) {
            return _this.filterMessage(handler, msg);
        });
        widget.addClass(DOCUMENT_CLASS);
        widget.title.closable = true;
        widget.disposed.connect(this._widgetDisposed, this);
        Private.contextProperty.set(widget, context);
    };
    /**
     * See if a widget already exists for the given context and widget name.
     *
     * @param context - The document context object.
     *
     * @returns The found widget, or `undefined`.
     *
     * #### Notes
     * This can be used to use an existing widget instead of opening
     * a new widget.
     */
    DocumentWidgetManager.prototype.findWidget = function (context, widgetName) {
        var widgets = Private.widgetsProperty.get(context);
        return algorithm_1.find(widgets, function (widget) {
            var name = Private.nameProperty.get(widget);
            if (name === widgetName) {
                return true;
            }
        });
    };
    /**
     * Get the document context for a widget.
     *
     * @param widget - The widget of interest.
     *
     * @returns The context associated with the widget, or `undefined`.
     */
    DocumentWidgetManager.prototype.contextForWidget = function (widget) {
        return Private.contextProperty.get(widget);
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
    DocumentWidgetManager.prototype.cloneWidget = function (widget) {
        var context = Private.contextProperty.get(widget);
        if (!context) {
            return;
        }
        var name = Private.nameProperty.get(widget);
        var newWidget = this.createWidget(name, context);
        this.adoptWidget(context, newWidget);
        return widget;
    };
    /**
     * Close the widgets associated with a given context.
     *
     * @param context - The document context object.
     */
    DocumentWidgetManager.prototype.closeWidgets = function (context) {
        var _this = this;
        var widgets = Private.widgetsProperty.get(context);
        return Promise.all(algorithm_1.toArray(algorithm_1.map(widgets, function (widget) { return _this.onClose(widget); }))).then(function () { return undefined; });
    };
    /**
     * Filter a message sent to a message handler.
     *
     * @param handler - The target handler of the message.
     *
     * @param msg - The message dispatched to the handler.
     *
     * @returns `false` if the message should be filtered, of `true`
     *   if the message should be dispatched to the handler as normal.
     */
    DocumentWidgetManager.prototype.filterMessage = function (handler, msg) {
        switch (msg.type) {
            case 'close-request':
                if (this._closeGuard) {
                    return true;
                }
                this.onClose(handler);
                return false;
            case 'activate-request':
                var context = this.contextForWidget(handler);
                this._activateRequested.emit(context.path);
                break;
            default:
                break;
        }
        return true;
    };
    /**
     * Set the caption for widget title.
     *
     * @param widget - The target widget.
     */
    DocumentWidgetManager.prototype.setCaption = function (widget) {
        var context = Private.contextProperty.get(widget);
        var model = context.contentsModel;
        if (!model) {
            widget.title.caption = '';
            return;
        }
        context.listCheckpoints().then(function (checkpoints) {
            if (widget.isDisposed) {
                return;
            }
            var last = checkpoints[checkpoints.length - 1];
            var checkpoint = last ? coreutils_1.Time.format(last.last_modified) : 'None';
            widget.title.caption = ("Name: " + model.name + "\n" +
                ("Path: " + model.path + "\n") +
                ("Last Saved: " + coreutils_1.Time.format(model.last_modified) + "\n") +
                ("Last Checkpoint: " + checkpoint));
        });
    };
    /**
     * Handle `'close-request'` messages.
     *
     * @param widget - The target widget.
     *
     * @returns A promise that resolves with whether the widget was closed.
     */
    DocumentWidgetManager.prototype.onClose = function (widget) {
        var _this = this;
        // Handle dirty state.
        return this._maybeClose(widget).then(function (result) {
            if (widget.isDisposed) {
                return true;
            }
            if (result) {
                _this._closeGuard = true;
                widget.close();
                _this._closeGuard = false;
                // Dispose of document widgets when they are closed.
                widget.dispose();
            }
            return result;
        }).catch(function () {
            widget.dispose();
        });
    };
    /**
     * Ask the user whether to close an unsaved file.
     */
    DocumentWidgetManager.prototype._maybeClose = function (widget) {
        // Bail if the model is not dirty or other widgets are using the model.)
        var context = Private.contextProperty.get(widget);
        if (!context) {
            return Promise.resolve(true);
        }
        var widgets = Private.widgetsProperty.get(context);
        var model = context.model;
        if (!model.dirty || widgets.length > 1) {
            return Promise.resolve(true);
        }
        var fileName = widget.title.label;
        return apputils_1.showDialog({
            title: 'Close without saving?',
            body: "File \"" + fileName + "\" has unsaved changes, close without saving?",
            buttons: [apputils_1.Dialog.cancelButton(), apputils_1.Dialog.warnButton()]
        }).then(function (value) {
            return value.accept;
        });
    };
    /**
     * Handle the disposal of a widget.
     */
    DocumentWidgetManager.prototype._widgetDisposed = function (widget) {
        var context = Private.contextProperty.get(widget);
        var widgets = Private.widgetsProperty.get(context);
        // Remove the widget.
        algorithm_1.ArrayExt.removeFirstOf(widgets, widget);
        // Dispose of the context if this is the last widget using it.
        if (!widgets.length) {
            context.dispose();
        }
    };
    /**
     * Handle the disposal of a widget.
     */
    DocumentWidgetManager.prototype._onWidgetDisposed = function (widget) {
        var disposables = Private.disposablesProperty.get(widget);
        disposables.dispose();
    };
    /**
     * Handle a file changed signal for a context.
     */
    DocumentWidgetManager.prototype._onFileChanged = function (context) {
        var _this = this;
        var widgets = Private.widgetsProperty.get(context);
        algorithm_1.each(widgets, function (widget) { _this.setCaption(widget); });
    };
    /**
     * Handle a path changed signal for a context.
     */
    DocumentWidgetManager.prototype._onPathChanged = function (context) {
        var _this = this;
        var widgets = Private.widgetsProperty.get(context);
        algorithm_1.each(widgets, function (widget) { _this.setCaption(widget); });
    };
    return DocumentWidgetManager;
}());
exports.DocumentWidgetManager = DocumentWidgetManager;
/**
 * A private namespace for DocumentManager data.
 */
var Private;
(function (Private) {
    /**
     * A private attached property for a widget context.
     */
    Private.contextProperty = new properties_1.AttachedProperty({
        name: 'context',
        create: function () { return null; }
    });
    /**
     * A private attached property for a widget factory name.
     */
    Private.nameProperty = new properties_1.AttachedProperty({
        name: 'name',
        create: function () { return ''; }
    });
    /**
     * A private attached property for the widgets associated with a context.
     */
    Private.widgetsProperty = new properties_1.AttachedProperty({
        name: 'widgets',
        create: function () { return []; }
    });
    /**
     * A private attached property for a widget's disposables.
     */
    Private.disposablesProperty = new properties_1.AttachedProperty({
        name: 'disposables',
        create: function () { return new disposable_1.DisposableSet(); }
    });
})(Private || (Private = {}));

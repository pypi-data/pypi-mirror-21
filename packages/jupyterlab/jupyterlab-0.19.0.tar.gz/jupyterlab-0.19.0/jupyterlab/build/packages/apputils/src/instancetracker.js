// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var algorithm_1 = require("@phosphor/algorithm");
var properties_1 = require("@phosphor/properties");
var signaling_1 = require("@phosphor/signaling");
var widgets_1 = require("@phosphor/widgets");
/**
 * A class that keeps track of widget instances on an Application shell.
 *
 * #### Notes
 * The API surface area of this concrete implementation is substantially larger
 * than the instance tracker interface it implements. The interface is intended
 * for export by JupyterLab plugins that create widgets and have clients who may
 * wish to keep track of newly created widgets. This class, however, can be used
 * internally by plugins to restore state as well.
 */
var InstanceTracker = (function () {
    /**
     * Create a new instance tracker.
     *
     * @param options - The instantiation options for an instance tracker.
     */
    function InstanceTracker(options) {
        this._restore = null;
        this._tracker = new widgets_1.FocusTracker();
        this._currentChanged = new signaling_1.Signal(this);
        this._widgetAdded = new signaling_1.Signal(this);
        this._widgets = [];
        this._currentWidget = null;
        this._shell = options.shell;
        this.namespace = options.namespace;
        this._tracker.currentChanged.connect(this._onCurrentChanged, this);
    }
    Object.defineProperty(InstanceTracker.prototype, "currentChanged", {
        /**
         * A signal emitted when the current widget changes.
         */
        get: function () {
            return this._currentChanged;
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(InstanceTracker.prototype, "widgetAdded", {
        /**
         * A signal emitted when a widget is added.
         *
         * #### Notes
         * This signal will only fire when a widget is added to the tracker. It will
         * not fire if a widget is injected into the tracker.
         */
        get: function () {
            return this._widgetAdded;
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(InstanceTracker.prototype, "currentWidget", {
        /**
         * The current widget is the most recently focused or added widget.
         *
         * #### Notes
         * It is the most recently focused widget, or the most recently added
         * widget if no widget has taken focus.
         */
        get: function () {
            return this._currentWidget;
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(InstanceTracker.prototype, "size", {
        /**
         * The number of widgets held by the tracker.
         */
        get: function () {
            return this._tracker.widgets.length;
        },
        enumerable: true,
        configurable: true
    });
    /**
     * Add a new widget to the tracker.
     *
     * @param widget - The widget being added.
     */
    InstanceTracker.prototype.add = function (widget) {
        if (this._tracker.has(widget)) {
            var warning = widget.id + " already exists in the tracker.";
            console.warn(warning);
            return Promise.reject(warning);
        }
        this._tracker.add(widget);
        this._widgets.push(widget);
        var injected = Private.injectedProperty.get(widget);
        var promise = Promise.resolve(void 0);
        if (injected) {
            return promise;
        }
        widget.disposed.connect(this._onWidgetDisposed, this);
        // Handle widget state restoration.
        if (this._restore) {
            var state = this._restore.state;
            var widgetName = this._restore.name(widget);
            if (widgetName) {
                var name_1 = this.namespace + ":" + widgetName;
                var data = this._restore.args(widget);
                Private.nameProperty.set(widget, name_1);
                promise = state.save(name_1, { data: data });
            }
        }
        // If there is no focused widget, set this as the current widget.
        if (!this._tracker.currentWidget) {
            this._currentWidget = widget;
            this.onCurrentChanged(widget);
            this._currentChanged.emit(widget);
        }
        // Emit the widget added signal.
        this._widgetAdded.emit(widget);
        return promise;
    };
    Object.defineProperty(InstanceTracker.prototype, "isDisposed", {
        /**
         * Test whether the tracker is disposed.
         */
        get: function () {
            return this._tracker === null;
        },
        enumerable: true,
        configurable: true
    });
    /**
     * Dispose of the resources held by the tracker.
     */
    InstanceTracker.prototype.dispose = function () {
        if (this._tracker === null) {
            return;
        }
        var tracker = this._tracker;
        this._tracker = null;
        signaling_1.Signal.clearData(this);
        tracker.dispose();
    };
    /**
     * Find the first widget in the tracker that satisfies a filter function.
     *
     * @param - fn The filter function to call on each widget.
     *
     * #### Notes
     * If no widget is found, the value returned is `undefined`.
     */
    InstanceTracker.prototype.find = function (fn) {
        return algorithm_1.find(this._tracker.widgets, fn);
    };
    /**
     * Iterate through each widget in the tracker.
     *
     * @param fn - The function to call on each widget.
     */
    InstanceTracker.prototype.forEach = function (fn) {
        algorithm_1.each(this._tracker.widgets, function (widget) { fn(widget); });
    };
    /**
     * Inject a foreign widget into the instance tracker.
     *
     * @param widget - The widget to inject into the tracker.
     *
     * #### Notes
     * Any widgets injected into an instance tracker will not have their state
     * saved by the tracker. The primary use case for widget injection is for a
     * plugin that offers a sub-class of an extant plugin to have its instances
     * share the same commands as the parent plugin (since most relevant commands
     * will use the `currentWidget` of the parent plugin's instance tracker). In
     * this situation, the sub-class plugin may well have its own instance tracker
     * for layout and state restoration in addition to injecting its widgets into
     * the parent plugin's instance tracker.
     */
    InstanceTracker.prototype.inject = function (widget) {
        Private.injectedProperty.set(widget, true);
        this.add(widget);
    };
    /**
     * Check if this tracker has the specified widget.
     *
     * @param widget - The widget whose existence is being checked.
     */
    InstanceTracker.prototype.has = function (widget) {
        return this._tracker.has(widget);
    };
    /**
     * Activate the given widget in the application shell.
     */
    InstanceTracker.prototype.activate = function (widget) {
        this._shell.activateById(widget.id);
    };
    /**
     * Restore the widgets in this tracker's namespace.
     *
     * @param options - The configuration options that describe restoration.
     *
     * @returns A promise that resolves when restoration has completed.
     *
     * #### Notes
     * This function should almost never be invoked by client code. Its primary
     * use case is to be invoked by a layout restorer plugin that handles
     * multiple instance trackers and, when ready, asks them each to restore their
     * respective widgets.
     */
    InstanceTracker.prototype.restore = function (options) {
        this._restore = options;
        var command = options.command, registry = options.registry, state = options.state, when = options.when;
        var namespace = this.namespace;
        var promises = [state.fetchNamespace(namespace)];
        if (when) {
            promises = promises.concat(when);
        }
        return Promise.all(promises).then(function (_a) {
            var saved = _a[0];
            return Promise.all(saved.map(function (item) {
                var args = item.value.data;
                // Execute the command and if it fails, delete the state restore data.
                return registry.execute(command, args)
                    .catch(function () { state.remove(item.id); });
            }));
        });
    };
    /**
     * Save the restore data for a given widget.
     *
     * @param widget - The widget being saved.
     */
    InstanceTracker.prototype.save = function (widget) {
        var injected = Private.injectedProperty.get(widget);
        if (!this._restore || !this.has(widget) || injected) {
            return;
        }
        var state = this._restore.state;
        var widgetName = this._restore.name(widget);
        var oldName = Private.nameProperty.get(widget);
        var newName = widgetName ? this.namespace + ":" + widgetName : null;
        if (oldName && oldName !== newName) {
            state.remove(oldName);
        }
        // Set the name property irrespective of whether the new name is null.
        Private.nameProperty.set(widget, newName);
        if (newName) {
            var data = this._restore.args(widget);
            state.save(newName, { data: data });
        }
    };
    /**
     * Handle the current change event.
     *
     * #### Notes
     * The default implementation is a no-op.
     */
    InstanceTracker.prototype.onCurrentChanged = function (value) { };
    /**
     * Handle the current change signal from the internal focus tracker.
     */
    InstanceTracker.prototype._onCurrentChanged = function (sender, args) {
        // Bail if the active widget did not change.
        if (args.newValue === this._currentWidget) {
            return;
        }
        this._currentWidget = args.newValue;
        this.onCurrentChanged(args.newValue);
        this._currentChanged.emit(args.newValue);
    };
    /**
     * Clean up after disposed widgets.
     */
    InstanceTracker.prototype._onWidgetDisposed = function (widget) {
        var injected = Private.injectedProperty.get(widget);
        if (injected) {
            return;
        }
        // Handle widget removal.
        algorithm_1.ArrayExt.removeFirstOf(this._widgets, widget);
        // Handle a current changed.
        if (widget === this._currentWidget) {
            this._currentWidget = (this._tracker.currentWidget ||
                this._widgets[this._widgets.length - 1] ||
                null);
            this._currentChanged.emit(this._currentWidget);
            this.onCurrentChanged(this._currentWidget);
        }
        if (!this._restore) {
            return;
        }
        // If restore data was saved, delete it from the database.
        var state = this._restore.state;
        var name = Private.nameProperty.get(widget);
        if (name) {
            state.remove(name);
        }
    };
    return InstanceTracker;
}());
exports.InstanceTracker = InstanceTracker;
/*
 * A namespace for private data.
 */
var Private;
(function (Private) {
    /**
     * An attached property to indicate whether a widget has been injected.
     */
    Private.injectedProperty = new properties_1.AttachedProperty({
        name: 'injected',
        create: function () { return false; }
    });
    /**
     * An attached property for a widget's ID in the state database.
     */
    Private.nameProperty = new properties_1.AttachedProperty({
        name: 'name',
        create: function () { return ''; }
    });
})(Private || (Private = {}));

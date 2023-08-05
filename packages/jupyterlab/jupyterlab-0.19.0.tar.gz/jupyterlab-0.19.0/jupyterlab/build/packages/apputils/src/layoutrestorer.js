/*-----------------------------------------------------------------------------
| Copyright (c) Jupyter Development Team.
| Distributed under the terms of the Modified BSD License.
|----------------------------------------------------------------------------*/
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var coreutils_1 = require("@phosphor/coreutils");
var properties_1 = require("@phosphor/properties");
/* tslint:disable */
/**
 * The layout restorer token.
 */
exports.ILayoutRestorer = new coreutils_1.Token('jupyter.services.layout-restorer');
/**
 * The state database key for restorer data.
 */
var KEY = 'layout-restorer:data';
/**
 * The default implementation of a layout restorer.
 *
 * #### Notes
 * The lifecycle for state restoration is subtle. The sequence of events is:
 *
 * 1. The layout restorer plugin is instantiated. It installs itself as the
 *    layout database that the application shell can use to `fetch` and `save`
 *    layout restoration data.
 *
 * 2. Other plugins that care about state restoration require the layout
 *    restorer as a dependency.
 *
 * 3. As each load-time plugin initializes (which happens before the lab
 *    application has `started`), it instructs the layout restorer whether
 *    the restorer ought to `restore` its state by passing in its tracker.
 *    Alternatively, a plugin that does not require its own instance tracker
 *    (because perhaps it only creates a single widget, like a command palette),
 *    can simply `add` its widget along with a persistent unique name to the
 *    layout restorer so that its layout state can be restored when the lab
 *    application restores.
 *
 * 4. After all the load-time plugins have finished initializing, the lab
 *    application `started` promise will resolve. This is the `first`
 *    promise that the layout restorer waits for. By this point, all of the
 *    plugins that care about restoration will have instructed the layout
 *    restorer to `restore` their state.
 *
 * 5. The layout restorer will then instruct each plugin's instance tracker
 *    to restore its state and reinstantiate whichever widgets it wants. The
 *    tracker returns a promise to the layout restorer that resolves when it
 *    has completed restoring the tracked widgets it cares about.
 *
 * 6. As each instance tracker finishes restoring the widget instances it cares
 *    about, it resolves the promise that was made to the layout restorer
 *    (in step 5). After all of the promises that the restorer is awaiting have
 *    resolved, the restorer then resolves its `restored` promise allowing the
 *    application shell to `fetch` the dehydrated layout state and rehydrate the
 *    saved layout.
 *
 * Of particular note are steps 5 and 6: since state restoration of plugins
 * is accomplished by executing commands, the command that is used to restore
 * the state of each plugin must return a promise that only resolves when the
 * widget has been created and added to the plugin's instance tracker.
 */
var LayoutRestorer = (function () {
    /**
     * Create a layout restorer.
     */
    function LayoutRestorer(options) {
        var _this = this;
        this._first = null;
        this._promises = [];
        this._restored = new coreutils_1.PromiseDelegate();
        this._registry = null;
        this._state = null;
        this._trackers = new Set();
        this._widgets = new Map();
        this._registry = options.registry;
        this._state = options.state;
        this._first = options.first;
        this._first.then(function () { return Promise.all(_this._promises); }).then(function () {
            // Release the promises held in memory.
            _this._promises = null;
            // Release the tracker set.
            _this._trackers.clear();
            _this._trackers = null;
        }).then(function () { _this._restored.resolve(void 0); });
    }
    Object.defineProperty(LayoutRestorer.prototype, "restored", {
        /**
         * A promise resolved when the layout restorer is ready to receive signals.
         */
        get: function () {
            return this._restored.promise;
        },
        enumerable: true,
        configurable: true
    });
    /**
     * Add a widget to be tracked by the layout restorer.
     */
    LayoutRestorer.prototype.add = function (widget, name) {
        Private.nameProperty.set(widget, name);
        this._widgets.set(name, widget);
        widget.disposed.connect(this._onWidgetDisposed, this);
    };
    /**
     * Fetch the layout state for the application.
     *
     * #### Notes
     * Fetching the layout relies on all widget restoration to be complete, so
     * calls to `fetch` are guaranteed to return after restoration is complete.
     */
    LayoutRestorer.prototype.fetch = function () {
        var _this = this;
        var blank = {
            fresh: true, mainArea: null, leftArea: null, rightArea: null
        };
        var layout = this._state.fetch(KEY);
        return Promise.all([layout, this.restored]).then(function (_a) {
            var data = _a[0];
            if (!data) {
                return blank;
            }
            var _b = data, main = _b.main, left = _b.left, right = _b.right;
            // If any data exists, then this is not a fresh session.
            var fresh = false;
            // Rehydrate main area.
            var mainArea = _this._rehydrateMainArea(main);
            // Rehydrate left area.
            var leftArea = _this._rehydrateSideArea(left);
            // Rehydrate right area.
            var rightArea = _this._rehydrateSideArea(right);
            return { fresh: fresh, mainArea: mainArea, leftArea: leftArea, rightArea: rightArea };
        }).catch(function () { return blank; }); // Let fetch fail gracefully; return blank slate.
    };
    /**
     * Restore the widgets of a particular instance tracker.
     *
     * @param tracker - The instance tracker whose widgets will be restored.
     *
     * @param options - The restoration options.
     */
    LayoutRestorer.prototype.restore = function (tracker, options) {
        var _this = this;
        if (!this._promises) {
            var warning = 'restore() can only be called before `first` has resolved.';
            console.warn(warning);
            return Promise.reject(warning);
        }
        var namespace = tracker.namespace;
        if (this._trackers.has(namespace)) {
            var warning = "A tracker namespaced " + namespace + " was already restored.";
            console.warn(warning);
            return Promise.reject(warning);
        }
        var args = options.args, command = options.command, name = options.name, when = options.when;
        // Add the tracker to the private trackers collection.
        this._trackers.add(namespace);
        // Whenever a new widget is added to the tracker, record its name.
        tracker.widgetAdded.connect(function (sender, widget) {
            var widgetName = name(widget);
            if (widgetName) {
                _this.add(widget, widgetName);
            }
        }, this);
        var first = this._first;
        var promise = tracker.restore({
            args: args, command: command, name: name,
            registry: this._registry,
            state: this._state,
            when: when ? [first].concat(when) : first
        });
        this._promises.push(promise);
        return promise;
    };
    /**
     * Save the layout state for the application.
     */
    LayoutRestorer.prototype.save = function (data) {
        // If there are promises that are unresolved, bail.
        if (this._promises) {
            var warning = 'save() was called prematurely.';
            console.warn(warning);
            return Promise.reject(warning);
        }
        var dehydrated = {};
        // Dehydrate main area.
        dehydrated.main = this._dehydrateMainArea(data.mainArea);
        // Dehydrate left area.
        dehydrated.left = this._dehydrateSideArea(data.leftArea);
        // Dehydrate right area.
        dehydrated.right = this._dehydrateSideArea(data.rightArea);
        return this._state.save(KEY, dehydrated);
    };
    /**
     * Dehydrate a main area description into a serializable object.
     */
    LayoutRestorer.prototype._dehydrateMainArea = function (area) {
        return Private.serializeMain(area);
    };
    /**
     * Reydrate a serialized main area description object.
     *
     * #### Notes
     * This function consumes data that can become corrupted, so it uses type
     * coercion to guarantee the dehydrated object is safely processed.
     */
    LayoutRestorer.prototype._rehydrateMainArea = function (area) {
        return Private.deserializeMain(area, this._widgets);
    };
    /**
     * Dehydrate a side area description into a serializable object.
     */
    LayoutRestorer.prototype._dehydrateSideArea = function (area) {
        var dehydrated = { collapsed: area.collapsed };
        if (area.currentWidget) {
            var current = Private.nameProperty.get(area.currentWidget);
            if (current) {
                dehydrated.current = current;
            }
        }
        if (area.widgets) {
            dehydrated.widgets = area.widgets
                .map(function (widget) { return Private.nameProperty.get(widget); })
                .filter(function (name) { return !!name; });
        }
        return dehydrated;
    };
    /**
     * Reydrate a serialized side area description object.
     *
     * #### Notes
     * This function consumes data that can become corrupted, so it uses type
     * coercion to guarantee the dehydrated object is safely processed.
     */
    LayoutRestorer.prototype._rehydrateSideArea = function (area) {
        if (!area) {
            return { collapsed: true, currentWidget: null, widgets: null };
        }
        var internal = this._widgets;
        var collapsed = area.hasOwnProperty('collapsed') ? !!area.collapsed
            : false;
        var currentWidget = area.current && internal.has("" + area.current) ?
            internal.get("" + area.current) : null;
        var widgets = !Array.isArray(area.widgets) ? null
            : area.widgets
                .map(function (name) { return internal.has("" + name) ? internal.get("" + name) : null; })
                .filter(function (widget) { return !!widget; });
        return { collapsed: collapsed, currentWidget: currentWidget, widgets: widgets };
    };
    /**
     * Handle a widget disposal.
     */
    LayoutRestorer.prototype._onWidgetDisposed = function (widget) {
        var name = Private.nameProperty.get(widget);
        this._widgets.delete(name);
    };
    return LayoutRestorer;
}());
exports.LayoutRestorer = LayoutRestorer;
/*
 * A namespace for private data.
 */
var Private;
(function (Private) {
    /**
     * An attached property for a widget's ID in the state database.
     */
    Private.nameProperty = new properties_1.AttachedProperty({
        name: 'name',
        create: function (owner) { return ''; }
    });
    /**
     * Serialize individual areas within the main area.
     */
    function serializeArea(area) {
        if (!area || !area.type) {
            return null;
        }
        if (area.type === 'tab-area') {
            return {
                type: 'tab-area',
                currentIndex: area.currentIndex,
                widgets: area.widgets
                    .map(function (widget) { return Private.nameProperty.get(widget); })
                    .filter(function (name) { return !!name; })
            };
        }
        return {
            type: 'split-area',
            orientation: area.orientation,
            sizes: area.sizes,
            children: area.children.map(serializeArea)
        };
    }
    /**
     * Return a dehydrated, serializable version of the main dock panel.
     */
    function serializeMain(area) {
        var dehydrated = {
            dock: area && area.dock && serializeArea(area.dock.main) || null
        };
        if (area && area.currentWidget) {
            var current = Private.nameProperty.get(area.currentWidget);
            if (current) {
                dehydrated.current = current;
            }
        }
        return dehydrated;
    }
    Private.serializeMain = serializeMain;
    /**
     * Deserialize individual areas within the main area.
     *
     * #### Notes
     * Because this data comes from a potentially unreliable foreign source, it is
     * typed as a `JSONObject`; but the actual expected type is:
     * `ITabArea | ISplitArea`.
     *
     * For fault tolerance, types are manually checked in deserialization.
     */
    function deserializeArea(area, names) {
        if (!area) {
            return null;
        }
        // Because this data is saved to a foreign data source, its type safety is
        // not guaranteed when it is retrieved, so exhaustive checks are necessary.
        var type = area.type || 'unknown';
        if (type === 'unknown' || (type !== 'tab-area' && type !== 'split-area')) {
            console.warn("Attempted to deserialize unknown type: " + type);
            return null;
        }
        if (type === 'tab-area') {
            var _a = area, currentIndex = _a.currentIndex, widgets = _a.widgets;
            var hydrated_1 = {
                type: 'tab-area',
                currentIndex: currentIndex || 0,
                widgets: widgets && widgets.map(function (widget) { return names.get(widget); })
                    .filter(function (widget) { return !!widget; }) || []
            };
            // Make sure the current index is within bounds.
            if (hydrated_1.currentIndex > hydrated_1.widgets.length - 1) {
                hydrated_1.currentIndex = 0;
            }
            return hydrated_1;
        }
        var _b = area, orientation = _b.orientation, sizes = _b.sizes, children = _b.children;
        var hydrated = {
            type: 'split-area',
            orientation: orientation,
            sizes: sizes || [],
            children: children &&
                children.map(function (child) { return deserializeArea(child, names); })
                    .filter(function (widget) { return !!widget; }) || []
        };
        return hydrated;
    }
    /**
     * Return the hydrated version of the main dock panel, ready to restore.
     *
     * #### Notes
     * Because this data comes from a potentially unreliable foreign source, it is
     * typed as a `JSONObject`; but the actual expected type is: `IMainArea`.
     *
     * For fault tolerance, types are manually checked in deserialization.
     */
    function deserializeMain(area, names) {
        if (!area) {
            return null;
        }
        var name = area.current || null;
        var dock = area.dock || null;
        return {
            currentWidget: name && names.has(name) && names.get(name) || null,
            dock: dock ? { main: deserializeArea(dock, names) } : null
        };
    }
    Private.deserializeMain = deserializeMain;
})(Private || (Private = {}));

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
var algorithm_1 = require("@phosphor/algorithm");
var coreutils_1 = require("@phosphor/coreutils");
var messaging_1 = require("@phosphor/messaging");
var signaling_1 = require("@phosphor/signaling");
var widgets_1 = require("@phosphor/widgets");
/**
 * The class name added to AppShell instances.
 */
var APPLICATION_SHELL_CLASS = 'jp-ApplicationShell';
/**
 * The class name added to side bar instances.
 */
var SIDEBAR_CLASS = 'jp-SideBar';
/**
 * The class name added to the current widget's title.
 */
var CURRENT_CLASS = 'jp-mod-current';
/**
 * The class name added to the active widget's title.
 */
var ACTIVE_CLASS = 'jp-mod-active';
/**
 * The application shell for JupyterLab.
 */
var ApplicationShell = (function (_super) {
    __extends(ApplicationShell, _super);
    /**
     * Construct a new application shell.
     */
    function ApplicationShell() {
        var _this = _super.call(this) || this;
        _this._database = null;
        _this._isRestored = false;
        _this._restored = new coreutils_1.PromiseDelegate();
        _this._tracker = new widgets_1.FocusTracker();
        _this._currentChanged = new signaling_1.Signal(_this);
        _this._activeChanged = new signaling_1.Signal(_this);
        _this.addClass(APPLICATION_SHELL_CLASS);
        _this.id = 'main';
        var topPanel = _this._topPanel = new widgets_1.Panel();
        var hboxPanel = _this._hboxPanel = new widgets_1.BoxPanel();
        var dockPanel = _this._dockPanel = new widgets_1.DockPanel();
        var hsplitPanel = _this._hsplitPanel = new widgets_1.SplitPanel();
        var leftHandler = _this._leftHandler = new Private.SideBarHandler('left');
        var rightHandler = _this._rightHandler = new Private.SideBarHandler('right');
        var rootLayout = new widgets_1.BoxLayout();
        topPanel.id = 'jp-top-panel';
        hboxPanel.id = 'jp-main-content-panel';
        dockPanel.id = 'jp-main-dock-panel';
        hsplitPanel.id = 'jp-main-split-panel';
        leftHandler.sideBar.addClass(SIDEBAR_CLASS);
        leftHandler.sideBar.addClass('jp-mod-left');
        leftHandler.stackedPanel.id = 'jp-left-stack';
        rightHandler.sideBar.addClass(SIDEBAR_CLASS);
        rightHandler.sideBar.addClass('jp-mod-right');
        rightHandler.stackedPanel.id = 'jp-right-stack';
        hboxPanel.spacing = 0;
        dockPanel.spacing = 5;
        hsplitPanel.spacing = 1;
        hboxPanel.direction = 'left-to-right';
        hsplitPanel.orientation = 'horizontal';
        widgets_1.SplitPanel.setStretch(leftHandler.stackedPanel, 0);
        widgets_1.SplitPanel.setStretch(dockPanel, 1);
        widgets_1.SplitPanel.setStretch(rightHandler.stackedPanel, 0);
        widgets_1.BoxPanel.setStretch(leftHandler.sideBar, 0);
        widgets_1.BoxPanel.setStretch(hsplitPanel, 1);
        widgets_1.BoxPanel.setStretch(rightHandler.sideBar, 0);
        hsplitPanel.addWidget(leftHandler.stackedPanel);
        hsplitPanel.addWidget(dockPanel);
        hsplitPanel.addWidget(rightHandler.stackedPanel);
        hboxPanel.addWidget(leftHandler.sideBar);
        hboxPanel.addWidget(hsplitPanel);
        hboxPanel.addWidget(rightHandler.sideBar);
        rootLayout.direction = 'top-to-bottom';
        rootLayout.spacing = 0; // TODO make this configurable?
        widgets_1.BoxLayout.setStretch(topPanel, 0);
        widgets_1.BoxLayout.setStretch(hboxPanel, 1);
        rootLayout.addWidget(topPanel);
        rootLayout.addWidget(hboxPanel);
        _this.layout = rootLayout;
        // Connect change listeners.
        _this._tracker.currentChanged.connect(_this._onCurrentChanged, _this);
        _this._tracker.activeChanged.connect(_this._onActiveChanged, _this);
        // Connect main layout change listener.
        _this._dockPanel.layoutModified.connect(_this._save, _this);
        return _this;
    }
    Object.defineProperty(ApplicationShell.prototype, "currentChanged", {
        /**
         * A signal emitted when main area's current focus changes.
         */
        get: function () {
            return this._currentChanged;
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(ApplicationShell.prototype, "activeChanged", {
        /**
         * A signal emitted when main area's active focus changes.
         */
        get: function () {
            return this._activeChanged;
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(ApplicationShell.prototype, "currentWidget", {
        /**
         * The current widget in the shell's main area.
         */
        get: function () {
            return this._tracker.currentWidget;
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(ApplicationShell.prototype, "activeWidget", {
        /**
         * The active widget in the shell's main area.
         */
        get: function () {
            return this._tracker.activeWidget;
        },
        enumerable: true,
        configurable: true
    });
    /**
     * True if the given area is empty.
     */
    ApplicationShell.prototype.isEmpty = function (area) {
        switch (area) {
            case 'left':
                return this._leftHandler.stackedPanel.widgets.length === 0;
            case 'main':
                return this._dockPanel.isEmpty;
            case 'top':
                return this._topPanel.widgets.length === 0;
            case 'right':
                return this._rightHandler.stackedPanel.widgets.length === 0;
            default:
                return true;
        }
    };
    Object.defineProperty(ApplicationShell.prototype, "restored", {
        /**
         * Promise that resolves when state is restored, returning layout description.
         */
        get: function () {
            return this._restored.promise;
        },
        enumerable: true,
        configurable: true
    });
    /**
     * Activate a widget in it's area.
     */
    ApplicationShell.prototype.activateById = function (id) {
        if (this._leftHandler.has(id)) {
            this._leftHandler.activate(id);
        }
        else if (this._rightHandler.has(id)) {
            this._rightHandler.activate(id);
        }
        else {
            var dock = this._dockPanel;
            var widget = algorithm_1.find(dock.widgets(), function (value) { return value.id === id; });
            if (widget) {
                dock.activateWidget(widget);
            }
        }
    };
    /*
     * Activate the next Tab in the active TabBar.
    */
    ApplicationShell.prototype.activateNextTab = function () {
        var current = this._currentTabBar();
        if (!current) {
            return;
        }
        var ci = current.currentIndex;
        if (ci === -1) {
            return;
        }
        if (ci < current.titles.length - 1) {
            current.currentIndex += 1;
            current.currentTitle.owner.activate();
            return;
        }
        if (ci === current.titles.length - 1) {
            var nextBar = this._nextTabBar();
            if (nextBar) {
                nextBar.currentIndex = 0;
                nextBar.currentTitle.owner.activate();
            }
        }
    };
    /*
     * Activate the previous Tab in the active TabBar.
    */
    ApplicationShell.prototype.activatePreviousTab = function () {
        var current = this._currentTabBar();
        if (!current) {
            return;
        }
        var ci = current.currentIndex;
        if (ci === -1) {
            return;
        }
        if (ci > 0) {
            current.currentIndex -= 1;
            current.currentTitle.owner.activate();
            return;
        }
        if (ci === 0) {
            var prevBar = this._previousTabBar();
            if (prevBar) {
                var len = prevBar.titles.length;
                prevBar.currentIndex = len - 1;
                prevBar.currentTitle.owner.activate();
            }
        }
    };
    /**
     * Add a widget to the left content area.
     *
     * #### Notes
     * Widgets must have a unique `id` property, which will be used as the DOM id.
     */
    ApplicationShell.prototype.addToLeftArea = function (widget, options) {
        if (options === void 0) { options = {}; }
        if (!widget.id) {
            console.error('widgets added to app shell must have unique id property');
            return;
        }
        var rank = 'rank' in options ? options.rank : 100;
        this._leftHandler.addWidget(widget, rank);
        this._save();
    };
    /**
     * Add a widget to the main content area.
     *
     * #### Notes
     * Widgets must have a unique `id` property, which will be used as the DOM id.
     * All widgets added to the main area should be disposed after removal (or
     * simply disposed in order to remove).
     */
    ApplicationShell.prototype.addToMainArea = function (widget) {
        if (!widget.id) {
            console.error('widgets added to app shell must have unique id property');
            return;
        }
        this._dockPanel.addWidget(widget, { mode: 'tab-after' });
        this._tracker.add(widget);
    };
    /**
     * Add a widget to the right content area.
     *
     * #### Notes
     * Widgets must have a unique `id` property, which will be used as the DOM id.
     */
    ApplicationShell.prototype.addToRightArea = function (widget, options) {
        if (options === void 0) { options = {}; }
        if (!widget.id) {
            console.error('widgets added to app shell must have unique id property');
            return;
        }
        var rank = 'rank' in options ? options.rank : 100;
        this._rightHandler.addWidget(widget, rank);
        this._save();
    };
    /**
     * Add a widget to the top content area.
     *
     * #### Notes
     * Widgets must have a unique `id` property, which will be used as the DOM id.
     */
    ApplicationShell.prototype.addToTopArea = function (widget, options) {
        if (options === void 0) { options = {}; }
        if (!widget.id) {
            console.error('widgets added to app shell must have unique id property');
            return;
        }
        // Temporary: widgets are added to the panel in order of insertion.
        this._topPanel.addWidget(widget);
        this._save();
    };
    /**
     * Collapse the left area.
     */
    ApplicationShell.prototype.collapseLeft = function () {
        this._leftHandler.collapse();
        this._save();
    };
    /**
     * Collapse the right area.
     */
    ApplicationShell.prototype.collapseRight = function () {
        this._rightHandler.collapse();
        this._save();
    };
    /**
     * Close all widgets in the main area.
     */
    ApplicationShell.prototype.closeAll = function () {
        // Make a copy of all the widget in the dock panel (using `toArray()`)
        // before removing them because removing them while iterating through them
        // modifies the underlying data of the iterator.
        algorithm_1.each(algorithm_1.toArray(this._dockPanel.widgets()), function (widget) { widget.close(); });
    };
    /**
     * Set the layout data store for the application shell.
     */
    ApplicationShell.prototype.setLayoutDB = function (database) {
        var _this = this;
        if (this._database) {
            throw new Error('cannot reset layout database');
        }
        this._database = database;
        this._database.fetch().then(function (saved) {
            if (_this.isDisposed || !saved) {
                return;
            }
            var mainArea = saved.mainArea, leftArea = saved.leftArea, rightArea = saved.rightArea;
            // Rehydrate the main area.
            if (mainArea) {
                if (mainArea.dock) {
                    _this._dockPanel.restoreLayout(mainArea.dock);
                }
                if (mainArea.currentWidget) {
                    _this.activateById(mainArea.currentWidget.id);
                }
            }
            // Rehydrate the left area.
            if (leftArea) {
                _this._leftHandler.rehydrate(leftArea);
            }
            // Rehydrate the right area.
            if (rightArea) {
                _this._rightHandler.rehydrate(rightArea);
            }
            // Set restored flag, save state, and resolve the restoration promise.
            _this._isRestored = true;
            return _this._save().then(function () {
                // Make sure all messages in the queue are finished before notifying
                // any extensions that are waiting for the promise that guarantees the
                // application state has been restored.
                messaging_1.MessageLoop.flush();
                _this._restored.resolve(saved);
            });
        });
        // Catch current changed events on the side handlers.
        this._tracker.currentChanged.connect(this._save, this);
        this._leftHandler.sideBar.currentChanged.connect(this._save, this);
        this._rightHandler.sideBar.currentChanged.connect(this._save, this);
    };
    /*
     * Return the TabBar that has the currently active Widget or null.
     */
    ApplicationShell.prototype._currentTabBar = function () {
        var current = this._tracker.currentWidget;
        if (!current) {
            return null;
        }
        var title = current.title;
        return algorithm_1.find(this._dockPanel.tabBars(), function (bar) {
            return algorithm_1.ArrayExt.firstIndexOf(bar.titles, title) > -1;
        }) || null;
    };
    /*
     * Return the TabBar previous to the current TabBar (see above) or null.
     */
    ApplicationShell.prototype._previousTabBar = function () {
        var current = this._currentTabBar();
        if (current) {
            return null;
        }
        var bars = algorithm_1.toArray(this._dockPanel.tabBars());
        var len = bars.length;
        var ci = algorithm_1.ArrayExt.firstIndexOf(bars, current);
        if (ci > 0) {
            return bars[ci - 1];
        }
        if (ci === 0) {
            return bars[len - 1];
        }
        return null;
    };
    /*
     * Return the TabBar next to the current TabBar (see above) or null.
     */
    ApplicationShell.prototype._nextTabBar = function () {
        var current = this._currentTabBar();
        if (!current) {
            return null;
        }
        var bars = algorithm_1.toArray(this._dockPanel.tabBars());
        var len = bars.length;
        var ci = algorithm_1.ArrayExt.firstIndexOf(bars, current);
        if (ci < (len - 1)) {
            return bars[ci + 1];
        }
        if (ci === len - 1) {
            return bars[0];
        }
        return null;
    };
    /**
     * Save the dehydrated state of the application shell.
     */
    ApplicationShell.prototype._save = function () {
        if (!this._database || !this._isRestored) {
            return;
        }
        var data = {
            mainArea: {
                currentWidget: this._tracker.currentWidget,
                dock: this._dockPanel.saveLayout()
            },
            leftArea: this._leftHandler.dehydrate(),
            rightArea: this._rightHandler.dehydrate()
        };
        return this._database.save(data);
    };
    /**
     * Handle a change to the dock area current widget.
     */
    ApplicationShell.prototype._onCurrentChanged = function (sender, args) {
        if (args.newValue) {
            args.newValue.title.className += " " + CURRENT_CLASS;
        }
        if (args.oldValue) {
            args.oldValue.title.className = (args.oldValue.title.className.replace(CURRENT_CLASS, ''));
        }
        this._currentChanged.emit(args);
    };
    /**
     * Handle a change to the dock area active widget.
     */
    ApplicationShell.prototype._onActiveChanged = function (sender, args) {
        if (args.newValue) {
            args.newValue.title.className += " " + ACTIVE_CLASS;
        }
        if (args.oldValue) {
            args.oldValue.title.className = (args.oldValue.title.className.replace(ACTIVE_CLASS, ''));
        }
        this._activeChanged.emit(args);
    };
    return ApplicationShell;
}(widgets_1.Widget));
exports.ApplicationShell = ApplicationShell;
/**
 * The namespace for `ApplicationShell` class statics.
 */
(function (ApplicationShell) {
    ;
})(ApplicationShell = exports.ApplicationShell || (exports.ApplicationShell = {}));
exports.ApplicationShell = ApplicationShell;
var Private;
(function (Private) {
    /**
     * A less-than comparison function for side bar rank items.
     */
    function itemCmp(first, second) {
        return first.rank - second.rank;
    }
    Private.itemCmp = itemCmp;
    /**
     * A class which manages a side bar and related stacked panel.
     */
    var SideBarHandler = (function () {
        /**
         * Construct a new side bar handler.
         */
        function SideBarHandler(side) {
            this._items = new Array();
            this._side = side;
            this._sideBar = new widgets_1.TabBar({
                insertBehavior: 'none',
                removeBehavior: 'none',
                allowDeselect: true
            });
            this._stackedPanel = new widgets_1.StackedPanel();
            this._sideBar.hide();
            this._stackedPanel.hide();
            this._sideBar.currentChanged.connect(this._onCurrentChanged, this);
            this._sideBar.tabActivateRequested.connect(this._onTabActivateRequested, this);
            this._stackedPanel.widgetRemoved.connect(this._onWidgetRemoved, this);
        }
        Object.defineProperty(SideBarHandler.prototype, "sideBar", {
            /**
             * Get the tab bar managed by the handler.
             */
            get: function () {
                return this._sideBar;
            },
            enumerable: true,
            configurable: true
        });
        Object.defineProperty(SideBarHandler.prototype, "stackedPanel", {
            /**
             * Get the stacked panel managed by the handler
             */
            get: function () {
                return this._stackedPanel;
            },
            enumerable: true,
            configurable: true
        });
        /**
         * Activate a widget residing in the side bar by ID.
         *
         * @param id - The widget's unique ID.
         */
        SideBarHandler.prototype.activate = function (id) {
            var widget = this._findWidgetByID(id);
            if (widget) {
                this._sideBar.currentTitle = widget.title;
                widget.activate();
            }
        };
        /**
         * Test whether the sidebar has the given widget by id.
         */
        SideBarHandler.prototype.has = function (id) {
            return this._findWidgetByID(id) !== null;
        };
        /**
         * Collapse the sidebar so no items are expanded.
         */
        SideBarHandler.prototype.collapse = function () {
            this._sideBar.currentTitle = null;
        };
        /**
         * Add a widget and its title to the stacked panel and side bar.
         *
         * If the widget is already added, it will be moved.
         */
        SideBarHandler.prototype.addWidget = function (widget, rank) {
            widget.parent = null;
            widget.hide();
            var item = { widget: widget, rank: rank };
            var index = this._findInsertIndex(item);
            algorithm_1.ArrayExt.insert(this._items, index, item);
            this._stackedPanel.insertWidget(index, widget);
            this._sideBar.insertTab(index, widget.title);
            this._refreshVisibility();
        };
        /**
         * Dehydrate the side bar data.
         */
        SideBarHandler.prototype.dehydrate = function () {
            var collapsed = this._sideBar.currentTitle === null;
            var widgets = algorithm_1.toArray(this._stackedPanel.widgets);
            var currentWidget = widgets[this._sideBar.currentIndex];
            return { collapsed: collapsed, currentWidget: currentWidget, widgets: widgets };
        };
        /**
         * Rehydrate the side bar.
         */
        SideBarHandler.prototype.rehydrate = function (data) {
            if (data.currentWidget) {
                this.activate(data.currentWidget.id);
            }
            else if (data.collapsed) {
                this.collapse();
            }
        };
        /**
         * Find the insertion index for a rank item.
         */
        SideBarHandler.prototype._findInsertIndex = function (item) {
            return algorithm_1.ArrayExt.upperBound(this._items, item, Private.itemCmp);
        };
        /**
         * Find the index of the item with the given widget, or `-1`.
         */
        SideBarHandler.prototype._findWidgetIndex = function (widget) {
            return algorithm_1.ArrayExt.findFirstIndex(this._items, function (item) { return item.widget === widget; });
        };
        /**
         * Find the widget which owns the given title, or `null`.
         */
        SideBarHandler.prototype._findWidgetByTitle = function (title) {
            var item = algorithm_1.find(this._items, function (value) { return value.widget.title === title; });
            return item ? item.widget : null;
        };
        /**
         * Find the widget with the given id, or `null`.
         */
        SideBarHandler.prototype._findWidgetByID = function (id) {
            var item = algorithm_1.find(this._items, function (value) { return value.widget.id === id; });
            return item ? item.widget : null;
        };
        /**
         * Refresh the visibility of the side bar and stacked panel.
         */
        SideBarHandler.prototype._refreshVisibility = function () {
            this._sideBar.setHidden(this._sideBar.titles.length === 0);
            this._stackedPanel.setHidden(this._sideBar.currentTitle === null);
        };
        /**
         * Handle the `currentChanged` signal from the sidebar.
         */
        SideBarHandler.prototype._onCurrentChanged = function (sender, args) {
            var oldWidget = this._findWidgetByTitle(args.previousTitle);
            var newWidget = this._findWidgetByTitle(args.currentTitle);
            if (oldWidget) {
                oldWidget.hide();
            }
            if (newWidget) {
                newWidget.show();
            }
            if (newWidget) {
                document.body.setAttribute("data-" + this._side + "Area", newWidget.id);
            }
            else {
                document.body.removeAttribute("data-" + this._side + "Area");
            }
            this._refreshVisibility();
        };
        /**
         * Handle a `tabActivateRequest` signal from the sidebar.
         */
        SideBarHandler.prototype._onTabActivateRequested = function (sender, args) {
            args.title.owner.activate();
        };
        /*
         * Handle the `widgetRemoved` signal from the stacked panel.
         */
        SideBarHandler.prototype._onWidgetRemoved = function (sender, widget) {
            algorithm_1.ArrayExt.removeAt(this._items, this._findWidgetIndex(widget));
            this._sideBar.removeTab(widget.title);
            this._refreshVisibility();
        };
        return SideBarHandler;
    }());
    Private.SideBarHandler = SideBarHandler;
})(Private || (Private = {}));

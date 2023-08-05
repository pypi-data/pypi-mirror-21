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
var coreutils_1 = require("@phosphor/coreutils");
var disposable_1 = require("@phosphor/disposable");
var widgets_1 = require("@phosphor/widgets");
var widgets_2 = require("@phosphor/widgets");
var apputils_1 = require("@jupyterlab/apputils");
/**
 * The class name added to inspector panels.
 */
var PANEL_CLASS = 'jp-Inspector';
/**
 * The class name added to inspector child item widgets.
 */
var ITEM_CLASS = 'jp-InspectorItem';
/**
 * The class name added to inspector child item widgets' content.
 */
var CONTENT_CLASS = 'jp-InspectorItem-content';
/**
 * The history clear button class name.
 */
var CLEAR_CLASS = 'jp-InspectorItem-clear';
/**
 * The back button class name.
 */
var BACK_CLASS = 'jp-InspectorItem-back';
/**
 * The forward button class name.
 */
var FORWARD_CLASS = 'jp-InspectorItem-forward';
/* tslint:disable */
/**
 * The inspector panel token.
 */
exports.IInspector = new coreutils_1.Token('jupyter.services.inspector');
/**
 * A panel which contains a set of inspectors.
 */
var InspectorPanel = (function (_super) {
    __extends(InspectorPanel, _super);
    /**
     * Construct an inspector.
     */
    function InspectorPanel() {
        var _this = _super.call(this) || this;
        _this._items = Object.create(null);
        _this._source = null;
        _this.addClass(PANEL_CLASS);
        return _this;
    }
    Object.defineProperty(InspectorPanel.prototype, "source", {
        /**
         * The source of events the inspector panel listens for.
         */
        get: function () {
            return this._source;
        },
        set: function (source) {
            var _this = this;
            if (this._source === source) {
                return;
            }
            // Disconnect old signal handler.
            if (this._source) {
                this._source.standby = true;
                this._source.inspected.disconnect(this.onInspectorUpdate, this);
                this._source.disposed.disconnect(this.onSourceDisposed, this);
            }
            // Clear the inspector child items (but maintain history) if necessary.
            if (this._items) {
                Object.keys(this._items).forEach(function (i) { return _this._items[i].content = null; });
            }
            this._source = source;
            // Connect new signal handler.
            if (this._source) {
                this._source.standby = false;
                this._source.inspected.connect(this.onInspectorUpdate, this);
                this._source.disposed.connect(this.onSourceDisposed, this);
            }
        },
        enumerable: true,
        configurable: true
    });
    /**
     * Create an inspector child item and return a disposable to remove it.
     *
     * @param item - The inspector child item being added to the inspector.
     *
     * @returns A disposable that removes the child item from the inspector.
     */
    InspectorPanel.prototype.add = function (item) {
        var _this = this;
        var widget = new InspectorItemWidget();
        widget.rank = item.rank;
        widget.remembers = !!item.remembers;
        widget.title.closable = false;
        widget.title.label = item.name;
        if (item.className) {
            widget.addClass(item.className);
        }
        this._items[item.type] = widget;
        this.addWidget(widget);
        if ((Object.keys(this._items)).length < 2) {
            this.tabBar.hide();
        }
        else {
            this.tabBar.show();
        }
        return new disposable_1.DisposableDelegate(function () {
            if (widget.isDisposed || _this.isDisposed) {
                return;
            }
            widget.dispose();
            delete _this._items[item.type];
            if ((Object.keys(_this._items)).length < 2) {
                _this.tabBar.hide();
            }
            else {
                _this.tabBar.show();
            }
        });
    };
    /**
     * Dispose of the resources held by the widget.
     */
    InspectorPanel.prototype.dispose = function () {
        if (this._items == null) {
            return;
        }
        var items = this._items;
        this._items = null;
        this.source = null;
        // Dispose the inspector child items.
        if (items) {
            Object.keys(items).forEach(function (i) { items[i].dispose(); });
        }
        _super.prototype.dispose.call(this);
    };
    /**
     * Handle `'activate-request'` messages.
     */
    InspectorPanel.prototype.onActivateRequest = function (msg) {
        this.node.tabIndex = -1;
        this.node.focus();
    };
    /**
     * Handle `'close-request'` messages.
     */
    InspectorPanel.prototype.onCloseRequest = function (msg) {
        _super.prototype.onCloseRequest.call(this, msg);
        this.dispose();
    };
    /**
     * Handle inspector update signals.
     */
    InspectorPanel.prototype.onInspectorUpdate = function (sender, args) {
        var widget = this._items[args.type];
        if (!widget) {
            return;
        }
        // Update the content of the inspector widget.
        widget.content = args.content;
        var items = this._items;
        // If any inspector with a higher rank has content, do not change focus.
        if (args.content) {
            for (var type in items) {
                var inspector = this._items[type];
                if (inspector.rank < widget.rank && inspector.content) {
                    return;
                }
            }
            this.currentWidget = widget;
            return;
        }
        // If the inspector was emptied, show the next best ranked inspector.
        var lowest = Infinity;
        widget = null;
        for (var type in items) {
            var inspector = this._items[type];
            if (inspector.rank < lowest && inspector.content) {
                lowest = inspector.rank;
                widget = inspector;
            }
        }
        if (widget) {
            this.currentWidget = widget;
        }
    };
    /**
     * Handle source disposed signals.
     */
    InspectorPanel.prototype.onSourceDisposed = function (sender, args) {
        this.source = null;
    };
    return InspectorPanel;
}(widgets_1.TabPanel));
exports.InspectorPanel = InspectorPanel;
/**
 * A code inspector child widget.
 */
var InspectorItemWidget = (function (_super) {
    __extends(InspectorItemWidget, _super);
    /**
     * Construct an inspector widget.
     */
    function InspectorItemWidget() {
        var _this = _super.call(this) || this;
        _this._content = null;
        _this._history = null;
        _this._index = -1;
        _this._rank = Infinity;
        _this._remembers = false;
        _this._toolbar = null;
        _this.layout = new widgets_1.PanelLayout();
        _this.addClass(ITEM_CLASS);
        _this._toolbar = _this._createToolbar();
        _this.layout.addWidget(_this._toolbar);
        return _this;
    }
    Object.defineProperty(InspectorItemWidget.prototype, "content", {
        /**
         * The text of the inspector.
         */
        get: function () {
            return this._content;
        },
        set: function (newValue) {
            if (newValue === this._content) {
                return;
            }
            if (this._content) {
                if (this._remembers) {
                    this._content.hide();
                }
                else {
                    this._content.dispose();
                }
            }
            this._content = newValue;
            if (this._content) {
                this._content.addClass(CONTENT_CLASS);
                this.layout.addWidget(this._content);
                if (this.remembers) {
                    this._history.push(newValue);
                    this._index++;
                }
            }
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(InspectorItemWidget.prototype, "remembers", {
        /**
         * A flag that indicates whether the inspector remembers history.
         */
        get: function () {
            return this._remembers;
        },
        set: function (newValue) {
            if (newValue === this._remembers) {
                return;
            }
            this._clear();
            this._remembers = newValue;
            if (!this._remembers) {
                this._history = null;
            }
            this.update();
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(InspectorItemWidget.prototype, "rank", {
        /**
         * The display rank of the inspector.
         */
        get: function () {
            return this._rank;
        },
        set: function (newValue) {
            this._rank = newValue;
        },
        enumerable: true,
        configurable: true
    });
    /**
     * Dispose of the resources held by the widget.
     */
    InspectorItemWidget.prototype.dispose = function () {
        if (this._toolbar === null) {
            return;
        }
        var toolbar = this._toolbar;
        var history = this._history;
        this._toolbar = null;
        this._history = null;
        if (history) {
            history.forEach(function (widget) { return widget.dispose(); });
        }
        toolbar.dispose();
        _super.prototype.dispose.call(this);
    };
    /**
     * Navigate back in history.
     */
    InspectorItemWidget.prototype._back = function () {
        if (this._history.length) {
            this._navigateTo(Math.max(this._index - 1, 0));
        }
    };
    /**
     * Clear history.
     */
    InspectorItemWidget.prototype._clear = function () {
        if (this._history) {
            this._history.forEach(function (widget) { return widget.dispose(); });
        }
        this._history = [];
        this._index = -1;
    };
    /**
     * Navigate forward in history.
     */
    InspectorItemWidget.prototype._forward = function () {
        if (this._history.length) {
            this._navigateTo(Math.min(this._index + 1, this._history.length - 1));
        }
    };
    /**
     * Create a history toolbar.
     */
    InspectorItemWidget.prototype._createToolbar = function () {
        var _this = this;
        var toolbar = new apputils_1.Toolbar();
        if (!this._remembers) {
            return toolbar;
        }
        var clear = new apputils_1.ToolbarButton({
            className: CLEAR_CLASS,
            onClick: function () { _this._clear(); },
            tooltip: 'Clear history.'
        });
        toolbar.addItem('clear', clear);
        var back = new apputils_1.ToolbarButton({
            className: BACK_CLASS,
            onClick: function () { _this._back(); },
            tooltip: 'Navigate back in history.'
        });
        toolbar.addItem('back', back);
        var forward = new apputils_1.ToolbarButton({
            className: FORWARD_CLASS,
            onClick: function () { _this._forward(); },
            tooltip: 'Navigate forward in history.'
        });
        toolbar.addItem('forward', forward);
        return toolbar;
    };
    /**
     * Navigate to a known index in history.
     */
    InspectorItemWidget.prototype._navigateTo = function (index) {
        if (this._content) {
            this._content.hide();
        }
        this._content = this._history[index];
        this._index = index;
        this._content.show();
    };
    return InspectorItemWidget;
}(widgets_2.Widget));

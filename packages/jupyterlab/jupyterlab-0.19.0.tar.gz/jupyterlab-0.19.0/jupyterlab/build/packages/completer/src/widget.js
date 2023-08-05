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
var signaling_1 = require("@phosphor/signaling");
var domutils_1 = require("@phosphor/domutils");
var widgets_1 = require("@phosphor/widgets");
var apputils_1 = require("@jupyterlab/apputils");
/**
 * The class name added to completer menu widgets.
 */
var COMPLETER_CLASS = 'jp-Completer';
/**
 * The class name added to completer menu items.
 */
var ITEM_CLASS = 'jp-Completer-item';
/**
 * The class name added to an active completer menu item.
 */
var ACTIVE_CLASS = 'jp-mod-active';
/**
 * The minimum height of a completer widget.
 */
var MIN_HEIGHT = 20;
/**
 * The maximum height of a completer widget.
 */
var MAX_HEIGHT = 200;
/**
 * A flag to indicate that event handlers are caught in the capture phase.
 */
var USE_CAPTURE = true;
/**
 * A widget that enables text completion.
 */
var CompleterWidget = (function (_super) {
    __extends(CompleterWidget, _super);
    /**
     * Construct a text completer menu widget.
     */
    function CompleterWidget(options) {
        var _this = _super.call(this, { node: document.createElement('ul') }) || this;
        _this._activeIndex = 0;
        _this._editor = null;
        _this._model = null;
        _this._renderer = null;
        _this._resetFlag = false;
        _this._selected = new signaling_1.Signal(_this);
        _this._visibilityChanged = new signaling_1.Signal(_this);
        _this._renderer = options.renderer || CompleterWidget.defaultRenderer;
        _this.model = options.model;
        _this._editor = options.editor;
        _this.addClass(COMPLETER_CLASS);
        return _this;
    }
    Object.defineProperty(CompleterWidget.prototype, "editor", {
        /**
         * The editor used by the completion widget.
         */
        get: function () {
            return this._editor;
        },
        set: function (newValue) {
            this._editor = newValue;
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(CompleterWidget.prototype, "selected", {
        /**
         * A signal emitted when a selection is made from the completer menu.
         */
        get: function () {
            return this._selected;
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(CompleterWidget.prototype, "visibilityChanged", {
        /**
         * A signal emitted when the completer widget's visibility changes.
         *
         * #### Notes
         * This signal is useful when there are multiple floating widgets that may
         * contend with the same space and ought to be mutually exclusive.
         */
        get: function () {
            return this._visibilityChanged;
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(CompleterWidget.prototype, "model", {
        /**
         * The model used by the completer widget.
         */
        get: function () {
            return this._model;
        },
        set: function (model) {
            if (!model && !this._model || model === this._model) {
                return;
            }
            if (this._model) {
                this._model.stateChanged.disconnect(this.onModelStateChanged, this);
            }
            this._model = model;
            if (this._model) {
                this._model.stateChanged.connect(this.onModelStateChanged, this);
            }
        },
        enumerable: true,
        configurable: true
    });
    /**
     * Dispose of the resources held by the completer widget.
     */
    CompleterWidget.prototype.dispose = function () {
        this._model = null;
        _super.prototype.dispose.call(this);
    };
    /**
     * Handle the DOM events for the widget.
     *
     * @param event - The DOM event sent to the widget.
     *
     * #### Notes
     * This method implements the DOM `EventListener` interface and is
     * called in response to events on the dock panel's node. It should
     * not be called directly by user code.
     */
    CompleterWidget.prototype.handleEvent = function (event) {
        if (this.isHidden || !this._editor) {
            return;
        }
        switch (event.type) {
            case 'keydown':
                this._evtKeydown(event);
                break;
            case 'mousedown':
                this._evtMousedown(event);
                break;
            case 'scroll':
                this._evtScroll(event);
                break;
            default:
                break;
        }
    };
    /**
     * Reset the widget.
     */
    CompleterWidget.prototype.reset = function () {
        this._activeIndex = 0;
        if (this._model) {
            this._model.reset(true);
        }
    };
    /**
     * Emit the selected signal for the current active item and reset.
     */
    CompleterWidget.prototype.selectActive = function () {
        var active = this.node.querySelector("." + ACTIVE_CLASS);
        if (!active) {
            this.reset();
            return;
        }
        this._selected.emit(active.getAttribute('data-value'));
        this.reset();
    };
    /**
     * Handle `after-attach` messages for the widget.
     */
    CompleterWidget.prototype.onAfterAttach = function (msg) {
        document.addEventListener('keydown', this, USE_CAPTURE);
        document.addEventListener('mousedown', this, USE_CAPTURE);
        document.addEventListener('scroll', this, USE_CAPTURE);
    };
    /**
     * Handle `before-detach` messages for the widget.
     */
    CompleterWidget.prototype.onBeforeDetach = function (msg) {
        document.removeEventListener('keydown', this, USE_CAPTURE);
        document.removeEventListener('mousedown', this, USE_CAPTURE);
        document.removeEventListener('scroll', this, USE_CAPTURE);
    };
    /**
     * Handle model state changes.
     */
    CompleterWidget.prototype.onModelStateChanged = function () {
        if (this.isAttached) {
            this._activeIndex = 0;
            this.update();
        }
    };
    /**
     * Handle `update-request` messages.
     */
    CompleterWidget.prototype.onUpdateRequest = function (msg) {
        var model = this._model;
        if (!model) {
            return;
        }
        if (this._resetFlag) {
            this._resetFlag = false;
            if (!this.isHidden) {
                this.hide();
                this._visibilityChanged.emit(void 0);
            }
            return;
        }
        var items = algorithm_1.toArray(model.items());
        // If there are no items, reset and bail.
        if (!items || !items.length) {
            this._resetFlag = true;
            this.reset();
            if (!this.isHidden) {
                this.hide();
                this._visibilityChanged.emit(void 0);
            }
            return;
        }
        // If there is only one item, signal and bail.
        if (items.length === 1) {
            this._selected.emit(items[0].raw);
            this.reset();
            return;
        }
        // Clear the node.
        var node = this.node;
        node.textContent = '';
        // Populate the completer items.
        for (var _i = 0, items_1 = items; _i < items_1.length; _i++) {
            var item = items_1[_i];
            var li = this._renderer.createItemNode(item);
            // Set the raw, un-marked up value as a data attribute.
            li.setAttribute('data-value', item.raw);
            node.appendChild(li);
        }
        var active = node.querySelectorAll("." + ITEM_CLASS)[this._activeIndex];
        active.classList.add(ACTIVE_CLASS);
        // If this is the first time the current completer session has loaded,
        // populate any initial subset match.
        if (this._model.subsetMatch) {
            var populated = this._populateSubset();
            this.model.subsetMatch = false;
            if (populated) {
                this.update();
                return;
            }
        }
        if (this.isHidden) {
            this.show();
            this._setGeometry();
            this._visibilityChanged.emit(void 0);
        }
        else {
            this._setGeometry();
        }
    };
    /**
     * Cycle through the available completer items.
     *
     * #### Notes
     * When the user cycles all the way `down` to the last index, subsequent
     * `down` cycles will remain on the last index. When the user cycles `up` to
     * the first item, subsequent `up` cycles will remain on the first cycle.
     */
    CompleterWidget.prototype._cycle = function (direction) {
        var items = this.node.querySelectorAll("." + ITEM_CLASS);
        var index = this._activeIndex;
        var active = this.node.querySelector("." + ACTIVE_CLASS);
        active.classList.remove(ACTIVE_CLASS);
        if (direction === 'up') {
            this._activeIndex = index === 0 ? index : index - 1;
        }
        else {
            this._activeIndex = index < items.length - 1 ? index + 1 : index;
        }
        active = items[this._activeIndex];
        active.classList.add(ACTIVE_CLASS);
        domutils_1.ElementExt.scrollIntoViewIfNeeded(this.node, active);
    };
    /**
     * Handle keydown events for the widget.
     */
    CompleterWidget.prototype._evtKeydown = function (event) {
        if (this.isHidden || !this._editor) {
            return;
        }
        if (!this._editor.host.contains(event.target)) {
            this.reset();
            return;
        }
        switch (event.keyCode) {
            case 9:
                event.preventDefault();
                event.stopPropagation();
                event.stopImmediatePropagation();
                this._model.subsetMatch = true;
                var populated = this._populateSubset();
                this.model.subsetMatch = false;
                if (populated) {
                    return;
                }
                this.selectActive();
                return;
            case 27:
                event.preventDefault();
                event.stopPropagation();
                event.stopImmediatePropagation();
                this.reset();
                return;
            case 38: // Up arrow key
            case 40:
                event.preventDefault();
                event.stopPropagation();
                event.stopImmediatePropagation();
                this._cycle(event.keyCode === 38 ? 'up' : 'down');
                return;
            default:
                return;
        }
    };
    /**
     * Handle mousedown events for the widget.
     */
    CompleterWidget.prototype._evtMousedown = function (event) {
        if (this.isHidden || !this._editor) {
            return;
        }
        if (Private.nonstandardClick(event)) {
            this.reset();
            return;
        }
        var target = event.target;
        while (target !== document.documentElement) {
            // If the user has made a selection, emit its value and reset the widget.
            if (target.classList.contains(ITEM_CLASS)) {
                event.preventDefault();
                event.stopPropagation();
                event.stopImmediatePropagation();
                this._selected.emit(target.getAttribute('data-value'));
                this.reset();
                return;
            }
            // If the mouse event happened anywhere else in the widget, bail.
            if (target === this.node) {
                event.preventDefault();
                event.stopPropagation();
                event.stopImmediatePropagation();
                return;
            }
            target = target.parentElement;
        }
        this.reset();
    };
    /**
     * Handle scroll events for the widget
     */
    CompleterWidget.prototype._evtScroll = function (event) {
        if (this.isHidden || !this._editor) {
            return;
        }
        // All scrolls except scrolls in the actual hover box node may cause the
        // referent editor that anchors the node to move, so the only scroll events
        // that can safely be ignored are ones that happen inside the hovering node.
        if (this.node.contains(event.target)) {
            return;
        }
        this._setGeometry();
    };
    /**
     * Populate the completer up to the longest initial subset of items.
     *
     * @returns `true` if a subset match was found and populated.
     */
    CompleterWidget.prototype._populateSubset = function () {
        var items = this.node.querySelectorAll("." + ITEM_CLASS);
        var subset = Private.commonSubset(Private.itemValues(items));
        var query = this.model.query;
        if (subset && subset !== query && subset.indexOf(query) === 0) {
            this.model.query = subset;
            this._selected.emit(subset);
            return true;
        }
        return false;
    };
    /**
     * Set the visible dimensions of the widget.
     */
    CompleterWidget.prototype._setGeometry = function () {
        var model = this._model;
        // This is an overly defensive test: `cursor` will always exist if
        // `original` exists, except in contrived tests. But since it is possible
        // to generate a runtime error, the check occurs here.
        if (!model || !model.original || !model.cursor) {
            return;
        }
        var editor = this._editor;
        var position = editor.getPositionAt(model.cursor.start);
        var anchor = editor.getCoordinateForPosition(position);
        var style = window.getComputedStyle(this.node);
        var borderLeft = parseInt(style.borderLeftWidth, 10) || 0;
        var paddingLeft = parseInt(style.paddingLeft, 10) || 0;
        // Calculate the geometry of the completer.
        apputils_1.HoverBox.setGeometry({
            anchor: anchor,
            host: editor.host,
            maxHeight: MAX_HEIGHT,
            minHeight: MIN_HEIGHT,
            node: this.node,
            offset: { horizontal: borderLeft + paddingLeft },
            privilege: 'below'
        });
    };
    return CompleterWidget;
}(widgets_1.Widget));
exports.CompleterWidget = CompleterWidget;
(function (CompleterWidget) {
    /**
     * The default implementation of an `IRenderer`.
     */
    var Renderer = (function () {
        function Renderer() {
        }
        /**
         * Create an item node for a text completer menu.
         */
        Renderer.prototype.createItemNode = function (item) {
            var li = document.createElement('li');
            var code = document.createElement('code');
            // Use innerHTML because search results include <mark> tags.
            code.innerHTML = item.text;
            li.className = ITEM_CLASS;
            li.appendChild(code);
            return li;
        };
        return Renderer;
    }());
    CompleterWidget.Renderer = Renderer;
    /**
     * The default `IRenderer` instance.
     */
    CompleterWidget.defaultRenderer = new Renderer();
})(CompleterWidget = exports.CompleterWidget || (exports.CompleterWidget = {}));
exports.CompleterWidget = CompleterWidget;
/**
 * A namespace for completer widget private data.
 */
var Private;
(function (Private) {
    /**
     * Returns the common subset string that a list of strings shares.
     */
    function commonSubset(values) {
        var len = values.length;
        var subset = '';
        if (len < 2) {
            return subset;
        }
        var strlen = values[0].length;
        for (var i = 0; i < strlen; i++) {
            var ch = values[0][i];
            for (var j = 1; j < len; j++) {
                if (values[j][i] !== ch) {
                    return subset;
                }
            }
            subset += ch;
        }
        return subset;
    }
    Private.commonSubset = commonSubset;
    /**
     * Returns the list of raw item values currently in the DOM.
     */
    function itemValues(items) {
        var values = [];
        for (var i = 0, len = items.length; i < len; i++) {
            values.push(items[i].getAttribute('data-value'));
        }
        return values;
    }
    Private.itemValues = itemValues;
    /**
     * Returns true for any modified click event (i.e., not a left-click).
     */
    function nonstandardClick(event) {
        return event.button !== 0 ||
            event.altKey ||
            event.ctrlKey ||
            event.shiftKey ||
            event.metaKey;
    }
    Private.nonstandardClick = nonstandardClick;
})(Private || (Private = {}));

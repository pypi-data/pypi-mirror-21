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
var properties_1 = require("@phosphor/properties");
var widgets_1 = require("@phosphor/widgets");
/**
 * The class name added to toolbars.
 */
var TOOLBAR_CLASS = 'jp-Toolbar';
/**
 * The class name added to toolbar items.
 */
var TOOLBAR_ITEM_CLASS = 'jp-Toolbar-item';
/**
 * The class name added to toolbar buttons.
 */
var TOOLBAR_BUTTON_CLASS = 'jp-Toolbar-button';
/**
 * The class name added to a pressed button.
 */
var TOOLBAR_PRESSED_CLASS = 'jp-mod-pressed';
/**
 * The class name added to toolbar interrupt button.
 */
var TOOLBAR_INTERRUPT_CLASS = 'jp-StopIcon';
/**
 * The class name added to toolbar restart button.
 */
var TOOLBAR_RESTART_CLASS = 'jp-RefreshIcon';
/**
 * The class name added to toolbar kernel name text.
 */
var TOOLBAR_KERNEL_CLASS = 'jp-Kernel-toolbarKernelName';
/**
 * The class name added to toolbar kernel indicator icon.
 */
var TOOLBAR_INDICATOR_CLASS = 'jp-Kernel-toolbarKernelIndicator';
/**
 * The class name added to a busy kernel indicator.
 */
var TOOLBAR_BUSY_CLASS = 'jp-mod-busy';
/**
 * A class which provides a toolbar widget.
 */
var Toolbar = (function (_super) {
    __extends(Toolbar, _super);
    /**
     * Construct a new toolbar widget.
     */
    function Toolbar() {
        var _this = _super.call(this) || this;
        _this.addClass(TOOLBAR_CLASS);
        _this.layout = new widgets_1.PanelLayout();
        return _this;
    }
    /**
     * Get an iterator over the ordered toolbar item names.
     *
     * @returns An iterator over the toolbar item names.
     */
    Toolbar.prototype.names = function () {
        var layout = this.layout;
        return algorithm_1.map(layout.widgets, function (widget) {
            return Private.nameProperty.get(widget);
        });
    };
    /**
     * Add an item to the end of the toolbar.
     *
     * @param name - The name of the widget to add to the toolbar.
     *
     * @param widget - The widget to add to the toolbar.
     *
     * @param index - The optional name of the item to insert after.
     *
     * @returns Whether the item was added to toolbar.  Returns false if
     *   an item of the same name is already in the toolbar.
     */
    Toolbar.prototype.addItem = function (name, widget) {
        var layout = this.layout;
        return this.insertItem(layout.widgets.length, name, widget);
    };
    /**
     * Insert an item into the toolbar at the specified index.
     *
     * @param index - The index at which to insert the item.
     *
     * @param name - The name of the item.
     *
     * @param widget - The widget to add.
     *
     * @returns Whether the item was added to the toolbar. Returns false if
     *   an item of the same name is already in the toolbar.
     *
     * #### Notes
     * The index will be clamped to the bounds of the items.
     */
    Toolbar.prototype.insertItem = function (index, name, widget) {
        var existing = algorithm_1.find(this.names(), function (value) { return value === name; });
        if (existing) {
            return false;
        }
        widget.addClass(TOOLBAR_ITEM_CLASS);
        var layout = this.layout;
        layout.insertWidget(index, widget);
        Private.nameProperty.set(widget, name);
        return true;
    };
    /**
     * Remove an item in the toolbar by value.
     *
     *  @param name - The name of the widget to remove from the toolbar.
     */
    Toolbar.prototype.removeItem = function (widget) {
        var layout = this.layout;
        layout.removeWidget(widget);
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
    Toolbar.prototype.handleEvent = function (event) {
        switch (event.type) {
            case 'click':
                if (!this.node.contains(document.activeElement)) {
                    this.parent.activate();
                }
                break;
            default:
                break;
        }
    };
    /**
     * Handle `after-attach` messages for the widget.
     */
    Toolbar.prototype.onAfterAttach = function (msg) {
        this.node.addEventListener('click', this);
    };
    /**
     * Handle `before-detach` messages for the widget.
     */
    Toolbar.prototype.onBeforeDetach = function (msg) {
        this.node.removeEventListener('click', this);
    };
    return Toolbar;
}(widgets_1.Widget));
exports.Toolbar = Toolbar;
/**
 * The namespace for Toolbar class statics.
 */
(function (Toolbar) {
    /**
     * Create an interrupt toolbar item.
     */
    function createInterruptButton(session) {
        return new ToolbarButton({
            className: TOOLBAR_INTERRUPT_CLASS,
            onClick: function () {
                if (session.kernel) {
                    session.kernel.interrupt();
                }
            },
            tooltip: 'Interrupt the kernel'
        });
    }
    Toolbar.createInterruptButton = createInterruptButton;
    /**
     * Create a restart toolbar item.
     */
    function createRestartButton(session) {
        return new ToolbarButton({
            className: TOOLBAR_RESTART_CLASS,
            onClick: function () {
                session.restart();
            },
            tooltip: 'Restart the kernel'
        });
    }
    Toolbar.createRestartButton = createRestartButton;
    /**
     * Create a kernel name indicator item.
     *
     * #### Notes
     * It will display the `'display_name`' of the current kernel,
     * or `'No Kernel!'` if there is no kernel.
     * It can handle a change in context or kernel.
     */
    function createKernelNameItem(session) {
        return new Private.KernelName(session);
    }
    Toolbar.createKernelNameItem = createKernelNameItem;
    /**
     * Create a kernel status indicator item.
     *
     * #### Notes
     * It show display a busy status if the kernel status is
     * not idle.
     * It will show the current status in the node title.
     * It can handle a change to the context or the kernel.
     */
    function createKernelStatusItem(session) {
        return new Private.KernelIndicator(session);
    }
    Toolbar.createKernelStatusItem = createKernelStatusItem;
})(Toolbar = exports.Toolbar || (exports.Toolbar = {}));
exports.Toolbar = Toolbar;
/**
 * A widget which acts as a button in a toolbar.
 */
var ToolbarButton = (function (_super) {
    __extends(ToolbarButton, _super);
    /**
     * Construct a new toolbar button.
     */
    function ToolbarButton(options) {
        if (options === void 0) { options = {}; }
        var _this = _super.call(this, { node: document.createElement('span') }) || this;
        options = options || {};
        _this.addClass(TOOLBAR_BUTTON_CLASS);
        _this._onClick = options.onClick;
        if (options.className) {
            _this.addClass(options.className);
        }
        _this.node.title = options.tooltip || '';
        return _this;
    }
    /**
     * Dispose of the resources held by the widget.
     */
    ToolbarButton.prototype.dispose = function () {
        this._onClick = null;
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
    ToolbarButton.prototype.handleEvent = function (event) {
        switch (event.type) {
            case 'click':
                if (this._onClick) {
                    this._onClick();
                }
                break;
            case 'mousedown':
                this.addClass(TOOLBAR_PRESSED_CLASS);
                break;
            case 'mouseup':
            case 'mouseout':
                this.removeClass(TOOLBAR_PRESSED_CLASS);
                break;
            default:
                break;
        }
    };
    /**
     * Handle `after-attach` messages for the widget.
     */
    ToolbarButton.prototype.onAfterAttach = function (msg) {
        this.node.addEventListener('click', this);
        this.node.addEventListener('mousedown', this);
        this.node.addEventListener('mouseup', this);
        this.node.addEventListener('mouseout', this);
    };
    /**
     * Handle `before-detach` messages for the widget.
     */
    ToolbarButton.prototype.onBeforeDetach = function (msg) {
        this.node.removeEventListener('click', this);
        this.node.removeEventListener('mousedown', this);
        this.node.removeEventListener('mouseup', this);
        this.node.removeEventListener('mouseout', this);
    };
    return ToolbarButton;
}(widgets_1.Widget));
exports.ToolbarButton = ToolbarButton;
/**
 * A namespace for private data.
 */
var Private;
(function (Private) {
    /**
     * An attached property for the name of a toolbar item.
     */
    Private.nameProperty = new properties_1.AttachedProperty({
        name: 'name',
        create: function () { return ''; }
    });
    /**
     * A kernel name widget.
     */
    var KernelName = (function (_super) {
        __extends(KernelName, _super);
        /**
         * Construct a new kernel name widget.
         */
        function KernelName(session) {
            var _this = _super.call(this) || this;
            _this.addClass(TOOLBAR_KERNEL_CLASS);
            _this._onKernelChanged(session);
            session.kernelChanged.connect(_this._onKernelChanged, _this);
            return _this;
        }
        /**
         * Update the text of the kernel name item.
         */
        KernelName.prototype._onKernelChanged = function (session) {
            this.node.textContent = session.kernelDisplayName;
        };
        return KernelName;
    }(widgets_1.Widget));
    Private.KernelName = KernelName;
    /**
     * A toolbar item that displays kernel status.
     */
    var KernelIndicator = (function (_super) {
        __extends(KernelIndicator, _super);
        /**
         * Construct a new kernel status widget.
         */
        function KernelIndicator(session) {
            var _this = _super.call(this) || this;
            _this.addClass(TOOLBAR_INDICATOR_CLASS);
            _this._onStatusChanged(session);
            session.statusChanged.connect(_this._onStatusChanged, _this);
            return _this;
        }
        /**
         * Handle a status on a kernel.
         */
        KernelIndicator.prototype._onStatusChanged = function (session) {
            if (this.isDisposed) {
                return;
            }
            var status = session.status;
            this.toggleClass(TOOLBAR_BUSY_CLASS, status !== 'idle');
            var title = 'Kernel ' + status[0].toUpperCase() + status.slice(1);
            this.node.title = title;
        };
        return KernelIndicator;
    }(widgets_1.Widget));
    Private.KernelIndicator = KernelIndicator;
})(Private || (Private = {}));

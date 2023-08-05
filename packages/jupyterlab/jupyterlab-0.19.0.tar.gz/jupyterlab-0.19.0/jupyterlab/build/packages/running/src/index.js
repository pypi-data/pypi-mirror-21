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
var signaling_1 = require("@phosphor/signaling");
var domutils_1 = require("@phosphor/domutils");
var widgets_1 = require("@phosphor/widgets");
var apputils_1 = require("@jupyterlab/apputils");
/**
 * The class name added to a running widget.
 */
var RUNNING_CLASS = 'jp-RunningSessions';
/**
 * The class name added to a running widget header.
 */
var HEADER_CLASS = 'jp-RunningSessions-header';
/**
 * The class name added to a running widget header refresh button.
 */
var REFRESH_CLASS = 'jp-RunningSessions-headerRefresh';
/**
 * The class name added to the running terminal sessions section.
 */
var SECTION_CLASS = 'jp-RunningSessions-section';
/**
 * The class name added to the running terminal sessions section.
 */
var TERMINALS_CLASS = 'jp-RunningSessions-terminalSection';
/**
 * The class name added to the running kernel sessions section.
 */
var SESSIONS_CLASS = 'jp-RunningSessions-sessionsSection';
/**
 * The class name added to the running sessions section header.
 */
var SECTION_HEADER_CLASS = 'jp-RunningSessions-sectionHeader';
/**
 * The class name added to a section container.
 */
var CONTAINER_CLASS = 'jp-RunningSessions-sectionContainer';
/**
 * The class name added to the running kernel sessions section list.
 */
var LIST_CLASS = 'jp-RunningSessions-sectionList';
/**
 * The class name added to the running sessions items.
 */
var ITEM_CLASS = 'jp-RunningSessions-item';
/**
 * The class name added to a running session item icon.
 */
var ITEM_ICON_CLASS = 'jp-RunningSessions-itemIcon';
/**
 * The class name added to a running session item label.
 */
var ITEM_LABEL_CLASS = 'jp-RunningSessions-itemLabel';
/**
 * The class name added to a running session item shutdown button.
 */
var SHUTDOWN_BUTTON_CLASS = 'jp-RunningSessions-itemShutdown';
/**
 * The class name added to a notebook icon.
 */
var NOTEBOOK_ICON_CLASS = 'jp-mod-notebook';
/**
 * The class name added to a console icon.
 */
var CONSOLE_ICON_CLASS = 'jp-mod-console';
/**
 * The class name added to a file icon.
 */
var FILE_ICON_CLASS = 'jp-mod-file';
/**
 * The class name added to a terminal icon.
 */
var TERMINAL_ICON_CLASS = 'jp-mod-terminal';
/**
 * A regex for console names.
 */
exports.CONSOLE_REGEX = /^console-(\d)+-[0-9a-f]+$/;
/**
 * A class that exposes the running terminal and kernel sessions.
 */
var RunningSessions = (function (_super) {
    __extends(RunningSessions, _super);
    /**
     * Construct a new running widget.
     */
    function RunningSessions(options) {
        var _this = _super.call(this, {
            node: (options.renderer || RunningSessions.defaultRenderer).createNode()
        }) || this;
        _this._manager = null;
        _this._renderer = null;
        _this._runningSessions = [];
        _this._runningTerminals = [];
        _this._refreshId = -1;
        _this._sessionOpenRequested = new signaling_1.Signal(_this);
        _this._terminalOpenRequested = new signaling_1.Signal(_this);
        var manager = _this._manager = options.manager;
        _this._renderer = options.renderer || RunningSessions.defaultRenderer;
        _this.addClass(RUNNING_CLASS);
        // Populate the terminals section.
        if (manager.terminals.isAvailable()) {
            var termNode = apputils_1.DOMUtils.findElement(_this.node, TERMINALS_CLASS);
            var termHeader = _this._renderer.createTerminalHeaderNode();
            termHeader.className = SECTION_HEADER_CLASS;
            termNode.appendChild(termHeader);
            var termContainer = document.createElement('div');
            termContainer.className = CONTAINER_CLASS;
            var termList = document.createElement('ul');
            termList.className = LIST_CLASS;
            termContainer.appendChild(termList);
            termNode.appendChild(termContainer);
            manager.terminals.runningChanged.connect(_this._onTerminalsChanged, _this);
        }
        // Populate the sessions section.
        var sessionNode = apputils_1.DOMUtils.findElement(_this.node, SESSIONS_CLASS);
        var sessionHeader = _this._renderer.createSessionHeaderNode();
        sessionHeader.className = SECTION_HEADER_CLASS;
        sessionNode.appendChild(sessionHeader);
        var sessionContainer = document.createElement('div');
        sessionContainer.className = CONTAINER_CLASS;
        var sessionList = document.createElement('ul');
        sessionList.className = LIST_CLASS;
        sessionContainer.appendChild(sessionList);
        sessionNode.appendChild(sessionContainer);
        manager.sessions.runningChanged.connect(_this._onSessionsChanged, _this);
        return _this;
    }
    Object.defineProperty(RunningSessions.prototype, "sessionOpenRequested", {
        /**
         * A signal emitted when a kernel session open is requested.
         */
        get: function () {
            return this._sessionOpenRequested;
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(RunningSessions.prototype, "terminalOpenRequested", {
        /**
         * A signal emitted when a terminal session open is requested.
         */
        get: function () {
            return this._terminalOpenRequested;
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(RunningSessions.prototype, "renderer", {
        /**
         * The renderer used by the running sessions widget.
         */
        get: function () {
            return this._renderer;
        },
        enumerable: true,
        configurable: true
    });
    /**
     * Dispose of the resources used by the widget.
     */
    RunningSessions.prototype.dispose = function () {
        this._manager = null;
        this._runningSessions = null;
        this._runningTerminals = null;
        this._renderer = null;
        _super.prototype.dispose.call(this);
    };
    /**
     * Refresh the widget.
     */
    RunningSessions.prototype.refresh = function () {
        var terminals = this._manager.terminals;
        var sessions = this._manager.sessions;
        clearTimeout(this._refreshId);
        var promises = [];
        if (terminals.isAvailable()) {
            promises.push(terminals.refreshRunning());
        }
        promises.push(sessions.refreshRunning());
        return Promise.all(promises).then(function () { return void 0; });
    };
    /**
     * Handle the DOM events for the widget.
     *
     * @param event - The DOM event sent to the widget.
     *
     * #### Notes
     * This method implements the DOM `EventListener` interface and is
     * called in response to events on the widget's DOM nodes. It should
     * not be called directly by user code.
     */
    RunningSessions.prototype.handleEvent = function (event) {
        if (event.type === 'click') {
            this._evtClick(event);
        }
    };
    /**
     * A message handler invoked on an `'after-attach'` message.
     */
    RunningSessions.prototype.onAfterAttach = function (msg) {
        this.node.addEventListener('click', this);
    };
    /**
     * A message handler invoked on a `'before-detach'` message.
     */
    RunningSessions.prototype.onBeforeDetach = function (msg) {
        this.node.removeEventListener('click', this);
    };
    /**
     * A message handler invoked on an `'update-request'` message.
     */
    RunningSessions.prototype.onUpdateRequest = function (msg) {
        // Fetch common variables.
        var termSection = apputils_1.DOMUtils.findElement(this.node, TERMINALS_CLASS);
        var termList = apputils_1.DOMUtils.findElement(termSection, LIST_CLASS);
        var sessionSection = apputils_1.DOMUtils.findElement(this.node, SESSIONS_CLASS);
        var sessionList = apputils_1.DOMUtils.findElement(sessionSection, LIST_CLASS);
        var renderer = this._renderer;
        var specs = this._manager.specs;
        // Create a dummy div if terminals are not available.
        termList = termList || document.createElement('div');
        // Remove any excess item nodes.
        while (termList.children.length > this._runningTerminals.length) {
            termList.removeChild(termList.firstChild);
        }
        while (sessionList.children.length > this._runningSessions.length) {
            sessionList.removeChild(sessionList.firstChild);
        }
        // Add any missing item nodes.
        while (termList.children.length < this._runningTerminals.length) {
            var node = renderer.createTerminalNode();
            node.classList.add(ITEM_CLASS);
            termList.appendChild(node);
        }
        while (sessionList.children.length < this._runningSessions.length) {
            var node = renderer.createSessionNode();
            node.classList.add(ITEM_CLASS);
            sessionList.appendChild(node);
        }
        // Populate the nodes.
        for (var i = 0; i < this._runningTerminals.length; i++) {
            var node = termList.children[i];
            renderer.updateTerminalNode(node, this._runningTerminals[i]);
        }
        for (var i = 0; i < this._runningSessions.length; i++) {
            var node = sessionList.children[i];
            var model = this._runningSessions[i];
            var kernelName = model.kernel.name;
            if (specs) {
                kernelName = specs.kernelspecs[kernelName].display_name;
            }
            renderer.updateSessionNode(node, model, kernelName);
        }
    };
    /**
     * Handle the `'click'` event for the widget.
     *
     * #### Notes
     * This listener is attached to the document node.
     */
    RunningSessions.prototype._evtClick = function (event) {
        // Fetch common variables.
        var termSection = apputils_1.DOMUtils.findElement(this.node, TERMINALS_CLASS);
        var termList = apputils_1.DOMUtils.findElement(termSection, LIST_CLASS);
        var sessionSection = apputils_1.DOMUtils.findElement(this.node, SESSIONS_CLASS);
        var sessionList = apputils_1.DOMUtils.findElement(sessionSection, LIST_CLASS);
        var refresh = apputils_1.DOMUtils.findElement(this.node, REFRESH_CLASS);
        var renderer = this._renderer;
        var clientX = event.clientX;
        var clientY = event.clientY;
        // Check for a refresh.
        if (domutils_1.ElementExt.hitTest(refresh, clientX, clientY)) {
            return;
        }
        // Check for a terminal item click.
        var index = apputils_1.DOMUtils.hitTestNodes(termList.children, clientX, clientY);
        if (index !== -1) {
            var node = termList.children[index];
            var shutdown = renderer.getTerminalShutdown(node);
            var model = this._runningTerminals[index];
            if (domutils_1.ElementExt.hitTest(shutdown, clientX, clientY)) {
                this._manager.terminals.shutdown(model.name);
                return;
            }
            this._terminalOpenRequested.emit(model);
        }
        // Check for a session item click.
        index = apputils_1.DOMUtils.hitTestNodes(sessionList.children, clientX, clientY);
        if (index !== -1) {
            var node = sessionList.children[index];
            var shutdown = renderer.getSessionShutdown(node);
            var model = this._runningSessions[index];
            if (domutils_1.ElementExt.hitTest(shutdown, clientX, clientY)) {
                this._manager.sessions.shutdown(model.id);
                return;
            }
            this._sessionOpenRequested.emit(model);
        }
    };
    /**
     * Handle a change to the running sessions.
     */
    RunningSessions.prototype._onSessionsChanged = function (sender, models) {
        // Strip out non-file backed sessions.
        this._runningSessions = [];
        for (var _i = 0, models_1 = models; _i < models_1.length; _i++) {
            var session = models_1[_i];
            var name_1 = session.notebook.path.split('/').pop();
            if (name_1.indexOf('.') !== -1 || exports.CONSOLE_REGEX.test(name_1)) {
                this._runningSessions.push(session);
            }
        }
        this.update();
    };
    /**
     * Handle a change to the running terminals.
     */
    RunningSessions.prototype._onTerminalsChanged = function (sender, models) {
        this._runningTerminals = models;
        this.update();
    };
    return RunningSessions;
}(widgets_1.Widget));
exports.RunningSessions = RunningSessions;
/**
 * The namespace for the `RunningSessions` class statics.
 */
(function (RunningSessions) {
    /**
     * The default implementation of `IRenderer`.
     */
    var Renderer = (function () {
        function Renderer() {
        }
        /**
         * Create the root node for the running sessions widget.
         */
        Renderer.prototype.createNode = function () {
            var node = document.createElement('div');
            var header = document.createElement('div');
            header.className = HEADER_CLASS;
            var terminals = document.createElement('div');
            terminals.className = SECTION_CLASS + " " + TERMINALS_CLASS;
            var sessions = document.createElement('div');
            sessions.className = SECTION_CLASS + " " + SESSIONS_CLASS;
            var refresh = document.createElement('button');
            refresh.className = REFRESH_CLASS;
            header.appendChild(refresh);
            node.appendChild(header);
            node.appendChild(terminals);
            node.appendChild(sessions);
            return node;
        };
        /**
         * Create a fully populated header node for the terminals section.
         *
         * @returns A new node for a running terminal session header.
         */
        Renderer.prototype.createTerminalHeaderNode = function () {
            var node = document.createElement('div');
            node.textContent = 'Terminal Sessions';
            return node;
        };
        /**
         * Create a fully populated header node for the sessions section.
         *
         * @returns A new node for a running kernel session header.
         */
        Renderer.prototype.createSessionHeaderNode = function () {
            var node = document.createElement('div');
            node.textContent = 'Kernel Sessions';
            return node;
        };
        /**
         * Create a node for a running terminal session item.
         *
         * @returns A new node for a running terminal session item.
         *
         * #### Notes
         * The data in the node should be uninitialized.
         *
         * The `updateTerminalNode` method will be called for initialization.
         */
        Renderer.prototype.createTerminalNode = function () {
            var node = document.createElement('li');
            var icon = document.createElement('span');
            icon.className = ITEM_ICON_CLASS + " " + TERMINAL_ICON_CLASS;
            var label = document.createElement('span');
            label.className = ITEM_LABEL_CLASS;
            var shutdown = document.createElement('button');
            shutdown.className = SHUTDOWN_BUTTON_CLASS + " jp-mod-styled";
            shutdown.textContent = 'SHUTDOWN';
            node.appendChild(icon);
            node.appendChild(label);
            node.appendChild(shutdown);
            return node;
        };
        /**
         * Create a node for a running kernel session item.
         *
         * @returns A new node for a running kernel session item.
         *
         * #### Notes
         * The data in the node should be uninitialized.
         *
         * The `updateSessionNode` method will be called for initialization.
         */
        Renderer.prototype.createSessionNode = function () {
            var node = document.createElement('li');
            var icon = document.createElement('span');
            icon.className = ITEM_ICON_CLASS;
            var label = document.createElement('span');
            label.className = ITEM_LABEL_CLASS;
            var shutdown = document.createElement('button');
            shutdown.className = SHUTDOWN_BUTTON_CLASS + " jp-mod-styled";
            shutdown.textContent = 'SHUTDOWN';
            node.appendChild(icon);
            node.appendChild(label);
            node.appendChild(shutdown);
            return node;
        };
        /**
         * Get the shutdown node for a terminal node.
         *
         * @param node - A node created by a call to `createTerminalNode`.
         *
         * @returns The node representing the shutdown option.
         *
         * #### Notes
         * A click on this node is considered a shutdown request.
         * A click anywhere else on the node is considered an open request.
         */
        Renderer.prototype.getTerminalShutdown = function (node) {
            return apputils_1.DOMUtils.findElement(node, SHUTDOWN_BUTTON_CLASS);
        };
        /**
         * Get the shutdown node for a session node.
         *
         * @param node - A node created by a call to `createSessionNode`.
         *
         * @returns The node representing the shutdown option.
         *
         * #### Notes
         * A click on this node is considered a shutdown request.
         * A click anywhere else on the node is considered an open request.
         */
        Renderer.prototype.getSessionShutdown = function (node) {
            return apputils_1.DOMUtils.findElement(node, SHUTDOWN_BUTTON_CLASS);
        };
        /**
         * Populate a node with running terminal session data.
         *
         * @param node - A node created by a call to `createTerminalNode`.
         *
         * @param models - The list of terminal session models.
         *
         * #### Notes
         * This method should completely reset the state of the node to
         * reflect the data for the session models.
         */
        Renderer.prototype.updateTerminalNode = function (node, model) {
            var label = apputils_1.DOMUtils.findElement(node, ITEM_LABEL_CLASS);
            label.textContent = "terminals/" + model.name;
        };
        /**
         * Populate a node with running kernel session data.
         *
         * @param node - A node created by a call to `createSessionNode`.
         *
         * @param models - The list of kernel session models.
         *
         * @param kernelName - The kernel display name.
         *
         * #### Notes
         * This method should completely reset the state of the node to
         * reflect the data for the session models.
         */
        Renderer.prototype.updateSessionNode = function (node, model, kernelName) {
            var icon = apputils_1.DOMUtils.findElement(node, ITEM_ICON_CLASS);
            var path = model.notebook.path;
            var name = path.split('/').pop();
            if (name.indexOf('.ipynb') !== -1) {
                icon.className = ITEM_ICON_CLASS + " " + NOTEBOOK_ICON_CLASS;
            }
            else if (exports.CONSOLE_REGEX.test(name)) {
                icon.className = ITEM_ICON_CLASS + " " + CONSOLE_ICON_CLASS;
                path = "Console " + name.match(exports.CONSOLE_REGEX)[1];
            }
            else {
                icon.className = ITEM_ICON_CLASS + " " + FILE_ICON_CLASS;
            }
            var label = apputils_1.DOMUtils.findElement(node, ITEM_LABEL_CLASS);
            label.textContent = path;
            var title = ("Path: " + model.notebook.path + "\n" +
                ("Kernel: " + kernelName));
            label.title = title;
        };
        return Renderer;
    }());
    RunningSessions.Renderer = Renderer;
    /**
     * The default `Renderer` instance.
     */
    RunningSessions.defaultRenderer = new Renderer();
})(RunningSessions = exports.RunningSessions || (exports.RunningSessions = {}));
exports.RunningSessions = RunningSessions;

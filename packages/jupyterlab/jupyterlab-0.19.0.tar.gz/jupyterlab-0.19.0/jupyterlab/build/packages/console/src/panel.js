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
var apputils_1 = require("@jupyterlab/apputils");
var coreutils_1 = require("@jupyterlab/coreutils");
var rendermime_1 = require("@jupyterlab/rendermime");
var coreutils_2 = require("@phosphor/coreutils");
var widgets_1 = require("@phosphor/widgets");
var widget_1 = require("./widget");
/**
 * The class name added to console panels.
 */
var PANEL_CLASS = 'jp-ConsolePanel';
/**
 * A panel which contains a console and the ability to add other children.
 */
var ConsolePanel = (function (_super) {
    __extends(ConsolePanel, _super);
    /**
     * Construct a console panel.
     */
    function ConsolePanel(options) {
        var _this = _super.call(this) || this;
        _this._executed = null;
        _this._connected = null;
        _this.addClass(PANEL_CLASS);
        var rendermime = options.rendermime, mimeTypeService = options.mimeTypeService, path = options.path, basePath = options.basePath, name = options.name, manager = options.manager, modelFactory = options.modelFactory;
        var factory = options.contentFactory;
        var contentFactory = factory.consoleContentFactory;
        var count = Private.count++;
        if (!path) {
            path = (basePath || '') + "/console-" + count + "-" + coreutils_1.uuid();
        }
        var session = _this._session = new apputils_1.ClientSession({
            manager: manager.sessions,
            path: path,
            name: name || "Console " + count,
            type: 'console',
            kernelPreference: options.kernelPreference
        });
        rendermime.resolver = new rendermime_1.RenderMime.UrlResolver({
            session: session,
            contents: manager.contents
        });
        _this.console = factory.createConsole({
            rendermime: rendermime, session: session, mimeTypeService: mimeTypeService, contentFactory: contentFactory, modelFactory: modelFactory
        });
        _this.addWidget(_this.console);
        session.ready.then(function () {
            _this._connected = new Date();
            _this._updateTitle();
        });
        _this._manager = manager;
        _this.console.executed.connect(_this._onExecuted, _this);
        session.kernelChanged.connect(_this._updateTitle, _this);
        session.propertyChanged.connect(_this._updateTitle, _this);
        _this.title.icon = 'jp-ImageCodeConsole';
        _this.title.closable = true;
        _this.id = "console-" + count;
        return _this;
    }
    Object.defineProperty(ConsolePanel.prototype, "session", {
        /**
         * The session used by the panel.
         */
        get: function () {
            return this._session;
        },
        enumerable: true,
        configurable: true
    });
    /**
     * Dispose of the resources held by the widget.
     */
    ConsolePanel.prototype.dispose = function () {
        this.console.dispose();
        _super.prototype.dispose.call(this);
    };
    /**
     * Handle `'after-attach'` messages.
     */
    ConsolePanel.prototype.onAfterAttach = function (msg) {
        this._session.initialize();
    };
    /**
     * Handle `'activate-request'` messages.
     */
    ConsolePanel.prototype.onActivateRequest = function (msg) {
        this.console.prompt.editor.focus();
    };
    /**
     * Handle `'close-request'` messages.
     */
    ConsolePanel.prototype.onCloseRequest = function (msg) {
        _super.prototype.onCloseRequest.call(this, msg);
        this.dispose();
    };
    /**
     * Handle a console execution.
     */
    ConsolePanel.prototype._onExecuted = function (sender, args) {
        this._executed = args;
        this._updateTitle();
    };
    /**
     * Update the console panel title.
     */
    ConsolePanel.prototype._updateTitle = function () {
        Private.updateTitle(this, this._connected, this._executed);
    };
    return ConsolePanel;
}(widgets_1.Panel));
exports.ConsolePanel = ConsolePanel;
/**
 * A namespace for ConsolePanel statics.
 */
(function (ConsolePanel) {
    /**
     * Default implementation of `IContentFactory`.
     */
    var ContentFactory = (function () {
        /**
         * Create a new content factory.
         */
        function ContentFactory(options) {
            this.editorFactory = options.editorFactory;
            this.consoleContentFactory = (options.consoleContentFactory ||
                new widget_1.CodeConsole.ContentFactory({
                    editorFactory: this.editorFactory,
                    outputAreaContentFactory: options.outputAreaContentFactory,
                    codeCellContentFactory: options.codeCellContentFactory,
                    rawCellContentFactory: options.rawCellContentFactory
                }));
        }
        /**
         * Create a new console panel.
         */
        ContentFactory.prototype.createConsole = function (options) {
            return new widget_1.CodeConsole(options);
        };
        return ContentFactory;
    }());
    ConsolePanel.ContentFactory = ContentFactory;
    /* tslint:disable */
    /**
     * The console renderer token.
     */
    ConsolePanel.IContentFactory = new coreutils_2.Token('jupyter.services.console.content-factory');
    /* tslint:enable */
})(ConsolePanel = exports.ConsolePanel || (exports.ConsolePanel = {}));
exports.ConsolePanel = ConsolePanel;
/**
 * A namespace for private data.
 */
var Private;
(function (Private) {
    /**
     * The counter for new consoles.
     */
    Private.count = 1;
    /**
     * Update the title of a console panel.
     */
    function updateTitle(panel, connected, executed) {
        var session = panel.console.session;
        var caption = ("Name: " + session.name + "\n" +
            ("Directory: " + coreutils_1.PathExt.dirname(session.path) + "\n") +
            ("Kernel: " + session.kernelDisplayName));
        if (connected) {
            caption += "\nConnected: " + coreutils_1.Time.format(connected.toISOString());
        }
        if (executed) {
            caption += "\nLast Execution: " + coreutils_1.Time.format(executed.toISOString());
        }
        panel.title.label = session.name;
        panel.title.caption = caption;
    }
    Private.updateTitle = updateTitle;
})(Private || (Private = {}));

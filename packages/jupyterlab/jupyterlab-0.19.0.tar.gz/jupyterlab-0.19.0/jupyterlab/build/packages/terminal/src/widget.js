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
var messaging_1 = require("@phosphor/messaging");
var domutils_1 = require("@phosphor/domutils");
var widgets_1 = require("@phosphor/widgets");
var Xterm = require("xterm");
/**
 * The class name added to a terminal widget.
 */
var TERMINAL_CLASS = 'jp-TerminalWidget';
/**
 * The class name added to a terminal body.
 */
var TERMINAL_BODY_CLASS = 'jp-TerminalWidget-body';
/**
 * The number of rows to use in the dummy terminal.
 */
var DUMMY_ROWS = 24;
/**
 * The number of cols to use in the dummy terminal.
 */
var DUMMY_COLS = 80;
/**
 * A widget which manages a terminal session.
 */
var TerminalWidget = (function (_super) {
    __extends(TerminalWidget, _super);
    /**
     * Construct a new terminal widget.
     *
     * @param options - The terminal configuration options.
     */
    function TerminalWidget(options) {
        if (options === void 0) { options = {}; }
        var _this = _super.call(this) || this;
        _this._term = null;
        _this._sheet = null;
        _this._dummyTerm = null;
        _this._fontSize = -1;
        _this._needsSnap = true;
        _this._needsResize = true;
        _this._needsStyle = true;
        _this._rowHeight = -1;
        _this._colWidth = -1;
        _this._offsetWidth = -1;
        _this._offsetHeight = -1;
        _this._sessionSize = [1, 1, 1, 1];
        _this._background = '';
        _this._color = '';
        _this._box = null;
        _this._session = null;
        _this.addClass(TERMINAL_CLASS);
        // Create the xterm, dummy terminal, and private style sheet.
        _this._term = new Xterm(Private.getConfig(options));
        _this._initializeTerm();
        _this._dummyTerm = Private.createDummyTerm();
        _this._sheet = document.createElement('style');
        _this.node.appendChild(_this._sheet);
        // Initialize settings.
        var defaults = TerminalWidget.defaultOptions;
        _this._fontSize = options.fontSize || defaults.fontSize;
        _this._background = options.background || defaults.background;
        _this._color = options.color || defaults.color;
        _this.id = "jp-TerminalWidget-" + Private.id++;
        _this.title.label = 'Terminal';
        return _this;
    }
    Object.defineProperty(TerminalWidget.prototype, "session", {
        /**
         * The terminal session associated with the widget.
         */
        get: function () {
            return this._session;
        },
        set: function (value) {
            var _this = this;
            if (this._session && !this._session.isDisposed) {
                this._session.messageReceived.disconnect(this._onMessage, this);
            }
            this._session = value || null;
            if (!value) {
                return;
            }
            this._session.ready.then(function () {
                if (_this.isDisposed) {
                    return;
                }
                _this._session.messageReceived.connect(_this._onMessage, _this);
                _this.title.label = "Terminal " + _this._session.name;
                _this._setSessionSize();
            });
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(TerminalWidget.prototype, "fontSize", {
        /**
         * Get the font size of the terminal in pixels.
         */
        get: function () {
            return this._fontSize;
        },
        /**
         * Set the font size of the terminal in pixels.
         */
        set: function (size) {
            if (this._fontSize === size) {
                return;
            }
            this._fontSize = size;
            this._needsSnap = true;
            this.update();
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(TerminalWidget.prototype, "background", {
        /**
         * Get the background color of the terminal.
         */
        get: function () {
            return this._background;
        },
        /**
         * Set the background color of the terminal.
         */
        set: function (value) {
            if (this._background === value) {
                return;
            }
            this._background = value;
            this._needsStyle = true;
            this.update();
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(TerminalWidget.prototype, "color", {
        /**
         * Get the text color of the terminal.
         */
        get: function () {
            return this._color;
        },
        /**
         * Set the text color of the terminal.
         */
        set: function (value) {
            if (this._color === value) {
                return;
            }
            this._color = value;
            this._needsStyle = true;
            this.update();
        },
        enumerable: true,
        configurable: true
    });
    /**
     * Dispose of the resources held by the terminal widget.
     */
    TerminalWidget.prototype.dispose = function () {
        this._session = null;
        this._sheet = null;
        this._term = null;
        this._dummyTerm = null;
        this._box = null;
        _super.prototype.dispose.call(this);
    };
    /**
     * Refresh the terminal session.
     */
    TerminalWidget.prototype.refresh = function () {
        var _this = this;
        if (!this._session) {
            return Promise.reject(void 0);
        }
        return this._session.reconnect().then(function () {
            _this._term.clear();
        });
    };
    /**
     * Process a message sent to the widget.
     *
     * @param msg - The message sent to the widget.
     *
     * #### Notes
     * Subclasses may reimplement this method as needed.
     */
    TerminalWidget.prototype.processMessage = function (msg) {
        _super.prototype.processMessage.call(this, msg);
        switch (msg.type) {
            case 'fit-request':
                this.onFitRequest(msg);
                break;
            default:
                break;
        }
    };
    /**
     * Set the size of the terminal when attached if dirty.
     */
    TerminalWidget.prototype.onAfterAttach = function (msg) {
        this.update();
    };
    /**
     * Set the size of the terminal when shown if dirty.
     */
    TerminalWidget.prototype.onAfterShow = function (msg) {
        this.update();
    };
    /**
     * Dispose of the terminal when closing.
     */
    TerminalWidget.prototype.onCloseRequest = function (msg) {
        _super.prototype.onCloseRequest.call(this, msg);
        this.dispose();
    };
    /**
     * On resize, use the computed row and column sizes to resize the terminal.
     */
    TerminalWidget.prototype.onResize = function (msg) {
        this._offsetWidth = msg.width;
        this._offsetHeight = msg.height;
        this._needsResize = true;
        this.update();
    };
    /**
     * A message handler invoked on an `'update-request'` message.
     */
    TerminalWidget.prototype.onUpdateRequest = function (msg) {
        if (!this.isVisible) {
            return;
        }
        if (this._needsSnap) {
            this._snapTermSizing();
        }
        if (this._needsResize) {
            this._resizeTerminal();
        }
        if (this._needsStyle) {
            this._setStyle();
        }
    };
    /**
     * A message handler invoked on an `'fit-request'` message.
     */
    TerminalWidget.prototype.onFitRequest = function (msg) {
        var resize = widgets_1.Widget.ResizeMessage.UnknownSize;
        messaging_1.MessageLoop.sendMessage(this, resize);
    };
    /**
     * Handle `'activate-request'` messages.
     */
    TerminalWidget.prototype.onActivateRequest = function (msg) {
        this._term.focus();
    };
    /**
     * Create the terminal object.
     */
    TerminalWidget.prototype._initializeTerm = function () {
        var _this = this;
        this._term.open(this.node);
        this._term.element.classList.add(TERMINAL_BODY_CLASS);
        this._term.on('data', function (data) {
            if (_this._session) {
                _this._session.send({
                    type: 'stdin',
                    content: [data]
                });
            }
        });
        this._term.on('title', function (title) {
            _this.title.label = title;
        });
    };
    /**
     * Handle a message from the terminal session.
     */
    TerminalWidget.prototype._onMessage = function (sender, msg) {
        switch (msg.type) {
            case 'stdout':
                this._term.write(msg.content[0]);
                break;
            case 'disconnect':
                this._term.write('\r\n\r\n[Finished... Term Session]\r\n');
                break;
            default:
                break;
        }
    };
    /**
     * Use the dummy terminal to measure the row and column sizes.
     */
    TerminalWidget.prototype._snapTermSizing = function () {
        this._term.element.style.fontSize = this.fontSize + "px";
        var node = this._dummyTerm;
        this._term.element.appendChild(node);
        this._rowHeight = node.offsetHeight / DUMMY_ROWS;
        this._colWidth = node.offsetWidth / DUMMY_COLS;
        this._term.element.removeChild(node);
        this._needsSnap = false;
        this._needsResize = true;
    };
    /**
     * Resize the terminal based on computed geometry.
     */
    TerminalWidget.prototype._resizeTerminal = function () {
        var offsetWidth = this._offsetWidth;
        var offsetHeight = this._offsetHeight;
        if (offsetWidth < 0) {
            offsetWidth = this.node.offsetWidth;
        }
        if (offsetHeight < 0) {
            offsetHeight = this.node.offsetHeight;
        }
        var box = this._box || (this._box = domutils_1.ElementExt.boxSizing(this.node));
        var height = offsetHeight - box.verticalSum;
        var width = offsetWidth - box.horizontalSum;
        var rows = Math.floor(height / this._rowHeight) - 1;
        var cols = Math.floor(width / this._colWidth) - 1;
        this._term.resize(cols, rows);
        this._sessionSize = [rows, cols, height, width];
        this._setSessionSize();
        this._needsResize = false;
    };
    /**
     * Send the size to the session.
     */
    TerminalWidget.prototype._setSessionSize = function () {
        if (this._session) {
            this._session.send({
                type: 'set_size',
                content: this._sessionSize
            });
        }
    };
    /**
     * Set the stylesheet.
     */
    TerminalWidget.prototype._setStyle = function () {
        // Set the fg and bg colors of the terminal and cursor.
        this._sheet.innerHTML = ("\n      #" + this.node.id + " {\n        background: " + this._background + ";\n        color: " + this._color + ";\n      }\n      #" + this.node.id + " .xterm-viewport, #" + this.node.id + " .xterm-rows {\n        background-color: " + this._background + ";\n        color: " + this._color + ";\n      }\n      #" + this.node.id + " .terminal.focus .terminal-cursor.blinking {\n          animation: " + this.node.id + "-blink-cursor 1.2s infinite step-end;\n      }\n      @keyframes " + this.node.id + "-blink-cursor {\n          0% {\n              background-color: " + this._color + ";\n              color: " + this._background + ";\n          }\n          50% {\n              background-color: transparent;\n              color: " + this._color + ";\n          }\n      }\n    ");
        this._needsStyle = false;
    };
    return TerminalWidget;
}(widgets_1.Widget));
exports.TerminalWidget = TerminalWidget;
/**
 * The namespace for `TerminalWidget` class statics.
 */
(function (TerminalWidget) {
    /**
     * The default options used for creating terminals.
     */
    TerminalWidget.defaultOptions = {
        background: 'black',
        color: 'white',
        fontSize: 13,
        cursorBlink: true
    };
})(TerminalWidget = exports.TerminalWidget || (exports.TerminalWidget = {}));
exports.TerminalWidget = TerminalWidget;
/**
 * A namespace for private data.
 */
var Private;
(function (Private) {
    /**
     * Get term.js options from ITerminalOptions.
     */
    function getConfig(options) {
        var config = {};
        if (options.cursorBlink !== void 0) {
            config.cursorBlink = options.cursorBlink;
        }
        else {
            config.cursorBlink = TerminalWidget.defaultOptions.cursorBlink;
        }
        return config;
    }
    Private.getConfig = getConfig;
    /**
     * Create a dummy terminal element used to measure text size.
     */
    function createDummyTerm() {
        var node = document.createElement('div');
        var rowspan = document.createElement('span');
        rowspan.innerHTML = Array(DUMMY_ROWS).join('a<br>');
        var colspan = document.createElement('span');
        colspan.textContent = Array(DUMMY_COLS + 1).join('a');
        node.appendChild(rowspan);
        node.appendChild(colspan);
        node.style.visibility = 'hidden';
        node.style.position = 'absolute';
        node.style.height = 'auto';
        node.style.width = 'auto';
        node.style['white-space'] = 'nowrap';
        return node;
    }
    Private.createDummyTerm = createDummyTerm;
    /**
     * An incrementing counter for ids.
     */
    Private.id = 0;
})(Private || (Private = {}));

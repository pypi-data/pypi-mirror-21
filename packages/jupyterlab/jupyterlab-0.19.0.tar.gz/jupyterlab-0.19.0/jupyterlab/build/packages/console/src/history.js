// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var signaling_1 = require("@phosphor/signaling");
/**
 * A console history manager object.
 */
var ConsoleHistory = (function () {
    /**
     * Construct a new console history object.
     */
    function ConsoleHistory(options) {
        this._cursor = 0;
        this._hasSession = false;
        this._history = [];
        this._placeholder = '';
        this._setByHistory = false;
        this._isDisposed = false;
        this._editor = null;
        this.session = options.session;
        this._handleKernel();
        this.session.kernelChanged.connect(this._handleKernel, this);
    }
    Object.defineProperty(ConsoleHistory.prototype, "editor", {
        /**
         * The current editor used by the history manager.
         */
        get: function () {
            return this._editor;
        },
        set: function (value) {
            if (this._editor === value) {
                return;
            }
            var editor = this._editor;
            if (editor) {
                editor.edgeRequested.disconnect(this.onEdgeRequest, this);
                editor.model.value.changed.disconnect(this.onTextChange, this);
            }
            editor = this._editor = value;
            editor.edgeRequested.connect(this.onEdgeRequest, this);
            editor.model.value.changed.connect(this.onTextChange, this);
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(ConsoleHistory.prototype, "placeholder", {
        /**
         * The placeholder text that a history session began with.
         */
        get: function () {
            return this._placeholder;
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(ConsoleHistory.prototype, "isDisposed", {
        /**
         * Get whether the console history manager is disposed.
         */
        get: function () {
            return this._isDisposed;
        },
        enumerable: true,
        configurable: true
    });
    /**
     * Dispose of the resources held by the console history manager.
     */
    ConsoleHistory.prototype.dispose = function () {
        this._isDisposed = true;
        this._history.length = 0;
        signaling_1.Signal.clearData(this);
    };
    /**
     * Get the previous item in the console history.
     *
     * @param placeholder - The placeholder string that gets temporarily added
     * to the history only for the duration of one history session. If multiple
     * placeholders are sent within a session, only the first one is accepted.
     *
     * @returns A Promise for console command text or `undefined` if unavailable.
     */
    ConsoleHistory.prototype.back = function (placeholder) {
        if (!this._hasSession) {
            this._hasSession = true;
            this._placeholder = placeholder;
        }
        var content = this._history[--this._cursor];
        this._cursor = Math.max(0, this._cursor);
        return Promise.resolve(content);
    };
    /**
     * Get the next item in the console history.
     *
     * @param placeholder - The placeholder string that gets temporarily added
     * to the history only for the duration of one history session. If multiple
     * placeholders are sent within a session, only the first one is accepted.
     *
     * @returns A Promise for console command text or `undefined` if unavailable.
     */
    ConsoleHistory.prototype.forward = function (placeholder) {
        if (!this._hasSession) {
            this._hasSession = true;
            this._placeholder = placeholder;
        }
        var content = this._history[++this._cursor];
        this._cursor = Math.min(this._history.length, this._cursor);
        return Promise.resolve(content);
    };
    /**
     * Add a new item to the bottom of history.
     *
     * @param item The item being added to the bottom of history.
     *
     * #### Notes
     * If the item being added is undefined or empty, it is ignored. If the item
     * being added is the same as the last item in history, it is ignored as well
     * so that the console's history will consist of no contiguous repetitions.
     */
    ConsoleHistory.prototype.push = function (item) {
        if (item && item !== this._history[this._history.length - 1]) {
            this._history.push(item);
        }
        this.reset();
    };
    /**
     * Reset the history navigation state, i.e., start a new history session.
     */
    ConsoleHistory.prototype.reset = function () {
        this._cursor = this._history.length;
        this._hasSession = false;
        this._placeholder = '';
    };
    /**
     * Populate the history collection on history reply from a kernel.
     *
     * @param value The kernel message history reply.
     *
     * #### Notes
     * History entries have the shape:
     * [session: number, line: number, input: string]
     * Contiguous duplicates are stripped out of the API response.
     */
    ConsoleHistory.prototype.onHistory = function (value) {
        this._history.length = 0;
        var last = '';
        var current = '';
        for (var i = 0; i < value.content.history.length; i++) {
            current = value.content.history[i][2];
            if (current !== last) {
                this._history.push(last = current);
            }
        }
        // Reset the history navigation cursor back to the bottom.
        this._cursor = this._history.length;
    };
    /**
     * Handle a text change signal from the editor.
     */
    ConsoleHistory.prototype.onTextChange = function () {
        if (this._setByHistory) {
            this._setByHistory = false;
            return;
        }
        this.reset();
    };
    /**
     * Handle an edge requested signal.
     */
    ConsoleHistory.prototype.onEdgeRequest = function (editor, location) {
        var _this = this;
        var model = this._editor.model;
        var source = model.value.text;
        if (location === 'top') {
            this.back(source).then(function (value) {
                if (_this.isDisposed || !value) {
                    return;
                }
                if (model.value.text === value) {
                    return;
                }
                _this._setByHistory = true;
                model.value.text = value;
                editor.setCursorPosition({ line: 0, column: 0 });
            });
        }
        else {
            this.forward(source).then(function (value) {
                if (_this.isDisposed) {
                    return;
                }
                var text = value || _this.placeholder;
                if (model.value.text === text) {
                    return;
                }
                _this._setByHistory = true;
                model.value.text = text;
                editor.setCursorPosition(editor.getPositionAt(text.length));
            });
        }
    };
    /**
     * Handle the current kernel changing.
     */
    ConsoleHistory.prototype._handleKernel = function () {
        var _this = this;
        var kernel = this.session.kernel;
        if (!kernel) {
            this._history.length = 0;
            return;
        }
        kernel.requestHistory(Private.initialRequest).then(function (v) {
            _this.onHistory(v);
        });
    };
    return ConsoleHistory;
}());
exports.ConsoleHistory = ConsoleHistory;
/**
 * A namespace for private data.
 */
var Private;
(function (Private) {
    Private.initialRequest = {
        output: false,
        raw: true,
        hist_access_type: 'tail',
        n: 500
    };
})(Private || (Private = {}));

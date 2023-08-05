// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var messaging_1 = require("@phosphor/messaging");
/**
 * A class added to editors that can host a completer.
 */
var COMPLETER_ENABLED_CLASS = 'jp-mod-completer-enabled';
/**
 * A class added to editors that have an active completer.
 */
var COMPLETER_ACTIVE_CLASS = 'jp-mod-completer-active';
/**
 * A completion handler for editors.
 */
var CompletionHandler = (function () {
    /**
     * Construct a new completion handler for a widget.
     */
    function CompletionHandler(options) {
        this._editor = null;
        this._enabled = false;
        this._completer = null;
        this._pending = 0;
        this._completer = options.completer;
        this._completer.selected.connect(this.onCompletionSelected, this);
        this._completer.visibilityChanged.connect(this.onVisibilityChanged, this);
        this.session = options.session;
    }
    Object.defineProperty(CompletionHandler.prototype, "completer", {
        /**
         * The completer widget managed by the handler.
         */
        get: function () {
            return this._completer;
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(CompletionHandler.prototype, "editor", {
        /**
         * The editor used by the completion handler.
         */
        get: function () {
            return this._editor;
        },
        set: function (newValue) {
            if (newValue === this._editor) {
                return;
            }
            var editor = this._editor;
            // Clean up and disconnect from old editor.
            if (editor && !editor.isDisposed) {
                var model = editor.model;
                editor.host.classList.remove(COMPLETER_ENABLED_CLASS);
                model.selections.changed.disconnect(this.onSelectionsChanged, this);
                model.value.changed.disconnect(this.onTextChanged, this);
            }
            // Reset completer state.
            if (this._completer) {
                this._completer.reset();
                this._completer.editor = newValue;
            }
            // Update the editor and signal connections.
            editor = this._editor = newValue;
            if (editor) {
                var model = editor.model;
                this._enabled = false;
                model.selections.changed.connect(this.onSelectionsChanged, this);
                model.value.changed.connect(this.onTextChanged, this);
                // On initial load, manually check the cursor position.
                this.onSelectionsChanged();
            }
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(CompletionHandler.prototype, "isDisposed", {
        /**
         * Get whether the completion handler is disposed.
         */
        get: function () {
            return this._completer === null;
        },
        enumerable: true,
        configurable: true
    });
    /**
     * Dispose of the resources used by the handler.
     */
    CompletionHandler.prototype.dispose = function () {
        this._completer = null;
        // Use public accessor to disconnect from editor signals.
        this.editor = null;
    };
    /**
     * Invoke the handler and launch a completer.
     */
    CompletionHandler.prototype.invoke = function () {
        messaging_1.MessageLoop.sendMessage(this, CompletionHandler.Msg.InvokeRequest);
    };
    /**
     * Process a message sent to the completion handler.
     */
    CompletionHandler.prototype.processMessage = function (msg) {
        switch (msg.type) {
            case CompletionHandler.Msg.InvokeRequest.type:
                this.onInvokeRequest(msg);
                break;
            default:
                break;
        }
    };
    /**
     * Get the state of the text editor at the given position.
     */
    CompletionHandler.prototype.getState = function (position) {
        var editor = this.editor;
        return {
            text: editor.model.value.text,
            lineHeight: editor.lineHeight,
            charWidth: editor.charWidth,
            line: position.line,
            column: position.column
        };
    };
    /**
     * Make a complete request using the session.
     */
    CompletionHandler.prototype.makeRequest = function (position) {
        var _this = this;
        if (!this.session.kernel) {
            return Promise.reject(new Error('no kernel for completion request'));
        }
        var editor = this.editor;
        if (!editor) {
            return Promise.reject(new Error('No active editor'));
        }
        var offset = editor.getOffsetAt(position);
        var content = {
            code: editor.model.value.text,
            cursor_pos: offset
        };
        var pending = ++this._pending;
        var request = this.getState(position);
        return this.session.kernel.requestComplete(content).then(function (msg) {
            if (_this.isDisposed) {
                return;
            }
            // If a newer completion request has created a pending request, bail.
            if (pending !== _this._pending) {
                return;
            }
            _this.onReply(request, msg);
        });
    };
    /**
     * Handle a completion selected signal from the completion widget.
     */
    CompletionHandler.prototype.onCompletionSelected = function (completer, value) {
        var model = completer.model;
        var editor = this._editor;
        if (!editor || !model) {
            return;
        }
        var patch = model.createPatch(value);
        if (!patch) {
            return;
        }
        var offset = patch.offset, text = patch.text;
        editor.model.value.text = text;
        var position = editor.getPositionAt(offset);
        editor.setCursorPosition(position);
    };
    /**
     * Handle `invoke-request` messages.
     */
    CompletionHandler.prototype.onInvokeRequest = function (msg) {
        // If there is neither a kernel nor a completer model, bail.
        if (!this.session.kernel || !this._completer.model) {
            return;
        }
        // If a completer session is already active, bail.
        if (this._completer.model.original) {
            return;
        }
        var editor = this._editor;
        this.makeRequest(editor.getCursorPosition());
    };
    /**
     * Receive a completion reply from the kernel.
     *
     * @param state - The state of the editor when completion request was made.
     *
     * @param reply - The API response returned for a completion request.
     */
    CompletionHandler.prototype.onReply = function (state, reply) {
        var model = this._completer.model;
        if (!model) {
            return;
        }
        // Completion request failures or negative results fail silently.
        var value = reply.content;
        if (value.status !== 'ok') {
            model.reset(true);
            return;
        }
        // Update the original request.
        model.original = state;
        // Update the options.
        model.setOptions(value.matches || []);
        // Update the cursor.
        model.cursor = { start: value.cursor_start, end: value.cursor_end };
    };
    /**
     * Handle selection changed signal from an editor.
     *
     * #### Notes
     * If a sub-class reimplements this method, then that class must either call
     * its super method or it must take responsibility for adding and removing
     * the completer completable class to the editor host node.
     *
     * Despite the fact that the editor widget adds a class whenever there is a
     * primary selection, this method checks indepenently for two reasons:
     *
     * 1. The editor widget connects to the same signal to add that class, so
     *    there is no guarantee that the class will be added before this method
     *    is invoked so simply checking for the CSS class's existence is not an
     *    option. Secondarily, checking the editor state should be faster than
     *    querying the DOM in either case.
     * 2. Because this method adds a class that indicates whether completer
     *    functionality ought to be enabled, relying on the behavior of the
     *    `jp-mod-has-primary-selection` to filter out any editors that have
     *    a selection means the semantic meaning of `jp-mod-completer-enabled`
     *    is obscured because there may be cases where the enabled class is added
     *    even though the completer is not available.
     */
    CompletionHandler.prototype.onSelectionsChanged = function () {
        var model = this._completer.model;
        var editor = this._editor;
        var host = editor.host;
        // If there is no model, return.
        if (!model) {
            this._enabled = false;
            host.classList.remove(COMPLETER_ENABLED_CLASS);
            return;
        }
        var position = editor.getCursorPosition();
        var line = editor.getLine(position.line);
        var _a = editor.getSelection(), start = _a.start, end = _a.end;
        // If there is a text selection, return.
        if (start.column !== end.column || start.line !== end.line) {
            this._enabled = false;
            model.reset(true);
            host.classList.remove(COMPLETER_ENABLED_CLASS);
            return;
        }
        // If the entire line is white space, return.
        if (line.match(/^\W*$/)) {
            this._enabled = false;
            model.reset(true);
            host.classList.remove(COMPLETER_ENABLED_CLASS);
            return;
        }
        // Enable completion.
        if (!this._enabled) {
            this._enabled = true;
            host.classList.add(COMPLETER_ENABLED_CLASS);
        }
        // Dispatch the cursor change.
        model.handleCursorChange(this.getState(editor.getCursorPosition()));
    };
    /**
     * Handle a text changed signal from an editor.
     */
    CompletionHandler.prototype.onTextChanged = function () {
        var model = this._completer.model;
        if (!model || !this._enabled) {
            return;
        }
        // If there is a text selection, no completion is allowed.
        var editor = this.editor;
        var _a = editor.getSelection(), start = _a.start, end = _a.end;
        if (start.column !== end.column || start.line !== end.line) {
            return;
        }
        // Dispatch the text change.
        model.handleTextChange(this.getState(editor.getCursorPosition()));
    };
    /**
     * Handle a visiblity change signal from a completer widget.
     */
    CompletionHandler.prototype.onVisibilityChanged = function (completer) {
        // Completer is not active.
        if (completer.isDisposed || completer.isHidden) {
            if (this._editor) {
                this._editor.host.classList.remove(COMPLETER_ACTIVE_CLASS);
                this._editor.focus();
            }
            return;
        }
        // Completer is active.
        if (this._editor) {
            this._editor.host.classList.add(COMPLETER_ACTIVE_CLASS);
        }
    };
    return CompletionHandler;
}());
exports.CompletionHandler = CompletionHandler;
/**
 * A namespace for cell completion handler statics.
 */
(function (CompletionHandler) {
    /**
     * A namespace for completion handler messages.
     */
    var Msg;
    (function (Msg) {
        /* tslint:disable */
        /**
         * A singleton `'invoke-request'` message.
         */
        Msg.InvokeRequest = new messaging_1.Message('invoke-request');
        /* tslint:enable */
    })(Msg = CompletionHandler.Msg || (CompletionHandler.Msg = {}));
})(CompletionHandler = exports.CompletionHandler || (exports.CompletionHandler = {}));
exports.CompletionHandler = CompletionHandler;

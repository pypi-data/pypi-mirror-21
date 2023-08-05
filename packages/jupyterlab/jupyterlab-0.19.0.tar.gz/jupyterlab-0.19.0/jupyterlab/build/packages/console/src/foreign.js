// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var signaling_1 = require("@phosphor/signaling");
/**
 * A handler for capturing API messages from other sessions that should be
 * rendered in a given parent.
 */
var ForeignHandler = (function () {
    /**
     * Construct a new foreign message handler.
     */
    function ForeignHandler(options) {
        this._cells = new Map();
        this._enabled = true;
        this._parent = null;
        this._factory = null;
        this.session = options.session;
        this.session.iopubMessage.connect(this.onIOPubMessage, this);
        this._factory = options.cellFactory;
        this._parent = options.parent;
    }
    Object.defineProperty(ForeignHandler.prototype, "enabled", {
        /**
         * Set whether the handler is able to inject foreign cells into a console.
         */
        get: function () {
            return this._enabled;
        },
        set: function (value) {
            this._enabled = value;
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(ForeignHandler.prototype, "parent", {
        /**
         * The foreign handler's parent receiver.
         */
        get: function () {
            return this._parent;
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(ForeignHandler.prototype, "isDisposed", {
        /**
         * Test whether the handler is disposed.
         */
        get: function () {
            return this._cells === null;
        },
        enumerable: true,
        configurable: true
    });
    /**
     * Dispose the resources held by the handler.
     */
    ForeignHandler.prototype.dispose = function () {
        if (this._cells === null) {
            return;
        }
        var cells = this._cells;
        this._cells = null;
        cells.clear();
        signaling_1.Signal.clearData(this);
    };
    /**
     * Handler IOPub messages.
     *
     * @returns `true` if the message resulted in a new cell injection or a
     * previously injected cell being updated and `false` for all other messages.
     */
    ForeignHandler.prototype.onIOPubMessage = function (sender, msg) {
        // Only process messages if foreign cell injection is enabled.
        if (!this._enabled) {
            return false;
        }
        var kernel = this.session.kernel;
        if (!kernel) {
            return;
        }
        // Check whether this message came from an external session.
        var parent = this._parent;
        var session = msg.parent_header.session;
        if (session === kernel.clientId) {
            return false;
        }
        var msgType = msg.header.msg_type;
        var parentHeader = msg.parent_header;
        var parentMsgId = parentHeader.msg_id;
        var cell;
        switch (msgType) {
            case 'execute_input':
                var inputMsg = msg;
                cell = this._newCell(parentMsgId);
                var model = cell.model;
                model.executionCount = inputMsg.content.execution_count;
                model.value.text = inputMsg.content.code;
                model.trusted = true;
                parent.update();
                return true;
            case 'execute_result':
            case 'display_data':
            case 'stream':
            case 'error':
                if (!this._cells.has(parentMsgId)) {
                    // This is an output from an input that was broadcast before our
                    // session started listening. We will ignore it.
                    console.warn('Ignoring output with no associated input cell.');
                    return false;
                }
                var output = msg.content;
                cell = this._cells.get(parentMsgId);
                output.output_type = msgType;
                cell.model.outputs.add(output);
                parent.update();
                return true;
            case 'clear_output':
                var wait = msg.content.wait;
                cell = this._cells.get(parentMsgId);
                cell.model.outputs.clear(wait);
                return true;
            default:
                return false;
        }
    };
    /**
     * Create a new code cell for an input originated from a foreign session.
     */
    ForeignHandler.prototype._newCell = function (parentMsgId) {
        var cell = this._factory();
        this._cells.set(parentMsgId, cell);
        this._parent.addCell(cell);
        return cell;
    };
    return ForeignHandler;
}());
exports.ForeignHandler = ForeignHandler;

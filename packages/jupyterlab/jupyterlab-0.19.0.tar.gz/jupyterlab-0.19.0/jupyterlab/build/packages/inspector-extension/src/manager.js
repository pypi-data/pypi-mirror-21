// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
/**
 * A class that manages inspector widget instances and offers persistent
 * `IInspector` instance that other plugins can communicate with.
 */
var InspectorManager = (function () {
    function InspectorManager() {
        this._inspector = null;
        this._source = null;
    }
    Object.defineProperty(InspectorManager.prototype, "inspector", {
        /**
         * The current inspector widget.
         */
        get: function () {
            return this._inspector;
        },
        set: function (inspector) {
            if (this._inspector === inspector) {
                return;
            }
            this._inspector = inspector;
            // If an inspector was added and it has no source
            if (inspector && !inspector.source) {
                inspector.source = this._source;
            }
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(InspectorManager.prototype, "source", {
        /**
         * The source of events the inspector panel listens for.
         */
        get: function () {
            return this._source;
        },
        set: function (source) {
            if (this._source === source) {
                return;
            }
            if (this._source) {
                this._source.disposed.disconnect(this._onSourceDisposed, this);
            }
            this._source = source;
            if (this._inspector && !this._inspector.isDisposed) {
                this._inspector.source = this._source;
            }
            if (this._source) {
                this._source.disposed.connect(this._onSourceDisposed, this);
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
    InspectorManager.prototype.add = function (item) {
        if (!this._inspector) {
            throw new Error('Cannot add child item before creating an inspector.');
        }
        return this._inspector.add(item);
    };
    /**
     * Handle the source disposed signal.
     */
    InspectorManager.prototype._onSourceDisposed = function () {
        this._source = null;
    };
    return InspectorManager;
}());
exports.InspectorManager = InspectorManager;

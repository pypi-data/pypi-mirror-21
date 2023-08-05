// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var algorithm_1 = require("@phosphor/algorithm");
var signaling_1 = require("@phosphor/signaling");
var coreutils_1 = require("@jupyterlab/coreutils");
var rendermime_1 = require("@jupyterlab/rendermime");
/**
 * The default implementation of the IOutputAreaModel.
 */
var OutputAreaModel = (function () {
    /**
     * Construct a new observable outputs instance.
     */
    function OutputAreaModel(options) {
        if (options === void 0) { options = {}; }
        var _this = this;
        this.clearNext = false;
        this.list = null;
        this._trusted = false;
        this._isDisposed = false;
        this._stateChanged = new signaling_1.Signal(this);
        this._changed = new signaling_1.Signal(this);
        this._trusted = !!options.trusted;
        this.contentFactory = (options.contentFactory ||
            OutputAreaModel.defaultContentFactory);
        this.list = new coreutils_1.ObservableVector();
        if (options.values) {
            algorithm_1.each(options.values, function (value) { _this._add(value); });
        }
        this.list.changed.connect(this._onListChanged, this);
    }
    Object.defineProperty(OutputAreaModel.prototype, "stateChanged", {
        /**
         * A signal emitted when the model state changes.
         */
        get: function () {
            return this._stateChanged;
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(OutputAreaModel.prototype, "changed", {
        /**
         * A signal emitted when the model changes.
         */
        get: function () {
            return this._changed;
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(OutputAreaModel.prototype, "length", {
        /**
         * Get the length of the items in the model.
         */
        get: function () {
            return this.list ? this.list.length : 0;
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(OutputAreaModel.prototype, "trusted", {
        /**
         * Get whether the model is trusted.
         */
        get: function () {
            return this._trusted;
        },
        /**
         * Set whether the model is trusted.
         *
         * #### Notes
         * Changing the value will cause all of the models to re-set.
         */
        set: function (value) {
            if (value === this._trusted) {
                return;
            }
            var trusted = this._trusted = value;
            for (var i = 0; i < this.list.length; i++) {
                var item = this.list.at(i);
                var value_1 = item.toJSON();
                item.dispose();
                item = this._createItem({ value: value_1, trusted: trusted });
                this.list.set(i, item);
            }
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(OutputAreaModel.prototype, "isDisposed", {
        /**
         * Test whether the model is disposed.
         */
        get: function () {
            return this._isDisposed;
        },
        enumerable: true,
        configurable: true
    });
    /**
     * Dispose of the resources used by the model.
     */
    OutputAreaModel.prototype.dispose = function () {
        if (this.isDisposed) {
            return;
        }
        this._isDisposed = true;
        this.list.dispose();
        signaling_1.Signal.clearData(this);
    };
    /**
     * Get an item at the specified index.
     */
    OutputAreaModel.prototype.get = function (index) {
        return this.list.at(index);
    };
    /**
     * Add an output, which may be combined with previous output.
     *
     * #### Notes
     * The output bundle is copied.
     * Contiguous stream outputs of the same `name` are combined.
     */
    OutputAreaModel.prototype.add = function (output) {
        // If we received a delayed clear message, then clear now.
        if (this.clearNext) {
            this.clear();
            this.clearNext = false;
        }
        return this._add(output);
    };
    /**
     * Clear all of the output.
     *
     * @param wait Delay clearing the output until the next message is added.
     */
    OutputAreaModel.prototype.clear = function (wait) {
        if (wait === void 0) { wait = false; }
        this._lastStream = '';
        if (wait) {
            this.clearNext = true;
            return;
        }
        algorithm_1.each(this.list, function (item) { item.dispose(); });
        this.list.clear();
    };
    /**
     * Deserialize the model from JSON.
     *
     * #### Notes
     * This will clear any existing data.
     */
    OutputAreaModel.prototype.fromJSON = function (values) {
        var _this = this;
        this.clear();
        algorithm_1.each(values, function (value) { _this._add(value); });
    };
    /**
     * Serialize the model to JSON.
     */
    OutputAreaModel.prototype.toJSON = function () {
        return algorithm_1.toArray(algorithm_1.map(this.list, function (output) { return output.toJSON(); }));
    };
    /**
     * Add an item to the list.
     */
    OutputAreaModel.prototype._add = function (value) {
        var trusted = this._trusted;
        // Normalize stream data.
        if (coreutils_1.nbformat.isStream(value)) {
            if (Array.isArray(value.text)) {
                value.text = value.text.join('\n');
            }
        }
        // Consolidate outputs if they are stream outputs of the same kind.
        if (coreutils_1.nbformat.isStream(value) && this._lastStream &&
            value.name === this._lastName) {
            // In order to get a list change event, we add the previous
            // text to the current item and replace the previous item.
            // This also replaces the metadata of the last item.
            this._lastStream += value.text;
            value.text = this._lastStream;
            var item_1 = this._createItem({ value: value, trusted: trusted });
            var index = this.length - 1;
            var prev = this.list.at(index);
            prev.dispose();
            this.list.set(index, item_1);
            return index;
        }
        // Create the new item.
        var item = this._createItem({ value: value, trusted: trusted });
        // Update the stream information.
        if (coreutils_1.nbformat.isStream(value)) {
            this._lastStream = value.text;
            this._lastName = value.name;
        }
        else {
            this._lastStream = '';
        }
        // Add the item to our list and return the new length.
        return this.list.pushBack(item);
    };
    /**
     * Create an output item and hook up its signals.
     */
    OutputAreaModel.prototype._createItem = function (options) {
        var factory = this.contentFactory;
        var item = factory.createOutputModel(options);
        item.data.changed.connect(this._onGenericChange, this);
        item.metadata.changed.connect(this._onGenericChange, this);
        return item;
    };
    /**
     * Handle a change to the list.
     */
    OutputAreaModel.prototype._onListChanged = function (sender, args) {
        this._changed.emit(args);
        this._stateChanged.emit(void 0);
    };
    /**
     * Handle a change to an item.
     */
    OutputAreaModel.prototype._onGenericChange = function () {
        this._stateChanged.emit(void 0);
    };
    return OutputAreaModel;
}());
exports.OutputAreaModel = OutputAreaModel;
/**
 * The namespace for OutputAreaModel class statics.
 */
(function (OutputAreaModel) {
    /**
     * The default implementation of a `IModelOutputFactory`.
     */
    var ContentFactory = (function () {
        function ContentFactory() {
        }
        /**
         * Create an output model.
         */
        ContentFactory.prototype.createOutputModel = function (options) {
            return new rendermime_1.OutputModel(options);
        };
        return ContentFactory;
    }());
    OutputAreaModel.ContentFactory = ContentFactory;
    /**
     * The default output model factory.
     */
    OutputAreaModel.defaultContentFactory = new ContentFactory();
})(OutputAreaModel = exports.OutputAreaModel || (exports.OutputAreaModel = {}));
exports.OutputAreaModel = OutputAreaModel;

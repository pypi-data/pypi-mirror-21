// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var coreutils_1 = require("@jupyterlab/coreutils");
/**
 * The default mime model implementation.
 */
var MimeModel = (function () {
    /**
     * Construct a new mime model.
     */
    function MimeModel(options) {
        if (options === void 0) { options = {}; }
        this.trusted = !!options.trusted;
        this.data = new coreutils_1.ObservableJSON({ values: options.data });
        this.metadata = new coreutils_1.ObservableJSON({ values: options.metadata });
    }
    Object.defineProperty(MimeModel.prototype, "isDisposed", {
        /**
         * Test whether the model is disposed.
         */
        get: function () {
            return this.data.isDisposed;
        },
        enumerable: true,
        configurable: true
    });
    /**
     * Dispose of the resources used by the mime model.
     */
    MimeModel.prototype.dispose = function () {
        this.data.dispose();
        this.metadata.dispose();
    };
    /**
     * Serialize the model as JSON data.
     */
    MimeModel.prototype.toJSON = function () {
        return {
            trusted: this.trusted,
            data: this.data.toJSON(),
            metadata: this.metadata.toJSON()
        };
    };
    return MimeModel;
}());
exports.MimeModel = MimeModel;

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
var coreutils_1 = require("@phosphor/coreutils");
var coreutils_2 = require("@jupyterlab/coreutils");
var mimemodel_1 = require("./mimemodel");
/**
 * The default implementation of a notebook output model.
 */
var OutputModel = (function (_super) {
    __extends(OutputModel, _super);
    /**
     * Construct a new output model.
     */
    function OutputModel(options) {
        var _this = _super.call(this, Private.getBundleOptions(options)) || this;
        _this._raw = {};
        // Make a copy of the data.
        var value = options.value;
        for (var key in value) {
            // Ignore data and metadata that were stripped.
            switch (key) {
                case 'data':
                case 'metadata':
                    break;
                default:
                    _this._raw[key] = Private.extract(value, key);
            }
        }
        _this.type = value.output_type;
        if (coreutils_2.nbformat.isExecuteResult(value)) {
            _this.executionCount = value.execution_count;
        }
        else {
            _this.executionCount = null;
        }
        return _this;
    }
    /**
     * Serialize the model to JSON.
     */
    OutputModel.prototype.toJSON = function () {
        var output = {};
        for (var key in this._raw) {
            output[key] = Private.extract(this._raw, key);
        }
        switch (this.type) {
            case 'display_data':
            case 'execute_result':
                output['data'] = this.data.toJSON();
                output['metadata'] = this.metadata.toJSON();
                break;
            default:
                break;
        }
        // Remove transient data.
        delete output['transient'];
        return output;
    };
    return OutputModel;
}(mimemodel_1.MimeModel));
exports.OutputModel = OutputModel;
/**
 * The namespace for OutputModel statics.
 */
(function (OutputModel) {
    /**
     * Get the data for an output.
     *
     * @params output - A kernel output message payload.
     *
     * @returns - The data for the payload.
     */
    function getData(output) {
        return Private.getData(output);
    }
    OutputModel.getData = getData;
    /**
     * Get the metadata from an output message.
     *
     * @params output - A kernel output message payload.
     *
     * @returns - The metadata for the payload.
     */
    function getMetadata(output) {
        return Private.getMetadata(output);
    }
    OutputModel.getMetadata = getMetadata;
})(OutputModel = exports.OutputModel || (exports.OutputModel = {}));
exports.OutputModel = OutputModel;
/**
 * The namespace for module private data.
 */
var Private;
(function (Private) {
    /**
     * Get the data from a notebook output.
     */
    function getData(output) {
        var bundle = {};
        if (coreutils_2.nbformat.isExecuteResult(output) || coreutils_2.nbformat.isDisplayData(output)) {
            bundle = output.data;
        }
        else if (coreutils_2.nbformat.isStream(output)) {
            if (output.name === 'stderr') {
                bundle['application/vnd.jupyter.stderr'] = output.text;
            }
            else {
                bundle['application/vnd.jupyter.stdout'] = output.text;
            }
        }
        else if (coreutils_2.nbformat.isError(output)) {
            var traceback = output.traceback.join('\n');
            bundle['application/vnd.jupyter.stderr'] = (traceback || output.ename + ": " + output.evalue);
        }
        return convertBundle(bundle);
    }
    Private.getData = getData;
    /**
     * Get the metadata from an output message.
     */
    function getMetadata(output) {
        var value = Object.create(null);
        if (coreutils_2.nbformat.isExecuteResult(output) || coreutils_2.nbformat.isDisplayData(output)) {
            for (var key in output.metadata) {
                value[key] = extract(output.metadata, key);
            }
        }
        return value;
    }
    Private.getMetadata = getMetadata;
    /**
     * Get the bundle options given output model options.
     */
    function getBundleOptions(options) {
        var data = getData(options.value);
        var metadata = getMetadata(options.value);
        var trusted = !!options.trusted;
        return { data: data, trusted: trusted, metadata: metadata };
    }
    Private.getBundleOptions = getBundleOptions;
    /**
     * Extract a value from a JSONObject.
     */
    function extract(value, key) {
        var item = value[key];
        if (coreutils_1.JSONExt.isPrimitive(item)) {
            return item;
        }
        return JSON.parse(JSON.stringify(item));
    }
    Private.extract = extract;
    /**
     * Convert a mime bundle to mime data.
     */
    function convertBundle(bundle) {
        var map = Object.create(null);
        for (var mimeType in bundle) {
            var item = bundle[mimeType];
            // Convert multi-line strings to strings.
            if (coreutils_1.JSONExt.isArray(item)) {
                item = item.join('\n');
            }
            else if (!coreutils_1.JSONExt.isPrimitive(item)) {
                item = JSON.parse(JSON.stringify(item));
            }
            map[mimeType] = item;
        }
        return map;
    }
})(Private || (Private = {}));

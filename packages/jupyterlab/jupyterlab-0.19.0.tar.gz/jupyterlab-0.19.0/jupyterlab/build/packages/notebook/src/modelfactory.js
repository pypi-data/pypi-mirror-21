// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var model_1 = require("./model");
/**
 * A model factory for notebooks.
 */
var NotebookModelFactory = (function () {
    /**
     * Construct a new notebook model factory.
     */
    function NotebookModelFactory(options) {
        this._disposed = false;
        var codeCellContentFactory = options.codeCellContentFactory;
        this.contentFactory = (options.contentFactory ||
            new model_1.NotebookModel.ContentFactory({ codeCellContentFactory: codeCellContentFactory }));
    }
    Object.defineProperty(NotebookModelFactory.prototype, "name", {
        /**
         * The name of the model.
         */
        get: function () {
            return 'notebook';
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(NotebookModelFactory.prototype, "contentType", {
        /**
         * The content type of the file.
         */
        get: function () {
            return 'notebook';
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(NotebookModelFactory.prototype, "fileFormat", {
        /**
         * The format of the file.
         */
        get: function () {
            return 'json';
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(NotebookModelFactory.prototype, "isDisposed", {
        /**
         * Get whether the model factory has been disposed.
         */
        get: function () {
            return this._disposed;
        },
        enumerable: true,
        configurable: true
    });
    /**
     * Dispose of the model factory.
     */
    NotebookModelFactory.prototype.dispose = function () {
        this._disposed = true;
    };
    /**
     * Create a new model for a given path.
     *
     * @param languagePreference - An optional kernel language preference.
     *
     * @returns A new document model.
     */
    NotebookModelFactory.prototype.createNew = function (languagePreference) {
        var contentFactory = this.contentFactory;
        return new model_1.NotebookModel({ languagePreference: languagePreference, contentFactory: contentFactory });
    };
    /**
     * Get the preferred kernel language given a path.
     */
    NotebookModelFactory.prototype.preferredLanguage = function (path) {
        return '';
    };
    return NotebookModelFactory;
}());
exports.NotebookModelFactory = NotebookModelFactory;

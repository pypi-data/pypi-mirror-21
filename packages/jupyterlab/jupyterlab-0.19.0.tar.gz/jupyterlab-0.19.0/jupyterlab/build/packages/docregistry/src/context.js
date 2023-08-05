// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
"use strict";
var __assign = (this && this.__assign) || Object.assign || function(t) {
    for (var s, i = 1, n = arguments.length; i < n; i++) {
        s = arguments[i];
        for (var p in s) if (Object.prototype.hasOwnProperty.call(s, p))
            t[p] = s[p];
    }
    return t;
};
Object.defineProperty(exports, "__esModule", { value: true });
var coreutils_1 = require("@phosphor/coreutils");
var disposable_1 = require("@phosphor/disposable");
var signaling_1 = require("@phosphor/signaling");
var apputils_1 = require("@jupyterlab/apputils");
var coreutils_2 = require("@jupyterlab/coreutils");
var _1 = require(".");
/**
 * An implementation of a document context.
 *
 * This class is typically instantiated by the document manger.
 */
var Context = (function () {
    /**
     * Construct a new document context.
     */
    function Context(options) {
        var _this = this;
        this._manager = null;
        this._opener = null;
        this._model = null;
        this._path = '';
        this._factory = null;
        this._contentsModel = null;
        this._populatedPromise = new coreutils_1.PromiseDelegate();
        this._isPopulated = false;
        this._isReady = false;
        this._pathChanged = new signaling_1.Signal(this);
        this._fileChanged = new signaling_1.Signal(this);
        this._disposed = new signaling_1.Signal(this);
        var manager = this._manager = options.manager;
        this._factory = options.factory;
        this._opener = options.opener;
        this._path = options.path;
        var ext = _1.DocumentRegistry.extname(this._path);
        var lang = this._factory.preferredLanguage(ext);
        this._model = this._factory.createNew(lang);
        this._readyPromise = manager.ready.then(function () {
            return _this._populatedPromise.promise;
        });
        this.session = new apputils_1.ClientSession({
            manager: manager.sessions,
            path: this._path,
            name: this._path.split('/').pop(),
            kernelPreference: options.kernelPreference || { shouldStart: false }
        });
        this.session.propertyChanged.connect(this._onSessionChanged, this);
        manager.contents.fileChanged.connect(this._onFileChanged, this);
    }
    Object.defineProperty(Context.prototype, "pathChanged", {
        /**
         * A signal emitted when the path changes.
         */
        get: function () {
            return this._pathChanged;
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(Context.prototype, "fileChanged", {
        /**
         * A signal emitted when the model is saved or reverted.
         */
        get: function () {
            return this._fileChanged;
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(Context.prototype, "disposed", {
        /**
         * A signal emitted when the context is disposed.
         */
        get: function () {
            return this._disposed;
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(Context.prototype, "model", {
        /**
         * Get the model associated with the document.
         */
        get: function () {
            return this._model;
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(Context.prototype, "path", {
        /**
         * The current path associated with the document.
         */
        get: function () {
            return this._path;
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(Context.prototype, "contentsModel", {
        /**
         * The current contents model associated with the document
         *
         * #### Notes
         * The model will have an  empty `contents` field.
         */
        get: function () {
            return this._contentsModel;
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(Context.prototype, "factoryName", {
        /**
         * Get the model factory name.
         *
         * #### Notes
         * This is not part of the `IContext` API.
         */
        get: function () {
            return this.isDisposed ? '' : this._factory.name;
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(Context.prototype, "isDisposed", {
        /**
         * Test whether the context is disposed.
         */
        get: function () {
            return this._model === null;
        },
        enumerable: true,
        configurable: true
    });
    /**
     * Dispose of the resources held by the context.
     */
    Context.prototype.dispose = function () {
        if (this._model == null) {
            return;
        }
        var model = this._model;
        this.session.dispose();
        this._model = null;
        this._manager = null;
        this._factory = null;
        model.dispose();
        this._disposed.emit(void 0);
        signaling_1.Signal.clearData(this);
    };
    Object.defineProperty(Context.prototype, "isReady", {
        /**
         * Whether the context is ready.
         */
        get: function () {
            return this._isReady;
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(Context.prototype, "ready", {
        /**
         * A promise that is fulfilled when the context is ready.
         */
        get: function () {
            return this._readyPromise;
        },
        enumerable: true,
        configurable: true
    });
    /**
     * Save the document contents to disk.
     */
    Context.prototype.save = function () {
        var _this = this;
        var model = this._model;
        var path = this._path;
        if (model.readOnly) {
            return Promise.reject(new Error('Read only'));
        }
        var content;
        if (this._factory.fileFormat === 'json') {
            content = model.toJSON();
        }
        else {
            content = model.toString();
        }
        var options = {
            type: this._factory.contentType,
            format: this._factory.fileFormat,
            content: content
        };
        return this._manager.ready.then(function () {
            return _this._manager.contents.save(path, options);
        }).then(function (value) {
            if (_this.isDisposed) {
                return;
            }
            model.dirty = false;
            _this._updateContentsModel(value);
            if (!_this._isPopulated) {
                return _this._populate();
            }
        }).catch(function (err) {
            apputils_1.showDialog({
                title: 'File Save Error',
                body: err.xhr.responseText,
                buttons: [apputils_1.Dialog.okButton()]
            });
        });
    };
    /**
     * Save the document to a different path chosen by the user.
     */
    Context.prototype.saveAs = function () {
        var _this = this;
        return Private.getSavePath(this._path).then(function (newPath) {
            if (_this.isDisposed || !newPath) {
                return;
            }
            _this._path = newPath;
            _this.session.setName(newPath.split('/').pop());
            return _this.session.setPath(newPath).then(function () { return _this.save(); });
        });
    };
    /**
     * Revert the document contents to disk contents.
     */
    Context.prototype.revert = function () {
        var _this = this;
        var opts = {
            format: this._factory.fileFormat,
            type: this._factory.contentType,
            content: true
        };
        var path = this._path;
        var model = this._model;
        return this._manager.ready.then(function () {
            return _this._manager.contents.get(path, opts);
        }).then(function (contents) {
            if (_this.isDisposed) {
                return;
            }
            if (contents.format === 'json') {
                model.fromJSON(contents.content);
            }
            else {
                model.fromString(contents.content);
            }
            _this._updateContentsModel(contents);
            model.dirty = false;
            if (!_this._isPopulated) {
                return _this._populate();
            }
        }).catch(function (err) {
            apputils_1.showDialog({
                title: 'File Load Error',
                body: err.xhr.responseText,
                buttons: [apputils_1.Dialog.okButton()]
            });
        });
    };
    /**
     * Create a checkpoint for the file.
     */
    Context.prototype.createCheckpoint = function () {
        var _this = this;
        var contents = this._manager.contents;
        return this._manager.ready.then(function () {
            return contents.createCheckpoint(_this._path);
        });
    };
    /**
     * Delete a checkpoint for the file.
     */
    Context.prototype.deleteCheckpoint = function (checkpointId) {
        var _this = this;
        var contents = this._manager.contents;
        return this._manager.ready.then(function () {
            return contents.deleteCheckpoint(_this._path, checkpointId);
        });
    };
    /**
     * Restore the file to a known checkpoint state.
     */
    Context.prototype.restoreCheckpoint = function (checkpointId) {
        var _this = this;
        var contents = this._manager.contents;
        var path = this._path;
        return this._manager.ready.then(function () {
            if (checkpointId) {
                return contents.restoreCheckpoint(path, checkpointId);
            }
            return _this.listCheckpoints().then(function (checkpoints) {
                if (_this.isDisposed || !checkpoints.length) {
                    return;
                }
                checkpointId = checkpoints[checkpoints.length - 1].id;
                return contents.restoreCheckpoint(path, checkpointId);
            });
        });
    };
    /**
     * List available checkpoints for a file.
     */
    Context.prototype.listCheckpoints = function () {
        var _this = this;
        var contents = this._manager.contents;
        return this._manager.ready.then(function () {
            return contents.listCheckpoints(_this._path);
        });
    };
    /**
     * Resolve a relative url to a correct server path.
     */
    Context.prototype.resolveUrl = function (url) {
        if (coreutils_2.URLExt.isLocal(url)) {
            var cwd = coreutils_2.PathExt.dirname(this._path);
            url = coreutils_2.PathExt.resolve(cwd, url);
        }
        return Promise.resolve(url);
    };
    /**
     * Get the download url of a given absolute server path.
     */
    Context.prototype.getDownloadUrl = function (path) {
        var contents = this._manager.contents;
        if (coreutils_2.URLExt.isLocal(path)) {
            return this._manager.ready.then(function () { return contents.getDownloadUrl(path); });
        }
        return Promise.resolve(path);
    };
    /**
     * Add a sibling widget to the document manager.
     */
    Context.prototype.addSibling = function (widget) {
        var opener = this._opener;
        if (opener) {
            opener(widget);
        }
        return new disposable_1.DisposableDelegate(function () {
            widget.close();
        });
    };
    /**
     * Handle a change on the contents manager.
     */
    Context.prototype._onFileChanged = function (sender, change) {
        if (change.type !== 'rename') {
            return;
        }
        if (change.oldValue.path === this._path) {
            var newPath = change.newValue.path;
            this.session.setPath(newPath);
            this.session.setName(newPath.split('/').pop());
            this._path = newPath;
            this._updateContentsModel(change.newValue);
            this._pathChanged.emit(this._path);
        }
    };
    /**
     * Handle a change to a session property.
     */
    Context.prototype._onSessionChanged = function () {
        var path = this.session.path;
        if (path !== this._path) {
            this._path = path;
            this._pathChanged.emit(path);
        }
    };
    /**
     * Update our contents model, without the content.
     */
    Context.prototype._updateContentsModel = function (model) {
        var newModel = {
            path: model.path,
            name: model.name,
            type: model.type,
            writable: model.writable,
            created: model.created,
            last_modified: model.last_modified,
            mimetype: model.mimetype,
            format: model.format
        };
        var mod = this._contentsModel ? this._contentsModel.last_modified : null;
        this._contentsModel = newModel;
        if (!mod || newModel.last_modified !== mod) {
            this._fileChanged.emit(newModel);
        }
    };
    /**
     * Handle an initial population.
     */
    Context.prototype._populate = function () {
        var _this = this;
        this._isPopulated = true;
        // Add a checkpoint if none exists.
        return this.listCheckpoints().then(function (checkpoints) {
            if (!_this.isDisposed && !checkpoints) {
                return _this.createCheckpoint();
            }
        }).then(function () {
            if (_this.isDisposed) {
                return;
            }
            // Update the kernel preference.
            var name = (_this._model.defaultKernelName || _this.session.kernelPreference.name);
            _this.session.kernelPreference = __assign({}, _this.session.kernelPreference, { name: name, language: _this._model.defaultKernelLanguage });
            return _this.session.initialize();
        }).then(function () {
            _this._isReady = true;
            _this._populatedPromise.resolve(void 0);
        });
    };
    return Context;
}());
exports.Context = Context;
/**
 * A namespace for private data.
 */
var Private;
(function (Private) {
    /**
     * Get a new file path from the user.
     */
    function getSavePath(path) {
        var input = document.createElement('input');
        input.value = path;
        var saveBtn = apputils_1.Dialog.okButton({ label: 'SAVE' });
        return apputils_1.showDialog({
            title: 'Save File As..',
            body: input,
            buttons: [apputils_1.Dialog.cancelButton(), saveBtn]
        }).then(function (result) {
            if (result.label === 'SAVE') {
                return input.value;
            }
        });
    }
    Private.getSavePath = getSavePath;
})(Private || (Private = {}));

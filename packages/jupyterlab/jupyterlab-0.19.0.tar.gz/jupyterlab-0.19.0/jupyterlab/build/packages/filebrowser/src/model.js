// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var algorithm_1 = require("@phosphor/algorithm");
var signaling_1 = require("@phosphor/signaling");
var coreutils_1 = require("@jupyterlab/coreutils");
/**
 * The duration of auto-refresh in ms.
 */
var REFRESH_DURATION = 10000;
/**
 * The enforced time between refreshes in ms.
 */
var MIN_REFRESH = 1000;
/**
 * An implementation of a file browser model.
 *
 * #### Notes
 * All paths parameters without a leading `'/'` are interpreted as relative to
 * the current directory.  Supports `'../'` syntax.
 */
var FileBrowserModel = (function () {
    /**
     * Construct a new file browser model.
     */
    function FileBrowserModel(options) {
        var _this = this;
        this._maxUploadSizeMb = 15;
        this._manager = null;
        this._sessions = [];
        this._items = [];
        this._paths = new Set();
        this._pendingPath = null;
        this._pending = null;
        this._timeoutId = -1;
        this._refreshId = -1;
        this._blackoutId = -1;
        this._requested = false;
        this._pathChanged = new signaling_1.Signal(this);
        this._refreshed = new signaling_1.Signal(this);
        this._sessionsChanged = new signaling_1.Signal(this);
        this._fileChanged = new signaling_1.Signal(this);
        this._connectionFailure = new signaling_1.Signal(this);
        this._manager = options.manager;
        this._model = { path: '', name: '/', type: 'directory' };
        this._manager.contents.fileChanged.connect(this._onFileChanged, this);
        this._manager.sessions.runningChanged.connect(this._onRunningChanged, this);
        this._scheduleUpdate();
        this._refreshId = window.setInterval(function () {
            _this._scheduleUpdate();
        }, REFRESH_DURATION);
    }
    Object.defineProperty(FileBrowserModel.prototype, "pathChanged", {
        /**
         * A signal emitted when the path changes.
         */
        get: function () {
            return this._pathChanged;
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(FileBrowserModel.prototype, "refreshed", {
        /**
         * A signal emitted when the directory listing is refreshed.
         */
        get: function () {
            return this._refreshed;
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(FileBrowserModel.prototype, "sessionsChanged", {
        /**
         * A signal emitted when the running sessions in the directory changes.
         */
        get: function () {
            return this._sessionsChanged;
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(FileBrowserModel.prototype, "fileChanged", {
        /**
         * Get the file path changed signal.
         */
        get: function () {
            return this._fileChanged;
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(FileBrowserModel.prototype, "connectionFailure", {
        /**
         * A signal emitted when the file browser model loses connection.
         */
        get: function () {
            return this._connectionFailure;
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(FileBrowserModel.prototype, "path", {
        /**
         * Get the current path.
         */
        get: function () {
            return this._model ? this._model.path : '';
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(FileBrowserModel.prototype, "specs", {
        /**
         * Get the kernel spec models.
         */
        get: function () {
            return this._manager.sessions.specs;
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(FileBrowserModel.prototype, "isDisposed", {
        /**
         * Get whether the model is disposed.
         */
        get: function () {
            return this._model === null;
        },
        enumerable: true,
        configurable: true
    });
    /**
     * Dispose of the resources held by the model.
     */
    FileBrowserModel.prototype.dispose = function () {
        if (this._model === null) {
            return;
        }
        this._model = null;
        this._manager = null;
        clearTimeout(this._timeoutId);
        clearInterval(this._refreshId);
        clearTimeout(this._blackoutId);
        this._sessions.length = 0;
        this._items.length = 0;
        signaling_1.Signal.clearData(this);
    };
    /**
     * Create an iterator over the model's items.
     *
     * @returns A new iterator over the model's items.
     */
    FileBrowserModel.prototype.items = function () {
        return new algorithm_1.ArrayIterator(this._items);
    };
    /**
     * Create an iterator over the active sessions in the directory.
     *
     * @returns A new iterator over the model's active sessions.
     */
    FileBrowserModel.prototype.sessions = function () {
        return new algorithm_1.ArrayIterator(this._sessions);
    };
    /**
     * Force a refresh of the directory contents.
     */
    FileBrowserModel.prototype.refresh = function () {
        return this.cd('.');
    };
    /**
     * Change directory.
     *
     * @param path - The path to the file or directory.
     *
     * @returns A promise with the contents of the directory.
     */
    FileBrowserModel.prototype.cd = function (newValue) {
        var _this = this;
        if (newValue === void 0) { newValue = '.'; }
        if (newValue !== '.') {
            newValue = Private.normalizePath(this._model.path, newValue);
        }
        else {
            newValue = this._pendingPath || this._model.path;
        }
        // Collapse requests to the same directory.
        if (newValue === this._pendingPath) {
            return this._pending;
        }
        var oldValue = this.path;
        var options = { content: true };
        this._pendingPath = newValue;
        if (oldValue !== newValue) {
            this._sessions.length = 0;
        }
        var manager = this._manager;
        this._pending = manager.contents.get(newValue, options).then(function (contents) {
            if (_this.isDisposed) {
                return;
            }
            _this._handleContents(contents);
            _this._pendingPath = null;
            if (oldValue !== newValue) {
                _this._pathChanged.emit({
                    name: 'path',
                    oldValue: oldValue,
                    newValue: newValue
                });
            }
            _this._onRunningChanged(manager.sessions, manager.sessions.running());
            _this._refreshed.emit(void 0);
        }).catch(function (error) {
            _this._pendingPath = null;
            _this._connectionFailure.emit(error);
        });
        return this._pending;
    };
    /**
     * Copy a file.
     *
     * @param fromFile - The path of the original file.
     *
     * @param toDir - The path to the target directory.
     *
     * @returns A promise which resolves to the contents of the file.
     */
    FileBrowserModel.prototype.copy = function (fromFile, toDir) {
        var normalizePath = Private.normalizePath;
        fromFile = normalizePath(this._model.path, fromFile);
        toDir = normalizePath(this._model.path, toDir);
        return this._manager.contents.copy(fromFile, toDir);
    };
    /**
     * Delete a file.
     *
     * @param: path - The path to the file to be deleted.
     *
     * @returns A promise which resolves when the file is deleted.
     *
     * #### Notes
     * If there is a running session associated with the file and no other
     * sessions are using the kernel, the session will be shut down.
     */
    FileBrowserModel.prototype.deleteFile = function (path) {
        var _this = this;
        var normalizePath = Private.normalizePath;
        path = normalizePath(this._model.path, path);
        return this.stopIfNeeded(path).then(function () {
            return _this._manager.contents.delete(path);
        });
    };
    /**
     * Download a file.
     *
     * @param - path - The path of the file to be downloaded.
     *
     * @returns A promise which resolves when the file has begun
     *   downloading.
     */
    FileBrowserModel.prototype.download = function (path) {
        return this._manager.contents.getDownloadUrl(path).then(function (url) {
            var element = document.createElement('a');
            element.setAttribute('href', url);
            element.setAttribute('download', '');
            element.click();
            return void 0;
        });
    };
    /**
     * Create a new untitled file or directory in the current directory.
     *
     * @param type - The type of file object to create. One of
     *  `['file', 'notebook', 'directory']`.
     *
     * @param ext - Optional extension for `'file'` types (defaults to `'.txt'`).
     *
     * @returns A promise containing the new file contents model.
     */
    FileBrowserModel.prototype.newUntitled = function (options) {
        if (options.type === 'file') {
            options.ext = options.ext || '.txt';
        }
        options.path = options.path || this._model.path;
        return this._manager.contents.newUntitled(options);
    };
    /**
     * Rename a file or directory.
     *
     * @param path - The path to the original file.
     *
     * @param newPath - The path to the new file.
     *
     * @returns A promise containing the new file contents model.  The promise
     *   will reject if the newPath already exists.  Use [[overwrite]] to
     *   overwrite a file.
     */
    FileBrowserModel.prototype.rename = function (path, newPath) {
        // Handle relative paths.
        path = Private.normalizePath(this._model.path, path);
        newPath = Private.normalizePath(this._model.path, newPath);
        return this._manager.contents.rename(path, newPath);
    };
    /**
     * Overwrite a file.
     *
     * @param path - The path to the original file.
     *
     * @param newPath - The path to the new file.
     *
     * @returns A promise containing the new file contents model.
     */
    FileBrowserModel.prototype.overwrite = function (path, newPath) {
        var _this = this;
        // Cleanly overwrite the file by moving it, making sure the original
        // does not exist, and then renaming to the new path.
        var tempPath = newPath + "." + coreutils_1.uuid();
        var cb = function () { return _this.rename(tempPath, newPath); };
        return this.rename(path, tempPath).then(function () {
            return _this.deleteFile(newPath);
        }).then(cb, cb);
    };
    /**
     * Upload a `File` object.
     *
     * @param file - The `File` object to upload.
     *
     * @param overwrite - Whether to overwrite an existing file.
     *
     * @returns A promise containing the new file contents model.
     *
     * #### Notes
     * This will fail to upload files that are too big to be sent in one
     * request to the server.
     */
    FileBrowserModel.prototype.upload = function (file, overwrite) {
        var _this = this;
        // Skip large files with a warning.
        if (file.size > this._maxUploadSizeMb * 1024 * 1024) {
            var msg = "Cannot upload file (>" + this._maxUploadSizeMb + " MB) ";
            msg += "\"" + file.name + "\"";
            console.warn(msg);
            return Promise.reject(new Error(msg));
        }
        if (overwrite) {
            return this._upload(file);
        }
        var path = this._model.path;
        path = path ? path + '/' + file.name : file.name;
        return this._manager.contents.get(path, {}).then(function () {
            var msg = "\"" + file.name + "\" already exists";
            throw new Error(msg);
        }, function () {
            if (_this.isDisposed) {
                return;
            }
            return _this._upload(file);
        });
    };
    /**
     * Shut down a session by session id.
     *
     * @param id - The id of the session.
     *
     * @returns A promise that resolves when the action is complete.
     */
    FileBrowserModel.prototype.shutdown = function (id) {
        return this._manager.sessions.shutdown(id);
    };
    /**
     * Find a session associated with a path and stop it is the only
     * session using that kernel.
     */
    FileBrowserModel.prototype.stopIfNeeded = function (path) {
        var sessions = algorithm_1.toArray(this._sessions);
        var index = algorithm_1.ArrayExt.findFirstIndex(sessions, function (value) { return value.notebook.path === path; });
        if (index !== -1) {
            var count_1 = 0;
            var model_1 = sessions[index];
            algorithm_1.each(sessions, function (value) {
                if (model_1.kernel.id === value.kernel.id) {
                    count_1++;
                }
            });
            if (count_1 === 1) {
                // Try to delete the session, but succeed either way.
                return this.shutdown(model_1.id).catch(function () { });
            }
        }
        return Promise.resolve(void 0);
    };
    /**
     * Perform the actual upload.
     */
    FileBrowserModel.prototype._upload = function (file) {
        var _this = this;
        // Gather the file model parameters.
        var path = this._model.path;
        path = path ? path + '/' + file.name : file.name;
        var name = file.name;
        var isNotebook = file.name.indexOf('.ipynb') !== -1;
        var type = isNotebook ? 'notebook' : 'file';
        var format = isNotebook ? 'json' : 'base64';
        // Get the file content.
        var reader = new FileReader();
        if (isNotebook) {
            reader.readAsText(file);
        }
        else {
            reader.readAsArrayBuffer(file);
        }
        return new Promise(function (resolve, reject) {
            reader.onload = function (event) {
                var model = {
                    type: type,
                    format: format,
                    name: name,
                    content: Private.getContent(reader)
                };
                _this._manager.contents.save(path, model).then(function (contents) {
                    resolve(contents);
                }).catch(reject);
            };
            reader.onerror = function (event) {
                reject(Error("Failed to upload \"" + file.name + "\":" + event));
            };
        });
    };
    /**
     * Handle an updated contents model.
     */
    FileBrowserModel.prototype._handleContents = function (contents) {
        var _this = this;
        // Update our internal data.
        this._model = {
            name: contents.name,
            path: contents.path,
            type: contents.type,
            writable: contents.writable,
            created: contents.created,
            last_modified: contents.last_modified,
            mimetype: contents.mimetype,
            format: contents.format
        };
        this._items = contents.content;
        this._paths.clear();
        algorithm_1.each(contents.content, function (model) {
            _this._paths.add(model.path);
        });
    };
    /**
     * Handle a change to the running sessions.
     */
    FileBrowserModel.prototype._onRunningChanged = function (sender, models) {
        var _this = this;
        this._sessions.length = 0;
        algorithm_1.each(models, function (model) {
            if (_this._paths.has(model.notebook.path)) {
                _this._sessions.push(model);
            }
        });
        this._refreshed.emit(void 0);
    };
    /**
     * Handle a change on the contents manager.
     */
    FileBrowserModel.prototype._onFileChanged = function (sender, change) {
        var path = this._model.path || '.';
        var value = change.oldValue;
        if (value && value.path && coreutils_1.PathExt.dirname(value.path) === path) {
            this._fileChanged.emit(change);
            this._scheduleUpdate();
            return;
        }
        value = change.newValue;
        if (value && value.path && coreutils_1.PathExt.dirname(value.path) === path) {
            this._fileChanged.emit(change);
            this._scheduleUpdate();
            return;
        }
    };
    /**
     * Handle internal model refresh logic.
     */
    FileBrowserModel.prototype._scheduleUpdate = function () {
        var _this = this;
        // Send immediately if there is no pending action, otherwise defer.
        if (this._blackoutId !== -1) {
            this._requested = true;
            return;
        }
        this._timeoutId = window.setTimeout(function () {
            _this.refresh();
            if (_this._requested && _this._blackoutId !== -1) {
                _this._requested = false;
                clearTimeout(_this._blackoutId);
                _this._blackoutId = -1;
                _this._timeoutId = window.setTimeout(function () {
                    _this._scheduleUpdate();
                }, MIN_REFRESH);
            }
            else {
                _this._blackoutId = window.setTimeout(function () {
                    _this._blackoutId = -1;
                    if (_this._requested) {
                        _this._scheduleUpdate();
                    }
                }, MIN_REFRESH);
            }
        }, 0);
    };
    return FileBrowserModel;
}());
exports.FileBrowserModel = FileBrowserModel;
/**
 * The namespace for the file browser model private data.
 */
var Private;
(function (Private) {
    /**
     * Parse the content of a `FileReader`.
     *
     * If the result is an `ArrayBuffer`, return a Base64-encoded string.
     * Otherwise, return the JSON parsed result.
     */
    function getContent(reader) {
        if (reader.result instanceof ArrayBuffer) {
            // Base64-encode binary file data.
            var bytes = '';
            var buf = new Uint8Array(reader.result);
            var nbytes = buf.byteLength;
            for (var i = 0; i < nbytes; i++) {
                bytes += String.fromCharCode(buf[i]);
            }
            return btoa(bytes);
        }
        else {
            return JSON.parse(reader.result);
        }
    }
    Private.getContent = getContent;
    /**
     * Normalize a path based on a root directory, accounting for relative paths.
     */
    function normalizePath(root, path) {
        return coreutils_1.PathExt.resolve(root, path);
    }
    Private.normalizePath = normalizePath;
})(Private || (Private = {}));

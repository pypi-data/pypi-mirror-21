// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var signaling_1 = require("@phosphor/signaling");
var apputils_1 = require("@jupyterlab/apputils");
/**
 * A class that manages the auto saving of a document.
 *
 * #### Notes
 * Implements https://github.com/ipython/ipython/wiki/IPEP-15:-Autosaving-the-IPython-Notebook.
 */
var SaveHandler = (function () {
    /**
     * Construct a new save handler.
     */
    function SaveHandler(options) {
        this._autosaveTimer = -1;
        this._minInterval = -1;
        this._interval = -1;
        this._context = null;
        this._manager = null;
        this._isActive = false;
        this._inDialog = false;
        this._manager = options.manager;
        this._context = options.context;
        this._minInterval = options.saveInterval * 1000 || 120000;
        this._interval = this._minInterval;
        // Restart the timer when the contents model is updated.
        this._context.fileChanged.connect(this._setTimer, this);
        this._context.disposed.connect(this.dispose, this);
    }
    Object.defineProperty(SaveHandler.prototype, "saveInterval", {
        /**
         * The save interval used by the timer (in seconds).
         */
        get: function () {
            return this._interval / 1000;
        },
        set: function (value) {
            this._minInterval = this._interval = value * 1000;
            if (this._isActive) {
                this._setTimer();
            }
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(SaveHandler.prototype, "isActive", {
        /**
         * Get whether the handler is active.
         */
        get: function () {
            return this._isActive;
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(SaveHandler.prototype, "isDisposed", {
        /**
         * Get whether the save handler is disposed.
         */
        get: function () {
            return this._context === null;
        },
        enumerable: true,
        configurable: true
    });
    /**
     * Dispose of the resources used by the save handler.
     */
    SaveHandler.prototype.dispose = function () {
        if (this._context === null) {
            return;
        }
        this._context = null;
        clearTimeout(this._autosaveTimer);
        signaling_1.Signal.clearData(this);
    };
    /**
     * Start the autosaver.
     */
    SaveHandler.prototype.start = function () {
        this._isActive = true;
        this._setTimer();
    };
    /**
     * Stop the autosaver.
     */
    SaveHandler.prototype.stop = function () {
        this._isActive = false;
        clearTimeout(this._autosaveTimer);
    };
    /**
     * Set the timer.
     */
    SaveHandler.prototype._setTimer = function () {
        var _this = this;
        clearTimeout(this._autosaveTimer);
        if (!this._isActive) {
            return;
        }
        this._autosaveTimer = window.setTimeout(function () {
            _this._save();
        }, this._interval);
    };
    /**
     * Handle an autosave timeout.
     */
    SaveHandler.prototype._save = function () {
        var _this = this;
        var context = this._context;
        // Trigger the next update.
        this._setTimer();
        if (!context) {
            return;
        }
        // Bail if the model is not dirty or it is read only, or the dialog
        // is already showing.
        if (!context.model.dirty || context.model.readOnly || this._inDialog) {
            return;
        }
        // Make sure the file has not changed on disk.
        var promise = this._manager.contents.get(context.path);
        promise.then(function (model) {
            if (!_this.isDisposed && context.contentsModel &&
                model.last_modified !== context.contentsModel.last_modified) {
                return _this._timeConflict(model.last_modified);
            }
            return _this._finishSave();
        }, function (err) {
            return _this._finishSave();
        }).catch(function (err) {
            console.error('Error in Auto-Save', err.message);
        });
    };
    /**
     * Handle a time conflict.
     */
    SaveHandler.prototype._timeConflict = function (modified) {
        var _this = this;
        var localTime = new Date(this._context.contentsModel.last_modified);
        var remoteTime = new Date(modified);
        console.warn("Last saving peformed " + localTime + " " +
            "while the current file seem to have been saved " +
            ("" + remoteTime));
        var body = "The file has changed on disk since the last time we " +
            "opened or saved it. " +
            "Do you want to overwrite the file on disk with the version " +
            " open here, or load the version on disk (revert)?";
        this._inDialog = true;
        var revertBtn = apputils_1.Dialog.okButton({ label: 'REVERT' });
        var overwriteBtn = apputils_1.Dialog.warnButton({ label: 'OVERWRITE' });
        return apputils_1.showDialog({
            title: 'File Changed', body: body,
            buttons: [apputils_1.Dialog.cancelButton(), revertBtn, overwriteBtn]
        }).then(function (result) {
            if (_this.isDisposed) {
                return;
            }
            _this._inDialog = false;
            if (result.label === 'OVERWRITE') {
                return _this._finishSave();
            }
            else if (result.label === 'REVERT') {
                return _this._context.revert();
            }
        });
    };
    /**
     * Perform the save, adjusting the save interval as necessary.
     */
    SaveHandler.prototype._finishSave = function () {
        var _this = this;
        var start = new Date().getTime();
        return this._context.save().then(function () {
            if (_this.isDisposed) {
                return;
            }
            var duration = new Date().getTime() - start;
            // New save interval: higher of 10x save duration or min interval.
            _this._interval = Math.max(10 * duration, _this._minInterval);
            // Restart the update to pick up the new interval.
            _this._setTimer();
        });
    };
    return SaveHandler;
}());
exports.SaveHandler = SaveHandler;

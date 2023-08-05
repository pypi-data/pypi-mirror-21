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
var algorithm_1 = require("@phosphor/algorithm");
var widgets_1 = require("@phosphor/widgets");
var buttons_1 = require("./buttons");
var crumbs_1 = require("./crumbs");
var listing_1 = require("./listing");
var utils_1 = require("./utils");
/**
 * The class name added to the filebrowser crumbs node.
 */
var CRUMBS_CLASS = 'jp-FileBrowser-crumbs';
/**
 * The class name added to the filebrowser buttons node.
 */
var BUTTON_CLASS = 'jp-FileBrowser-buttons';
/**
 * The class name added to the filebrowser listing node.
 */
var LISTING_CLASS = 'jp-FileBrowser-listing';
/**
 * A widget which hosts a file browser.
 *
 * The widget uses the Jupyter Contents API to retreive contents,
 * and presents itself as a flat list of files and directories with
 * breadcrumbs.
 */
var FileBrowser = (function (_super) {
    __extends(FileBrowser, _super);
    /**
     * Construct a new file browser.
     *
     * @param model - The file browser view model.
     */
    function FileBrowser(options) {
        var _this = _super.call(this) || this;
        _this._buttons = null;
        _this._commands = null;
        _this._crumbs = null;
        _this._listing = null;
        _this._manager = null;
        _this._model = null;
        _this._showingError = false;
        _this.addClass(utils_1.FILE_BROWSER_CLASS);
        var commands = _this._commands = options.commands;
        var manager = _this._manager = options.manager;
        var model = _this._model = options.model;
        var renderer = options.renderer;
        model.connectionFailure.connect(_this._onConnectionFailure, _this);
        _this._crumbs = new crumbs_1.BreadCrumbs({ model: model });
        _this._buttons = new buttons_1.FileButtons({
            commands: commands, manager: manager, model: model
        });
        _this._listing = new listing_1.DirListing({ manager: manager, model: model, renderer: renderer });
        _this._crumbs.addClass(CRUMBS_CLASS);
        _this._buttons.addClass(BUTTON_CLASS);
        _this._listing.addClass(LISTING_CLASS);
        var layout = new widgets_1.PanelLayout();
        layout.addWidget(_this._buttons);
        layout.addWidget(_this._crumbs);
        layout.addWidget(_this._listing);
        _this.layout = layout;
        return _this;
    }
    Object.defineProperty(FileBrowser.prototype, "commands", {
        /**
         * Get the command registry used by the file browser.
         */
        get: function () {
            return this._commands;
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(FileBrowser.prototype, "model", {
        /**
         * Get the model used by the file browser.
         */
        get: function () {
            return this._model;
        },
        enumerable: true,
        configurable: true
    });
    /**
     * Dispose of the resources held by the file browser.
     */
    FileBrowser.prototype.dispose = function () {
        this._model = null;
        this._crumbs = null;
        this._buttons = null;
        this._listing = null;
        this._manager = null;
        _super.prototype.dispose.call(this);
    };
    /**
     * Open the currently selected item(s).
     *
     * Changes to the first directory encountered.
     */
    FileBrowser.prototype.open = function () {
        var _this = this;
        var foundDir = false;
        algorithm_1.each(this._model.items(), function (item) {
            if (!_this._listing.isSelected(item.name)) {
                return;
            }
            if (item.type === 'directory') {
                if (!foundDir) {
                    foundDir = true;
                    _this._model.cd(item.name);
                }
            }
            else {
                _this.openPath(item.path);
            }
        });
    };
    /**
     * Open a file by path.
     *
     * @param path - The path to of the file to open.
     *
     * @param widgetName - The name of the widget factory to use.
     *
     * @returns The widget for the file.
     */
    FileBrowser.prototype.openPath = function (path, widgetName) {
        if (widgetName === void 0) { widgetName = 'default'; }
        return this._buttons.open(path, widgetName);
    };
    /**
     * Create a file from a creator.
     *
     * @param creatorName - The name of the widget creator.
     *
     * @returns A promise that resolves with the created widget.
     */
    FileBrowser.prototype.createFrom = function (creatorName) {
        return this._buttons.createFrom(creatorName);
    };
    /**
     * Create a new untitled file in the current directory.
     *
     * @param options - The options used to create the file.
     *
     * @returns A promise that resolves with the created widget.
     */
    FileBrowser.prototype.createNew = function (options) {
        var _this = this;
        var model = this.model;
        return model.newUntitled(options).then(function (contents) {
            if (!_this.isDisposed) {
                return _this._buttons.createNew(contents.path);
            }
        });
    };
    /**
     * Rename the first currently selected item.
     *
     * @returns A promise that resolves with the new name of the item.
     */
    FileBrowser.prototype.rename = function () {
        return this._listing.rename();
    };
    /**
     * Cut the selected items.
     */
    FileBrowser.prototype.cut = function () {
        this._listing.cut();
    };
    /**
     * Copy the selected items.
     */
    FileBrowser.prototype.copy = function () {
        this._listing.copy();
    };
    /**
     * Paste the items from the clipboard.
     *
     * @returns A promise that resolves when the operation is complete.
     */
    FileBrowser.prototype.paste = function () {
        return this._listing.paste();
    };
    /**
     * Delete the currently selected item(s).
     *
     * @returns A promise that resolves when the operation is complete.
     */
    FileBrowser.prototype.delete = function () {
        return this._listing.delete();
    };
    /**
     * Duplicate the currently selected item(s).
     *
     * @returns A promise that resolves when the operation is complete.
     */
    FileBrowser.prototype.duplicate = function () {
        return this._listing.duplicate();
    };
    /**
     * Download the currently selected item(s).
     */
    FileBrowser.prototype.download = function () {
        this._listing.download();
    };
    /**
     * Shut down kernels on the applicable currently selected items.
     *
     * @returns A promise that resolves when the operation is complete.
     */
    FileBrowser.prototype.shutdownKernels = function () {
        return this._listing.shutdownKernels();
    };
    /**
     * Select next item.
     */
    FileBrowser.prototype.selectNext = function () {
        this._listing.selectNext();
    };
    /**
     * Select previous item.
     */
    FileBrowser.prototype.selectPrevious = function () {
        this._listing.selectPrevious();
    };
    /**
     * Find a path given a click.
     *
     * @param event - The mouse event.
     *
     * @returns The path to the selected file.
     */
    FileBrowser.prototype.pathForClick = function (event) {
        return this._listing.pathForClick(event);
    };
    /**
     * Handle a connection lost signal from the model.
     */
    FileBrowser.prototype._onConnectionFailure = function (sender, args) {
        var _this = this;
        if (this._showingError) {
            return;
        }
        this._showingError = true;
        utils_1.showErrorMessage('Server Connection Error', args).then(function () {
            _this._showingError = false;
        });
    };
    return FileBrowser;
}(widgets_1.Widget));
exports.FileBrowser = FileBrowser;

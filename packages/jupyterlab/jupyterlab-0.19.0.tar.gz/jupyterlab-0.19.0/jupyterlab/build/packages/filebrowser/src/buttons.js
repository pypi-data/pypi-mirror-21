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
var disposable_1 = require("@phosphor/disposable");
var widgets_1 = require("@phosphor/widgets");
var apputils_1 = require("@jupyterlab/apputils");
var dialogs_1 = require("./dialogs");
var utils = require("./utils");
/**
 * The class name added to a file buttons widget.
 */
var FILE_BUTTONS_CLASS = 'jp-FileButtons';
/**
 * The class name added to a button node.
 */
var BUTTON_CLASS = 'jp-FileButtons-button';
/**
 * The class name added to a button content node.
 */
var CONTENT_CLASS = 'jp-FileButtons-buttonContent';
/**
 * The class name added to a button icon node.
 */
var ICON_CLASS = 'jp-FileButtons-buttonIcon';
/**
 * The class name added to the create button.
 */
var CREATE_CLASS = 'jp-id-create';
/**
 * The class name added to the add button.
 */
var MATERIAL_CREATE = 'jp-AddIcon';
/**
 * The class name added to the upload button.
 */
var MATERIAL_UPLOAD = 'jp-UploadIcon';
/**
 * The class name added to the refresh button.
 */
var MATERIAL_REFRESH = 'jp-RefreshIcon';
/**
 * The class name added to the down caret.
 */
var MATERIAL_DOWNCARET = 'jp-DownCaretIcon';
/**
 * The class name added to a material icon button.
 */
var MATERIAL_CLASS = 'jp-MaterialIcon';
/**
 * The class name added to the upload button.
 */
var UPLOAD_CLASS = 'jp-id-upload';
/**
 * The class name added to the refresh button.
 */
var REFRESH_CLASS = 'jp-id-refresh';
/**
 * The class name added to an active create button.
 */
var ACTIVE_CLASS = 'jp-mod-active';
/**
 * The class name added to a dropdown icon.
 */
var DROPDOWN_CLASS = 'jp-FileButtons-dropdownIcon';
/**
 * A widget which hosts the file browser buttons.
 */
var FileButtons = (function (_super) {
    __extends(FileButtons, _super);
    /**
     * Construct a new file browser buttons widget.
     */
    function FileButtons(options) {
        var _this = _super.call(this) || this;
        _this._buttons = Private.createButtons();
        _this._commands = null;
        _this._input = Private.createUploadInput();
        _this._manager = null;
        _this.addClass(FILE_BUTTONS_CLASS);
        _this._model = options.model;
        _this._buttons.create.onmousedown = _this._onCreateButtonPressed.bind(_this);
        _this._buttons.upload.onclick = _this._onUploadButtonClicked.bind(_this);
        _this._buttons.refresh.onclick = _this._onRefreshButtonClicked.bind(_this);
        _this._input.onchange = _this._onInputChanged.bind(_this);
        var node = _this.node;
        node.appendChild(_this._buttons.create);
        node.appendChild(_this._buttons.upload);
        node.appendChild(_this._buttons.refresh);
        _this._commands = options.commands;
        _this._manager = options.manager;
        return _this;
    }
    /**
     * Dispose of the resources held by the widget.
     */
    FileButtons.prototype.dispose = function () {
        this._buttons = null;
        this._commands = null;
        this._input = null;
        this._manager = null;
        this._model = null;
        _super.prototype.dispose.call(this);
    };
    Object.defineProperty(FileButtons.prototype, "model", {
        /**
         * Get the model used by the widget.
         */
        get: function () {
            return this._model;
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(FileButtons.prototype, "manager", {
        /**
         * Get the document manager used by the widget.
         */
        get: function () {
            return this._manager;
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(FileButtons.prototype, "createNode", {
        /**
         * Get the create button node.
         */
        get: function () {
            return this._buttons.create;
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(FileButtons.prototype, "uploadNode", {
        /**
         * Get the upload button node.
         */
        get: function () {
            return this._buttons.upload;
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(FileButtons.prototype, "refreshNode", {
        /**
         * Get the refresh button node.
         */
        get: function () {
            return this._buttons.refresh;
        },
        enumerable: true,
        configurable: true
    });
    /**
     * Create a file from a creator.
     *
     * @param creatorName - The name of the file creator.
     *
     * @returns A promise that resolves with the created widget.
     */
    FileButtons.prototype.createFrom = function (creatorName) {
        return dialogs_1.createFromDialog(this.model, this.manager, creatorName);
    };
    /**
     * Open a file by path.
     *
     * @param path - The path of the file.
     *
     * @param widgetName - The name of the widget factory to use.
     *
     * @param kernel - The kernel model to use.
     *
     * @return The widget for the path.
     */
    FileButtons.prototype.open = function (path, widgetName, kernel) {
        if (widgetName === void 0) { widgetName = 'default'; }
        var widget = this._manager.openOrReveal(path, widgetName, kernel);
        return widget;
    };
    /**
     * Create a new file by path.
     *
     * @param path - The path of the file.
     *
     * @param widgetName - The name of the widget factory to use.
     *
     * @param kernel - The kernel model to use.
     *
     * @return The widget for the path.
     */
    FileButtons.prototype.createNew = function (path, widgetName, kernel) {
        if (widgetName === void 0) { widgetName = 'default'; }
        return this._manager.createNew(path, widgetName, kernel);
    };
    /**
     * The 'mousedown' handler for the create button.
     */
    FileButtons.prototype._onCreateButtonPressed = function (event) {
        // Do nothing if nothing if it's not a left press.
        if (event.button !== 0) {
            return;
        }
        // Do nothing if the create button is already active.
        var button = this._buttons.create;
        if (button.classList.contains(ACTIVE_CLASS)) {
            return;
        }
        // Create a new dropdown menu and snap the button geometry.
        var commands = this._commands;
        var dropdown = Private.createDropdownMenu(this, commands);
        var rect = button.getBoundingClientRect();
        // Mark the button as active.
        button.classList.add(ACTIVE_CLASS);
        // Setup the `aboutToClose` signal handler. The menu is disposed on an
        // animation frame to allow a mouse press event which closed the
        // menu to run its course. This keeps the button from re-opening.
        dropdown.aboutToClose.connect(this._onDropDownAboutToClose, this);
        // Setup the `disposed` signal handler. This restores the button
        // to the non-active state and allows a new menu to be opened.
        dropdown.disposed.connect(this._onDropDownDisposed, this);
        // Popup the menu aligned with the bottom of the create button.
        dropdown.open(rect.left, rect.bottom, { forceX: false, forceY: false });
    };
    ;
    /**
     * Handle a dropdwon about to close.
     */
    FileButtons.prototype._onDropDownAboutToClose = function (sender) {
        requestAnimationFrame(function () { sender.dispose(); });
    };
    /**
     * Handle a dropdown disposal.
     */
    FileButtons.prototype._onDropDownDisposed = function (sender) {
        this._buttons.create.classList.remove(ACTIVE_CLASS);
    };
    /**
     * The 'click' handler for the upload button.
     */
    FileButtons.prototype._onUploadButtonClicked = function (event) {
        if (event.button !== 0) {
            return;
        }
        this._input.click();
    };
    /**
     * The 'click' handler for the refresh button.
     */
    FileButtons.prototype._onRefreshButtonClicked = function (event) {
        if (event.button !== 0) {
            return;
        }
        // Force a refresh of the current directory.
        this._model.refresh();
    };
    /**
     * The 'change' handler for the input field.
     */
    FileButtons.prototype._onInputChanged = function () {
        var files = Array.prototype.slice.call(this._input.files);
        Private.uploadFiles(this, files);
    };
    return FileButtons;
}(widgets_1.Widget));
exports.FileButtons = FileButtons;
/**
 * The namespace for the `FileButtons` private data.
 */
var Private;
(function (Private) {
    /**
     * The ID counter prefix for new commands.
     *
     * #### Notes
     * Even though the commands are disposed when the dropdown menu is disposed,
     * in order to guarantee there are no race conditions with other `FileButtons`
     * instances, each set of commands is prefixed.
     */
    var id = 0;
    /**
     * Create the button group for a file buttons widget.
     */
    function createButtons() {
        var create = document.createElement('button');
        var upload = document.createElement('button');
        var refresh = document.createElement('button');
        var createContent = document.createElement('span');
        var uploadContent = document.createElement('span');
        var refreshContent = document.createElement('span');
        var createIcon = document.createElement('span');
        var uploadIcon = document.createElement('span');
        var refreshIcon = document.createElement('span');
        var dropdownIcon = document.createElement('span');
        create.type = 'button';
        upload.type = 'button';
        refresh.type = 'button';
        create.title = 'Create New...';
        upload.title = 'Upload File(s)';
        refresh.title = 'Refresh File List';
        create.className = BUTTON_CLASS + " " + CREATE_CLASS;
        upload.className = BUTTON_CLASS + " " + UPLOAD_CLASS;
        refresh.className = BUTTON_CLASS + " " + REFRESH_CLASS;
        createContent.className = CONTENT_CLASS;
        uploadContent.className = CONTENT_CLASS;
        refreshContent.className = CONTENT_CLASS;
        // TODO make these icons configurable.
        createIcon.className = ICON_CLASS + ' ' + MATERIAL_CLASS + ' ' + MATERIAL_CREATE;
        uploadIcon.className = ICON_CLASS + ' ' + MATERIAL_CLASS + ' ' + MATERIAL_UPLOAD;
        refreshIcon.className = ICON_CLASS + ' ' + MATERIAL_CLASS + ' ' + MATERIAL_REFRESH;
        dropdownIcon.className = DROPDOWN_CLASS + ' ' + MATERIAL_CLASS + ' ' + MATERIAL_DOWNCARET;
        createContent.appendChild(createIcon);
        createContent.appendChild(dropdownIcon);
        uploadContent.appendChild(uploadIcon);
        refreshContent.appendChild(refreshIcon);
        create.appendChild(createContent);
        upload.appendChild(uploadContent);
        refresh.appendChild(refreshContent);
        return { create: create, upload: upload, refresh: refresh };
    }
    Private.createButtons = createButtons;
    /**
     * Create the upload input node for a file buttons widget.
     */
    function createUploadInput() {
        var input = document.createElement('input');
        input.type = 'file';
        input.multiple = true;
        return input;
    }
    Private.createUploadInput = createUploadInput;
    /**
     * Create a new folder.
     */
    function createNewFolder(widget) {
        widget.model.newUntitled({ type: 'directory' }).catch(function (error) {
            utils.showErrorMessage('New Folder Error', error);
        });
    }
    Private.createNewFolder = createNewFolder;
    /**
     * Create a new dropdown menu for the create new button.
     */
    function createDropdownMenu(widget, commands) {
        var menu = new widgets_1.Menu({ commands: commands });
        var prefix = "file-buttons-" + ++id;
        var disposables = new disposable_1.DisposableSet();
        var registry = widget.manager.registry;
        var command;
        // Remove all the commands associated with this menu upon disposal.
        menu.disposed.connect(function () { return disposables.dispose(); });
        command = prefix + ":new-text-folder";
        disposables.add(commands.addCommand(command, {
            execute: function () { createNewFolder(widget); },
            label: 'Folder'
        }));
        menu.addItem({ command: command });
        algorithm_1.each(registry.creators(), function (creator) {
            command = prefix + ":new-" + creator.name;
            disposables.add(commands.addCommand(command, {
                execute: function () {
                    widget.createFrom(creator.name);
                },
                label: creator.name
            }));
            menu.addItem({ command: command });
        });
        return menu;
    }
    Private.createDropdownMenu = createDropdownMenu;
    /**
     * Upload an array of files to the server.
     */
    function uploadFiles(widget, files) {
        var pending = files.map(function (file) { return uploadFile(widget, file); });
        Promise.all(pending).catch(function (error) {
            utils.showErrorMessage('Upload Error', error);
        });
    }
    Private.uploadFiles = uploadFiles;
    /**
     * Upload a file to the server.
     */
    function uploadFile(widget, file) {
        return widget.model.upload(file).catch(function (error) {
            var exists = error.message.ArrayExt.firstIndexOf('already exists') !== -1;
            if (exists) {
                return uploadFileOverride(widget, file);
            }
            throw error;
        });
    }
    /**
     * Upload a file to the server checking for override.
     */
    function uploadFileOverride(widget, file) {
        var overwrite = apputils_1.Dialog.warnButton({ label: 'OVERWRITE' });
        var options = {
            title: 'Overwrite File?',
            body: "\"" + file.name + "\" already exists, overwrite?",
            buttons: [apputils_1.Dialog.cancelButton(), overwrite]
        };
        return apputils_1.showDialog(options).then(function (button) {
            if (widget.isDisposed || button.accept) {
                return;
            }
            return widget.model.upload(file, true);
        });
    }
})(Private || (Private = {}));

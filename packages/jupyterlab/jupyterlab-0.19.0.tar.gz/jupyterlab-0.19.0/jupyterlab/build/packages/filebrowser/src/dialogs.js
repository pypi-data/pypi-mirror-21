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
var apputils_1 = require("@jupyterlab/apputils");
var docregistry_1 = require("@jupyterlab/docregistry");
/**
 * The class name added to file dialogs.
 */
var FILE_DIALOG_CLASS = 'jp-FileDialog';
/**
 * The class name added for a file conflict.
 */
var FILE_CONFLICT_CLASS = 'jp-mod-conflict';
/**
 * Create a file using a file creator.
 */
function createFromDialog(model, manager, creatorName) {
    var handler = new CreateFromHandler(model, manager, creatorName);
    return manager.services.ready.then(function () {
        return handler.populate();
    }).then(function () {
        return handler.showDialog();
    });
}
exports.createFromDialog = createFromDialog;
/**
 * Open a file using a dialog.
 */
function openWithDialog(path, manager, host) {
    var handler;
    return manager.services.ready.then(function () {
        handler = new OpenWithHandler(path, manager);
        return apputils_1.showDialog({
            title: 'Open File',
            body: handler.node,
            primaryElement: handler.inputNode,
            buttons: [apputils_1.Dialog.cancelButton(), apputils_1.Dialog.okButton({ label: 'OPEN' })]
        });
    }).then(function (result) {
        if (result.accept) {
            return handler.open();
        }
    });
}
exports.openWithDialog = openWithDialog;
/**
 * Create a new file using a dialog.
 */
function createNewDialog(model, manager, host) {
    var handler;
    return manager.services.ready.then(function () {
        handler = new CreateNewHandler(model, manager);
        return apputils_1.showDialog({
            title: 'Create New File',
            host: host,
            body: handler.node,
            primaryElement: handler.inputNode,
            buttons: [apputils_1.Dialog.cancelButton(), apputils_1.Dialog.okButton({ label: 'OPEN' })]
        });
    }).then(function (result) {
        if (result.accept) {
            return handler.open();
        }
    });
}
exports.createNewDialog = createNewDialog;
/**
 * Rename a file with optional dialog.
 */
function renameFile(model, oldPath, newPath) {
    return model.rename(oldPath, newPath).catch(function (error) {
        if (error.xhr) {
            error.message = error.xhr.statusText + " " + error.xhr.status;
        }
        var overwriteBtn = apputils_1.Dialog.warnButton({ label: 'OVERWRITE' });
        if (error.message.indexOf('409') !== -1) {
            var options = {
                title: 'Overwrite file?',
                body: "\"" + newPath + "\" already exists, overwrite?",
                buttons: [apputils_1.Dialog.cancelButton(), overwriteBtn]
            };
            return apputils_1.showDialog(options).then(function (button) {
                if (button.accept) {
                    return model.overwrite(oldPath, newPath);
                }
            });
        }
        else {
            throw error;
        }
    });
}
exports.renameFile = renameFile;
/**
 * A widget used to open files with a specific widget/kernel.
 */
var OpenWithHandler = (function (_super) {
    __extends(OpenWithHandler, _super);
    /**
     * Construct a new "open with" dialog.
     */
    function OpenWithHandler(path, manager) {
        var _this = _super.call(this, { node: Private.createOpenWithNode() }) || this;
        _this._ext = '';
        _this._manager = null;
        _this._manager = manager;
        _this.inputNode.textContent = path;
        _this._ext = docregistry_1.DocumentRegistry.extname(path);
        _this.populateFactories();
        _this.widgetDropdown.onchange = _this.widgetChanged.bind(_this);
        return _this;
    }
    /**
     * Dispose of the resources used by the widget.
     */
    OpenWithHandler.prototype.dispose = function () {
        this._manager = null;
        _super.prototype.dispose.call(this);
    };
    Object.defineProperty(OpenWithHandler.prototype, "inputNode", {
        /**
         * Get the input text node.
         */
        get: function () {
            return this.node.firstChild;
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(OpenWithHandler.prototype, "widgetDropdown", {
        /**
         * Get the widget dropdown node.
         */
        get: function () {
            return this.node.children[1];
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(OpenWithHandler.prototype, "kernelDropdownNode", {
        /**
         * Get the kernel dropdown node.
         */
        get: function () {
            return this.node.children[2];
        },
        enumerable: true,
        configurable: true
    });
    /**
     * Open the file and return the document widget.
     */
    OpenWithHandler.prototype.open = function () {
        var path = this.inputNode.textContent;
        var widgetName = this.widgetDropdown.value;
        var kernelValue = this.kernelDropdownNode.value;
        var kernelId;
        if (kernelValue !== 'null') {
            kernelId = JSON.parse(kernelValue);
        }
        return this._manager.open(path, widgetName, kernelId);
    };
    /**
     * Populate the widget factories.
     */
    OpenWithHandler.prototype.populateFactories = function () {
        var factories = this._manager.registry.preferredWidgetFactories(this._ext);
        var widgetDropdown = this.widgetDropdown;
        algorithm_1.each(factories, function (factory) {
            var option = document.createElement('option');
            option.text = factory.name;
            widgetDropdown.appendChild(option);
        });
        this.widgetChanged();
    };
    /**
     * Handle a change to the widget.
     */
    OpenWithHandler.prototype.widgetChanged = function () {
        var widgetName = this.widgetDropdown.value;
        var preference = this._manager.registry.getKernelPreference(this._ext, widgetName);
        var services = this._manager.services;
        apputils_1.ClientSession.populateKernelSelect(this.kernelDropdownNode, {
            specs: services.specs,
            sessions: services.sessions.running(),
            preference: preference
        });
    };
    return OpenWithHandler;
}(widgets_1.Widget));
/**
 * A widget used to create a file using a creator.
 */
var CreateFromHandler = (function (_super) {
    __extends(CreateFromHandler, _super);
    /**
     * Construct a new "create from" dialog.
     */
    function CreateFromHandler(model, manager, creatorName) {
        var _this = _super.call(this, { node: Private.createCreateFromNode() }) || this;
        _this._model = null;
        _this._orig = null;
        _this.addClass(FILE_DIALOG_CLASS);
        _this._model = model;
        _this._manager = manager;
        _this._creatorName = creatorName;
        // Check for name conflicts when the inputNode changes.
        _this.inputNode.addEventListener('input', function () {
            var value = _this.inputNode.value;
            if (value !== _this._orig) {
                algorithm_1.each(_this._model.items(), function (item) {
                    if (item.name === value) {
                        _this.addClass(FILE_CONFLICT_CLASS);
                        return;
                    }
                });
            }
            _this.removeClass(FILE_CONFLICT_CLASS);
        });
        return _this;
    }
    /**
     * Dispose of the resources used by the widget.
     */
    CreateFromHandler.prototype.dispose = function () {
        this._model = null;
        this._manager = null;
        _super.prototype.dispose.call(this);
    };
    Object.defineProperty(CreateFromHandler.prototype, "inputNode", {
        /**
         * Get the input text node.
         */
        get: function () {
            return this.node.getElementsByTagName('input')[0];
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(CreateFromHandler.prototype, "kernelDropdownNode", {
        /**
         * Get the kernel dropdown node.
         */
        get: function () {
            return this.node.getElementsByTagName('select')[0];
        },
        enumerable: true,
        configurable: true
    });
    /**
     * Show the createNew dialog.
     */
    CreateFromHandler.prototype.showDialog = function () {
        var _this = this;
        return apputils_1.showDialog({
            title: "Create New " + this._creatorName,
            body: this.node,
            primaryElement: this.inputNode,
            buttons: [apputils_1.Dialog.cancelButton(), apputils_1.Dialog.okButton({ label: 'CREATE' })]
        }).then(function (result) {
            if (result.accept) {
                return _this._open().then(function (widget) {
                    if (!widget) {
                        return _this.showDialog();
                    }
                    return widget;
                });
            }
            _this._model.deleteFile('/' + _this._orig.path);
            return null;
        });
    };
    /**
     * Populate the create from widget.
     */
    CreateFromHandler.prototype.populate = function () {
        var _this = this;
        var model = this._model;
        var manager = this._manager;
        var registry = manager.registry;
        var creator = registry.getCreator(this._creatorName);
        if (!creator) {
            return Promise.reject("Creator not registered: " + this._creatorName);
        }
        var fileType = creator.fileType, widgetName = creator.widgetName, kernelName = creator.kernelName;
        var fType = registry.getFileType(fileType);
        var ext = '.txt';
        var type = 'file';
        if (fType) {
            ext = fType.extension;
            type = fType.contentType || 'file';
        }
        if (!widgetName || widgetName === 'default') {
            this._widgetName = widgetName = registry.defaultWidgetFactory(ext).name;
        }
        // Handle the kernel preferences.
        var preference = registry.getKernelPreference(ext, widgetName, { name: kernelName });
        if (!preference.canStart) {
            this.node.removeChild(this.kernelDropdownNode.previousSibling);
            this.node.removeChild(this.kernelDropdownNode);
        }
        else {
            var services = this._manager.services;
            apputils_1.ClientSession.populateKernelSelect(this.kernelDropdownNode, {
                specs: services.specs,
                sessions: services.sessions.running(),
                preference: preference
            });
        }
        return model.newUntitled({ ext: ext, type: type }).then(function (contents) {
            var value = _this.inputNode.value = contents.name;
            _this.inputNode.setSelectionRange(0, value.length - ext.length);
            _this._orig = contents;
        });
    };
    /**
     * Open the file and return the document widget.
     */
    CreateFromHandler.prototype._open = function () {
        var _this = this;
        var file = this.inputNode.value;
        var widgetName = this._widgetName;
        var kernelValue = this.kernelDropdownNode ? this.kernelDropdownNode.value
            : 'null';
        var kernelId;
        if (kernelValue !== 'null') {
            kernelId = JSON.parse(kernelValue);
        }
        if (file !== this._orig.name) {
            var promise = renameFile(this._model, this._orig.name, file);
            return promise.then(function (contents) {
                if (!contents) {
                    return null;
                }
                return _this._manager.open(contents.path, widgetName, kernelId);
            });
        }
        var path = this._orig.path;
        return Promise.resolve(this._manager.createNew(path, widgetName, kernelId));
    };
    return CreateFromHandler;
}(widgets_1.Widget));
/**
 * A widget used to create new files.
 */
var CreateNewHandler = (function (_super) {
    __extends(CreateNewHandler, _super);
    /**
     * Construct a new "create new" dialog.
     */
    function CreateNewHandler(model, manager) {
        var _this = _super.call(this, { node: Private.createCreateNewNode() }) || this;
        _this._model = null;
        _this._manager = null;
        _this._sentinel = 'UNKNOWN_EXTENSION';
        _this._prevExt = '';
        _this._extensions = [];
        _this._model = model;
        _this._manager = manager;
        // Create a file name based on the current time.
        var time = new Date();
        time.setMinutes(time.getMinutes() - time.getTimezoneOffset());
        var name = time.toJSON().slice(0, 10);
        name += '-' + time.getHours() + time.getMinutes() + time.getSeconds();
        _this.inputNode.value = name + '.txt';
        _this.inputNode.setSelectionRange(0, name.length);
        // Check for name conflicts when the inputNode changes.
        _this.inputNode.addEventListener('input', function () {
            _this.inputNodeChanged();
        });
        // Update the widget choices when the file type changes.
        _this.fileTypeDropdown.addEventListener('change', function () {
            _this.fileTypeChanged();
        });
        // Update the kernel choices when the widget changes.
        _this.widgetDropdown.addEventListener('change', function () {
            _this.widgetDropdownChanged();
        });
        // Populate the lists of file types and widget factories.
        _this.populateFileTypes();
        _this.populateFactories();
        return _this;
    }
    /**
     * Dispose of the resources used by the widget.
     */
    CreateNewHandler.prototype.dispose = function () {
        this._model = null;
        this._manager = null;
        _super.prototype.dispose.call(this);
    };
    Object.defineProperty(CreateNewHandler.prototype, "inputNode", {
        /**
         * Get the input text node.
         */
        get: function () {
            return this.node.firstChild;
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(CreateNewHandler.prototype, "fileTypeDropdown", {
        /**
         * Get the file type dropdown node.
         */
        get: function () {
            return this.node.children[1];
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(CreateNewHandler.prototype, "widgetDropdown", {
        /**
         * Get the widget dropdown node.
         */
        get: function () {
            return this.node.children[2];
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(CreateNewHandler.prototype, "kernelDropdownNode", {
        /**
         * Get the kernel dropdown node.
         */
        get: function () {
            return this.node.children[3];
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(CreateNewHandler.prototype, "ext", {
        /**
         * Get the current extension for the file.
         */
        get: function () {
            return docregistry_1.DocumentRegistry.extname(this.inputNode.value);
        },
        enumerable: true,
        configurable: true
    });
    /**
     * Open the file and return the document widget.
     */
    CreateNewHandler.prototype.open = function () {
        var path = this.inputNode.textContent;
        var widgetName = this.widgetDropdown.value;
        var kernelValue = this.kernelDropdownNode.value;
        var kernelId;
        if (kernelValue !== 'null') {
            kernelId = JSON.parse(kernelValue);
        }
        return this._manager.createNew(path, widgetName, kernelId);
    };
    /**
     * Handle a change to the inputNode.
     */
    CreateNewHandler.prototype.inputNodeChanged = function () {
        var _this = this;
        var path = this.inputNode.value;
        algorithm_1.each(this._model.items(), function (item) {
            if (item.path === path) {
                _this.addClass(FILE_CONFLICT_CLASS);
                return;
            }
        });
        var ext = this.ext;
        if (ext === this._prevExt) {
            return;
        }
        // Update the file type dropdown and the factories.
        if (this._extensions.indexOf(ext) === -1) {
            this.fileTypeDropdown.value = this._sentinel;
        }
        else {
            this.fileTypeDropdown.value = ext;
        }
        this.populateFactories();
    };
    /**
     * Populate the file types.
     */
    CreateNewHandler.prototype.populateFileTypes = function () {
        var _this = this;
        var dropdown = this.fileTypeDropdown;
        var option = document.createElement('option');
        option.text = 'File';
        option.value = this._sentinel;
        algorithm_1.each(this._manager.registry.fileTypes(), function (ft) {
            option = document.createElement('option');
            option.text = ft.name + " (" + ft.extension + ")";
            option.value = ft.extension;
            dropdown.appendChild(option);
            _this._extensions.push(ft.extension);
        });
        if (this.ext in this._extensions) {
            dropdown.value = this.ext;
        }
        else {
            dropdown.value = this._sentinel;
        }
    };
    /**
     * Populate the widget factories.
     */
    CreateNewHandler.prototype.populateFactories = function () {
        var ext = this.ext;
        var factories = this._manager.registry.preferredWidgetFactories(ext);
        var widgetDropdown = this.widgetDropdown;
        algorithm_1.each(factories, function (factory) {
            var option = document.createElement('option');
            option.text = factory.name;
            widgetDropdown.appendChild(option);
        });
        this.widgetDropdownChanged();
        this._prevExt = ext;
    };
    /**
     * Handle changes to the file type dropdown.
     */
    CreateNewHandler.prototype.fileTypeChanged = function () {
        // Update the current inputNode.
        var oldExt = this.ext;
        var newExt = this.fileTypeDropdown.value;
        if (oldExt === newExt || newExt === '') {
            return;
        }
        var oldName = this.inputNode.value;
        var base = oldName.slice(0, oldName.length - oldExt.length - 1);
        this.inputNode.value = base + newExt;
    };
    /**
     * Handle a change to the widget dropdown.
     */
    CreateNewHandler.prototype.widgetDropdownChanged = function () {
        var ext = this.ext;
        var widgetName = this.widgetDropdown.value;
        var manager = this._manager;
        var preference = manager.registry.getKernelPreference(ext, widgetName);
        var services = this._manager.services;
        apputils_1.ClientSession.populateKernelSelect(this.kernelDropdownNode, {
            specs: services.specs,
            sessions: services.sessions.running(),
            preference: preference
        });
    };
    return CreateNewHandler;
}(widgets_1.Widget));
/**
 * A namespace for private data.
 */
var Private;
(function (Private) {
    /**
     * Create the node for an open with handler.
     */
    function createOpenWithNode() {
        var body = document.createElement('div');
        var nameTitle = document.createElement('label');
        nameTitle.textContent = 'File Name';
        var name = document.createElement('div');
        var widgetTitle = document.createElement('label');
        widgetTitle.textContent = 'Widget Type';
        var widgetDropdown = document.createElement('select');
        var kernelTitle = document.createElement('label');
        kernelTitle.textContent = 'Kernel';
        var kernelDropdownNode = document.createElement('select');
        body.appendChild(nameTitle);
        body.appendChild(name);
        body.appendChild(widgetTitle);
        body.appendChild(widgetDropdown);
        body.appendChild(kernelTitle);
        body.appendChild(kernelDropdownNode);
        return body;
    }
    Private.createOpenWithNode = createOpenWithNode;
    /**
     * Create the node for a create new handler.
     */
    function createCreateNewNode() {
        var body = document.createElement('div');
        var nameTitle = document.createElement('label');
        nameTitle.textContent = 'File Name';
        var name = document.createElement('input');
        var typeTitle = document.createElement('label');
        typeTitle.textContent = 'File Type';
        var fileTypeDropdown = document.createElement('select');
        var widgetTitle = document.createElement('label');
        widgetTitle.textContent = 'Widget Type';
        var widgetDropdown = document.createElement('select');
        var kernelTitle = document.createElement('label');
        kernelTitle.textContent = 'Kernel';
        var kernelDropdownNode = document.createElement('select');
        body.appendChild(nameTitle);
        body.appendChild(name);
        body.appendChild(typeTitle);
        body.appendChild(fileTypeDropdown);
        body.appendChild(widgetTitle);
        body.appendChild(widgetDropdown);
        body.appendChild(kernelTitle);
        body.appendChild(kernelDropdownNode);
        return body;
    }
    Private.createCreateNewNode = createCreateNewNode;
    /**
     * Create the node for a create from handler.
     */
    function createCreateFromNode() {
        var body = document.createElement('div');
        var nameTitle = document.createElement('label');
        nameTitle.textContent = 'File Name';
        var name = document.createElement('input');
        var kernelTitle = document.createElement('label');
        kernelTitle.textContent = 'Kernel';
        var kernelDropdownNode = document.createElement('select');
        body.appendChild(nameTitle);
        body.appendChild(name);
        body.appendChild(kernelTitle);
        body.appendChild(kernelDropdownNode);
        return body;
    }
    Private.createCreateFromNode = createCreateFromNode;
})(Private || (Private = {}));

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
var coreutils_1 = require("@phosphor/coreutils");
var disposable_1 = require("@phosphor/disposable");
var virtualdom_1 = require("@phosphor/virtualdom");
var apputils_1 = require("@jupyterlab/apputils");
/**
 * The command IDs used by the launcher plugin.
 */
var CommandIDs;
(function (CommandIDs) {
    CommandIDs.show = 'launcher-jupyterlab:show';
})(CommandIDs = exports.CommandIDs || (exports.CommandIDs = {}));
;
/* tslint:disable */
/**
 * The launcher token.
 */
exports.ILauncher = new coreutils_1.Token('jupyter.services.launcher');
/* tslint:enable */
/**
 * The class name added to LauncherWidget instances.
 */
var LAUNCHER_CLASS = 'jp-LauncherWidget';
/**
 * The class name added to LauncherWidget image nodes.
 */
var IMAGE_CLASS = 'jp-LauncherWidget-image';
/**
 * The class name added to LauncherWidget text nodes.
 */
var TEXT_CLASS = 'jp-LauncherWidget-text';
/**
 * The class name added to LauncherWidget item nodes.
 */
var ITEM_CLASS = 'jp-LauncherWidget-item';
/**
 * The class name added to LauncherWidget folder node.
 */
var FOLDER_CLASS = 'jp-LauncherWidget-folder';
/**
 * The class name added for the folder icon from default-theme.
 */
var FOLDER_ICON_CLASS = 'jp-FolderIcon';
/**
 * The class name added to LauncherWidget path nodes.
 */
var PATH_CLASS = 'jp-LauncherWidget-path';
/**
 * The class name added to LauncherWidget current working directory node.
 */
var CWD_CLASS = 'jp-LauncherWidget-cwd';
/**
 * The class name added to LauncherWidget body nodes.
 */
var BODY_CLASS = 'jp-LauncherWidget-body';
/**
 * The class name added to LauncherWidget dialog node.
 */
var DIALOG_CLASS = 'jp-LauncherWidget-dialog';
/**
 * LauncherModel keeps track of the path to working directory and has a list of
 * LauncherItems, which the LauncherWidget will render.
 */
var LauncherModel = (function (_super) {
    __extends(LauncherModel, _super);
    /**
     * Create a new launcher model.
     */
    function LauncherModel() {
        var _this = _super.call(this) || this;
        _this._items = [];
        _this._path = 'home';
        return _this;
    }
    Object.defineProperty(LauncherModel.prototype, "path", {
        /**
         * The path to the current working directory.
         */
        get: function () {
            return this._path;
        },
        set: function (path) {
            if (path === this._path) {
                return;
            }
            this._path = path;
            this.stateChanged.emit(void 0);
        },
        enumerable: true,
        configurable: true
    });
    /**
     * Add a command item to the launcher, and trigger re-render event for parent
     * widget.
     *
     * @param options - The specification options for a launcher item.
     *
     * @returns A disposable that will remove the item from Launcher, and trigger
     * re-render event for parent widget.
     *
     */
    LauncherModel.prototype.add = function (options) {
        var _this = this;
        // Create a copy of the options to circumvent mutations to the original.
        var item = JSON.parse(JSON.stringify(options));
        // If image class name is not set, use the default value.
        item.imgClassName = item.imgClassName ||
            "jp-Image" + item.name.replace(/\ /g, '');
        this._items.push(item);
        this.stateChanged.emit(void 0);
        return new disposable_1.DisposableDelegate(function () {
            algorithm_1.ArrayExt.removeFirstOf(_this._items, item);
            _this.stateChanged.emit(void 0);
        });
    };
    /**
     * Return an iterator of launcher items.
     */
    LauncherModel.prototype.items = function () {
        return new algorithm_1.ArrayIterator(this._items);
    };
    return LauncherModel;
}(apputils_1.VDomModel));
exports.LauncherModel = LauncherModel;
/**
 * A virtual-DOM-based widget for the Launcher.
 */
var LauncherWidget = (function (_super) {
    __extends(LauncherWidget, _super);
    /**
     * Construct a new launcher widget.
     */
    function LauncherWidget(options) {
        var _this = _super.call(this) || this;
        _this._linker = null;
        _this.addClass(LAUNCHER_CLASS);
        _this._linker = options.linker;
        return _this;
    }
    /**
     * Render the launcher to virtual DOM nodes.
     */
    LauncherWidget.prototype.render = function () {
        // Create an iterator that yields rendered item nodes.
        var linker = this._linker;
        var children = algorithm_1.map(this.model.items(), function (item) {
            var img = virtualdom_1.h.span({ className: item.imgClassName + ' ' + IMAGE_CLASS });
            var text = virtualdom_1.h.span({ className: TEXT_CLASS }, item.name);
            return virtualdom_1.h.div({
                className: ITEM_CLASS,
                dataset: linker.populateVNodeDataset(item.command, item.args)
            }, [img, text]);
        });
        var folderImage = virtualdom_1.h.span({
            className: FOLDER_CLASS + " " + FOLDER_ICON_CLASS
        });
        var p = this.model.path;
        var pathName = p.length ? "home > " + p.replace(/\//g, ' > ') : 'home';
        var path = virtualdom_1.h.span({ className: PATH_CLASS }, pathName);
        var cwd = virtualdom_1.h.div({ className: CWD_CLASS }, [folderImage, path]);
        var body = virtualdom_1.h.div({ className: BODY_CLASS }, algorithm_1.toArray(children));
        return virtualdom_1.h.div({ className: DIALOG_CLASS }, [cwd, body]);
    };
    return LauncherWidget;
}(apputils_1.VDomWidget));
exports.LauncherWidget = LauncherWidget;

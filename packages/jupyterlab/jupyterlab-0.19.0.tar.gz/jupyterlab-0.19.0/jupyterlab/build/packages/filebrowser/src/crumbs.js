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
var domutils_1 = require("@phosphor/domutils");
var widgets_1 = require("@phosphor/widgets");
var apputils_1 = require("@jupyterlab/apputils");
var apputils_2 = require("@jupyterlab/apputils");
var utils = require("./utils");
/**
 * The class name added to material icons
 */
var MATERIAL_CLASS = 'jp-MaterialIcon';
/**
 * The class name added to the breadcrumb node.
 */
var BREADCRUMB_CLASS = 'jp-BreadCrumbs';
/**
 * The class name added to add the home icon for the breadcrumbs
 */
var BREADCRUMB_HOME = 'jp-HomeIcon';
/**
 * The class named associated to the ellipses icon
 */
var BREADCRUMB_ELLIPSES = 'jp-EllipsesIcon';
/**
 * The class name added to the breadcrumb node.
 */
var BREADCRUMB_ITEM_CLASS = 'jp-BreadCrumbs-item';
/**
 * Bread crumb paths.
 */
var BREAD_CRUMB_PATHS = ['/', '../../', '../', ''];
/**
 * A class which hosts folder breadcrumbs.
 */
var BreadCrumbs = (function (_super) {
    __extends(BreadCrumbs, _super);
    /**
     * Construct a new file browser crumb widget.
     *
     * @param model - The file browser view model.
     */
    function BreadCrumbs(options) {
        var _this = _super.call(this) || this;
        _this._model = null;
        _this._crumbs = null;
        _this._crumbSeps = null;
        _this._model = options.model;
        _this.addClass(BREADCRUMB_CLASS);
        _this._crumbs = Private.createCrumbs();
        _this._crumbSeps = Private.createCrumbSeparators();
        _this.node.appendChild(_this._crumbs[Private.Crumb.Home]);
        _this._model.refreshed.connect(_this.update, _this);
        return _this;
    }
    /**
     * Handle the DOM events for the bread crumbs.
     *
     * @param event - The DOM event sent to the widget.
     *
     * #### Notes
     * This method implements the DOM `EventListener` interface and is
     * called in response to events on the panel's DOM node. It should
     * not be called directly by user code.
     */
    BreadCrumbs.prototype.handleEvent = function (event) {
        switch (event.type) {
            case 'click':
                this._evtClick(event);
                break;
            case 'p-dragenter':
                this._evtDragEnter(event);
                break;
            case 'p-dragleave':
                this._evtDragLeave(event);
                break;
            case 'p-dragover':
                this._evtDragOver(event);
                break;
            case 'p-drop':
                this._evtDrop(event);
                break;
            default:
                return;
        }
    };
    /**
     * A message handler invoked on an `'after-attach'` message.
     */
    BreadCrumbs.prototype.onAfterAttach = function (msg) {
        _super.prototype.onAfterAttach.call(this, msg);
        this.update();
        var node = this.node;
        node.addEventListener('click', this);
        node.addEventListener('p-dragenter', this);
        node.addEventListener('p-dragleave', this);
        node.addEventListener('p-dragover', this);
        node.addEventListener('p-drop', this);
    };
    /**
     * A message handler invoked on a `'before-detach'` message.
     */
    BreadCrumbs.prototype.onBeforeDetach = function (msg) {
        _super.prototype.onBeforeDetach.call(this, msg);
        var node = this.node;
        node.removeEventListener('click', this);
        node.removeEventListener('p-dragenter', this);
        node.removeEventListener('p-dragleave', this);
        node.removeEventListener('p-dragover', this);
        node.removeEventListener('p-drop', this);
    };
    /**
     * A handler invoked on an `'update-request'` message.
     */
    BreadCrumbs.prototype.onUpdateRequest = function (msg) {
        // Update the breadcrumb list.
        Private.updateCrumbs(this._crumbs, this._crumbSeps, this._model.path);
    };
    /**
     * Handle the `'click'` event for the widget.
     */
    BreadCrumbs.prototype._evtClick = function (event) {
        // Do nothing if it's not a left mouse press.
        if (event.button !== 0) {
            return;
        }
        // Find a valid click target.
        var node = event.target;
        while (node && node !== this.node) {
            if (node.classList.contains(BREADCRUMB_ITEM_CLASS)) {
                var index = algorithm_1.ArrayExt.findFirstIndex(this._crumbs, function (value) { return value === node; });
                this._model.cd(BREAD_CRUMB_PATHS[index]).catch(function (error) {
                    return utils.showErrorMessage('Open Error', error);
                });
                // Stop the event propagation.
                event.preventDefault();
                event.stopPropagation();
                return;
            }
            node = node.parentElement;
        }
    };
    /**
     * Handle the `'p-dragenter'` event for the widget.
     */
    BreadCrumbs.prototype._evtDragEnter = function (event) {
        if (event.mimeData.hasData(utils.CONTENTS_MIME)) {
            var index = algorithm_1.ArrayExt.findFirstIndex(this._crumbs, function (node) { return domutils_1.ElementExt.hitTest(node, event.clientX, event.clientY); });
            if (index !== -1) {
                if (index !== Private.Crumb.Current) {
                    this._crumbs[index].classList.add(utils.DROP_TARGET_CLASS);
                    event.preventDefault();
                    event.stopPropagation();
                }
            }
        }
    };
    /**
     * Handle the `'p-dragleave'` event for the widget.
     */
    BreadCrumbs.prototype._evtDragLeave = function (event) {
        event.preventDefault();
        event.stopPropagation();
        var dropTarget = apputils_2.DOMUtils.findElement(this.node, utils.DROP_TARGET_CLASS);
        if (dropTarget) {
            dropTarget.classList.remove(utils.DROP_TARGET_CLASS);
        }
    };
    /**
     * Handle the `'p-dragover'` event for the widget.
     */
    BreadCrumbs.prototype._evtDragOver = function (event) {
        event.preventDefault();
        event.stopPropagation();
        event.dropAction = event.proposedAction;
        var dropTarget = apputils_2.DOMUtils.findElement(this.node, utils.DROP_TARGET_CLASS);
        if (dropTarget) {
            dropTarget.classList.remove(utils.DROP_TARGET_CLASS);
        }
        var index = algorithm_1.ArrayExt.findFirstIndex(this._crumbs, function (node) { return domutils_1.ElementExt.hitTest(node, event.clientX, event.clientY); });
        if (index !== -1) {
            this._crumbs[index].classList.add(utils.DROP_TARGET_CLASS);
        }
    };
    /**
     * Handle the `'p-drop'` event for the widget.
     */
    BreadCrumbs.prototype._evtDrop = function (event) {
        var _this = this;
        event.preventDefault();
        event.stopPropagation();
        if (event.proposedAction === 'none') {
            event.dropAction = 'none';
            return;
        }
        if (!event.mimeData.hasData(utils.CONTENTS_MIME)) {
            return;
        }
        event.dropAction = event.proposedAction;
        var target = event.target;
        while (target && target.parentElement) {
            if (target.classList.contains(utils.DROP_TARGET_CLASS)) {
                target.classList.remove(utils.DROP_TARGET_CLASS);
                break;
            }
            target = target.parentElement;
        }
        // Get the path based on the target node.
        var index = algorithm_1.ArrayExt.findFirstIndex(this._crumbs, function (node) { return node === target; });
        if (index === -1) {
            return;
        }
        var path = BREAD_CRUMB_PATHS[index];
        var model = this._model;
        // Move all of the items.
        var promises = [];
        var names = event.mimeData.getData(utils.CONTENTS_MIME);
        var _loop_1 = function (name_1) {
            var newPath = path + name_1;
            promises.push(this_1._model.rename(name_1, newPath).catch(function (error) {
                if (error.xhr) {
                    error.message = error.xhr.status + ": error.statusText";
                }
                if (error.message.ArrayExt.firstIndexOf('409') !== -1) {
                    var overwrite = apputils_1.Dialog.warnButton({ label: 'OVERWRITE' });
                    var options = {
                        title: 'Overwrite file?',
                        body: "\"" + newPath + "\" already exists, overwrite?",
                        buttons: [apputils_1.Dialog.cancelButton(), overwrite]
                    };
                    return apputils_1.showDialog(options).then(function (button) {
                        if (!model.isDisposed && button.accept) {
                            return model.deleteFile(newPath).then(function () {
                                if (!model.isDisposed) {
                                    return _this._model.rename(name_1, newPath);
                                }
                            });
                        }
                    });
                }
            }));
        };
        var this_1 = this;
        for (var _i = 0, names_1 = names; _i < names_1.length; _i++) {
            var name_1 = names_1[_i];
            _loop_1(name_1);
        }
        Promise.all(promises).catch(function (err) {
            utils.showErrorMessage('Move Error', err);
        });
    };
    return BreadCrumbs;
}(widgets_1.Widget));
exports.BreadCrumbs = BreadCrumbs;
/**
 * The namespace for the crumbs private data.
 */
var Private;
(function (Private) {
    /**
     * Breadcrumb item list enum.
     */
    var Crumb;
    (function (Crumb) {
        Crumb[Crumb["Home"] = 0] = "Home";
        Crumb[Crumb["Ellipsis"] = 1] = "Ellipsis";
        Crumb[Crumb["Parent"] = 2] = "Parent";
        Crumb[Crumb["Current"] = 3] = "Current";
    })(Crumb = Private.Crumb || (Private.Crumb = {}));
    /**
     * Populate the breadcrumb node.
     */
    function updateCrumbs(breadcrumbs, separators, path) {
        var node = breadcrumbs[0].parentNode;
        // Remove all but the home node.
        while (node.firstChild.nextSibling) {
            node.removeChild(node.firstChild.nextSibling);
        }
        var parts = path.split('/');
        if (parts.length > 2) {
            node.appendChild(separators[0]);
            node.appendChild(breadcrumbs[Crumb.Ellipsis]);
            var grandParent = parts.slice(0, parts.length - 2).join('/');
            breadcrumbs[Crumb.Ellipsis].title = grandParent;
        }
        if (path) {
            if (parts.length >= 2) {
                node.appendChild(separators[1]);
                breadcrumbs[Crumb.Parent].textContent = parts[parts.length - 2];
                node.appendChild(breadcrumbs[Crumb.Parent]);
                var parent_1 = parts.slice(0, parts.length - 1).join('/');
                breadcrumbs[Crumb.Parent].title = parent_1;
            }
            node.appendChild(separators[2]);
            breadcrumbs[Crumb.Current].textContent = parts[parts.length - 1];
            node.appendChild(breadcrumbs[Crumb.Current]);
            breadcrumbs[Crumb.Current].title = path;
        }
    }
    Private.updateCrumbs = updateCrumbs;
    /**
     * Create the breadcrumb nodes.
     */
    function createCrumbs() {
        var home = document.createElement('span');
        home.className = MATERIAL_CLASS + ' ' + BREADCRUMB_HOME + ' ' + BREADCRUMB_ITEM_CLASS;
        var ellipsis = document.createElement('span');
        ellipsis.className = MATERIAL_CLASS + ' ' + BREADCRUMB_ELLIPSES + ' ' + BREADCRUMB_ITEM_CLASS;
        var parent = document.createElement('span');
        parent.className = BREADCRUMB_ITEM_CLASS;
        var current = document.createElement('span');
        current.className = BREADCRUMB_ITEM_CLASS;
        return [home, ellipsis, parent, current];
    }
    Private.createCrumbs = createCrumbs;
    /**
     * Create the breadcrumb separator nodes.
     */
    function createCrumbSeparators() {
        var items = [];
        for (var i = 0; i < 3; i++) {
            var item = document.createElement('i');
            item.className = 'fa fa-angle-right';
            items.push(item);
        }
        return items;
    }
    Private.createCrumbSeparators = createCrumbSeparators;
})(Private || (Private = {}));

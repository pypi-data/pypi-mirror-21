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
var messaging_1 = require("@phosphor/messaging");
var coreutils_1 = require("@phosphor/coreutils");
var dragdrop_1 = require("@phosphor/dragdrop");
var domutils_1 = require("@phosphor/domutils");
var widgets_1 = require("@phosphor/widgets");
var apputils_1 = require("@jupyterlab/apputils");
var coreutils_2 = require("@jupyterlab/coreutils");
var dialogs_1 = require("./dialogs");
var utils = require("./utils");
var utils_1 = require("./utils");
/**
 * The class name added to DirListing widget.
 */
var DIR_LISTING_CLASS = 'jp-DirListing';
/**
 * The class name added to a dir listing header node.
 */
var HEADER_CLASS = 'jp-DirListing-header';
/**
 * The class name added to a dir listing list header cell.
 */
var HEADER_ITEM_CLASS = 'jp-DirListing-headerItem';
/**
 * The class name added to a header cell text node.
 */
var HEADER_ITEM_TEXT_CLASS = 'jp-DirListing-headerItemText';
/**
 * The class name added to a header cell icon node.
 */
var HEADER_ITEM_ICON_CLASS = 'jp-DirListing-headerItemIcon';
/**
 * The class name added to the dir listing content node.
 */
var CONTENT_CLASS = 'jp-DirListing-content';
/**
 * The class name added to dir listing content item.
 */
var ITEM_CLASS = 'jp-DirListing-item';
/**
 * The class name added to the listing item text cell.
 */
var ITEM_TEXT_CLASS = 'jp-DirListing-itemText';
/**
 * The class name added to the listing item icon cell.
 */
var ITEM_ICON_CLASS = 'jp-DirListing-itemIcon';
/**
 * The class name added to the listing item modified cell.
 */
var ITEM_MODIFIED_CLASS = 'jp-DirListing-itemModified';
/**
 * The class name added to the dir listing editor node.
 */
var EDITOR_CLASS = 'jp-DirListing-editor';
/**
 * The class name added to the name column header cell.
 */
var NAME_ID_CLASS = 'jp-id-name';
/**
 * The class name added to the modified column header cell.
 */
var MODIFIED_ID_CLASS = 'jp-id-modified';
/**
 * The class name added to a file type content item.
 */
var FILE_TYPE_CLASS = 'jp-FileIcon';
/**
 * The class name added to a material icon content item.
 */
var FOLDER_MATERIAL_ICON_CLASS = 'jp-OpenFolderIcon';
var NOTEBOOK_MATERIAL_ICON_CLASS = 'jp-NotebookIcon';
var MATERIAL_ICON_CLASS = 'jp-MaterialIcon';
/**
 * The class name added to drag state icons to add space between the icon and the file name
 */
var DRAG_ICON_CLASS = 'jp-DragIcon';
/**
 * The class name added to the widget when there are items on the clipboard.
 */
var CLIPBOARD_CLASS = 'jp-mod-clipboard';
/**
 * The class name added to cut rows.
 */
var CUT_CLASS = 'jp-mod-cut';
/**
 * The class name added when there are more than one selected rows.
 */
var MULTI_SELECTED_CLASS = 'jp-mod-multiSelected';
/**
 * The class name added to indicate running notebook.
 */
var RUNNING_CLASS = 'jp-mod-running';
/**
 * The class name added for a decending sort.
 */
var DESCENDING_CLASS = 'jp-mod-descending';
/**
 * The minimum duration for a rename select in ms.
 */
var RENAME_DURATION = 1000;
/**
 * The threshold in pixels to start a drag event.
 */
var DRAG_THRESHOLD = 5;
/**
 * A boolean indicating whether the platform is Mac.
 */
var IS_MAC = !!navigator.platform.match(/Mac/i);
/**
 * The factory MIME type supported by phosphor dock panels.
 */
var FACTORY_MIME = 'application/vnd.phosphor.widget-factory';
/**
 * A widget which hosts a file list area.
 */
var DirListing = (function (_super) {
    __extends(DirListing, _super);
    /**
     * Construct a new file browser directory listing widget.
     *
     * @param model - The file browser view model.
     */
    function DirListing(options) {
        var _this = _super.call(this, {
            node: (options.renderer || DirListing.defaultRenderer).createNode()
        }) || this;
        _this._model = null;
        _this._editNode = null;
        _this._items = [];
        _this._sortedItems = [];
        _this._sortState = { direction: 'ascending', key: 'name' };
        _this._drag = null;
        _this._dragData = null;
        _this._selectTimer = -1;
        _this._noSelectTimer = -1;
        _this._isCut = false;
        _this._prevPath = '';
        _this._clipboard = [];
        _this._manager = null;
        _this._softSelection = '';
        _this._inContext = false;
        _this._selection = Object.create(null);
        _this._renderer = null;
        _this.addClass(DIR_LISTING_CLASS);
        _this._model = options.model;
        _this._model.fileChanged.connect(_this._onFileChanged, _this);
        _this._model.refreshed.connect(_this._onModelRefreshed, _this);
        _this._model.pathChanged.connect(_this._onPathChanged, _this);
        _this._editNode = document.createElement('input');
        _this._editNode.className = EDITOR_CLASS;
        _this._manager = options.manager;
        _this._renderer = options.renderer || DirListing.defaultRenderer;
        var headerNode = apputils_1.DOMUtils.findElement(_this.node, HEADER_CLASS);
        _this._renderer.populateHeaderNode(headerNode);
        _this._manager.activateRequested.connect(_this._onActivateRequested, _this);
        return _this;
    }
    /**
     * Dispose of the resources held by the directory listing.
     */
    DirListing.prototype.dispose = function () {
        this._model = null;
        this._items = null;
        this._editNode = null;
        this._drag = null;
        this._dragData = null;
        this._manager = null;
        _super.prototype.dispose.call(this);
    };
    Object.defineProperty(DirListing.prototype, "model", {
        /**
         * Get the model used by the listing.
         */
        get: function () {
            return this._model;
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(DirListing.prototype, "headerNode", {
        /**
         * Get the dir listing header node.
         *
         * #### Notes
         * This is the node which holds the header cells.
         *
         * Modifying this node directly can lead to undefined behavior.
         */
        get: function () {
            return apputils_1.DOMUtils.findElement(this.node, HEADER_CLASS);
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(DirListing.prototype, "contentNode", {
        /**
         * Get the dir listing content node.
         *
         * #### Notes
         * This is the node which holds the item nodes.
         *
         * Modifying this node directly can lead to undefined behavior.
         */
        get: function () {
            return apputils_1.DOMUtils.findElement(this.node, CONTENT_CLASS);
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(DirListing.prototype, "renderer", {
        /**
         * The renderer instance used by the directory listing.
         */
        get: function () {
            return this._renderer;
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(DirListing.prototype, "sortState", {
        /**
         * The current sort state.
         */
        get: function () {
            return this._sortState;
        },
        enumerable: true,
        configurable: true
    });
    /**
     * Create an iterator over the listing's sorted items.
     *
     * @returns A new iterator over the listing's sorted items.
     */
    DirListing.prototype.sortedItems = function () {
        return new algorithm_1.ArrayIterator(this._sortedItems);
    };
    /**
     * Sort the items using a sort condition.
     */
    DirListing.prototype.sort = function (state) {
        this._sortedItems = Private.sort(this.model.items(), state);
        this._sortState = state;
        this.update();
    };
    /**
     * Rename the first currently selected item.
     *
     * @returns A promise that resolves with the new name of the item.
     */
    DirListing.prototype.rename = function () {
        return this._doRename();
    };
    /**
     * Cut the selected items.
     */
    DirListing.prototype.cut = function () {
        this._isCut = true;
        this._copy();
    };
    /**
     * Copy the selected items.
     */
    DirListing.prototype.copy = function () {
        this._copy();
    };
    /**
     * Paste the items from the clipboard.
     *
     * @returns A promise that resolves when the operation is complete.
     */
    DirListing.prototype.paste = function () {
        var _this = this;
        if (!this._clipboard.length) {
            return;
        }
        var promises = [];
        algorithm_1.each(this._clipboard, function (path) {
            if (_this._isCut) {
                var parts = path.split('/');
                var name_1 = parts[parts.length - 1];
                promises.push(_this._model.rename(path, name_1));
            }
            else {
                promises.push(_this._model.copy(path, '.'));
            }
        });
        // Remove any cut modifiers.
        algorithm_1.each(this._items, function (item) {
            item.classList.remove(CUT_CLASS);
        });
        this._clipboard.length = 0;
        this._isCut = false;
        this.removeClass(CLIPBOARD_CLASS);
        return Promise.all(promises).catch(function (error) {
            utils.showErrorMessage('Paste Error', error);
        });
    };
    /**
     * Delete the currently selected item(s).
     *
     * @returns A promise that resolves when the operation is complete.
     */
    DirListing.prototype.delete = function () {
        var _this = this;
        var names = [];
        algorithm_1.each(this._sortedItems, function (item) {
            if (_this._selection[item.name]) {
                names.push(item.name);
            }
        });
        var message = "Permanently delete these " + names.length + " files?";
        if (names.length === 1) {
            message = "Permanently delete file \"" + names[0] + "\"?";
        }
        if (names.length) {
            return apputils_1.showDialog({
                title: 'Delete file?',
                body: message,
                buttons: [apputils_1.Dialog.cancelButton(), apputils_1.Dialog.warnButton({ label: 'DELETE' })]
            }).then(function (result) {
                if (!_this.isDisposed && result.accept) {
                    return _this._delete(names);
                }
            });
        }
        return Promise.resolve(void 0);
    };
    /**
     * Duplicate the currently selected item(s).
     *
     * @returns A promise that resolves when the operation is complete.
     */
    DirListing.prototype.duplicate = function () {
        var promises = [];
        for (var _i = 0, _a = this._getSelectedItems(); _i < _a.length; _i++) {
            var item = _a[_i];
            if (item.type !== 'directory') {
                promises.push(this._model.copy(item.name, '.'));
            }
        }
        return Promise.all(promises).catch(function (error) {
            if (error.throwError) {
                error.message = error.throwError;
            }
            utils.showErrorMessage('Duplicate file', error);
        });
    };
    /**
     * Download the currently selected item(s).
     */
    DirListing.prototype.download = function () {
        for (var _i = 0, _a = this._getSelectedItems(); _i < _a.length; _i++) {
            var item = _a[_i];
            if (item.type !== 'directory') {
                this._model.download(item.path);
            }
        }
    };
    /**
     * Shut down kernels on the applicable currently selected items.
     *
     * @returns A promise that resolves when the operation is complete.
     */
    DirListing.prototype.shutdownKernels = function () {
        var _this = this;
        var promises = [];
        var items = this._sortedItems;
        var paths = algorithm_1.toArray(algorithm_1.map(items, function (item) { return item.path; }));
        algorithm_1.each(this._model.sessions(), function (session) {
            var index = algorithm_1.ArrayExt.firstIndexOf(paths, session.notebook.path);
            if (_this._selection[items[index].name]) {
                promises.push(_this._model.shutdown(session.id));
            }
        });
        return Promise.all(promises).catch(function (error) {
            utils.showErrorMessage('Shutdown kernel', error);
        });
    };
    /**
     * Select next item.
     *
     * @param keepExisting - Whether to keep the current selection and add to it.
     */
    DirListing.prototype.selectNext = function (keepExisting) {
        if (keepExisting === void 0) { keepExisting = false; }
        var index = -1;
        var selected = Object.keys(this._selection);
        var items = this._sortedItems;
        if (selected.length === 1 || keepExisting) {
            // Select the next item.
            var name_2 = selected[selected.length - 1];
            index = algorithm_1.ArrayExt.findFirstIndex(items, function (value) { return value.name === name_2; });
            index += 1;
            if (index === this._items.length) {
                index = 0;
            }
        }
        else if (selected.length === 0) {
            // Select the first item.
            index = 0;
        }
        else {
            // Select the last selected item.
            var name_3 = selected[selected.length - 1];
            index = algorithm_1.ArrayExt.findFirstIndex(items, function (value) { return value.name === name_3; });
        }
        if (index !== -1) {
            this._selectItem(index, keepExisting);
            domutils_1.ElementExt.scrollIntoViewIfNeeded(this.contentNode, this._items[index]);
        }
    };
    /**
     * Select previous item.
     *
     * @param keepExisting - Whether to keep the current selection and add to it.
     */
    DirListing.prototype.selectPrevious = function (keepExisting) {
        if (keepExisting === void 0) { keepExisting = false; }
        var index = -1;
        var selected = Object.keys(this._selection);
        var items = this._sortedItems;
        if (selected.length === 1 || keepExisting) {
            // Select the previous item.
            var name_4 = selected[0];
            index = algorithm_1.ArrayExt.findFirstIndex(items, function (value) { return value.name === name_4; });
            index -= 1;
            if (index === -1) {
                index = this._items.length - 1;
            }
        }
        else if (selected.length === 0) {
            // Select the last item.
            index = this._items.length - 1;
        }
        else {
            // Select the first selected item.
            var name_5 = selected[0];
            index = algorithm_1.ArrayExt.findFirstIndex(items, function (value) { return value.name === name_5; });
        }
        if (index !== -1) {
            this._selectItem(index, keepExisting);
            domutils_1.ElementExt.scrollIntoViewIfNeeded(this.contentNode, this._items[index]);
        }
    };
    /**
     * Get whether an item is selected by name.
     *
     * @param name - The name of of the item.
     *
     * @returns Whether the item is selected.
     */
    DirListing.prototype.isSelected = function (name) {
        return this._selection[name] === true;
    };
    /**
     * Find a path given a click.
     *
     * @param event - The mouse event.
     *
     * @returns The path to the selected file.
     */
    DirListing.prototype.pathForClick = function (event) {
        var items = this._sortedItems;
        var index = Private.hitTestNodes(this._items, event.clientX, event.clientY);
        if (index !== -1) {
            return items[index].path;
        }
    };
    /**
     * Handle the DOM events for the directory listing.
     *
     * @param event - The DOM event sent to the widget.
     *
     * #### Notes
     * This method implements the DOM `EventListener` interface and is
     * called in response to events on the panel's DOM node. It should
     * not be called directly by user code.
     */
    DirListing.prototype.handleEvent = function (event) {
        switch (event.type) {
            case 'mousedown':
                this._evtMousedown(event);
                break;
            case 'mouseup':
                this._evtMouseup(event);
                break;
            case 'mousemove':
                this._evtMousemove(event);
                break;
            case 'keydown':
                this._evtKeydown(event);
                break;
            case 'click':
                this._evtClick(event);
                break;
            case 'dblclick':
                this._evtDblClick(event);
                break;
            case 'contextmenu':
                this._evtContextMenu(event);
                break;
            case 'scroll':
                this._evtScroll(event);
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
                break;
        }
    };
    /**
     * A message handler invoked on an `'after-attach'` message.
     */
    DirListing.prototype.onAfterAttach = function (msg) {
        _super.prototype.onAfterAttach.call(this, msg);
        var node = this.node;
        var content = apputils_1.DOMUtils.findElement(node, CONTENT_CLASS);
        node.addEventListener('mousedown', this);
        node.addEventListener('keydown', this);
        node.addEventListener('click', this);
        node.addEventListener('dblclick', this);
        node.addEventListener('contextmenu', this);
        content.addEventListener('scroll', this);
        content.addEventListener('p-dragenter', this);
        content.addEventListener('p-dragleave', this);
        content.addEventListener('p-dragover', this);
        content.addEventListener('p-drop', this);
    };
    /**
     * A message handler invoked on a `'before-detach'` message.
     */
    DirListing.prototype.onBeforeDetach = function (msg) {
        _super.prototype.onBeforeDetach.call(this, msg);
        var node = this.node;
        var content = apputils_1.DOMUtils.findElement(node, CONTENT_CLASS);
        node.removeEventListener('mousedown', this);
        node.removeEventListener('keydown', this);
        node.removeEventListener('click', this);
        node.removeEventListener('dblclick', this);
        node.removeEventListener('contextmenu', this);
        content.removeEventListener('scroll', this);
        content.removeEventListener('p-dragenter', this);
        content.removeEventListener('p-dragleave', this);
        content.removeEventListener('p-dragover', this);
        content.removeEventListener('p-drop', this);
        document.removeEventListener('mousemove', this, true);
        document.removeEventListener('mouseup', this, true);
    };
    /**
     * A handler invoked on an `'update-request'` message.
     */
    DirListing.prototype.onUpdateRequest = function (msg) {
        var _this = this;
        // Fetch common variables.
        var items = this._sortedItems;
        var nodes = this._items;
        var content = apputils_1.DOMUtils.findElement(this.node, CONTENT_CLASS);
        var renderer = this._renderer;
        this.removeClass(MULTI_SELECTED_CLASS);
        this.removeClass(utils_1.SELECTED_CLASS);
        // Remove any excess item nodes.
        while (nodes.length > items.length) {
            var node = nodes.pop();
            content.removeChild(node);
        }
        // Add any missing item nodes.
        while (nodes.length < items.length) {
            var node = renderer.createItemNode();
            node.classList.add(ITEM_CLASS);
            nodes.push(node);
            content.appendChild(node);
        }
        // Remove extra classes from the nodes.
        algorithm_1.each(nodes, function (item) {
            item.classList.remove(utils_1.SELECTED_CLASS);
            item.classList.remove(RUNNING_CLASS);
            item.classList.remove(CUT_CLASS);
        });
        // Add extra classes to item nodes based on widget state.
        for (var i = 0, n = items.length; i < n; ++i) {
            var node = nodes[i];
            var item = items[i];
            renderer.updateItemNode(node, item);
            if (this._selection[item.name]) {
                node.classList.add(utils_1.SELECTED_CLASS);
                if (this._isCut && this._model.path === this._prevPath) {
                    node.classList.add(CUT_CLASS);
                }
            }
        }
        // Handle the selectors on the widget node.
        var selectedNames = Object.keys(this._selection);
        if (selectedNames.length > 1) {
            this.addClass(MULTI_SELECTED_CLASS);
        }
        if (selectedNames.length) {
            this.addClass(utils_1.SELECTED_CLASS);
        }
        // Handle notebook session statuses.
        var paths = algorithm_1.toArray(algorithm_1.map(items, function (item) { return item.path; }));
        algorithm_1.each(this._model.sessions(), function (session) {
            var index = algorithm_1.ArrayExt.firstIndexOf(paths, session.notebook.path);
            var node = nodes[index];
            node.classList.add(RUNNING_CLASS);
            var name = session.kernel.name;
            var specs = _this._model.specs;
            if (specs) {
                name = specs.kernelspecs[name].display_name;
            }
            node.title = name;
        });
        this._prevPath = this._model.path;
    };
    /**
     * Handle the `'click'` event for the widget.
     */
    DirListing.prototype._evtClick = function (event) {
        var target = event.target;
        var header = this.headerNode;
        if (header.contains(target)) {
            var state = this.renderer.handleHeaderClick(header, event);
            if (state) {
                this.sort(state);
            }
            return;
        }
    };
    /**
     * Handle the `'scroll'` event for the widget.
     */
    DirListing.prototype._evtScroll = function (event) {
        this.headerNode.scrollLeft = this.contentNode.scrollLeft;
    };
    /**
     * Handle the `'contextmenu'` event for the widget.
     */
    DirListing.prototype._evtContextMenu = function (event) {
        this._inContext = true;
    };
    /**
     * Handle the `'mousedown'` event for the widget.
     */
    DirListing.prototype._evtMousedown = function (event) {
        // Bail if clicking within the edit node
        if (event.target === this._editNode) {
            return;
        }
        // Blur the edit node if necessary.
        if (this._editNode.parentNode) {
            if (this._editNode !== event.target) {
                this._editNode.focus();
                this._editNode.blur();
                clearTimeout(this._selectTimer);
            }
            else {
                return;
            }
        }
        // Check for clearing a context menu.
        var newContext = (IS_MAC && event.ctrlKey) || (event.button === 2);
        if (this._inContext && !newContext) {
            this._inContext = false;
            return;
        }
        this._inContext = false;
        var index = Private.hitTestNodes(this._items, event.clientX, event.clientY);
        if (index === -1) {
            return;
        }
        this._handleFileSelect(event);
        // Left mouse press for drag start.
        if (event.button === 0) {
            this._dragData = { pressX: event.clientX, pressY: event.clientY,
                index: index };
            document.addEventListener('mouseup', this, true);
            document.addEventListener('mousemove', this, true);
        }
        if (event.button !== 0) {
            clearTimeout(this._selectTimer);
        }
    };
    /**
     * Handle the `'mouseup'` event for the widget.
     */
    DirListing.prototype._evtMouseup = function (event) {
        // Handle any soft selection from the previous mouse down.
        if (this._softSelection) {
            var altered = event.metaKey || event.shiftKey || event.ctrlKey;
            // See if we need to clear the other selection.
            if (!altered && event.button === 0) {
                this._selection = Object.create(null);
                this._selection[this._softSelection] = true;
                this.update();
            }
            this._softSelection = '';
        }
        // Remove the drag listeners if necessary.
        if (event.button !== 0 || !this._drag) {
            document.removeEventListener('mousemove', this, true);
            document.removeEventListener('mouseup', this, true);
            return;
        }
        event.preventDefault();
        event.stopPropagation();
    };
    /**
     * Handle the `'mousemove'` event for the widget.
     */
    DirListing.prototype._evtMousemove = function (event) {
        event.preventDefault();
        event.stopPropagation();
        // Bail if we are the one dragging.
        if (this._drag) {
            return;
        }
        // Check for a drag initialization.
        var data = this._dragData;
        var dx = Math.abs(event.clientX - data.pressX);
        var dy = Math.abs(event.clientY - data.pressY);
        if (dx < DRAG_THRESHOLD && dy < DRAG_THRESHOLD) {
            return;
        }
        this._startDrag(data.index, event.clientX, event.clientY);
    };
    /**
     * Handle the `'keydown'` event for the widget.
     */
    DirListing.prototype._evtKeydown = function (event) {
        switch (event.keyCode) {
            case 13:
                // Do nothing if any modifier keys are pressed.
                if (event.ctrlKey || event.shiftKey || event.altKey || event.metaKey) {
                    return;
                }
                event.preventDefault();
                event.stopPropagation();
                if (IS_MAC) {
                    this._doRename();
                    return;
                }
                var selected = Object.keys(this._selection);
                var name_6 = selected[0];
                var items = this._sortedItems;
                var i = algorithm_1.ArrayExt.findFirstIndex(items, function (value) { return value.name === name_6; });
                if (i === -1) {
                    return;
                }
                var model = this._model;
                var item = this._sortedItems[i];
                if (item.type === 'directory') {
                    model.cd(item.name).catch(function (error) {
                        return utils_1.showErrorMessage('Open directory', error);
                    });
                }
                else {
                    var path = item.path;
                    this._manager.openOrReveal(path);
                }
                break;
            case 38:
                this.selectPrevious(event.shiftKey);
                event.stopPropagation();
                event.preventDefault();
                break;
            case 40:
                this.selectNext(event.shiftKey);
                event.stopPropagation();
                event.preventDefault();
                break;
            default:
                break;
        }
    };
    /**
     * Handle the `'dblclick'` event for the widget.
     */
    DirListing.prototype._evtDblClick = function (event) {
        var _this = this;
        // Do nothing if it's not a left mouse press.
        if (event.button !== 0) {
            return;
        }
        // Do nothing if any modifier keys are pressed.
        if (event.ctrlKey || event.shiftKey || event.altKey || event.metaKey) {
            return;
        }
        // Stop the event propagation.
        event.preventDefault();
        event.stopPropagation();
        clearTimeout(this._selectTimer);
        this._noSelectTimer = window.setTimeout(function () {
            _this._noSelectTimer = -1;
        }, RENAME_DURATION);
        this._editNode.blur();
        // Find a valid double click target.
        var target = event.target;
        var i = algorithm_1.ArrayExt.findFirstIndex(this._items, function (node) { return node.contains(target); });
        if (i === -1) {
            return;
        }
        var model = this._model;
        var item = this._sortedItems[i];
        if (item.type === 'directory') {
            model.cd(item.name).catch(function (error) {
                return utils_1.showErrorMessage('Open directory', error);
            });
        }
        else {
            var path = item.path;
            this._manager.openOrReveal(path);
        }
    };
    /**
     * Handle the `'p-dragenter'` event for the widget.
     */
    DirListing.prototype._evtDragEnter = function (event) {
        if (event.mimeData.hasData(utils.CONTENTS_MIME)) {
            var index = Private.hitTestNodes(this._items, event.clientX, event.clientY);
            if (index === -1) {
                return;
            }
            var item = this._sortedItems[index];
            if (item.type !== 'directory' || this._selection[item.name]) {
                return;
            }
            var target = event.target;
            target.classList.add(utils.DROP_TARGET_CLASS);
            event.preventDefault();
            event.stopPropagation();
        }
    };
    /**
     * Handle the `'p-dragleave'` event for the widget.
     */
    DirListing.prototype._evtDragLeave = function (event) {
        event.preventDefault();
        event.stopPropagation();
        var dropTarget = apputils_1.DOMUtils.findElement(this.node, utils.DROP_TARGET_CLASS);
        if (dropTarget) {
            dropTarget.classList.remove(utils.DROP_TARGET_CLASS);
        }
    };
    /**
     * Handle the `'p-dragover'` event for the widget.
     */
    DirListing.prototype._evtDragOver = function (event) {
        event.preventDefault();
        event.stopPropagation();
        event.dropAction = event.proposedAction;
        var dropTarget = apputils_1.DOMUtils.findElement(this.node, utils.DROP_TARGET_CLASS);
        if (dropTarget) {
            dropTarget.classList.remove(utils.DROP_TARGET_CLASS);
        }
        var index = Private.hitTestNodes(this._items, event.clientX, event.clientY);
        this._items[index].classList.add(utils.DROP_TARGET_CLASS);
    };
    /**
     * Handle the `'p-drop'` event for the widget.
     */
    DirListing.prototype._evtDrop = function (event) {
        event.preventDefault();
        event.stopPropagation();
        clearTimeout(this._selectTimer);
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
        var index = algorithm_1.ArrayExt.firstIndexOf(this._items, target);
        var items = this._sortedItems;
        var path = items[index].name + '/';
        // Move all of the items.
        var promises = [];
        var names = event.mimeData.getData(utils.CONTENTS_MIME);
        for (var _i = 0, names_1 = names; _i < names_1.length; _i++) {
            var name_7 = names_1[_i];
            var newPath = path + name_7;
            promises.push(dialogs_1.renameFile(this._model, name_7, newPath));
        }
        Promise.all(promises).catch(function (error) {
            utils.showErrorMessage('Move Error', error);
        });
    };
    /**
     * Start a drag event.
     */
    DirListing.prototype._startDrag = function (index, clientX, clientY) {
        var _this = this;
        var selectedNames = Object.keys(this._selection);
        var source = this._items[index];
        var items = this._sortedItems;
        var item = null;
        // If the source node is not selected, use just that node.
        if (!source.classList.contains(utils_1.SELECTED_CLASS)) {
            item = items[index];
            selectedNames = [item.name];
        }
        else if (selectedNames.length === 1) {
            var name_8 = selectedNames[0];
            item = algorithm_1.find(items, function (value) { return value.name === name_8; });
        }
        // Create the drag image.
        var dragImage = this.renderer.createDragImage(source, selectedNames.length, item);
        // Set up the drag event.
        this._drag = new dragdrop_1.Drag({
            dragImage: dragImage,
            mimeData: new coreutils_1.MimeData(),
            supportedActions: 'move',
            proposedAction: 'move'
        });
        this._drag.mimeData.setData(utils.CONTENTS_MIME, selectedNames);
        if (item && item.type !== 'directory') {
            this._drag.mimeData.setData(FACTORY_MIME, function () {
                var path = item.path;
                var widget = _this._manager.findWidget(path);
                if (!widget) {
                    widget = _this._manager.open(item.path);
                }
                return widget;
            });
        }
        // Start the drag and remove the mousemove and mouseup listeners.
        document.removeEventListener('mousemove', this, true);
        document.removeEventListener('mouseup', this, true);
        clearTimeout(this._selectTimer);
        this._drag.start(clientX, clientY).then(function (action) {
            _this._drag = null;
            clearTimeout(_this._selectTimer);
        });
    };
    /**
     * Handle selection on a file node.
     */
    DirListing.prototype._handleFileSelect = function (event) {
        var _this = this;
        // Fetch common variables.
        var items = this._sortedItems;
        var index = Private.hitTestNodes(this._items, event.clientX, event.clientY);
        var target = event.target;
        var inText = target.classList.contains(ITEM_TEXT_CLASS);
        clearTimeout(this._selectTimer);
        if (index === -1) {
            return;
        }
        // Clear any existing soft selection.
        this._softSelection = '';
        var name = items[index].name;
        var selected = Object.keys(this._selection);
        // Handle toggling.
        if ((IS_MAC && event.metaKey) || (!IS_MAC && event.ctrlKey)) {
            if (this._selection[name]) {
                delete this._selection[name];
            }
            else {
                this._selection[name] = true;
            }
            // Handle multiple select.
        }
        else if (event.shiftKey) {
            this._handleMultiSelect(selected, index);
            // Handle a 'soft' selection
        }
        else if (name in this._selection && selected.length > 1) {
            this._softSelection = name;
            // Default to selecting the only the item.
        }
        else {
            // Handle a rename.
            if (inText && selected.length === 1 && selected[0] === name) {
                this._selectTimer = window.setTimeout(function () {
                    if (_this._noSelectTimer === -1) {
                        _this._doRename();
                    }
                }, RENAME_DURATION);
            }
            // Select only the given item.
            this._selection = Object.create(null);
            this._selection[name] = true;
        }
        this._isCut = false;
        this.update();
    };
    /**
     * Select an item by name.
     *
     * @parem name - The name of the item to select.
     *
     * @returns A promise that resolves when the name is selected.
     */
    DirListing.prototype._selectItemByName = function (name) {
        var _this = this;
        // Make sure the file is available.
        return this.model.refresh().then(function () {
            if (_this.isDisposed) {
                return;
            }
            var items = _this._sortedItems;
            var index = algorithm_1.ArrayExt.findFirstIndex(items, function (value) { return value.name === name; });
            if (index === -1) {
                return;
            }
            _this._selectItem(index, false);
            messaging_1.MessageLoop.sendMessage(_this, widgets_1.Widget.Msg.UpdateRequest);
            domutils_1.ElementExt.scrollIntoViewIfNeeded(_this.contentNode, _this._items[index]);
        });
    };
    /**
     * Handle a multiple select on a file item node.
     */
    DirListing.prototype._handleMultiSelect = function (selected, index) {
        // Find the "nearest selected".
        var items = this._sortedItems;
        var nearestIndex = -1;
        for (var i = 0; i < this._items.length; i++) {
            if (i === index) {
                continue;
            }
            var name_9 = items[i].name;
            if (selected.indexOf(name_9) !== -1) {
                if (nearestIndex === -1) {
                    nearestIndex = i;
                }
                else {
                    if (Math.abs(index - i) < Math.abs(nearestIndex - i)) {
                        nearestIndex = i;
                    }
                }
            }
        }
        // Default to the first element (and fill down).
        if (nearestIndex === -1) {
            nearestIndex = 0;
        }
        // Select the rows between the current and the nearest selected.
        for (var i = 0; i < this._items.length; i++) {
            if (nearestIndex >= i && index <= i ||
                nearestIndex <= i && index >= i) {
                this._selection[items[i].name] = true;
            }
        }
    };
    /**
     * Get the currently selected items.
     */
    DirListing.prototype._getSelectedItems = function () {
        var _this = this;
        var items = this._sortedItems;
        return algorithm_1.toArray(algorithm_1.filter(items, function (item) { return _this._selection[item.name]; }));
    };
    /**
     * Copy the selected items, and optionally cut as well.
     */
    DirListing.prototype._copy = function () {
        this._clipboard.length = 0;
        for (var _i = 0, _a = this._getSelectedItems(); _i < _a.length; _i++) {
            var item = _a[_i];
            if (item.type !== 'directory') {
                // Store the absolute path of the item.
                this._clipboard.push('/' + item.path);
            }
        }
        this.update();
    };
    /**
     * Delete the files with the given names.
     */
    DirListing.prototype._delete = function (names) {
        var promises = [];
        for (var _i = 0, names_2 = names; _i < names_2.length; _i++) {
            var name_10 = names_2[_i];
            promises.push(this._model.deleteFile(name_10));
        }
        return Promise.all(promises).catch(function (error) {
            utils.showErrorMessage('Delete file', error);
        });
    };
    /**
     * Allow the user to rename item on a given row.
     */
    DirListing.prototype._doRename = function () {
        var _this = this;
        var items = this._sortedItems;
        var name = Object.keys(this._selection)[0];
        var index = algorithm_1.ArrayExt.findFirstIndex(items, function (value) { return value.name === name; });
        var row = this._items[index];
        var item = items[index];
        var nameNode = this.renderer.getNameNode(row);
        var original = item.name;
        this._editNode.value = original;
        this._selectItem(index, false);
        return Private.doRename(nameNode, this._editNode).then(function (newName) {
            if (newName === original) {
                return original;
            }
            if (_this.isDisposed) {
                return;
            }
            return dialogs_1.renameFile(_this._model, original, newName).catch(function (error) {
                utils.showErrorMessage('Rename Error', error);
                return original;
            }).then(function () {
                if (_this.isDisposed) {
                    return;
                }
                _this._selectItemByName(newName);
                return newName;
            });
        });
    };
    /**
     * Select a given item.
     */
    DirListing.prototype._selectItem = function (index, keepExisting) {
        // Selected the given row(s)
        var items = this._sortedItems;
        if (!keepExisting) {
            this._selection = Object.create(null);
        }
        var name = items[index].name;
        this._selection[name] = true;
        this._isCut = false;
        this.update();
    };
    /**
     * Handle the `refreshed` signal from the model.
     */
    DirListing.prototype._onModelRefreshed = function () {
        var _this = this;
        // Update the selection.
        var existing = Object.keys(this._selection);
        this._selection = Object.create(null);
        algorithm_1.each(this._model.items(), function (item) {
            var name = item.name;
            if (existing.indexOf(name) !== -1) {
                _this._selection[name] = true;
            }
        });
        // Update the sorted items.
        this.sort(this.sortState);
    };
    /**
     * Handle a `pathChanged` signal from the model.
     */
    DirListing.prototype._onPathChanged = function () {
        // Reset the selection.
        this._selection = Object.create(null);
        // Update the sorted items.
        this.sort(this.sortState);
    };
    /**
     * Handle a `fileChanged` signal from the model.
     */
    DirListing.prototype._onFileChanged = function (sender, args) {
        var _this = this;
        if (args.type === 'new') {
            this._selectItemByName(args.newValue.name).then(function () {
                if (!_this.isDisposed && args.newValue === 'directory') {
                    _this._doRename();
                }
            });
        }
    };
    /**
     * Handle an `activateRequested` signal from the manager.
     */
    DirListing.prototype._onActivateRequested = function (sender, args) {
        var dirname = coreutils_2.PathExt.dirname(args);
        if (dirname === '.') {
            dirname = '';
        }
        if (dirname !== this._model.path) {
            return;
        }
        var basename = coreutils_2.PathExt.basename(args);
        this._selectItemByName(basename);
    };
    return DirListing;
}(widgets_1.Widget));
exports.DirListing = DirListing;
/**
 * The namespace for the `DirListing` class statics.
 */
(function (DirListing) {
    /**
     * The default implementation of an `IRenderer`.
     */
    var Renderer = (function () {
        function Renderer() {
        }
        /**
         * Create the DOM node for a dir listing.
         */
        Renderer.prototype.createNode = function () {
            var node = document.createElement('div');
            var header = document.createElement('div');
            var content = document.createElement('ul');
            content.className = CONTENT_CLASS;
            header.className = HEADER_CLASS;
            node.appendChild(header);
            node.appendChild(content);
            node.tabIndex = 1;
            return node;
        };
        /**
         * Populate and empty header node for a dir listing.
         *
         * @param node - The header node to populate.
         */
        Renderer.prototype.populateHeaderNode = function (node) {
            var name = this._createHeaderItemNode('Name');
            var modified = this._createHeaderItemNode('Last Modified');
            name.classList.add(NAME_ID_CLASS);
            name.classList.add(utils_1.SELECTED_CLASS);
            modified.classList.add(MODIFIED_ID_CLASS);
            node.appendChild(name);
            node.appendChild(modified);
        };
        /**
         * Handle a header click.
         *
         * @param node - A node populated by [[populateHeaderNode]].
         *
         * @param event - A click event on the node.
         *
         * @returns The sort state of the header after the click event.
         */
        Renderer.prototype.handleHeaderClick = function (node, event) {
            var name = apputils_1.DOMUtils.findElement(node, NAME_ID_CLASS);
            var modified = apputils_1.DOMUtils.findElement(node, MODIFIED_ID_CLASS);
            var state = { direction: 'ascending', key: 'name' };
            var target = event.target;
            if (name.contains(target)) {
                if (name.classList.contains(utils_1.SELECTED_CLASS)) {
                    if (!name.classList.contains(DESCENDING_CLASS)) {
                        state.direction = 'descending';
                        name.classList.add(DESCENDING_CLASS);
                    }
                    else {
                        name.classList.remove(DESCENDING_CLASS);
                    }
                }
                else {
                    name.classList.remove(DESCENDING_CLASS);
                }
                name.classList.add(utils_1.SELECTED_CLASS);
                modified.classList.remove(utils_1.SELECTED_CLASS);
                modified.classList.remove(DESCENDING_CLASS);
                return state;
            }
            if (modified.contains(target)) {
                state.key = 'last_modified';
                if (modified.classList.contains(utils_1.SELECTED_CLASS)) {
                    if (!modified.classList.contains(DESCENDING_CLASS)) {
                        state.direction = 'descending';
                        modified.classList.add(DESCENDING_CLASS);
                    }
                    else {
                        modified.classList.remove(DESCENDING_CLASS);
                    }
                }
                else {
                    modified.classList.remove(DESCENDING_CLASS);
                }
                modified.classList.add(utils_1.SELECTED_CLASS);
                name.classList.remove(utils_1.SELECTED_CLASS);
                name.classList.remove(DESCENDING_CLASS);
                return state;
            }
            return void 0;
        };
        /**
         * Create a new item node for a dir listing.
         *
         * @returns A new DOM node to use as a content item.
         */
        Renderer.prototype.createItemNode = function () {
            var node = document.createElement('li');
            var icon = document.createElement('span');
            var text = document.createElement('span');
            var modified = document.createElement('span');
            icon.className = ITEM_ICON_CLASS;
            text.className = ITEM_TEXT_CLASS;
            modified.className = ITEM_MODIFIED_CLASS;
            node.appendChild(icon);
            node.appendChild(text);
            node.appendChild(modified);
            return node;
        };
        /**
         * Update an item node to reflect the current state of a model.
         *
         * @param node - A node created by [[createItemNode]].
         *
         * @param model - The model object to use for the item state.
         */
        Renderer.prototype.updateItemNode = function (node, model) {
            var icon = apputils_1.DOMUtils.findElement(node, ITEM_ICON_CLASS);
            var text = apputils_1.DOMUtils.findElement(node, ITEM_TEXT_CLASS);
            var modified = apputils_1.DOMUtils.findElement(node, ITEM_MODIFIED_CLASS);
            icon.className = ITEM_ICON_CLASS + ' ' + MATERIAL_ICON_CLASS;
            switch (model.type) {
                case 'directory':
                    icon.classList.add(FOLDER_MATERIAL_ICON_CLASS);
                    break;
                case 'notebook':
                    icon.classList.add(NOTEBOOK_MATERIAL_ICON_CLASS);
                    break;
                default:
                    icon.classList.add(MATERIAL_ICON_CLASS);
                    icon.classList.add(FILE_TYPE_CLASS);
                    break;
            }
            var modText = '';
            var modTitle = '';
            if (model.last_modified) {
                modText = coreutils_2.Time.formatHuman(model.last_modified);
                modTitle = coreutils_2.Time.format(model.last_modified);
            }
            // If an item is being edited currently, its text node is unavailable.
            if (text) {
                text.textContent = model.name;
            }
            modified.textContent = modText;
            modified.title = modTitle;
        };
        /**
         * Get the node containing the file name.
         *
         * @param node - A node created by [[createItemNode]].
         *
         * @returns The node containing the file name.
         */
        Renderer.prototype.getNameNode = function (node) {
            return apputils_1.DOMUtils.findElement(node, ITEM_TEXT_CLASS);
        };
        /**
         * Create a drag image for an item.
         *
         * @param node - A node created by [[createItemNode]].
         *
         * @param count - The number of items being dragged.
         *
         * @returns An element to use as the drag image.
         */
        Renderer.prototype.createDragImage = function (node, count, model) {
            var dragImage = node.cloneNode(true);
            var modified = apputils_1.DOMUtils.findElement(dragImage, ITEM_MODIFIED_CLASS);
            var iconNode = apputils_1.DOMUtils.findElement(dragImage, ITEM_ICON_CLASS);
            dragImage.removeChild(modified);
            if (model) {
                switch (model.type) {
                    case 'directory':
                        iconNode.className = MATERIAL_ICON_CLASS + " " + FOLDER_MATERIAL_ICON_CLASS + " " + DRAG_ICON_CLASS;
                        break;
                    case 'notebook':
                        iconNode.className = MATERIAL_ICON_CLASS + " " + NOTEBOOK_MATERIAL_ICON_CLASS + " " + DRAG_ICON_CLASS;
                        break;
                    default:
                        iconNode.className = MATERIAL_ICON_CLASS + " " + FILE_TYPE_CLASS + " " + DRAG_ICON_CLASS;
                        break;
                }
            }
            if (count > 1) {
                var nameNode = apputils_1.DOMUtils.findElement(dragImage, ITEM_TEXT_CLASS);
                nameNode.textContent = count + ' Items';
            }
            return dragImage;
        };
        /**
         * Create a node for a header item.
         */
        Renderer.prototype._createHeaderItemNode = function (label) {
            var node = document.createElement('div');
            var text = document.createElement('span');
            var icon = document.createElement('span');
            node.className = HEADER_ITEM_CLASS;
            text.className = HEADER_ITEM_TEXT_CLASS;
            icon.className = HEADER_ITEM_ICON_CLASS;
            text.textContent = label;
            node.appendChild(text);
            node.appendChild(icon);
            return node;
        };
        return Renderer;
    }());
    DirListing.Renderer = Renderer;
    /**
     * The default `IRenderer` instance.
     */
    DirListing.defaultRenderer = new Renderer();
})(DirListing = exports.DirListing || (exports.DirListing = {}));
exports.DirListing = DirListing;
/**
 * The namespace for the listing private data.
 */
var Private;
(function (Private) {
    /**
     * Handle editing text on a node.
     *
     * @returns Boolean indicating whether the name changed.
     */
    function doRename(text, edit) {
        var changed = true;
        var parent = text.parentElement;
        parent.replaceChild(edit, text);
        edit.focus();
        var index = edit.value.lastIndexOf('.');
        if (index === -1) {
            edit.setSelectionRange(0, edit.value.length);
        }
        else {
            edit.setSelectionRange(0, index);
        }
        return new Promise(function (resolve, reject) {
            edit.onblur = function () {
                parent.replaceChild(text, edit);
                resolve(edit.value);
            };
            edit.onkeydown = function (event) {
                switch (event.keyCode) {
                    case 13:
                        event.stopPropagation();
                        event.preventDefault();
                        edit.blur();
                        break;
                    case 27:
                        event.stopPropagation();
                        event.preventDefault();
                        changed = false;
                        edit.blur();
                        break;
                    case 38:
                        event.stopPropagation();
                        event.preventDefault();
                        if (edit.selectionStart !== edit.selectionEnd) {
                            edit.selectionStart = edit.selectionEnd = 0;
                        }
                        break;
                    case 40:
                        event.stopPropagation();
                        event.preventDefault();
                        if (edit.selectionStart !== edit.selectionEnd) {
                            edit.selectionStart = edit.selectionEnd = edit.value.length;
                        }
                        break;
                    default:
                        break;
                }
            };
        });
    }
    Private.doRename = doRename;
    /**
     * Sort a list of items by sort state as a new array.
     */
    function sort(items, state) {
        // Shortcut for unmodified.
        if (state.key !== 'last_modified' && state.direction === 'ascending') {
            return algorithm_1.toArray(items);
        }
        var copy = algorithm_1.toArray(items);
        if (state.key === 'last_modified') {
            copy.sort(function (a, b) {
                var valA = new Date(a.last_modified).getTime();
                var valB = new Date(b.last_modified).getTime();
                return valB - valA;
            });
        }
        // Reverse the order if descending.
        if (state.direction === 'descending') {
            copy.reverse();
        }
        return copy;
    }
    Private.sort = sort;
    /**
     * Get the index of the node at a client position, or `-1`.
     */
    function hitTestNodes(nodes, x, y) {
        return algorithm_1.ArrayExt.findFirstIndex(nodes, function (node) { return domutils_1.ElementExt.hitTest(node, x, y); });
    }
    Private.hitTestNodes = hitTestNodes;
})(Private || (Private = {}));

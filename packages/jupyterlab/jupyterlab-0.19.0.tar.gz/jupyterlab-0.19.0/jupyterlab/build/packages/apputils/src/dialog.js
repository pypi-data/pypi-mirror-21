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
var virtualdom_1 = require("@phosphor/virtualdom");
var widgets_1 = require("@phosphor/widgets");
var styling_1 = require("./styling");
/**
 * Create and show a dialog.
 *
 * @param options - The dialog setup options.
 *
 * @returns A promise that resolves with whether the dialog was accepted.
 */
function showDialog(options) {
    if (options === void 0) { options = {}; }
    var dialog = new Dialog(options);
    return dialog.launch().then(function (result) {
        dialog.dispose();
        return result;
    });
}
exports.showDialog = showDialog;
/**
 * A modal dialog widget.
 */
var Dialog = (function (_super) {
    __extends(Dialog, _super);
    /**
     * Create a dialog panel instance.
     *
     * @param options - The dialog setup options.
     */
    function Dialog(options) {
        if (options === void 0) { options = {}; }
        var _this = _super.call(this) || this;
        _this.addClass('jp-Dialog');
        options = Private.handleOptions(options);
        var renderer = options.renderer;
        _this._host = options.host;
        _this._defaultButton = options.defaultButton;
        _this._buttons = options.buttons;
        _this._buttonNodes = algorithm_1.toArray(algorithm_1.map(_this._buttons, function (button) {
            return renderer.createButtonNode(button);
        }));
        _this._primary = (options.primaryElement || _this._buttonNodes[_this._defaultButton]);
        var layout = _this.layout = new widgets_1.PanelLayout();
        var content = new widgets_1.Panel();
        content.addClass('jp-Dialog-content');
        layout.addWidget(content);
        var header = renderer.createHeader(options.title);
        var body = renderer.createBody(options.body);
        var footer = renderer.createFooter(_this._buttonNodes);
        content.addWidget(header);
        content.addWidget(body);
        content.addWidget(footer);
        return _this;
    }
    /**
     * Dispose of the resources used by the dialog.
     */
    Dialog.prototype.dispose = function () {
        if (this._promise) {
            var promise = this._promise;
            this._promise = null;
            promise.resolve(void 0);
            algorithm_1.ArrayExt.removeFirstOf(Private.launchQueue, promise.promise);
        }
        _super.prototype.dispose.call(this);
    };
    /**
     * Launch the dialog as a modal window.
     *
     * @returns a promise that resolves with the button that was selected.
     */
    Dialog.prototype.launch = function () {
        var _this = this;
        // Return the existing dialog if already open.
        if (this._promise) {
            return this._promise.promise;
        }
        this._promise = new coreutils_1.PromiseDelegate();
        var promise = Promise.all(Private.launchQueue);
        Private.launchQueue.push(this._promise.promise);
        return promise.then(function () {
            widgets_1.Widget.attach(_this, _this._host);
            return _this._promise.promise;
        });
    };
    /**
     * Resolve the current dialog.
     *
     * @param index - An optional index to the button to resolve.
     *
     * #### Notes
     * Will default to the defaultIndex.
     * Will resolve the current `show()` with the button value.
     * Will be a no-op if the dialog is not shown.
     */
    Dialog.prototype.resolve = function (index) {
        if (!this._promise) {
            return;
        }
        if (index === undefined) {
            index = this._defaultButton;
        }
        this._resolve(this._buttons[index]);
    };
    /**
     * Reject the current dialog with a default reject value.
     *
     * #### Notes
     * Will be a no-op if the dialog is not shown.
     */
    Dialog.prototype.reject = function () {
        if (!this._promise) {
            return;
        }
        this._resolve(Dialog.cancelButton());
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
    Dialog.prototype.handleEvent = function (event) {
        switch (event.type) {
            case 'keydown':
                this._evtKeydown(event);
                break;
            case 'click':
                this._evtClick(event);
                break;
            case 'focus':
                this._evtFocus(event);
                break;
            case 'contextmenu':
                event.preventDefault();
                event.stopPropagation();
                break;
            default:
                break;
        }
    };
    /**
     *  A message handler invoked on a `'before-attach'` message.
     */
    Dialog.prototype.onAfterAttach = function (msg) {
        var node = this.node;
        node.addEventListener('keydown', this, true);
        node.addEventListener('contextmenu', this, true);
        node.addEventListener('click', this, true);
        document.addEventListener('focus', this, true);
        this._first = Private.findFirstFocusable(this.node);
        this._original = document.activeElement;
        this._primary.focus();
    };
    /**
     *  A message handler invoked on a `'after-detach'` message.
     */
    Dialog.prototype.onAfterDetach = function (msg) {
        var node = this.node;
        node.removeEventListener('keydown', this, true);
        node.removeEventListener('contextmenu', this, true);
        node.removeEventListener('click', this, true);
        document.removeEventListener('focus', this, true);
        this._original.focus();
    };
    /**
     * A message handler invoked on a `'close-request'` message.
     */
    Dialog.prototype.onCloseRequest = function (msg) {
        if (this._promise) {
            this.reject();
        }
        _super.prototype.onCloseRequest.call(this, msg);
    };
    /**
     * Handle the `'click'` event for a dialog button.
     *
     * @param event - The DOM event sent to the widget
     */
    Dialog.prototype._evtClick = function (event) {
        var content = this.node.getElementsByClassName('jp-Dialog-content')[0];
        if (!content.contains(event.target)) {
            event.stopPropagation();
            event.preventDefault();
            return;
        }
        for (var _i = 0, _a = this._buttonNodes; _i < _a.length; _i++) {
            var buttonNode = _a[_i];
            if (buttonNode.contains(event.target)) {
                var index = this._buttonNodes.indexOf(buttonNode);
                this.resolve(index);
            }
        }
    };
    /**
     * Handle the `'keydown'` event for the widget.
     *
     * @param event - The DOM event sent to the widget
     */
    Dialog.prototype._evtKeydown = function (event) {
        // Check for escape key
        switch (event.keyCode) {
            case 27:
                event.stopPropagation();
                event.preventDefault();
                this.reject();
                break;
            case 9:
                // Handle a tab on the last button.
                var node = this._buttonNodes[this._buttons.length - 1];
                if (document.activeElement === node && !event.shiftKey) {
                    event.stopPropagation();
                    event.preventDefault();
                    this._first.focus();
                }
                break;
            case 13:
                event.stopPropagation();
                event.preventDefault();
                this.resolve();
                break;
            default:
                break;
        }
    };
    /**
     * Handle the `'focus'` event for the widget.
     *
     * @param event - The DOM event sent to the widget
     */
    Dialog.prototype._evtFocus = function (event) {
        var target = event.target;
        if (!this.node.contains(target)) {
            event.stopPropagation();
            this._buttonNodes[this._defaultButton].focus();
        }
    };
    /**
     * Resolve a button item.
     */
    Dialog.prototype._resolve = function (item) {
        // Prevent loopback.
        var promise = this._promise;
        this._promise = null;
        this.close();
        algorithm_1.ArrayExt.removeFirstOf(Private.launchQueue, promise.promise);
        promise.resolve(item);
    };
    return Dialog;
}(widgets_1.Widget));
exports.Dialog = Dialog;
/**
 * The namespace for Dialog class statics.
 */
(function (Dialog) {
    /**
     * Create an accept button.
     */
    function okButton(options) {
        if (options === void 0) { options = {}; }
        options.accept = true;
        return createButton(options);
    }
    Dialog.okButton = okButton;
    ;
    /**
     * Create a reject button.
     */
    function cancelButton(options) {
        if (options === void 0) { options = {}; }
        options.accept = false;
        return createButton(options);
    }
    Dialog.cancelButton = cancelButton;
    ;
    /**
     * Create a warn button.
     */
    function warnButton(options) {
        if (options === void 0) { options = {}; }
        options.displayType = 'warn';
        return createButton(options);
    }
    Dialog.warnButton = warnButton;
    ;
    /**
     * Create a button item.
     */
    function createButton(value) {
        value.accept = value.accept !== false;
        var defaultLabel = value.accept ? 'OK' : 'CANCEL';
        return {
            label: value.label || defaultLabel,
            icon: value.icon || '',
            caption: value.caption || '',
            className: value.className || '',
            accept: value.accept,
            displayType: value.displayType || 'default'
        };
    }
    Dialog.createButton = createButton;
    /**
     * The default implementation of a dialog renderer.
     */
    var Renderer = (function () {
        function Renderer() {
        }
        /**
         * Create the header of the dialog.
         *
         * @param title - The title of the dialog.
         *
         * @returns A widget for the dialog header.
         */
        Renderer.prototype.createHeader = function (title) {
            var header = new widgets_1.Widget();
            header.addClass('jp-Dialog-header');
            var titleNode = document.createElement('span');
            titleNode.textContent = title;
            titleNode.className = 'jp-Dialog-title';
            header.node.appendChild(titleNode);
            return header;
        };
        /**
         * Create the body of the dialog.
         *
         * @param value - The input value for the body.
         *
         * @returns A widget for the body.
         */
        Renderer.prototype.createBody = function (value) {
            var body;
            if (typeof value === 'string') {
                body = new widgets_1.Widget({ node: document.createElement('span') });
                body.node.textContent = value;
            }
            else if (value instanceof widgets_1.Widget) {
                body = value;
            }
            else {
                body = new widgets_1.Widget({ node: value });
            }
            body.addClass('jp-Dialog-body');
            styling_1.Styling.styleNode(body.node);
            return body;
        };
        /**
         * Create the footer of the dialog.
         *
         * @param buttonNodes - The buttons nodes to add to the footer.
         *
         * @returns A widget for the footer.
         */
        Renderer.prototype.createFooter = function (buttons) {
            var footer = new widgets_1.Widget();
            footer.addClass('jp-Dialog-footer');
            algorithm_1.each(buttons, function (button) {
                footer.node.appendChild(button);
            });
            styling_1.Styling.styleNode(footer.node);
            return footer;
        };
        /**
         * Create a button node for the dialog.
         *
         * @param button - The button data.
         *
         * @returns A node for the button.
         */
        Renderer.prototype.createButtonNode = function (button) {
            var className = this.createItemClass(button);
            // We use realize here instead of creating
            // nodes with document.createElement as a
            // shorthand, and only because this is not
            // called often.
            return virtualdom_1.VirtualDOM.realize(virtualdom_1.h.button({ className: className }, this.renderIcon(button), this.renderLabel(button)));
        };
        /**
         * Create the class name for the button.
         *
         * @param data - The data to use for the class name.
         *
         * @returns The full class name for the button.
         */
        Renderer.prototype.createItemClass = function (data) {
            // Setup the initial class name.
            var name = 'jp-Dialog-button';
            // Add the other state classes.
            if (data.accept) {
                name += ' jp-mod-accept';
            }
            else {
                name += ' jp-mod-reject';
            }
            if (data.displayType === 'warn') {
                name += ' jp-mod-warn';
            }
            // Add the extra class.
            var extra = data.className;
            if (extra) {
                name += " " + extra;
            }
            // Return the complete class name.
            return name;
        };
        /**
         * Render an icon element for a dialog item.
         *
         * @param data - The data to use for rendering the icon.
         *
         * @returns A virtual element representing the icon.
         */
        Renderer.prototype.renderIcon = function (data) {
            return virtualdom_1.h.div({ className: this.createIconClass(data) });
        };
        /**
         * Create the class name for the button icon.
         *
         * @param data - The data to use for the class name.
         *
         * @returns The full class name for the item icon.
         */
        Renderer.prototype.createIconClass = function (data) {
            var name = 'jp-Dialog-buttonIcon';
            var extra = data.icon;
            return extra ? name + " " + extra : name;
        };
        /**
         * Render the label element for a button.
         *
         * @param data - The data to use for rendering the label.
         *
         * @returns A virtual element representing the item label.
         */
        Renderer.prototype.renderLabel = function (data) {
            var className = 'jp-Dialog-buttonLabel';
            var title = data.caption;
            return virtualdom_1.h.div({ className: className, title: title }, data.label);
        };
        return Renderer;
    }());
    Dialog.Renderer = Renderer;
    /**
     * The default renderer instance.
     */
    Dialog.defaultRenderer = new Renderer();
})(Dialog = exports.Dialog || (exports.Dialog = {}));
exports.Dialog = Dialog;
/**
 * The namespace for module private data.
 */
var Private;
(function (Private) {
    /**
     * The queue for launching dialogs.
     */
    Private.launchQueue = [];
    /**
     * Handle the input options for a dialog.
     *
     * @param options - The input options.
     *
     * @returns A new options object with defaults applied.
     */
    function handleOptions(options) {
        var newOptions = {};
        newOptions.title = options.title || '';
        newOptions.body = options.body || '';
        newOptions.host = options.host || document.body;
        newOptions.buttons = (options.buttons || [Dialog.cancelButton(), Dialog.okButton()]);
        newOptions.defaultButton = options.defaultButton || newOptions.buttons.length - 1;
        newOptions.renderer = options.renderer || Dialog.defaultRenderer;
        newOptions.primaryElement = options.primaryElement;
        return newOptions;
    }
    Private.handleOptions = handleOptions;
    /**
     *  Find the first focusable item in the dialog.
     */
    function findFirstFocusable(node) {
        var candidateSelectors = [
            'input',
            'select',
            'a[href]',
            'textarea',
            'button',
            '[tabindex]',
        ].join(',');
        return node.querySelectorAll(candidateSelectors)[0];
    }
    Private.findFirstFocusable = findFirstFocusable;
})(Private || (Private = {}));

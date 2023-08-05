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
var widgets_1 = require("@phosphor/widgets");
/**
 * A phosphor widget which wraps an IFrame.
 */
var IFrameWidget = (function (_super) {
    __extends(IFrameWidget, _super);
    /**
     * Create a new IFrame widget.
     */
    function IFrameWidget() {
        var _this = _super.call(this, { node: Private.createNode() }) || this;
        _this.addClass('jp-IFrameWidget');
        return _this;
    }
    Object.defineProperty(IFrameWidget.prototype, "url", {
        /**
         * The url of the IFrame.
         */
        get: function () {
            return this.node.querySelector('iframe').getAttribute('src');
        },
        set: function (url) {
            this.node.querySelector('iframe').setAttribute('src', url);
        },
        enumerable: true,
        configurable: true
    });
    return IFrameWidget;
}(widgets_1.Widget));
exports.IFrameWidget = IFrameWidget;
/**
 * A namespace for private data.
 */
var Private;
(function (Private) {
    /**
     * Create the main content node of an iframe widget.
     */
    function createNode() {
        var node = document.createElement('div');
        var iframe = document.createElement('iframe');
        iframe.style.height = '100%';
        iframe.style.width = '100%';
        node.appendChild(iframe);
        return node;
    }
    Private.createNode = createNode;
})(Private || (Private = {}));

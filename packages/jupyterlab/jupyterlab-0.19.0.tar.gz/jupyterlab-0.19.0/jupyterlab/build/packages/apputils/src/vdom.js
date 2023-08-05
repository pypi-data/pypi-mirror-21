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
var signaling_1 = require("@phosphor/signaling");
var virtualdom_1 = require("@phosphor/virtualdom");
var widgets_1 = require("@phosphor/widgets");
/**
 * Phosphor widget that encodes best practices for VDOM based rendering.
 */
var VDomWidget = (function (_super) {
    __extends(VDomWidget, _super);
    function VDomWidget() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this._modelChanged = new signaling_1.Signal(_this);
        return _this;
    }
    Object.defineProperty(VDomWidget.prototype, "modelChanged", {
        /**
         * A signal emited when the model changes.
         */
        get: function () {
            return this._modelChanged;
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(VDomWidget.prototype, "model", {
        /**
         * Get the current model.
         */
        get: function () {
            return this._model;
        },
        /**
         * Set the model and fire changed signals.
         */
        set: function (newValue) {
            newValue = newValue || null;
            if (this._model === newValue) {
                return;
            }
            if (this._model) {
                this._model.stateChanged.disconnect(this.update, this);
            }
            this._model = newValue;
            if (this._model) {
                this._model.stateChanged.connect(this.update, this);
            }
            this.update();
            this._modelChanged.emit(void 0);
        },
        enumerable: true,
        configurable: true
    });
    /**
     * Dispose this widget.
     */
    VDomWidget.prototype.dispose = function () {
        this._model = null;
        _super.prototype.dispose.call(this);
    };
    /**
     * Called to update the state of the widget.
     *
     * The default implementation of this method triggers
     * VDOM based rendering by calling the this.render() method.
     */
    VDomWidget.prototype.onUpdateRequest = function (msg) {
        var vnode = this.render();
        virtualdom_1.VirtualDOM.render(vnode, this.node);
    };
    return VDomWidget;
}(widgets_1.Widget));
exports.VDomWidget = VDomWidget;
/**
 * Concrete implementation of VDomWidget model.
 */
var VDomModel = (function () {
    function VDomModel() {
        /**
         * A signal emitted when any model state changes.
         */
        this.stateChanged = new signaling_1.Signal(this);
        this._isDisposed = false;
    }
    Object.defineProperty(VDomModel.prototype, "isDisposed", {
        /**
         * Test whether the model is disposed.
         */
        get: function () {
            return this._isDisposed;
        },
        enumerable: true,
        configurable: true
    });
    /**
     * Dispose the model.
     */
    VDomModel.prototype.dispose = function () {
        if (this.isDisposed) {
            return;
        }
        this._isDisposed = true;
        signaling_1.Signal.clearData(this);
    };
    return VDomModel;
}());
exports.VDomModel = VDomModel;

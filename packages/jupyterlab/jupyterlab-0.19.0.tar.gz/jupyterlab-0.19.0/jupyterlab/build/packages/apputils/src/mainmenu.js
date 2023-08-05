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
var widgets_1 = require("@phosphor/widgets");
/* tslint:disable */
/**
 * The main menu token.
 */
exports.IMainMenu = new coreutils_1.Token('jupyter.services.main-menu');
/**
 * The main menu class.  It is intended to be used as a singleton.
 */
var MainMenu = (function (_super) {
    __extends(MainMenu, _super);
    function MainMenu() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this._items = [];
        return _this;
    }
    /**
     * Add a new menu to the main menu bar.
     */
    MainMenu.prototype.addMenu = function (menu, options) {
        if (options === void 0) { options = {}; }
        if (algorithm_1.ArrayExt.firstIndexOf(this.menus, menu) > -1) {
            return;
        }
        var rank = 'rank' in options ? options.rank : 100;
        var rankItem = { menu: menu, rank: rank };
        var index = algorithm_1.ArrayExt.upperBound(this._items, rankItem, Private.itemCmp);
        // Upon disposal, remove the menu and its rank reference.
        menu.disposed.connect(this._onMenuDisposed, this);
        algorithm_1.ArrayExt.insert(this._items, index, rankItem);
        this.insertMenu(index, menu);
    };
    /**
     * Handle the disposal of a menu.
     */
    MainMenu.prototype._onMenuDisposed = function (menu) {
        this.removeMenu(menu);
        var index = algorithm_1.ArrayExt.findFirstIndex(this._items, function (item) { return item.menu === menu; });
        if (index !== -1) {
            algorithm_1.ArrayExt.removeAt(this._items, index);
        }
    };
    return MainMenu;
}(widgets_1.MenuBar));
exports.MainMenu = MainMenu;
/**
 * A namespace for private data.
 */
var Private;
(function (Private) {
    /**
     * A comparator function for menu rank items.
     */
    function itemCmp(first, second) {
        return first.rank - second.rank;
    }
    Private.itemCmp = itemCmp;
})(Private || (Private = {}));

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
var virtualdom_1 = require("@phosphor/virtualdom");
var apputils_1 = require("@jupyterlab/apputils");
/**
 * The class name added to the landing scroll wrapper.
 */
var LANDING_WRAPPER_CLASS = 'jp-Landing-wrapper';
/**
 * The class name added to the dialog.
 */
var LANDING_DIALOG_CLASS = 'jp-Landing-dialog';
/**
 * The class name for the JupyterLab icon from default-theme.
 */
var JUPYTERLAB_ICON_CLASS = 'jp-ImageJupyterLab';
/**
 * The class name added to specify size of the JupyterLab logo.
 */
var LANDING_LOGO_CLASS = 'jp-Landing-logo';
/**
 * The class name added to the preview message subtitle.
 */
var LANDING_SUBTITLE_CLASS = 'jp-Landing-subtitle';
/**
 * The class name added for the tour icon from default-theme.
 */
var TOUR_ICON_CLASS = 'jp-Landing-tour';
/**
 * The class name added to the header text.
 */
var LANDING_HEADER_CLASS = 'jp-Landing-header';
/**
 * The class name added to the dialog body.
 */
var LANDING_BODY_CLASS = 'jp-Landing-body';
/**
 * The class name added to the column of the dialog.
 */
var LANDING_COLUMN_CLASS = 'jp-Landing-column';
/**
 * The class name added to specify size of activity icons.
 */
var LANDING_ICON_CLASS = 'jp-Landing-image';
/**
 * The class name added to the image text of an activity.
 */
var LANDING_TEXT_CLASS = 'jp-Landing-text';
/**
 * The class name added to the current working directory.
 */
var LANDING_CWD_CLASS = 'jp-Landing-cwd';
/**
 * The class name added to Landing folder node.
 */
var FOLDER_CLASS = 'jp-Landing-folder';
/**
 * The class name added for the folder icon from default-theme.
 */
var FOLDER_ICON_CLASS = 'jp-FolderIcon';
/**
 * The class name added to the current working directory path.
 */
var LANDING_PATH_CLASS = 'jp-Landing-path';
/**
 * The list of preview messages.
 */
var previewMessages = [
    'super alpha preview',
    'very alpha preview',
    'extremely alpha preview',
    'exceedingly alpha preview',
    'alpha alpha preview'
];
/**
 * LandingModel keeps track of the path to working directory and has text data,
 * which the LandingWidget will render.
 */
var LandingModel = (function (_super) {
    __extends(LandingModel, _super);
    /**
     * Construct a new landing model.
     */
    function LandingModel(terminalsAvailable) {
        if (terminalsAvailable === void 0) { terminalsAvailable = false; }
        var _this = _super.call(this) || this;
        _this.previewMessage = previewMessages[Math.floor(Math.random() * previewMessages.length)];
        _this.headerText = 'Start a new activity';
        _this.activities =
            [['Notebook', 'file-operations:new-notebook'],
                ['Code Console', 'console:create'],
                ['Text Editor', 'file-operations:new-text-file']];
        if (terminalsAvailable) {
            _this.activities.push(['Terminal', 'terminal:create-new']);
        }
        _this._path = 'home';
        return _this;
    }
    Object.defineProperty(LandingModel.prototype, "path", {
        /**
         * Get the path of the current working directory.
         */
        get: function () {
            return this._path;
        },
        /**
         * Set the path of the current working directory.
         */
        set: function (value) {
            this._path = value;
            this.stateChanged.emit(void 0);
        },
        enumerable: true,
        configurable: true
    });
    return LandingModel;
}(apputils_1.VDomModel));
exports.LandingModel = LandingModel;
/**
 * A virtual-DOM-based widget for the Landing plugin.
 */
var LandingWidget = (function (_super) {
    __extends(LandingWidget, _super);
    /**
     * Construct a new landing widget.
     */
    function LandingWidget(app) {
        var _this = _super.call(this) || this;
        _this._app = app;
        return _this;
    }
    /**
     * Handle `'activate-request'` messages.
     */
    LandingWidget.prototype.onActivateRequest = function (msg) {
        this.node.tabIndex = -1;
        this.node.focus();
    };
    /**
     * Handle `'close-request'` messages.
     */
    LandingWidget.prototype.onCloseRequest = function (msg) {
        _super.prototype.onCloseRequest.call(this, msg);
        this.dispose();
    };
    /**
     * Render the landing plugin to virtual DOM nodes.
     */
    LandingWidget.prototype.render = function () {
        var _this = this;
        var activitiesList = [];
        var activites = this.model.activities;
        var _loop_1 = function (activityName) {
            var imgName = activityName[0].replace(' ', '');
            var column = virtualdom_1.h.div({ className: LANDING_COLUMN_CLASS }, virtualdom_1.h.span({ className: LANDING_ICON_CLASS + (" jp-Image" + imgName),
                onclick: function () {
                    _this._app.commands.execute(activityName[1], void 0);
                } }), virtualdom_1.h.span({ className: LANDING_TEXT_CLASS }, activityName[0]));
            activitiesList.push(column);
        };
        for (var _i = 0, activites_1 = activites; _i < activites_1.length; _i++) {
            var activityName = activites_1[_i];
            _loop_1(activityName);
        }
        var logo = virtualdom_1.h.span({ className: JUPYTERLAB_ICON_CLASS + ' ' + LANDING_LOGO_CLASS });
        var subtitle = virtualdom_1.h.span({ className: LANDING_SUBTITLE_CLASS }, this.model.previewMessage);
        var tour = virtualdom_1.h.span({ className: TOUR_ICON_CLASS,
            onclick: function () {
                _this._app.commands.execute('about-jupyterlab:open', void 0);
            } });
        var header = virtualdom_1.h.span({
            className: LANDING_HEADER_CLASS
        }, this.model.headerText);
        var body = virtualdom_1.h.div({ className: LANDING_BODY_CLASS }, activitiesList);
        var dialog = virtualdom_1.h.div({ className: LANDING_DIALOG_CLASS }, logo, subtitle, tour, header, body, virtualdom_1.h.div({ className: LANDING_CWD_CLASS }, virtualdom_1.h.span({ className: FOLDER_ICON_CLASS + ' ' + FOLDER_CLASS }), virtualdom_1.h.span({ className: LANDING_PATH_CLASS }, this.model.path)));
        return virtualdom_1.h.div({ className: LANDING_WRAPPER_CLASS }, dialog);
    };
    return LandingWidget;
}(apputils_1.VDomWidget));
exports.LandingWidget = LandingWidget;

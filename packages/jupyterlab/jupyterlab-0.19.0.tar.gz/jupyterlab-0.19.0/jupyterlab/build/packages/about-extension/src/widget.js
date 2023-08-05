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
 * The class name added to each page in the About plugin.
 */
var SECTION_CLASS = 'jp-About-section';
/**
 * The class name added to center content.
 */
var SECTION_CENTER_CLASS = 'jp-About-sectioncenter';
/**
 * The class name added to group elements on the initial page.
 */
var CONTAINER_CLASS = 'jp-About-container';
/**
 * The class name added to elements in a row.
 */
var ROW_CLASS = 'jp-About-row';
/**
 * The class name added to elements in a column.
 */
var COLUMN_CLASS = 'jp-About-column';
/**
 * The class name used specify postion of elements.
 */
var HALF_CLASS = 'jp-About-one-half';
/**
 * The class name added to the About plugin description on the intial page.
 */
var DESC_ONE_CLASS = 'jp-About-desc-one';
/**
 * The class name added to other plugin descriptions on the intial page.
 */
var DESC_TWO_CLASS = 'jp-About-desc-two';
/**
 * The class name added to headers of other plugins on the intial page.
 */
var DESC_TWO_HEADER_CLASS = 'jp-About-desc-two-header';
/**
 * The class name added to headers.
 */
var HEADER_CLASS = 'jp-About-header';
/**
 * The class name added to plugin pages.
 */
var CONTENT_CLASS = 'jp-About-content';
/**
 * The class name added to descriptions on plugin pages.
 */
var CONTENT_DESC_CLASS = 'jp-About-content-desc';
/**
 * The class name added to the navigation down button.
 */
var NAV_CLASS = 'jp-About-nav-button';
/**
 * The class name added to all images and icons.
 */
var IMAGE_CLASS = 'jp-img';
/**
 * The class name added to the JupyterLab logo.
 */
var LOGO_CLASS = 'jp-About-logo';
/**
 * The class name added to the main area icon.
 */
var MAIN_AREA_ICON_CLASS = 'jp-About-hero-mainarea';
/**
 * The class name added the command palette icon.
 */
var COMMAND_ICON_CLASS = 'jp-About-hero-command';
/**
 * The class name added to the filebrowser icon.
 */
var FILEBROWSER_ICON_CLASS = 'jp-About-hero-filebrowser';
/**
 * The class name added for the notebook icon.
 */
var NOTEBOOK_ICON_CLASS = 'jp-About-hero-notebook';
/**
 * The class name added to the main area image.
 */
var MAIN_AREA_IMAGE_CLASS = 'jp-About-mainarea';
/**
 * The class name added to the command palette image.
 */
var COMMAND_IMAGE_CLASS = 'jp-About-command';
/**
 * The class name added to the filebrowser image.
 */
var FILEBROWSER_IMAGE_CLASS = 'jp-About-fb';
/**
 * The class name added to the notebook image.
 */
var NOTEBOOK_IMAGE_CLASS = 'jp-About-nb';
/**
 * Title of About page.
 */
var TITLE = 'Welcome to the JupyterLab alpha preview';
/**
 * Text on the first page that gives a high level overview of JupyterLab.
 */
var HEADER_TEXT = [
    'Click on the Launcher tab for the initial JupyterLab screen.',
    'This demo gives an alpha developer preview of the JupyterLab environment.',
    'It is not ready for general usage yet.',
    'We are developing JupyterLab at ',
    'https://github.com/jupyterlab/jupyterlab',
    '. Pull requests and feedback are welcome!',
    "Here is a brief description of some of the things you'll find in this demo."
];
/**
 * Contains the plugin names.
 */
var PLUGIN_HEADERS = [
    'Main Area',
    'Command Palette',
    'File Browser',
    'Notebook'
];
/**
 * Description of the main area and its functionality.
 */
var MAIN_AREA_DESC = [
    'Open tabs and drag and drop them to rearrange them.',
    "The main area is divided into panels of tabs. Drag a tab around the area\n   to split the main area in different ways. Drag a tab to the center of a\n   panel to move a tab without splitting the panel (in this case, the whole\n   panel will highlight instead of just a portion).",
    "Resize panels by dragging their borders (be aware that panels and sidebars\n   also have a minimum width). A file that contains changes to be saved has\n   a circle for a close icon."
];
/**
 * Description of the file browser and its functionality.
 */
var FILE_BROWSER_DESC = [
    'Navigate and organize your files.',
    "Clicking the \"Files\" tab, located on the left, will toggle the file browser.\n   Navigate into directories by double-clicking, and use the breadcrumbs at the\n   top to navigate out. Create a new file/directory by clicking the plus icon at\n   the top. Click the middle icon to upload files, and click the last icon to\n   reload the file listing. Drag and drop files to move them to subdirectories.\n   Click on a selected file to rename it. Sort the list by clicking on a column\n   header.\n   Open a file by double-clicking it or dragging it into the main area.\n   Opening an image displays the image. Opening a code file opens a code editor.\n   Opening a notebook opens a very preliminary notebook component."
];
/**
 * Description of the command palette and its functionality.
 */
var COMMAND_PALETTE_DESC = [
    'View list of commands and keyboard shortcuts.',
    "Clicking the \"Commands\" tab, located on the left, will toggle the command\n   palette. Execute a command by clicking, or navigating with your arrow keys\n   and pressing Enter. Filter commands by typing in the text box at the top of\n   the palette. The palette is organized into categories, and you can filter on\n   a single category by clicking on the category header or by typing the header\n   surrounded by colons in the search input (e.g., :file:).",
    'You can try these things from the command palette:',
    'Open a new terminal (requires macOS or Linux)',
    'Open an IPython console',
    'Open a new file',
    'Save a file',
    'Open a help panel on the right'
];
/**
 * Description of the notebook and its functionality.
 */
var NOTEBOOK_DESC = [
    'Dedicate a tab to running a class notebook.',
    "Opening a notebook will open a minimally-featured notebook.\n   Code execution, Markdown rendering, and basic cell toolbar actions are\n   supported.\n   Future versions will add more features from the existing Jupyter notebook."
];
/**
 * AboutModel holds data which the AboutWidgetwill render.
 */
var AboutModel = (function (_super) {
    __extends(AboutModel, _super);
    /**
     * Create an about model.
     */
    function AboutModel(options) {
        var _this = _super.call(this) || this;
        /**
         * Title of About page.
         */
        _this.title = TITLE;
        /**
         * Text on the first page that gives a high level overview of JupyterLab.
         */
        _this.headerText = HEADER_TEXT;
        /**
         * Contains the plugin names.
         */
        _this.pluginHeaders = PLUGIN_HEADERS;
        /**
         * Description of the main area and its functionality.
         */
        _this.mainAreaDesc = MAIN_AREA_DESC;
        /**
         * Description of the file browser and its functionality.
         */
        _this.filebrowserDesc = FILE_BROWSER_DESC;
        /**
         * Description of the command palette and its functionality.
         */
        _this.commandPaletteDesc = COMMAND_PALETTE_DESC;
        /**
         * Description of the notebook and its functionality.
         */
        _this.notebookDesc = NOTEBOOK_DESC;
        _this.version = options.version;
        return _this;
    }
    return AboutModel;
}(apputils_1.VDomModel));
exports.AboutModel = AboutModel;
/**
 * A virtual-DOM-based widget for the About plugin.
 */
var AboutWidget = (function (_super) {
    __extends(AboutWidget, _super);
    function AboutWidget() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    /**
     * Handle `'activate-request'` messages.
     */
    AboutWidget.prototype.onActivateRequest = function (msg) {
        this.node.tabIndex = -1;
        this.node.focus();
    };
    /**
     * Handle `'close-request'` messages.
     */
    AboutWidget.prototype.onCloseRequest = function (msg) {
        _super.prototype.onCloseRequest.call(this, msg);
        this.dispose();
    };
    /**
     * Render the about plugin to virtual DOM nodes.
     */
    AboutWidget.prototype.render = function () {
        var title = this.model.title;
        var version = "v" + this.model.version;
        var headerText = this.model.headerText;
        var pluginHeaders = this.model.pluginHeaders;
        var mainAreaDesc = this.model.mainAreaDesc;
        var filebrowserDesc = this.model.filebrowserDesc;
        var commandPaletteDesc = this.model.commandPaletteDesc;
        var notebookDesc = this.model.notebookDesc;
        var headerRow = virtualdom_1.h.div({ className: ROW_CLASS }, virtualdom_1.h.div({ className: COLUMN_CLASS }, virtualdom_1.h.span({ className: IMAGE_CLASS + ' ' + LOGO_CLASS }), virtualdom_1.h.p({ className: HEADER_CLASS }, title, virtualdom_1.h.span(' (', virtualdom_1.h.code(version), ')')), virtualdom_1.h.div({ className: DESC_ONE_CLASS }, virtualdom_1.h.p(headerText[0]), virtualdom_1.h.p(headerText[1], ' ', virtualdom_1.h.strong(headerText[2])), virtualdom_1.h.p(headerText[3], virtualdom_1.h.a({ href: headerText[4], target: '_blank' }, headerText[4]), headerText[5]), virtualdom_1.h.p(headerText[6]))));
        var mainAreaCommandPaletteRow = virtualdom_1.h.div({ className: ROW_CLASS }, virtualdom_1.h.div({ className: HALF_CLASS + ' ' + COLUMN_CLASS }, virtualdom_1.h.p({ className: DESC_TWO_HEADER_CLASS }, virtualdom_1.h.a({ href: '#about-main-area' }, virtualdom_1.h.span({ className: IMAGE_CLASS + ' ' + MAIN_AREA_ICON_CLASS }), pluginHeaders[0])), virtualdom_1.h.p({ className: DESC_TWO_CLASS }, mainAreaDesc[0])), virtualdom_1.h.div({ className: HALF_CLASS + ' ' + COLUMN_CLASS }, virtualdom_1.h.p({ className: DESC_TWO_HEADER_CLASS }, virtualdom_1.h.a({ href: '#about-command' }, virtualdom_1.h.span({ className: IMAGE_CLASS + ' ' + COMMAND_ICON_CLASS }), pluginHeaders[1])), virtualdom_1.h.p({ className: DESC_TWO_CLASS }, commandPaletteDesc[0])));
        var filebrowserNotebookRow = virtualdom_1.h.div({ className: ROW_CLASS }, virtualdom_1.h.div({ className: HALF_CLASS + ' ' + COLUMN_CLASS }, virtualdom_1.h.p({ className: DESC_TWO_HEADER_CLASS }, virtualdom_1.h.a({ href: '#about-filebrowser' }, virtualdom_1.h.span({ className: IMAGE_CLASS + ' ' + FILEBROWSER_ICON_CLASS }), pluginHeaders[2])), virtualdom_1.h.p({ className: DESC_TWO_CLASS }, filebrowserDesc[0])), virtualdom_1.h.div({ className: HALF_CLASS + ' ' + COLUMN_CLASS }, virtualdom_1.h.p({ className: DESC_TWO_HEADER_CLASS }, virtualdom_1.h.a({ href: '#about-notebook' }, virtualdom_1.h.span({ className: IMAGE_CLASS + ' ' + NOTEBOOK_ICON_CLASS }), pluginHeaders[3])), virtualdom_1.h.p({ className: DESC_TWO_CLASS }, notebookDesc[0])));
        var mainAreaPage = virtualdom_1.h.div({ className: SECTION_CLASS }, virtualdom_1.h.a({ id: 'about-main-area' }), virtualdom_1.h.div({ className: SECTION_CENTER_CLASS }, virtualdom_1.h.p({ className: HEADER_CLASS + ' ' + CONTENT_CLASS }, virtualdom_1.h.span({ className: IMAGE_CLASS + ' ' + MAIN_AREA_ICON_CLASS }), pluginHeaders[0]), virtualdom_1.h.span({ className: IMAGE_CLASS + ' ' + MAIN_AREA_IMAGE_CLASS }), virtualdom_1.h.p({ className: CONTENT_DESC_CLASS }, mainAreaDesc[1]), virtualdom_1.h.p({ className: CONTENT_DESC_CLASS }, mainAreaDesc[2]), virtualdom_1.h.a({ href: '#about-command' }, virtualdom_1.h.span({ className: NAV_CLASS }))));
        var commandPalettePage = virtualdom_1.h.div({ className: SECTION_CLASS }, virtualdom_1.h.a({ id: 'about-command' }), virtualdom_1.h.div({ className: SECTION_CENTER_CLASS }, virtualdom_1.h.p({ className: HEADER_CLASS + ' ' + CONTENT_CLASS }, virtualdom_1.h.span({ className: IMAGE_CLASS + ' ' + COMMAND_ICON_CLASS }), pluginHeaders[1]), virtualdom_1.h.span({ className: IMAGE_CLASS + ' ' + COMMAND_IMAGE_CLASS }), virtualdom_1.h.p({ className: CONTENT_DESC_CLASS }, commandPaletteDesc[1]), virtualdom_1.h.div({ className: CONTENT_DESC_CLASS }, virtualdom_1.h.p(commandPaletteDesc[2]), virtualdom_1.h.ul(virtualdom_1.h.li(commandPaletteDesc[3]), virtualdom_1.h.li(commandPaletteDesc[4]), virtualdom_1.h.li(commandPaletteDesc[5]), virtualdom_1.h.li(commandPaletteDesc[6]), virtualdom_1.h.li(commandPaletteDesc[7]))), virtualdom_1.h.a({ href: '#about-filebrowser' }, virtualdom_1.h.span({ className: NAV_CLASS }))));
        var filebrowserPage = virtualdom_1.h.div({ className: SECTION_CLASS }, virtualdom_1.h.a({ id: 'about-filebrowser' }), virtualdom_1.h.div({ className: SECTION_CENTER_CLASS }, virtualdom_1.h.p({ className: HEADER_CLASS + ' ' + CONTENT_CLASS }, virtualdom_1.h.span({ className: IMAGE_CLASS + ' ' + FILEBROWSER_ICON_CLASS }), pluginHeaders[2]), virtualdom_1.h.span({ className: IMAGE_CLASS + ' ' + FILEBROWSER_IMAGE_CLASS }), virtualdom_1.h.p({ className: CONTENT_DESC_CLASS }, filebrowserDesc[1]), virtualdom_1.h.a({ href: '#about-notebook' }, virtualdom_1.h.span({ className: NAV_CLASS }))));
        var notebookPage = virtualdom_1.h.div({ className: SECTION_CLASS }, virtualdom_1.h.a({ id: 'about-notebook' }), virtualdom_1.h.div({ className: SECTION_CENTER_CLASS }, virtualdom_1.h.p({ className: HEADER_CLASS + ' ' + CONTENT_CLASS }, virtualdom_1.h.span({ className: IMAGE_CLASS + ' ' + NOTEBOOK_ICON_CLASS }), pluginHeaders[3]), virtualdom_1.h.span({ className: IMAGE_CLASS + ' ' + NOTEBOOK_IMAGE_CLASS }), virtualdom_1.h.p({ className: CONTENT_DESC_CLASS }, notebookDesc[1])));
        return virtualdom_1.h.div({ id: 'about' }, virtualdom_1.h.div({ className: SECTION_CLASS }, virtualdom_1.h.div({ className: SECTION_CENTER_CLASS }, virtualdom_1.h.div({ className: CONTAINER_CLASS }, headerRow, mainAreaCommandPaletteRow, filebrowserNotebookRow), virtualdom_1.h.a({ href: '#about-main-area' }, virtualdom_1.h.span({ className: NAV_CLASS })))), mainAreaPage, commandPalettePage, filebrowserPage, notebookPage);
    };
    return AboutWidget;
}(apputils_1.VDomWidget));
exports.AboutWidget = AboutWidget;

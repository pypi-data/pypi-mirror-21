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
var services_1 = require("@jupyterlab/services");
var widgets_1 = require("@phosphor/widgets");
var apputils_1 = require("@jupyterlab/apputils");
var coreutils_1 = require("@jupyterlab/coreutils");
/**
 * The command IDs used by the help plugin.
 */
var CommandIDs;
(function (CommandIDs) {
    CommandIDs.open = 'help-jupyterlab:open';
    CommandIDs.activate = 'help-jupyterlab:activate';
    CommandIDs.close = 'help-jupyterlab:close';
    CommandIDs.show = 'help-jupyterlab:show';
    CommandIDs.hide = 'help-jupyterlab:hide';
    CommandIDs.toggle = 'help-jupyterlab:toggle';
    CommandIDs.launchClassic = 'classic-notebook:launchClassic';
})(CommandIDs || (CommandIDs = {}));
;
/**
 * A flag denoting whether the application is loaded over HTTPS.
 */
var LAB_IS_SECURE = window.location.protocol === 'https:';
/**
 * The class name added to the help widget.
 */
var HELP_CLASS = 'jp-Help';
/**
 * A list of help resources.
 */
var RESOURCES = [
    {
        text: 'Scipy Lecture Notes',
        url: 'http://www.scipy-lectures.org/'
    },
    {
        text: 'Numpy Reference',
        url: 'https://docs.scipy.org/doc/numpy/reference/'
    },
    {
        text: 'Scipy Reference',
        url: 'https://docs.scipy.org/doc/scipy/reference/'
    },
    {
        text: 'Notebook Tutorial',
        url: 'https://nbviewer.jupyter.org/github/jupyter/notebook/' +
            'blob/master/docs/source/examples/Notebook/Notebook Basics.ipynb'
    },
    {
        text: 'Python Reference',
        url: 'https://docs.python.org/3.5/'
    },
    {
        text: 'IPython Reference',
        url: 'https://ipython.org/documentation.html?v=20160707164940'
    },
    {
        text: 'Matplotlib Reference',
        url: 'http://matplotlib.org/contents.html?v=20160707164940'
    },
    {
        text: 'SymPy Reference',
        url: 'http://docs.sympy.org/latest/index.html?v=20160707164940'
    },
    {
        text: 'Pandas Reference',
        url: 'http://pandas.pydata.org/pandas-docs/stable/?v=20160707164940'
    },
    {
        text: 'Markdown Reference',
        url: 'https://help.github.com/articles/' +
            'getting-started-with-writing-and-formatting-on-github/'
    }
];
RESOURCES.sort(function (a, b) {
    return a.text.localeCompare(b.text);
});
/**
 * The help handler extension.
 */
var plugin = {
    activate: activate,
    id: 'jupyter.extensions.help-handler',
    requires: [apputils_1.IMainMenu, apputils_1.ICommandPalette, apputils_1.ILayoutRestorer],
    autoStart: true
};
/**
 * Export the plugin as default.
 */
exports.default = plugin;
/*
  * An IFrameWidget the disposes itself when closed.
  *
  * This is needed to clear the state restoration db when IFrames are closed.
 */
var ClosableIFrame = (function (_super) {
    __extends(ClosableIFrame, _super);
    function ClosableIFrame() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    /**
     * Dispose of the IFrameWidget when closing.
     */
    ClosableIFrame.prototype.onCloseRequest = function (msg) {
        this.dispose();
    };
    return ClosableIFrame;
}(apputils_1.IFrameWidget));
/**
 * Activate the help handler extension.
 *
 * @param app - The phosphide application object.
 *
 * returns A promise that resolves when the extension is activated.
 */
function activate(app, mainMenu, palette, restorer) {
    var counter = 0;
    var category = 'Help';
    var namespace = 'help-doc';
    var command = CommandIDs.open;
    var menu = createMenu();
    var commands = app.commands, shell = app.shell;
    var tracker = new apputils_1.InstanceTracker({ namespace: namespace, shell: shell });
    // Handle state restoration.
    restorer.restore(tracker, {
        command: command,
        args: function (widget) { return ({ url: widget.url, text: widget.title.label }); },
        name: function (widget) { return widget.url; }
    });
    /**
     * Create a new ClosableIFrame widget.
     */
    function newClosableIFrame(url, text) {
        var iframe = new ClosableIFrame();
        iframe.addClass(HELP_CLASS);
        iframe.title.label = text;
        iframe.title.closable = true;
        iframe.id = namespace + "-" + ++counter;
        iframe.url = url;
        tracker.add(iframe);
        return iframe;
    }
    /**
     * Create a menu for the help plugin.
     */
    function createMenu() {
        var commands = app.commands;
        var menu = new widgets_1.Menu({ commands: commands });
        menu.title.label = category;
        menu.addItem({ command: 'about-jupyterlab:open' });
        menu.addItem({ command: 'faq-jupyterlab:open' });
        menu.addItem({ command: CommandIDs.launchClassic });
        menu.addItem({ type: 'separator' });
        RESOURCES.forEach(function (args) { menu.addItem({ args: args, command: command }); });
        menu.addItem({ type: 'separator' });
        menu.addItem({ command: 'statedb:clear' });
        return menu;
    }
    commands.addCommand(command, {
        label: function (args) { return args['text']; },
        execute: function (args) {
            var url = args['url'];
            var text = args['text'];
            // If help resource will generate a mixed content error, load externally.
            if (LAB_IS_SECURE && coreutils_1.URLExt.parse(url).protocol !== 'https:') {
                window.open(url);
                return;
            }
            var iframe = newClosableIFrame(url, text);
            shell.addToMainArea(iframe);
            tracker.activate(iframe);
        }
    });
    commands.addCommand(CommandIDs.launchClassic, {
        label: 'Launch Classic Notebook',
        execute: function () { window.open(services_1.utils.getBaseUrl() + 'tree'); }
    });
    RESOURCES.forEach(function (args) { palette.addItem({ args: args, command: command, category: category }); });
    palette.addItem({ command: 'statedb:clear', category: category });
    palette.addItem({ command: CommandIDs.launchClassic, category: category });
    mainMenu.addMenu(menu);
}

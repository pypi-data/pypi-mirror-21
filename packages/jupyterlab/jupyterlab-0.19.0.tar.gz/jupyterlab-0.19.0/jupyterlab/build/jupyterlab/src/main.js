// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
require("es6-promise/auto"); // polyfill Promise on IE
var application_1 = require("@jupyterlab/application");
var aboutExtension = require("@jupyterlab/about-extension");
var applicationExtension = require("@jupyterlab/application-extension");
var apputilsExtension = require("@jupyterlab/apputils-extension");
var codemirrorExtension = require("@jupyterlab/codemirror-extension");
var completerExtension = require("@jupyterlab/completer-extension");
var consoleExtension = require("@jupyterlab/console-extension");
var csvwidgetExtension = require("@jupyterlab/csvwidget-extension");
var docmanagerExtension = require("@jupyterlab/docmanager-extension");
var docregistryExtension = require("@jupyterlab/docregistry-extension");
var editorwidgetExtension = require("@jupyterlab/editorwidget-extension");
var faqExtension = require("@jupyterlab/faq-extension");
var filebrowserExtension = require("@jupyterlab/filebrowser-extension");
var helpExtension = require("@jupyterlab/help-extension");
var imagewidgetExtension = require("@jupyterlab/imagewidget-extension");
var inspectorExtension = require("@jupyterlab/inspector-extension");
var landingExtension = require("@jupyterlab/landing-extension");
var launchExtension = require("@jupyterlab/launcher-extension");
var markdownwidgetExtension = require("@jupyterlab/markdownwidget-extension");
var notebookExtension = require("@jupyterlab/notebook-extension");
var rendermimeExtension = require("@jupyterlab/rendermime-extension");
var runningExtension = require("@jupyterlab/running-extension");
var servicesExtension = require("@jupyterlab/services-extension");
var shortcutsExtension = require("@jupyterlab/shortcuts-extension");
var terminalExtension = require("@jupyterlab/terminal-extension");
var tooltipExtension = require("@jupyterlab/tooltip-extension");
require("font-awesome/css/font-awesome.min.css");
require("@jupyterlab/default-theme/style/index.css");
var mods = [
    aboutExtension,
    applicationExtension,
    apputilsExtension,
    codemirrorExtension,
    completerExtension,
    consoleExtension,
    csvwidgetExtension,
    docmanagerExtension,
    docregistryExtension,
    editorwidgetExtension,
    faqExtension,
    filebrowserExtension,
    helpExtension,
    imagewidgetExtension,
    inspectorExtension,
    landingExtension,
    launchExtension,
    markdownwidgetExtension,
    notebookExtension,
    rendermimeExtension,
    runningExtension,
    servicesExtension,
    shortcutsExtension,
    terminalExtension,
    tooltipExtension,
];
/**
 * Create an application object.
 *
 * @param loader - The module loader for the application.
 *
 * @returns A new application object.
 */
function createLab(loader) {
    var lab = new application_1.JupyterLab({
        loader: loader,
        gitDescription: process.env.GIT_DESCRIPTION,
        namespace: 'jupyterlab',
        version: process.env.JUPYTERLAB_VERSION
    });
    lab.registerPluginModules(mods);
    return lab;
}
exports.createLab = createLab;

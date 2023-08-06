require('es6-promise/auto');  // polyfill Promise on IE'
require('font-awesome/css/font-awesome.min.css');
require('@jupyterlab/default-theme/style/index.css');

var app = require('@jupyterlab/application').JupyterLab;
var utils = require('@jupyterlab/services').utils;


function main() {
    lab = new app({
        gitDescription: process.env.GIT_DESCRIPTION,
        namespace: 'jupyterlab',
        version: process.env.JUPYTERLAB_VERSION
    });
    try {
        lab.registerPluginModule(require('@jupyterlab/about-extension'));
    } catch (e) {
        console.error(e);
    }
    try {
        lab.registerPluginModule(require('@jupyterlab/application-extension'));
    } catch (e) {
        console.error(e);
    }
    try {
        lab.registerPluginModule(require('@jupyterlab/apputils-extension'));
    } catch (e) {
        console.error(e);
    }
    try {
        lab.registerPluginModule(require('@jupyterlab/codemirror-extension'));
    } catch (e) {
        console.error(e);
    }
    try {
        lab.registerPluginModule(require('@jupyterlab/completer-extension'));
    } catch (e) {
        console.error(e);
    }
    try {
        lab.registerPluginModule(require('@jupyterlab/console-extension'));
    } catch (e) {
        console.error(e);
    }
    try {
        lab.registerPluginModule(require('@jupyterlab/csvwidget-extension'));
    } catch (e) {
        console.error(e);
    }
    try {
        lab.registerPluginModule(require('@jupyterlab/docmanager-extension'));
    } catch (e) {
        console.error(e);
    }
    try {
        lab.registerPluginModule(require('@jupyterlab/docregistry-extension'));
    } catch (e) {
        console.error(e);
    }
    try {
        lab.registerPluginModule(require('@jupyterlab/editorwidget-extension'));
    } catch (e) {
        console.error(e);
    }
    try {
        lab.registerPluginModule(require('@jupyterlab/faq-extension'));
    } catch (e) {
        console.error(e);
    }
    try {
        lab.registerPluginModule(require('@jupyterlab/filebrowser-extension'));
    } catch (e) {
        console.error(e);
    }
    try {
        lab.registerPluginModule(require('@jupyterlab/help-extension'));
    } catch (e) {
        console.error(e);
    }
    try {
        lab.registerPluginModule(require('@jupyterlab/imagewidget-extension'));
    } catch (e) {
        console.error(e);
    }
    try {
        lab.registerPluginModule(require('@jupyterlab/inspector-extension'));
    } catch (e) {
        console.error(e);
    }
    try {
        lab.registerPluginModule(require('@jupyterlab/landing-extension'));
    } catch (e) {
        console.error(e);
    }
    try {
        lab.registerPluginModule(require('@jupyterlab/launcher-extension'));
    } catch (e) {
        console.error(e);
    }
    try {
        lab.registerPluginModule(require('@jupyterlab/markdownwidget-extension'));
    } catch (e) {
        console.error(e);
    }
    try {
        lab.registerPluginModule(require('@jupyterlab/notebook-extension'));
    } catch (e) {
        console.error(e);
    }
    try {
        lab.registerPluginModule(require('@jupyterlab/rendermime-extension'));
    } catch (e) {
        console.error(e);
    }
    try {
        lab.registerPluginModule(require('@jupyterlab/running-extension'));
    } catch (e) {
        console.error(e);
    }
    try {
        lab.registerPluginModule(require('@jupyterlab/services-extension'));
    } catch (e) {
        console.error(e);
    }
    try {
        lab.registerPluginModule(require('@jupyterlab/shortcuts-extension'));
    } catch (e) {
        console.error(e);
    }
    try {
        lab.registerPluginModule(require('@jupyterlab/tabmanager-extension'));
    } catch (e) {
        console.error(e);
    }
    try {
        lab.registerPluginModule(require('@jupyterlab/terminal-extension'));
    } catch (e) {
        console.error(e);
    }
    try {
        lab.registerPluginModule(require('@jupyterlab/tooltip-extension'));
    } catch (e) {
        console.error(e);
    }
    var ignorePlugins = [];
    try {
        var option = utils.getConfigOption('ignorePlugins');
        ignorePlugins = JSON.parse(option);
    } catch (e) {
        console.error("Invalid ignorePlugins config:", option);
    }
    lab.start({ "ignorePlugins": ignorePlugins });
}

window.onload = main;

// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
"use strict";
function __export(m) {
    for (var p in m) if (!exports.hasOwnProperty(p)) exports[p] = m[p];
}
Object.defineProperty(exports, "__esModule", { value: true });
var coreutils_1 = require("@phosphor/coreutils");
__export(require("./widget"));
/* tslint:disable */
/**
 * The editor tracker token.
 */
exports.IImageTracker = new coreutils_1.Token('jupyter.services.image-tracker');
/* tslint:enable */
/**
 * Add the default commands for the image widget.
 */
function addDefaultCommands(tracker, commands) {
    commands.addCommand('imagewidget:zoom-in', {
        execute: zoomIn,
        label: 'Zoom In'
    });
    commands.addCommand('imagewidget:zoom-out', {
        execute: zoomOut,
        label: 'Zoom Out'
    });
    commands.addCommand('imagewidget:reset-zoom', {
        execute: resetZoom,
        label: 'Reset Zoom'
    });
    function zoomIn() {
        var widget = tracker.currentWidget;
        if (!widget) {
            return;
        }
        if (widget.scale > 1) {
            widget.scale += .5;
        }
        else {
            widget.scale *= 2;
        }
    }
    function zoomOut() {
        var widget = tracker.currentWidget;
        if (!widget) {
            return;
        }
        if (widget.scale > 1) {
            widget.scale -= .5;
        }
        else {
            widget.scale /= 2;
        }
    }
    function resetZoom() {
        var widget = tracker.currentWidget;
        if (!widget) {
            return;
        }
        widget.scale = 1;
    }
}
exports.addDefaultCommands = addDefaultCommands;

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
 * The tooltip manager token.
 */
exports.ITooltipManager = new coreutils_1.Token('jupyter.services.tooltip');

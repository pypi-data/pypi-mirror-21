// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
/**
 * The class name added to all hover boxes.
 */
var HOVERBOX_CLASS = 'jp-HoverBox';
/**
 * The class name added to a hovering node that is scrolled out of view.
 */
var OUTOFVIEW_CLASS = 'jp-mod-outofview';
/**
 * A namespace for `HoverBox` members.
 */
var HoverBox;
(function (HoverBox) {
    /**
     * Set the visible dimensions of a hovering box anchored to an editor cursor.
     *
     * @param options - The hover box geometry calculation options.
     */
    function setGeometry(options) {
        var anchor = options.anchor, host = options.host, node = options.node;
        // Add hover box class if it does not exist.
        node.classList.add(HOVERBOX_CLASS);
        // Hide the hover box before querying the DOM for the anchor coordinates.
        node.classList.add(OUTOFVIEW_CLASS);
        // If the current coordinates are not visible, bail.
        if (!host.contains(document.elementFromPoint(anchor.left, anchor.top))) {
            return;
        }
        // Clear any previously set max-height.
        node.style.maxHeight = '';
        // Clear any programmatically set margin-top.
        node.style.marginTop = '';
        // Make sure the node is visible so that its dimensions can be queried.
        node.classList.remove(OUTOFVIEW_CLASS);
        var style = window.getComputedStyle(node);
        var innerHeight = window.innerHeight;
        var spaceAbove = anchor.top;
        var spaceBelow = innerHeight - anchor.bottom;
        var marginTop = parseInt(style.marginTop, 10) || 0;
        var minHeight = parseInt(style.minHeight, 10) || options.minHeight;
        var maxHeight = parseInt(style.maxHeight, 10) || options.maxHeight;
        // Determine whether to render above or below; check privilege.
        var renderBelow = options.privilege === 'above' ?
            spaceAbove < maxHeight && spaceAbove < spaceBelow
            : spaceBelow >= maxHeight || spaceBelow >= spaceAbove;
        if (renderBelow) {
            maxHeight = Math.min(spaceBelow - marginTop, maxHeight);
        }
        else {
            maxHeight = Math.min(spaceAbove, maxHeight);
            // If the box renders above the text, its top margin is irrelevant.
            node.style.marginTop = '0px';
        }
        node.style.maxHeight = maxHeight + "px";
        // Make sure the box ought to be visible.
        var withinBounds = maxHeight > minHeight &&
            (spaceBelow >= minHeight || spaceAbove >= minHeight);
        if (!withinBounds) {
            node.classList.add(OUTOFVIEW_CLASS);
            return;
        }
        // Position the box vertically.
        var offsetAbove = options.offset && options.offset.vertical &&
            options.offset.vertical.above || 0;
        var offsetBelow = options.offset && options.offset.vertical &&
            options.offset.vertical.below || 0;
        var top = renderBelow ? (innerHeight - spaceBelow) + offsetBelow
            : (spaceAbove - node.getBoundingClientRect().height) + offsetAbove;
        node.style.top = Math.floor(top) + "px";
        // Position the box horizontally.
        var offsetHorizontal = options.offset && options.offset.horizontal || 0;
        var left = anchor.left + offsetHorizontal;
        node.style.left = Math.ceil(left) + "px";
        node.style.width = 'auto';
        // Expand the menu width by the scrollbar size, if present.
        if (node.scrollHeight >= maxHeight) {
            node.style.width = "" + (2 * node.offsetWidth - node.clientWidth);
            node.scrollTop = 0;
        }
    }
    HoverBox.setGeometry = setGeometry;
})(HoverBox = exports.HoverBox || (exports.HoverBox = {}));

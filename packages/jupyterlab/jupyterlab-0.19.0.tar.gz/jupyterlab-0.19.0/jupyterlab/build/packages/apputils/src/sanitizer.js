"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
var sanitize = require("sanitize-html");
/**
 * A class to sanitize HTML strings.
 */
var Sanitizer = (function () {
    function Sanitizer() {
        this._options = {
            allowedTags: sanitize.defaults.allowedTags
                .concat('svg', 'h1', 'h2', 'img', 'span'),
            allowedAttributes: {
                // Allow the "rel" attribute for <a> tags.
                'a': sanitize.defaults.allowedAttributes['a'].concat('rel'),
                // Allow the "src" attribute for <img> tags.
                'img': ['src', 'height', 'width', 'alt'],
                // Allow "class" attribute for <code> tags.
                'code': ['class'],
                // Allow "class" attribute for <span> tags.
                'span': ['class']
            },
            transformTags: {
                // Set the "rel" attribute for <a> tags to "nofollow".
                'a': sanitize.simpleTransform('a', { 'rel': 'nofollow' })
            }
        };
    }
    /**
     * Sanitize an HTML string.
     */
    Sanitizer.prototype.sanitize = function (dirty) {
        return sanitize(dirty, this._options);
    };
    return Sanitizer;
}());
/**
 * The default instance of an `ISanitizer` meant for use by user code.
 */
exports.defaultSanitizer = new Sanitizer();

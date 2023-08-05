// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var _1 = require(".");
/**
 * A renderer for raw html.
 */
var HTMLRenderer = (function () {
    function HTMLRenderer() {
        /**
         * The mimeTypes this renderer accepts.
         */
        this.mimeTypes = ['text/html'];
    }
    /**
     * Whether the renderer can render given the render options.
     */
    HTMLRenderer.prototype.canRender = function (options) {
        return this.mimeTypes.indexOf(options.mimeType) !== -1;
    };
    /**
     * Render the transformed mime bundle.
     */
    HTMLRenderer.prototype.render = function (options) {
        return new _1.RenderedHTML(options);
    };
    /**
     * Whether the renderer will sanitize the data given the render options.
     */
    HTMLRenderer.prototype.wouldSanitize = function (options) {
        return !options.model.trusted;
    };
    return HTMLRenderer;
}());
exports.HTMLRenderer = HTMLRenderer;
/**
 * A renderer for `<img>` data.
 */
var ImageRenderer = (function () {
    function ImageRenderer() {
        /**
         * The mimeTypes this renderer accepts.
         */
        this.mimeTypes = ['image/png', 'image/jpeg', 'image/gif'];
    }
    /**
     * Whether the renderer can render given the render options.
     */
    ImageRenderer.prototype.canRender = function (options) {
        return this.mimeTypes.indexOf(options.mimeType) !== -1;
    };
    /**
     * Render the transformed mime bundle.
     */
    ImageRenderer.prototype.render = function (options) {
        return new _1.RenderedImage(options);
    };
    /**
     * Whether the renderer will sanitize the data given the render options.
     */
    ImageRenderer.prototype.wouldSanitize = function (options) {
        return false;
    };
    return ImageRenderer;
}());
exports.ImageRenderer = ImageRenderer;
/**
 * A renderer for plain text and Jupyter console text data.
 */
var TextRenderer = (function () {
    function TextRenderer() {
        /**
         * The mimeTypes this renderer accepts.
         */
        this.mimeTypes = ['text/plain', 'application/vnd.jupyter.stdout',
            'application/vnd.jupyter.stderr'];
    }
    /**
     * Whether the renderer can render given the render options.
     */
    TextRenderer.prototype.canRender = function (options) {
        return this.mimeTypes.indexOf(options.mimeType) !== -1;
    };
    /**
     * Render the transformed mime bundle.
     */
    TextRenderer.prototype.render = function (options) {
        return new _1.RenderedText(options);
    };
    /**
     * Whether the renderer will sanitize the data given the render options.
     */
    TextRenderer.prototype.wouldSanitize = function (options) {
        return false;
    };
    return TextRenderer;
}());
exports.TextRenderer = TextRenderer;
/**
 * A renderer for raw `<script>` data.
 */
var JavaScriptRenderer = (function () {
    function JavaScriptRenderer() {
        /**
         * The mimeTypes this renderer accepts.
         */
        this.mimeTypes = ['text/javascript', 'application/javascript'];
    }
    /**
     * Whether the renderer can render given the render options.
     */
    JavaScriptRenderer.prototype.canRender = function (options) {
        return (options.model.trusted &&
            this.mimeTypes.indexOf(options.mimeType) !== -1);
    };
    /**
     * Render the transformed mime bundle.
     */
    JavaScriptRenderer.prototype.render = function (options) {
        return new _1.RenderedJavaScript(options);
    };
    /**
     * Whether the renderer will sanitize the data given the render options.
     */
    JavaScriptRenderer.prototype.wouldSanitize = function (options) {
        return false;
    };
    return JavaScriptRenderer;
}());
exports.JavaScriptRenderer = JavaScriptRenderer;
/**
 * A renderer for `<svg>` data.
 */
var SVGRenderer = (function () {
    function SVGRenderer() {
        /**
         * The mimeTypes this renderer accepts.
         */
        this.mimeTypes = ['image/svg+xml'];
    }
    /**
     * Whether the renderer can render given the render options.
     */
    SVGRenderer.prototype.canRender = function (options) {
        return (options.model.trusted &&
            this.mimeTypes.indexOf(options.mimeType) !== -1);
    };
    /**
     * Render the transformed mime bundle.
     */
    SVGRenderer.prototype.render = function (options) {
        return new _1.RenderedSVG(options);
    };
    /**
     * Whether the renderer will sanitize the data given the render options.
     */
    SVGRenderer.prototype.wouldSanitize = function (options) {
        return false;
    };
    return SVGRenderer;
}());
exports.SVGRenderer = SVGRenderer;
/**
 * A renderer for PDF data.
 */
var PDFRenderer = (function () {
    function PDFRenderer() {
        /**
         * The mimeTypes this renderer accepts.
         */
        this.mimeTypes = ['application/pdf'];
    }
    /**
     * Whether the renderer can render given the render options.
     */
    PDFRenderer.prototype.canRender = function (options) {
        return (options.model.trusted &&
            this.mimeTypes.indexOf(options.mimeType) !== -1);
    };
    /**
     * Render the transformed mime bundle.
     */
    PDFRenderer.prototype.render = function (options) {
        return new _1.RenderedPDF(options);
    };
    /**
     * Whether the renderer will sanitize the data given the render options.
     */
    PDFRenderer.prototype.wouldSanitize = function (options) {
        return false;
    };
    return PDFRenderer;
}());
exports.PDFRenderer = PDFRenderer;
/**
 * A renderer for LateX data.
 */
var LatexRenderer = (function () {
    function LatexRenderer() {
        /**
         * The mimeTypes this renderer accepts.
         */
        this.mimeTypes = ['text/latex'];
    }
    /**
     * Whether the renderer can render given the render options.
     */
    LatexRenderer.prototype.canRender = function (options) {
        return this.mimeTypes.indexOf(options.mimeType) !== -1;
    };
    /**
     * Render the transformed mime bundle.
     */
    LatexRenderer.prototype.render = function (options) {
        return new _1.RenderedLatex(options);
    };
    /**
     * Whether the renderer will sanitize the data given the render options.
     */
    LatexRenderer.prototype.wouldSanitize = function (options) {
        return false;
    };
    return LatexRenderer;
}());
exports.LatexRenderer = LatexRenderer;
/**
 * A renderer for Jupyter Markdown data.
 */
var MarkdownRenderer = (function () {
    function MarkdownRenderer() {
        /**
         * The mimeTypes this renderer accepts.
         */
        this.mimeTypes = ['text/markdown'];
    }
    /**
     * Whether the renderer can render given the render options.
     */
    MarkdownRenderer.prototype.canRender = function (options) {
        return this.mimeTypes.indexOf(options.mimeType) !== -1;
    };
    /**
     * Render the transformed mime bundle.
     */
    MarkdownRenderer.prototype.render = function (options) {
        return new _1.RenderedMarkdown(options);
    };
    /**
     * Whether the renderer will sanitize the data given the render options.
     */
    MarkdownRenderer.prototype.wouldSanitize = function (options) {
        return !options.model.trusted;
    };
    return MarkdownRenderer;
}());
exports.MarkdownRenderer = MarkdownRenderer;

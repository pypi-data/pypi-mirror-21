// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var CodeMirror = require("codemirror");
var algorithm_1 = require("@phosphor/algorithm");
var disposable_1 = require("@phosphor/disposable");
var signaling_1 = require("@phosphor/signaling");
var coreutils_1 = require("@jupyterlab/coreutils");
var mode_1 = require("./mode");
require("codemirror/addon/edit/matchbrackets.js");
require("codemirror/addon/edit/closebrackets.js");
require("codemirror/addon/comment/comment.js");
require("codemirror/keymap/vim.js");
/**
 * The class name added to CodeMirrorWidget instances.
 */
var EDITOR_CLASS = 'jp-CodeMirrorWidget';
/**
 * The class name added to read only cell editor widgets.
 */
var READ_ONLY_CLASS = 'jp-mod-readOnly';
/**
 * The key code for the up arrow key.
 */
var UP_ARROW = 38;
/**
 * The key code for the down arrow key.
 */
var DOWN_ARROW = 40;
/**
 * CodeMirror editor.
 */
var CodeMirrorEditor = (function () {
    /**
     * Construct a CodeMirror editor.
     */
    function CodeMirrorEditor(options, config) {
        if (config === void 0) { config = {}; }
        var _this = this;
        /**
         * A signal emitted when either the top or bottom edge is requested.
         */
        this.edgeRequested = new signaling_1.Signal(this);
        this.selectionMarkers = {};
        this._keydownHandlers = new Array();
        this._changeGuard = false;
        this._uuid = '';
        var host = this.host = options.host;
        host.classList.add(EDITOR_CLASS);
        this._uuid = options.uuid || coreutils_1.uuid();
        this._selectionStyle = options.selectionStyle || {};
        Private.updateConfig(options, config);
        var model = this._model = options.model;
        var editor = this._editor = CodeMirror(host, config);
        var doc = editor.getDoc();
        // Handle initial values for text, mimetype, and selections.
        doc.setValue(model.value.text);
        this._onMimeTypeChanged();
        this._onCursorActivity();
        // Connect to changes.
        model.value.changed.connect(this._onValueChanged, this);
        model.mimeTypeChanged.connect(this._onMimeTypeChanged, this);
        model.selections.changed.connect(this._onSelectionsChanged, this);
        CodeMirror.on(editor, 'keydown', function (editor, event) {
            var index = algorithm_1.ArrayExt.findFirstIndex(_this._keydownHandlers, function (handler) {
                if (handler(_this, event) === true) {
                    event.preventDefault();
                    return true;
                }
            });
            if (index === -1) {
                _this.onKeydown(event);
            }
        });
        CodeMirror.on(editor, 'cursorActivity', function () { return _this._onCursorActivity(); });
        CodeMirror.on(editor.getDoc(), 'change', function (instance, change) {
            _this._onDocChanged(instance, change);
        });
    }
    Object.defineProperty(CodeMirrorEditor.prototype, "uuid", {
        /**
         * The uuid of this editor;
         */
        get: function () {
            return this._uuid;
        },
        set: function (value) {
            this._uuid = value;
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(CodeMirrorEditor.prototype, "selectionStyle", {
        /**
         * The selection style of this editor.
         */
        get: function () {
            return this._selectionStyle;
        },
        set: function (value) {
            this._selectionStyle = value;
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(CodeMirrorEditor.prototype, "editor", {
        /**
         * Get the codemirror editor wrapped by the editor.
         */
        get: function () {
            return this._editor;
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(CodeMirrorEditor.prototype, "doc", {
        /**
         * Get the codemirror doc wrapped by the widget.
         */
        get: function () {
            return this._editor.getDoc();
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(CodeMirrorEditor.prototype, "lineCount", {
        /**
         * Get the number of lines in the editor.
         */
        get: function () {
            return this.doc.lineCount();
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(CodeMirrorEditor.prototype, "lineNumbers", {
        /**
         * Control the rendering of line numbers.
         */
        get: function () {
            return this._editor.getOption('lineNumbers');
        },
        set: function (value) {
            this._editor.setOption('lineNumbers', value);
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(CodeMirrorEditor.prototype, "wordWrap", {
        /**
         * Set to false for horizontal scrolling. Defaults to true.
         */
        get: function () {
            return this._editor.getOption('lineWrapping');
        },
        set: function (value) {
            this._editor.setOption('lineWrapping', value);
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(CodeMirrorEditor.prototype, "readOnly", {
        /**
         * Should the editor be read only.
         */
        get: function () {
            return this._editor.getOption('readOnly') !== false;
        },
        set: function (readOnly) {
            this._editor.setOption('readOnly', readOnly);
            if (readOnly) {
                this.host.classList.add(READ_ONLY_CLASS);
            }
            else {
                this.host.classList.remove(READ_ONLY_CLASS);
                this.blur();
            }
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(CodeMirrorEditor.prototype, "model", {
        /**
         * Returns a model for this editor.
         */
        get: function () {
            return this._model;
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(CodeMirrorEditor.prototype, "lineHeight", {
        /**
         * The height of a line in the editor in pixels.
         */
        get: function () {
            return this._editor.defaultTextHeight();
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(CodeMirrorEditor.prototype, "charWidth", {
        /**
         * The widget of a character in the editor in pixels.
         */
        get: function () {
            return this._editor.defaultCharWidth();
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(CodeMirrorEditor.prototype, "isDisposed", {
        /**
         * Tests whether the editor is disposed.
         */
        get: function () {
            return this._editor === null;
        },
        enumerable: true,
        configurable: true
    });
    /**
     * Dispose of the resources held by the widget.
     */
    CodeMirrorEditor.prototype.dispose = function () {
        if (this._editor === null) {
            return;
        }
        this._editor = null;
        this._model = null;
        this._keydownHandlers.length = 0;
        signaling_1.Signal.clearData(this);
    };
    /**
     * Returns the content for the given line number.
     */
    CodeMirrorEditor.prototype.getLine = function (line) {
        return this.doc.getLine(line);
    };
    /**
     * Find an offset for the given position.
     */
    CodeMirrorEditor.prototype.getOffsetAt = function (position) {
        return this.doc.indexFromPos({
            ch: position.column,
            line: position.line
        });
    };
    /**
     * Find a position fot the given offset.
     */
    CodeMirrorEditor.prototype.getPositionAt = function (offset) {
        var _a = this.doc.posFromIndex(offset), ch = _a.ch, line = _a.line;
        return { line: line, column: ch };
    };
    /**
     * Undo one edit (if any undo events are stored).
     */
    CodeMirrorEditor.prototype.undo = function () {
        this.doc.undo();
    };
    /**
     * Redo one undone edit.
     */
    CodeMirrorEditor.prototype.redo = function () {
        this.doc.redo();
    };
    /**
     * Clear the undo history.
     */
    CodeMirrorEditor.prototype.clearHistory = function () {
        this.doc.clearHistory();
    };
    /**
     * Brings browser focus to this editor text.
     */
    CodeMirrorEditor.prototype.focus = function () {
        this._editor.focus();
    };
    /**
     * Test whether the editor has keyboard focus.
     */
    CodeMirrorEditor.prototype.hasFocus = function () {
        return this._editor.hasFocus();
    };
    /**
     * Explicitly blur the editor.
     */
    CodeMirrorEditor.prototype.blur = function () {
        this._editor.getInputField().blur();
    };
    /**
     * Repaint editor.
     */
    CodeMirrorEditor.prototype.refresh = function () {
        this._editor.refresh();
    };
    /**
     * Add a keydown handler to the editor.
     *
     * @param handler - A keydown handler.
     *
     * @returns A disposable that can be used to remove the handler.
     */
    CodeMirrorEditor.prototype.addKeydownHandler = function (handler) {
        var _this = this;
        this._keydownHandlers.push(handler);
        return new disposable_1.DisposableDelegate(function () {
            algorithm_1.ArrayExt.removeAllWhere(_this._keydownHandlers, function (val) { return val === handler; });
        });
    };
    /**
     * Set the size of the editor in pixels.
     */
    CodeMirrorEditor.prototype.setSize = function (dimension) {
        if (dimension) {
            this._editor.setSize(dimension.width, dimension.height);
        }
        else {
            this._editor.setSize(null, null);
        }
    };
    /**
     * Reveal the given position in the editor.
     */
    CodeMirrorEditor.prototype.revealPosition = function (position) {
        var cmPosition = this._toCodeMirrorPosition(position);
        this._editor.scrollIntoView(cmPosition);
    };
    /**
     * Reveal the given selection in the editor.
     */
    CodeMirrorEditor.prototype.revealSelection = function (selection) {
        var range = this._toCodeMirrorRange(selection);
        this._editor.scrollIntoView(range);
    };
    /**
     * Get the window coordinates given a cursor position.
     */
    CodeMirrorEditor.prototype.getCoordinateForPosition = function (position) {
        var pos = this._toCodeMirrorPosition(position);
        var rect = this.editor.charCoords(pos, 'page');
        return rect;
    };
    /**
     * Get the cursor position given window coordinates.
     *
     * @param coordinate - The desired coordinate.
     *
     * @returns The position of the coordinates, or null if not
     *   contained in the editor.
     */
    CodeMirrorEditor.prototype.getPositionForCoordinate = function (coordinate) {
        return this._toPosition(this.editor.coordsChar(coordinate)) || null;
    };
    /**
     * Returns the primary position of the cursor, never `null`.
     */
    CodeMirrorEditor.prototype.getCursorPosition = function () {
        var cursor = this.doc.getCursor();
        return this._toPosition(cursor);
    };
    /**
     * Set the primary position of the cursor.
     *
     * #### Notes
     * This will remove any secondary cursors.
     */
    CodeMirrorEditor.prototype.setCursorPosition = function (position) {
        var cursor = this._toCodeMirrorPosition(position);
        this.doc.setCursor(cursor);
    };
    /**
     * Returns the primary selection, never `null`.
     */
    CodeMirrorEditor.prototype.getSelection = function () {
        return this.getSelections()[0];
    };
    /**
     * Set the primary selection. This will remove any secondary cursors.
     */
    CodeMirrorEditor.prototype.setSelection = function (selection) {
        this.setSelections([selection]);
    };
    /**
     * Gets the selections for all the cursors, never `null` or empty.
     */
    CodeMirrorEditor.prototype.getSelections = function () {
        var _this = this;
        var selections = this.doc.listSelections();
        if (selections.length > 0) {
            return selections.map(function (selection) { return _this._toSelection(selection); });
        }
        var cursor = this.doc.getCursor();
        var selection = this._toSelection({ anchor: cursor, head: cursor });
        return [selection];
    };
    /**
     * Sets the selections for all the cursors, should not be empty.
     * Cursors will be removed or added, as necessary.
     * Passing an empty array resets a cursor position to the start of a document.
     */
    CodeMirrorEditor.prototype.setSelections = function (selections) {
        var cmSelections = this._toCodeMirrorSelections(selections);
        this.doc.setSelections(cmSelections, 0);
    };
    /**
     * Handle keydown events from the editor.
     */
    CodeMirrorEditor.prototype.onKeydown = function (event) {
        var position = this.getCursorPosition();
        var line = position.line, column = position.column;
        if (line === 0 && column === 0 && event.keyCode === UP_ARROW) {
            if (!event.shiftKey) {
                this.edgeRequested.emit('top');
            }
            return false;
        }
        var lastLine = this.lineCount - 1;
        var lastCh = this.getLine(lastLine).length;
        if (line === lastLine && column === lastCh
            && event.keyCode === DOWN_ARROW) {
            if (!event.shiftKey) {
                this.edgeRequested.emit('bottom');
            }
            return false;
        }
        return false;
    };
    /**
     * Converts selections to code mirror selections.
     */
    CodeMirrorEditor.prototype._toCodeMirrorSelections = function (selections) {
        var _this = this;
        if (selections.length > 0) {
            return selections.map(function (selection) { return _this._toCodeMirrorSelection(selection); });
        }
        var position = { line: 0, ch: 0 };
        return [{ anchor: position, head: position }];
    };
    /**
     * Handles a mime type change.
     */
    CodeMirrorEditor.prototype._onMimeTypeChanged = function () {
        var mime = this._model.mimeType;
        var editor = this._editor;
        mode_1.loadModeByMIME(editor, mime);
        var isCode = (mime !== 'text/plain') && (mime !== 'text/x-ipythongfm');
        editor.setOption('matchBrackets', isCode);
        editor.setOption('autoCloseBrackets', isCode);
        var extraKeys = editor.getOption('extraKeys') || {};
        if (isCode) {
            extraKeys['Backspace'] = 'delSpaceToPrevTabStop';
        }
        else {
            delete extraKeys['Backspace'];
        }
        editor.setOption('extraKeys', extraKeys);
    };
    /**
     * Handles a selections change.
     */
    CodeMirrorEditor.prototype._onSelectionsChanged = function (selections, args) {
        var uuid = args.key;
        if (uuid !== this.uuid) {
            this._cleanSelections(uuid);
            this._markSelections(uuid, args.newValue);
        }
    };
    /**
     * Clean selections for the given uuid.
     */
    CodeMirrorEditor.prototype._cleanSelections = function (uuid) {
        var markers = this.selectionMarkers[uuid];
        if (markers) {
            markers.forEach(function (marker) { marker.clear(); });
        }
        delete this.selectionMarkers[uuid];
    };
    /**
     * Marks selections.
     */
    CodeMirrorEditor.prototype._markSelections = function (uuid, selections) {
        var _this = this;
        var markers = [];
        selections.forEach(function (selection) {
            var _a = _this._toCodeMirrorSelection(selection), anchor = _a.anchor, head = _a.head;
            var markerOptions = _this._toTextMarkerOptions(selection);
            _this.doc.markText(anchor, head, markerOptions);
        });
        this.selectionMarkers[uuid] = markers;
    };
    /**
     * Handles a cursor activity event.
     */
    CodeMirrorEditor.prototype._onCursorActivity = function () {
        var selections = this.getSelections();
        this.model.selections.set(this.uuid, selections);
    };
    /**
     * Converts a code mirror selection to an editor selection.
     */
    CodeMirrorEditor.prototype._toSelection = function (selection) {
        return {
            uuid: this.uuid,
            start: this._toPosition(selection.anchor),
            end: this._toPosition(selection.head),
            style: this.selectionStyle
        };
    };
    /**
     * Converts the selection style to a text marker options.
     */
    CodeMirrorEditor.prototype._toTextMarkerOptions = function (style) {
        if (style) {
            return {
                className: style.className,
                title: style.displayName
            };
        }
        return undefined;
    };
    /**
     * Converts an editor selection to a code mirror selection.
     */
    CodeMirrorEditor.prototype._toCodeMirrorSelection = function (selection) {
        return {
            anchor: this._toCodeMirrorPosition(selection.start),
            head: this._toCodeMirrorPosition(selection.end)
        };
    };
    /**
     * Converts an editor selection to a code mirror selection.
     */
    CodeMirrorEditor.prototype._toCodeMirrorRange = function (range) {
        return {
            from: this._toCodeMirrorPosition(range.start),
            to: this._toCodeMirrorPosition(range.end)
        };
    };
    /**
     * Convert a code mirror position to an editor position.
     */
    CodeMirrorEditor.prototype._toPosition = function (position) {
        return {
            line: position.line,
            column: position.ch
        };
    };
    /**
     * Convert an editor position to a code mirror position.
     */
    CodeMirrorEditor.prototype._toCodeMirrorPosition = function (position) {
        return {
            line: position.line,
            ch: position.column
        };
    };
    /**
     * Handle model value changes.
     */
    CodeMirrorEditor.prototype._onValueChanged = function (value, args) {
        if (this._changeGuard) {
            return;
        }
        this._changeGuard = true;
        this.doc.setValue(this._model.value.text);
        this._changeGuard = false;
    };
    /**
     * Handles document changes.
     */
    CodeMirrorEditor.prototype._onDocChanged = function (doc, change) {
        if (this._changeGuard) {
            return;
        }
        this._changeGuard = true;
        this._model.value.text = this.doc.getValue();
        this._changeGuard = false;
    };
    return CodeMirrorEditor;
}());
exports.CodeMirrorEditor = CodeMirrorEditor;
/**
 * The namespace for `CodeMirrorEditor` statics.
 */
(function (CodeMirrorEditor) {
    /**
     * The name of the default CodeMirror theme
     */
    CodeMirrorEditor.DEFAULT_THEME = 'jupyter';
})(CodeMirrorEditor = exports.CodeMirrorEditor || (exports.CodeMirrorEditor = {}));
exports.CodeMirrorEditor = CodeMirrorEditor;
/**
 * The namespace for module private data.
 */
var Private;
(function (Private) {
    /**
     * Handle extra codemirror config from codeeditor options.
     */
    function updateConfig(options, config) {
        if (options.readOnly !== undefined) {
            config.readOnly = options.readOnly;
        }
        else {
            config.readOnly = false;
        }
        if (options.lineNumbers !== undefined) {
            config.lineNumbers = options.lineNumbers;
        }
        else {
            config.lineNumbers = false;
        }
        if (options.wordWrap !== undefined) {
            config.lineWrapping = options.wordWrap;
        }
        else {
            config.lineWrapping = true;
        }
        config.theme = (config.theme || CodeMirrorEditor.DEFAULT_THEME);
        config.indentUnit = config.indentUnit || 4;
    }
    Private.updateConfig = updateConfig;
    /**
     * Delete spaces to the previous tab stob in a codemirror editor.
     */
    function delSpaceToPrevTabStop(cm) {
        var doc = cm.getDoc();
        var from = doc.getCursor('from');
        var to = doc.getCursor('to');
        var sel = !posEq(from, to);
        if (sel) {
            var ranges = doc.listSelections();
            for (var i = ranges.length - 1; i >= 0; i--) {
                var head = ranges[i].head;
                var anchor = ranges[i].anchor;
                doc.replaceRange('', CodeMirror.Pos(head.line, head.ch), CodeMirror.Pos(anchor.line, anchor.ch));
            }
            return;
        }
        var cur = doc.getCursor();
        var tabsize = cm.getOption('tabSize');
        var chToPrevTabStop = cur.ch - (Math.ceil(cur.ch / tabsize) - 1) * tabsize;
        from = { ch: cur.ch - chToPrevTabStop, line: cur.line };
        var select = doc.getRange(from, cur);
        if (select.match(/^\ +$/) !== null) {
            doc.replaceRange('', from, cur);
        }
        else {
            CodeMirror.commands['delCharBefore'](cm);
        }
    }
    Private.delSpaceToPrevTabStop = delSpaceToPrevTabStop;
    ;
    /**
     * Test whether two CodeMirror positions are equal.
     */
    function posEq(a, b) {
        return a.line === b.line && a.ch === b.ch;
    }
    Private.posEq = posEq;
    ;
})(Private || (Private = {}));
/**
 * Add a CodeMirror command to delete until previous non blanking space
 * character or first multiple of 4 tabstop.
 */
CodeMirror.commands['delSpaceToPrevTabStop'] = Private.delSpaceToPrevTabStop;

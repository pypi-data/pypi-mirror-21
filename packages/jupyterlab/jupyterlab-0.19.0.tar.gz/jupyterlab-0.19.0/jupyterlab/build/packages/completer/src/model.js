// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var algorithm_1 = require("@phosphor/algorithm");
var coreutils_1 = require("@phosphor/coreutils");
var algorithm_2 = require("@phosphor/algorithm");
var signaling_1 = require("@phosphor/signaling");
/**
 * An implementation of a completer model.
 */
var CompleterModel = (function () {
    function CompleterModel() {
        this._current = null;
        this._cursor = null;
        this._isDisposed = false;
        this._options = [];
        this._original = null;
        this._query = '';
        this._subsetMatch = false;
        this._stateChanged = new signaling_1.Signal(this);
    }
    Object.defineProperty(CompleterModel.prototype, "stateChanged", {
        /**
         * A signal emitted when state of the completer menu changes.
         */
        get: function () {
            return this._stateChanged;
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(CompleterModel.prototype, "original", {
        /**
         * The original completion request details.
         */
        get: function () {
            return this._original;
        },
        set: function (newValue) {
            var unchanged = this._original === newValue ||
                this._original && newValue &&
                    coreutils_1.JSONExt.deepEqual(newValue, this._original);
            if (unchanged) {
                return;
            }
            this._reset();
            this._original = newValue;
            this._stateChanged.emit(void 0);
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(CompleterModel.prototype, "current", {
        /**
         * The current text change details.
         */
        get: function () {
            return this._current;
        },
        set: function (newValue) {
            var unchanged = this._current === newValue ||
                this._current && newValue &&
                    coreutils_1.JSONExt.deepEqual(newValue, this._current);
            if (unchanged) {
                return;
            }
            // Original request must always be set before a text change. If it isn't
            // the model fails silently.
            if (!this.original) {
                return;
            }
            // Cursor must always be set before a text change. This happens
            // automatically in the completer handler, but since `current` is a public
            // attribute, this defensive check is necessary.
            if (!this._cursor) {
                return;
            }
            this._current = newValue;
            if (!this._current) {
                this._stateChanged.emit(void 0);
                return;
            }
            var original = this._original;
            var current = this._current;
            var originalLine = original.text.split('\n')[original.line];
            var currentLine = current.text.split('\n')[current.line];
            // If the text change means that the original start point has been preceded,
            // then the completion is no longer valid and should be reset.
            if (currentLine.length < originalLine.length) {
                this.reset(true);
                return;
            }
            var _a = this._cursor, start = _a.start, end = _a.end;
            // Clip the front of the current line.
            var query = current.text.substring(start);
            // Clip the back of the current line by calculating the end of the original.
            var ending = original.text.substring(end);
            query = query.substring(0, query.lastIndexOf(ending));
            this._query = query;
            this._stateChanged.emit(void 0);
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(CompleterModel.prototype, "cursor", {
        /**
         * The cursor details that the API has used to return matching options.
         */
        get: function () {
            return this._cursor;
        },
        set: function (newValue) {
            // Original request must always be set before a cursor change. If it isn't
            // the model fails silently.
            if (!this.original) {
                return;
            }
            this._cursor = newValue;
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(CompleterModel.prototype, "query", {
        /**
         * The query against which items are filtered.
         */
        get: function () {
            return this._query;
        },
        set: function (newValue) {
            this._query = newValue;
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(CompleterModel.prototype, "subsetMatch", {
        /**
         * A flag that is true when the model value was modified by a subset match.
         */
        get: function () {
            return this._subsetMatch;
        },
        set: function (newValue) {
            this._subsetMatch = newValue;
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(CompleterModel.prototype, "isDisposed", {
        /**
         * Get whether the model is disposed.
         */
        get: function () {
            return this._isDisposed;
        },
        enumerable: true,
        configurable: true
    });
    /**
     * Dispose of the resources held by the model.
     */
    CompleterModel.prototype.dispose = function () {
        // Do nothing if already disposed.
        if (this._isDisposed) {
            return;
        }
        this._isDisposed = true;
        signaling_1.Signal.clearData(this);
    };
    /**
     * The list of visible items in the completer menu.
     *
     * #### Notes
     * This is a read-only property.
     */
    CompleterModel.prototype.items = function () {
        return this._filter();
    };
    /**
     * The unfiltered list of all available options in a completer menu.
     */
    CompleterModel.prototype.options = function () {
        return algorithm_1.iter(this._options);
    };
    /**
     * Set the avilable options in the completer menu.
     */
    CompleterModel.prototype.setOptions = function (newValue) {
        var values = algorithm_1.toArray(newValue || []);
        if (coreutils_1.JSONExt.deepEqual(values, this._options)) {
            return;
        }
        if (values.length) {
            this._options = values;
            this._subsetMatch = true;
        }
        else {
            this._options = [];
        }
        this._stateChanged.emit(void 0);
    };
    /**
     * Handle a cursor change.
     */
    CompleterModel.prototype.handleCursorChange = function (change) {
        // If there is no active completion, return.
        if (!this._original) {
            return;
        }
        var column = change.column, line = change.line;
        var original = this.original;
        // If a cursor change results in a the cursor being on a different line
        // than the original request, cancel.
        if (line !== original.line) {
            this.reset(true);
            return;
        }
        // If a cursor change results in the cursor being set to a position that
        // precedes the original request, cancel.
        if (column < original.column) {
            this.reset(true);
            return;
        }
        // If a cursor change results in the cursor being set to a position beyond
        // the end of the area that would be affected by completion, cancel.
        var current = this.current;
        var cursorDelta = this._cursor.end - this._cursor.start;
        var originalLine = original.text.split('\n')[original.line];
        var currentLine = current.text.split('\n')[current.line];
        var inputDelta = currentLine.length - originalLine.length;
        if (column > original.column + cursorDelta + inputDelta) {
            this.reset(true);
            return;
        }
    };
    /**
     * Handle a text change.
     */
    CompleterModel.prototype.handleTextChange = function (change) {
        // If there is no active completion, return.
        if (!this._original) {
            return;
        }
        // When the completer detects a common subset prefix for all options,
        // it updates the model and sets the model source to that value, but this
        // text change should be ignored.
        if (this._subsetMatch) {
            return;
        }
        var text = change.text, column = change.column, line = change.line;
        var last = text.split('\n')[line][column - 1];
        // If last character entered is not whitespace, update completion.
        if (last && last.match(/\S/)) {
            this.current = change;
        }
        else {
            // If final character is whitespace, reset completion.
            this.reset();
        }
    };
    /**
     * Create a resolved patch between the original state and a patch string.
     *
     * @param patch - The patch string to apply to the original value.
     *
     * @returns A patched text change or null if original value did not exist.
     */
    CompleterModel.prototype.createPatch = function (patch) {
        var original = this._original;
        var cursor = this._cursor;
        if (!original || !cursor) {
            return null;
        }
        var prefix = original.text.substring(0, cursor.start);
        var suffix = original.text.substring(cursor.end);
        return { offset: (prefix + patch).length, text: prefix + patch + suffix };
    };
    /**
     * Reset the state of the model and emit a state change signal.
     *
     * @param hard - Reset even if a subset match is in progress.
     */
    CompleterModel.prototype.reset = function (hard) {
        if (hard === void 0) { hard = false; }
        // When the completer detects a common subset prefix for all options,
        // it updates the model and sets the model source to that value, triggering
        // a reset. Unless explicitly a hard reset, this should be ignored.
        if (!hard && this._subsetMatch) {
            return;
        }
        this._subsetMatch = false;
        this._reset();
        this._stateChanged.emit(void 0);
    };
    /**
     * Apply the query to the complete options list to return the matching subset.
     */
    CompleterModel.prototype._filter = function () {
        var options = this._options || [];
        var query = this._query;
        if (!query) {
            return algorithm_1.map(options, function (option) { return ({ raw: option, text: option }); });
        }
        var results = [];
        for (var _i = 0, options_1 = options; _i < options_1.length; _i++) {
            var option = options_1[_i];
            var match = algorithm_2.StringExt.matchSumOfSquares(option, query);
            if (match) {
                var marked_1 = algorithm_2.StringExt.highlight(option, match.indices, Private.mark);
                results.push({
                    raw: option,
                    score: match.score,
                    text: marked_1.join('')
                });
            }
        }
        return algorithm_1.map(results.sort(Private.scoreCmp), function (result) {
            return ({ text: result.text, raw: result.raw });
        });
    };
    /**
     * Reset the state of the model.
     */
    CompleterModel.prototype._reset = function () {
        this._current = null;
        this._cursor = null;
        this._options = [];
        this._original = null;
        this._query = '';
        this._subsetMatch = false;
    };
    return CompleterModel;
}());
exports.CompleterModel = CompleterModel;
/**
 * A namespace for completer model private data.
 */
var Private;
(function (Private) {
    /**
     * Mark a highlighted chunk of text.
     */
    function mark(value) {
        return "<mark>" + value + "</mark>";
    }
    Private.mark = mark;
    /**
     * A sort comparison function for item match scores.
     *
     * #### Notes
     * This orders the items first based on score (lower is better), then
     * by locale order of the item text.
     */
    function scoreCmp(a, b) {
        var delta = a.score - b.score;
        if (delta !== 0) {
            return delta;
        }
        return a.raw.localeCompare(b.raw);
    }
    Private.scoreCmp = scoreCmp;
})(Private || (Private = {}));

// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var algorithm_1 = require("@phosphor/algorithm");
var signaling_1 = require("@phosphor/signaling");
var coreutils_1 = require("@jupyterlab/coreutils");
/**
 * A cell list object that supports undo/redo.
 */
var CellList = (function () {
    /**
     * Construct the cell list.
     */
    function CellList() {
        this._isDisposed = false;
        this._cellOrder = null;
        this._cellMap = null;
        this._changed = new signaling_1.Signal(this);
        this._cellOrder = new coreutils_1.ObservableUndoableVector({
            toJSON: function (val) { return val; },
            fromJSON: function (val) { return val; }
        });
        this._cellMap = new coreutils_1.ObservableMap();
        this._cellOrder.changed.connect(this._onOrderChanged, this);
    }
    Object.defineProperty(CellList.prototype, "changed", {
        /**
         * A signal emitted when the cell list has changed.
         */
        get: function () {
            return this._changed;
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(CellList.prototype, "isDisposed", {
        /**
         * Test whether the cell list has been disposed.
         */
        get: function () {
            return this._isDisposed;
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(CellList.prototype, "isEmpty", {
        /**
         * Test whether the list is empty.
         *
         * @returns `true` if the cell list is empty, `false` otherwise.
         *
         * #### Notes
         * This is a read-only property.
         *
         * #### Complexity
         * Constant.
         *
         * #### Iterator Validity
         * No changes.
         */
        get: function () {
            return this._cellOrder.length === 0;
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(CellList.prototype, "length", {
        /**
         * Get the length of the cell list.
         *
         * @return The number of cells in the cell list.
         *
         * #### Notes
         * This is a read-only property.
         *
         * #### Complexity
         * Constant.
         *
         * #### Iterator Validity
         * No changes.
         */
        get: function () {
            return this._cellOrder.length;
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(CellList.prototype, "front", {
        /**
         * Get the cell at the front of the cell list.
         *
         * @returns The cell at the front of the cell list, or `undefined` if
         *   the cell list is empty.
         *
         * #### Notes
         * This is a read-only property.
         *
         * #### Complexity
         * Constant.
         *
         * #### Iterator Validity
         * No changes.
         */
        get: function () {
            return this.at(0);
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(CellList.prototype, "back", {
        /**
         * Get the cell at the back of the cell list.
         *
         * @returns The cell at the back of the cell list, or `undefined` if
         *   the cell list is empty.
         *
         * #### Notes
         * This is a read-only property.
         *
         * #### Complexity
         * Constant.
         *
         * #### Iterator Validity
         * No changes.
         */
        get: function () {
            return this.at(this.length - 1);
        },
        enumerable: true,
        configurable: true
    });
    /**
     * Create an iterator over the cells in the cell list.
     *
     * @returns A new iterator starting at the front of the cell list.
     *
     * #### Complexity
     * Constant.
     *
     * #### Iterator Validity
     * No changes.
     */
    CellList.prototype.iter = function () {
        var arr = [];
        for (var _i = 0, _a = algorithm_1.toArray(this._cellOrder); _i < _a.length; _i++) {
            var id = _a[_i];
            arr.push(this._cellMap.get(id));
        }
        return new algorithm_1.ArrayIterator(arr);
    };
    /**
     * Dispose of the resources held by the cell list.
     */
    CellList.prototype.dispose = function () {
        if (this._isDisposed) {
            return;
        }
        this._isDisposed = true;
        signaling_1.Signal.clearData(this);
        // Clean up the cell map and cell order objects.
        for (var _i = 0, _a = this._cellMap.values(); _i < _a.length; _i++) {
            var cell = _a[_i];
            cell.dispose();
        }
        this._cellMap.dispose();
        this._cellOrder.dispose();
    };
    /**
     * Get the cell at the specified index.
     *
     * @param index - The positive integer index of interest.
     *
     * @returns The cell at the specified index.
     *
     * #### Complexity
     * Constant.
     *
     * #### Iterator Validity
     * No changes.
     *
     * #### Undefined Behavior
     * An `index` which is non-integral or out of range.
     */
    CellList.prototype.at = function (index) {
        return this._cellMap.get(this._cellOrder.at(index));
    };
    /**
     * Set the cell at the specified index.
     *
     * @param index - The positive integer index of interest.
     *
     * @param cell - The cell to set at the specified index.
     *
     * #### Complexity
     * Constant.
     *
     * #### Iterator Validity
     * No changes.
     *
     * #### Undefined Behavior
     * An `index` which is non-integral or out of range.
     *
     * #### Notes
     * This should be considered to transfer ownership of the
     * cell to the `CellList`. As such, `cell.dispose()` should
     * not be called by other actors.
     */
    CellList.prototype.set = function (index, cell) {
        // Generate a new uuid for the cell.
        var id = coreutils_1.uuid();
        // Set the internal data structures.
        this._cellMap.set(id, cell);
        this._cellOrder.set(index, id);
    };
    /**
     * Add a cell to the back of the cell list.
     *
     * @param cell - The cell to add to the back of the cell list.
     *
     * @returns The new length of the cell list.
     *
     * #### Complexity
     * Constant.
     *
     * #### Iterator Validity
     * No changes.
     *
     * #### Notes
     * This should be considered to transfer ownership of the
     * cell to the `CellList`. As such, `cell.dispose()` should
     * not be called by other actors.
     */
    CellList.prototype.pushBack = function (cell) {
        // Generate a new uuid for the cell.
        var id = coreutils_1.uuid();
        // Set the internal data structures.
        this._cellMap.set(id, cell);
        var num = this._cellOrder.pushBack(id);
        return num;
    };
    /**
     * Remove and return the cell at the back of the cell list.
     *
     * @returns The cell at the back of the cell list, or `undefined` if
     *   the cell list is empty.
     *
     * #### Complexity
     * Constant.
     *
     * #### Iterator Validity
     * Iterators pointing at the removed cell are invalidated.
     */
    CellList.prototype.popBack = function () {
        //Don't clear the map in case we need to reinstate the cell
        var id = this._cellOrder.popBack();
        var cell = this._cellMap.get(id);
        return cell;
    };
    /**
     * Insert a cell into the cell list at a specific index.
     *
     * @param index - The index at which to insert the cell.
     *
     * @param cell - The cell to set at the specified index.
     *
     * @returns The new length of the cell list.
     *
     * #### Complexity
     * Linear.
     *
     * #### Iterator Validity
     * No changes.
     *
     * #### Notes
     * The `index` will be clamped to the bounds of the cell list.
     *
     * #### Undefined Behavior
     * An `index` which is non-integral.
     *
     * #### Notes
     * This should be considered to transfer ownership of the
     * cell to the `CellList`. As such, `cell.dispose()` should
     * not be called by other actors.
     */
    CellList.prototype.insert = function (index, cell) {
        // Generate a new uuid for the cell.
        var id = coreutils_1.uuid();
        // Set the internal data structures.
        this._cellMap.set(id, cell);
        var num = this._cellOrder.insert(index, id);
        return num;
    };
    /**
     * Remove the first occurrence of a cell from the cell list.
     *
     * @param cell - The cell of interest.
     *
     * @returns The index of the removed cell, or `-1` if the cell
     *   is not contained in the cell list.
     *
     * #### Complexity
     * Linear.
     *
     * #### Iterator Validity
     * Iterators pointing at the removed cell and beyond are invalidated.
     */
    CellList.prototype.remove = function (cell) {
        var _this = this;
        var index = algorithm_1.ArrayExt.findFirstIndex(algorithm_1.toArray(this._cellOrder), function (id) { return (_this._cellMap.get(id) === cell); });
        this.removeAt(index);
        return index;
    };
    /**
     * Remove and return the cell at a specific index.
     *
     * @param index - The index of the cell of interest.
     *
     * @returns The cell at the specified index, or `undefined` if the
     *   index is out of range.
     *
     * #### Complexity
     * Constant.
     *
     * #### Iterator Validity
     * Iterators pointing at the removed cell and beyond are invalidated.
     *
     * #### Undefined Behavior
     * An `index` which is non-integral.
     */
    CellList.prototype.removeAt = function (index) {
        var id = this._cellOrder.removeAt(index);
        var cell = this._cellMap.get(id);
        return cell;
    };
    /**
     * Remove all cells from the cell list.
     *
     * #### Complexity
     * Linear.
     *
     * #### Iterator Validity
     * All current iterators are invalidated.
     */
    CellList.prototype.clear = function () {
        this._cellOrder.clear();
    };
    /**
     * Move a cell from one index to another.
     *
     * @parm fromIndex - The index of the element to move.
     *
     * @param toIndex - The index to move the element to.
     *
     * #### Complexity
     * Constant.
     *
     * #### Iterator Validity
     * Iterators pointing at the lesser of the `fromIndex` and the `toIndex`
     * and beyond are invalidated.
     *
     * #### Undefined Behavior
     * A `fromIndex` or a `toIndex` which is non-integral.
     */
    CellList.prototype.move = function (fromIndex, toIndex) {
        this._cellOrder.move(fromIndex, toIndex);
    };
    /**
     * Push a set of cells to the back of the cell list.
     *
     * @param cells - An iterable or array-like set of cells to add.
     *
     * @returns The new length of the cell list.
     *
     * #### Complexity
     * Linear.
     *
     * #### Iterator Validity
     * No changes.
     *
     * #### Notes
     * This should be considered to transfer ownership of the
     * cells to the `CellList`. As such, `cell.dispose()` should
     * not be called by other actors.
     */
    CellList.prototype.pushAll = function (cells) {
        var _this = this;
        var newValues = algorithm_1.toArray(cells);
        algorithm_1.each(newValues, function (cell) {
            // Generate a new uuid for the cell.
            var id = coreutils_1.uuid();
            // Set the internal data structures.
            _this._cellMap.set(id, cell);
            _this._cellOrder.pushBack(id);
        });
        return this.length;
    };
    /**
     * Insert a set of items into the cell list at the specified index.
     *
     * @param index - The index at which to insert the cells.
     *
     * @param cells - The cells to insert at the specified index.
     *
     * @returns The new length of the cell list.
     *
     * #### Complexity.
     * Linear.
     *
     * #### Iterator Validity
     * No changes.
     *
     * #### Notes
     * The `index` will be clamped to the bounds of the cell list.
     *
     * #### Undefined Behavior.
     * An `index` which is non-integral.
     *
     * #### Notes
     * This should be considered to transfer ownership of the
     * cells to the `CellList`. As such, `cell.dispose()` should
     * not be called by other actors.
     */
    CellList.prototype.insertAll = function (index, cells) {
        var _this = this;
        var newValues = algorithm_1.toArray(cells);
        algorithm_1.each(newValues, function (cell) {
            // Generate a new uuid for the cell.
            var id = coreutils_1.uuid();
            _this._cellMap.set(id, cell);
            _this._cellOrder.beginCompoundOperation();
            _this._cellOrder.insert(index++, id);
            _this._cellOrder.endCompoundOperation();
        });
        return this.length;
    };
    /**
     * Remove a range of items from the cell list.
     *
     * @param startIndex - The start index of the range to remove (inclusive).
     *
     * @param endIndex - The end index of the range to remove (exclusive).
     *
     * @returns The new length of the cell list.
     *
     * #### Complexity
     * Linear.
     *
     * #### Iterator Validity
     * Iterators pointing to the first removed cell and beyond are invalid.
     *
     * #### Undefined Behavior
     * A `startIndex` or `endIndex` which is non-integral.
     */
    CellList.prototype.removeRange = function (startIndex, endIndex) {
        this._cellOrder.removeRange(startIndex, endIndex);
        return this.length;
    };
    Object.defineProperty(CellList.prototype, "canRedo", {
        /**
         * Whether the object can redo changes.
         */
        get: function () {
            return this._cellOrder.canRedo;
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(CellList.prototype, "canUndo", {
        /**
         * Whether the object can undo changes.
         */
        get: function () {
            return this._cellOrder.canUndo;
        },
        enumerable: true,
        configurable: true
    });
    /**
     * Begin a compound operation.
     *
     * @param isUndoAble - Whether the operation is undoable.
     *   The default is `true`.
     */
    CellList.prototype.beginCompoundOperation = function (isUndoAble) {
        this._cellOrder.beginCompoundOperation(isUndoAble);
    };
    /**
     * End a compound operation.
     */
    CellList.prototype.endCompoundOperation = function () {
        this._cellOrder.endCompoundOperation();
    };
    /**
     * Undo an operation.
     */
    CellList.prototype.undo = function () {
        this._cellOrder.undo();
    };
    /**
     * Redo an operation.
     */
    CellList.prototype.redo = function () {
        this._cellOrder.redo();
    };
    /**
     * Clear the change stack.
     */
    CellList.prototype.clearUndo = function () {
        var _loop_1 = function (key) {
            if (algorithm_1.ArrayExt.findFirstIndex(algorithm_1.toArray(this_1._cellOrder), function (id) { return id === key; }) === -1) {
                var cell = this_1._cellMap.get(key);
                cell.dispose();
                this_1._cellMap.delete(key);
            }
        };
        var this_1 = this;
        // Dispose of cells not in the current
        // cell order.
        for (var _i = 0, _a = this._cellMap.keys(); _i < _a.length; _i++) {
            var key = _a[_i];
            _loop_1(key);
        }
        this._cellOrder.clearUndo();
    };
    CellList.prototype._onOrderChanged = function (order, change) {
        var _this = this;
        var newValues = [];
        var oldValues = [];
        algorithm_1.each(change.newValues, function (id) {
            newValues.push(_this._cellMap.get(id));
        });
        algorithm_1.each(change.oldValues, function (id) {
            oldValues.push(_this._cellMap.get(id));
        });
        this._changed.emit({
            type: change.type,
            oldIndex: change.oldIndex,
            newIndex: change.newIndex,
            oldValues: oldValues,
            newValues: newValues
        });
    };
    return CellList;
}());
exports.CellList = CellList;

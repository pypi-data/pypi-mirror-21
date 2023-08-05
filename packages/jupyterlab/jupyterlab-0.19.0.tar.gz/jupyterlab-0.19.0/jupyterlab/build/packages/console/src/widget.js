// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
"use strict";
var __extends = (this && this.__extends) || (function () {
    var extendStatics = Object.setPrototypeOf ||
        ({ __proto__: [] } instanceof Array && function (d, b) { d.__proto__ = b; }) ||
        function (d, b) { for (var p in b) if (b.hasOwnProperty(p)) d[p] = b[p]; };
    return function (d, b) {
        extendStatics(d, b);
        function __() { this.constructor = d; }
        d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
var algorithm_1 = require("@phosphor/algorithm");
var signaling_1 = require("@phosphor/signaling");
var widgets_1 = require("@phosphor/widgets");
var widgets_2 = require("@phosphor/widgets");
var cells_1 = require("@jupyterlab/cells");
var coreutils_1 = require("@jupyterlab/coreutils");
var outputarea_1 = require("@jupyterlab/outputarea");
var foreign_1 = require("./foreign");
var history_1 = require("./history");
/**
 * The class name added to console widgets.
 */
var CONSOLE_CLASS = 'jp-CodeConsole';
/**
 * The class name added to the console banner.
 */
var BANNER_CLASS = 'jp-CodeConsole-banner';
/**
 * The class name of a cell whose input originated from a foreign session.
 */
var FOREIGN_CELL_CLASS = 'jp-CodeConsole-foreignCell';
/**
 * The class name of the active prompt
 */
var PROMPT_CLASS = 'jp-CodeConsole-prompt';
/**
 * The class name of the panel that holds cell content.
 */
var CONTENT_CLASS = 'jp-CodeConsole-content';
/**
 * The class name of the panel that holds prompts.
 */
var INPUT_CLASS = 'jp-CodeConsole-input';
/**
 * The timeout in ms for execution requests to the kernel.
 */
var EXECUTION_TIMEOUT = 250;
/**
 * A widget containing a Jupyter console.
 *
 * #### Notes
 * The CodeConsole class is intended to be used within a ConsolePanel
 * instance. Under most circumstances, it is not instantiated by user code.
 */
var CodeConsole = (function (_super) {
    __extends(CodeConsole, _super);
    /**
     * Construct a console widget.
     */
    function CodeConsole(options) {
        var _this = _super.call(this) || this;
        _this._cells = null;
        _this._content = null;
        _this._foreignHandler = null;
        _this._history = null;
        _this._input = null;
        _this._mimetype = 'text/x-ipython';
        _this._executed = new signaling_1.Signal(_this);
        _this._promptCreated = new signaling_1.Signal(_this);
        _this.addClass(CONSOLE_CLASS);
        // Create the panels that hold the content and input.
        var layout = _this.layout = new widgets_1.PanelLayout();
        _this._cells = new coreutils_1.ObservableVector();
        _this._content = new widgets_1.Panel();
        _this._input = new widgets_1.Panel();
        var factory = _this.contentFactory = options.contentFactory;
        var modelFactory = _this.modelFactory = (options.modelFactory || CodeConsole.defaultModelFactory);
        _this.rendermime = options.rendermime;
        _this.session = options.session;
        _this._mimeTypeService = options.mimeTypeService;
        // Add top-level CSS classes.
        _this._content.addClass(CONTENT_CLASS);
        _this._input.addClass(INPUT_CLASS);
        // Insert the content and input panes into the widget.
        layout.addWidget(_this._content);
        layout.addWidget(_this._input);
        // Create the banner.
        var model = modelFactory.createRawCell({});
        model.value.text = '...';
        var banner = _this.banner = factory.createBanner({
            model: model,
            contentFactory: factory.rawCellContentFactory
        }, _this);
        banner.addClass(BANNER_CLASS);
        banner.readOnly = true;
        _this._content.addWidget(banner);
        // Set up the foreign iopub handler.
        _this._foreignHandler = factory.createForeignHandler({
            session: _this.session,
            parent: _this,
            cellFactory: function () { return _this._createForeignCell(); },
        });
        _this._history = factory.createConsoleHistory({
            session: _this.session
        });
        _this._onKernelChanged();
        _this.session.kernelChanged.connect(_this._onKernelChanged, _this);
        return _this;
    }
    Object.defineProperty(CodeConsole.prototype, "executed", {
        /**
         * A signal emitted when the console finished executing its prompt.
         */
        get: function () {
            return this._executed;
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(CodeConsole.prototype, "promptCreated", {
        /**
         * A signal emitted when a new prompt is created.
         */
        get: function () {
            return this._promptCreated;
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(CodeConsole.prototype, "cells", {
        /**
         * The list of content cells in the console.
         *
         * #### Notes
         * This list does not include the banner or the prompt for a console.
         */
        get: function () {
            return this._cells;
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(CodeConsole.prototype, "prompt", {
        /*
         * The console input prompt.
         */
        get: function () {
            var inputLayout = this._input.layout;
            return inputLayout.widgets[0] || null;
        },
        enumerable: true,
        configurable: true
    });
    /**
     * Add a new cell to the content panel.
     *
     * @param cell - The cell widget being added to the content panel.
     *
     * #### Notes
     * This method is meant for use by outside classes that want to inject content
     * into a console. It is distinct from the `inject` method in that it requires
     * rendered code cell widgets and does not execute them.
     */
    CodeConsole.prototype.addCell = function (cell) {
        this._content.addWidget(cell);
        this._cells.pushBack(cell);
        cell.disposed.connect(this._onCellDisposed, this);
        this.update();
    };
    /**
     * Clear the code cells.
     */
    CodeConsole.prototype.clear = function () {
        // Dispose all the content cells except the first, which is the banner.
        var cells = this._content.widgets;
        while (cells.length > 1) {
            cells[1].dispose();
        }
    };
    /**
     * Dispose of the resources held by the widget.
     */
    CodeConsole.prototype.dispose = function () {
        // Do nothing if already disposed.
        if (this._foreignHandler === null) {
            return;
        }
        var foreignHandler = this._foreignHandler;
        var history = this._history;
        var cells = this._cells;
        this._foreignHandler = null;
        this._history = null;
        this._cells = null;
        foreignHandler.dispose();
        history.dispose();
        cells.clear();
        _super.prototype.dispose.call(this);
    };
    /**
     * Execute the current prompt.
     *
     * @param force - Whether to force execution without checking code
     * completeness.
     *
     * @param timeout - The length of time, in milliseconds, that the execution
     * should wait for the API to determine whether code being submitted is
     * incomplete before attempting submission anyway. The default value is `250`.
     */
    CodeConsole.prototype.execute = function (force, timeout) {
        var _this = this;
        if (force === void 0) { force = false; }
        if (timeout === void 0) { timeout = EXECUTION_TIMEOUT; }
        if (this.session.status === 'dead') {
            return Promise.resolve(void 0);
        }
        var prompt = this.prompt;
        prompt.model.trusted = true;
        if (force) {
            // Create a new prompt before kernel execution to allow typeahead.
            this.newPrompt();
            return this._execute(prompt);
        }
        // Check whether we should execute.
        return this._shouldExecute(timeout).then(function (should) {
            if (_this.isDisposed) {
                return;
            }
            if (should) {
                // Create a new prompt before kernel execution to allow typeahead.
                _this.newPrompt();
                return _this._execute(prompt);
            }
        });
    };
    /**
     * Inject arbitrary code for the console to execute immediately.
     *
     * @param code - The code contents of the cell being injected.
     *
     * @returns A promise that indicates when the injected cell's execution ends.
     */
    CodeConsole.prototype.inject = function (code) {
        var cell = this._createForeignCell();
        cell.model.value.text = code;
        this.addCell(cell);
        return this._execute(cell);
    };
    /**
     * Insert a line break in the prompt.
     */
    CodeConsole.prototype.insertLinebreak = function () {
        var prompt = this.prompt;
        var model = prompt.model;
        var editor = prompt.editor;
        // Insert the line break at the cursor position, and move cursor forward.
        var pos = editor.getCursorPosition();
        var offset = editor.getOffsetAt(pos);
        var text = model.value.text;
        model.value.text = text.substr(0, offset) + '\n' + text.substr(offset);
        pos = editor.getPositionAt(offset + 1);
        editor.setCursorPosition(pos);
    };
    /**
     * Serialize the output.
     */
    CodeConsole.prototype.serialize = function () {
        var prompt = this.prompt;
        var layout = this._content.layout;
        // Serialize content.
        var output = algorithm_1.map(layout.widgets, function (widget) {
            return widget.model.toJSON();
        });
        // Serialize prompt and return.
        return algorithm_1.toArray(output).concat(prompt.model.toJSON());
    };
    /**
     * Handle the DOM events for the widget.
     *
     * @param event - The DOM event sent to the widget.
     *
     * #### Notes
     * This method implements the DOM `EventListener` interface and is
     * called in response to events on the notebook panel's node. It should
     * not be called directly by user code.
     */
    CodeConsole.prototype.handleEvent = function (event) {
        switch (event.type) {
            case 'keydown':
                this._evtKeyDown(event);
                break;
            default:
                break;
        }
    };
    /**
     * Handle `after_attach` messages for the widget.
     */
    CodeConsole.prototype.onAfterAttach = function (msg) {
        var node = this.node;
        node.addEventListener('keydown', this, true);
        // Create a prompt if necessary.
        if (!this.prompt) {
            this.newPrompt();
        }
        else {
            this.prompt.editor.focus();
            this.update();
        }
    };
    /**
     * Handle `before-detach` messages for the widget.
     */
    CodeConsole.prototype.onBeforeDetach = function (msg) {
        var node = this.node;
        node.removeEventListener('keydown', this, true);
    };
    /**
     * Handle `'activate-request'` messages.
     */
    CodeConsole.prototype.onActivateRequest = function (msg) {
        this.prompt.editor.focus();
        this.update();
    };
    /**
     * Make a new prompt.
     */
    CodeConsole.prototype.newPrompt = function () {
        var prompt = this.prompt;
        var input = this._input;
        // Make the last prompt read-only, clear its signals, and move to content.
        if (prompt) {
            prompt.readOnly = true;
            prompt.removeClass(PROMPT_CLASS);
            signaling_1.Signal.clearData(prompt.editor);
            input.layout.removeWidgetAt(0);
            this.addCell(prompt);
        }
        // Create the new prompt.
        var factory = this.contentFactory;
        var options = this._createCodeCellOptions();
        prompt = factory.createPrompt(options, this);
        prompt.model.mimeType = this._mimetype;
        prompt.addClass(PROMPT_CLASS);
        this._input.addWidget(prompt);
        // Suppress the default "Enter" key handling.
        var editor = prompt.editor;
        editor.addKeydownHandler(this._onEditorKeydown);
        this._history.editor = editor;
        if (this.isAttached) {
            this.activate();
        }
        this._promptCreated.emit(prompt);
    };
    /**
     * Handle `update-request` messages.
     */
    CodeConsole.prototype.onUpdateRequest = function (msg) {
        Private.scrollToBottom(this._content.node);
    };
    /**
     * Handle the `'keydown'` event for the widget.
     */
    CodeConsole.prototype._evtKeyDown = function (event) {
        var editor = this.prompt.editor;
        if (event.keyCode === 13 && !editor.hasFocus()) {
            event.preventDefault();
            editor.focus();
        }
    };
    /**
     * Execute the code in the current prompt.
     */
    CodeConsole.prototype._execute = function (cell) {
        var _this = this;
        this._history.push(cell.model.value.text);
        cell.model.contentChanged.connect(this.update, this);
        var onSuccess = function (value) {
            if (_this.isDisposed) {
                return;
            }
            if (value && value.content.status === 'ok') {
                var content = value.content;
                // Use deprecated payloads for backwards compatibility.
                if (content.payload && content.payload.length) {
                    var setNextInput = content.payload.filter(function (i) {
                        return i.source === 'set_next_input';
                    })[0];
                    if (setNextInput) {
                        var text = setNextInput.text;
                        // Ignore the `replace` value and always set the next cell.
                        cell.model.value.text = text;
                    }
                }
            }
            cell.model.contentChanged.disconnect(_this.update, _this);
            _this.update();
            _this._executed.emit(new Date());
        };
        var onFailure = function () {
            if (_this.isDisposed) {
                return;
            }
            cell.model.contentChanged.disconnect(_this.update, _this);
            _this.update();
        };
        return cell.execute(this.session).then(onSuccess, onFailure);
    };
    /**
     * Update the console based on the kernel info.
     */
    CodeConsole.prototype._handleInfo = function (info) {
        var layout = this._content.layout;
        var banner = layout.widgets[0];
        banner.model.value.text = info.banner;
        var lang = info.language_info;
        this._mimetype = this._mimeTypeService.getMimeTypeByLanguage(lang);
        if (this.prompt) {
            this.prompt.model.mimeType = this._mimetype;
        }
    };
    /**
     * Create a new foreign cell.
     */
    CodeConsole.prototype._createForeignCell = function () {
        var factory = this.contentFactory;
        var options = this._createCodeCellOptions();
        var cell = factory.createForeignCell(options, this);
        cell.readOnly = true;
        cell.model.mimeType = this._mimetype;
        cell.addClass(FOREIGN_CELL_CLASS);
        return cell;
    };
    /**
     * Create the options used to initialize a code cell widget.
     */
    CodeConsole.prototype._createCodeCellOptions = function () {
        var factory = this.contentFactory;
        var contentFactory = factory.codeCellContentFactory;
        var modelFactory = this.modelFactory;
        var model = modelFactory.createCodeCell({});
        var rendermime = this.rendermime;
        return { model: model, rendermime: rendermime, contentFactory: contentFactory };
    };
    /**
     * Handle cell disposed signals.
     */
    CodeConsole.prototype._onCellDisposed = function (sender, args) {
        if (!this.isDisposed) {
            this._cells.remove(sender);
        }
    };
    /**
     * Test whether we should execute the prompt.
     */
    CodeConsole.prototype._shouldExecute = function (timeout) {
        var _this = this;
        var prompt = this.prompt;
        var model = prompt.model;
        var code = model.value.text + '\n';
        return new Promise(function (resolve, reject) {
            var timer = setTimeout(function () { resolve(true); }, timeout);
            _this.session.kernel.requestIsComplete({ code: code }).then(function (isComplete) {
                clearTimeout(timer);
                if (_this.isDisposed) {
                    resolve(false);
                }
                if (isComplete.content.status !== 'incomplete') {
                    resolve(true);
                    return;
                }
                model.value.text = code + isComplete.content.indent;
                var editor = prompt.editor;
                var pos = editor.getPositionAt(model.value.text.length);
                editor.setCursorPosition(pos);
                resolve(false);
            }).catch(function () { resolve(true); });
        });
    };
    /**
     * Handle a keydown event on an editor.
     */
    CodeConsole.prototype._onEditorKeydown = function (editor, event) {
        // Suppress "Enter" events.
        return event.keyCode === 13;
    };
    /**
     * Handle a change to the kernel.
     */
    CodeConsole.prototype._onKernelChanged = function () {
        var _this = this;
        this.clear();
        var kernel = this.session.kernel;
        if (!kernel) {
            return;
        }
        kernel.ready.then(function () {
            if (_this.isDisposed) {
                return;
            }
            _this._handleInfo(kernel.info);
        });
    };
    return CodeConsole;
}(widgets_2.Widget));
exports.CodeConsole = CodeConsole;
/**
 * A namespace for CodeConsole statics.
 */
(function (CodeConsole) {
    /**
     * Default implementation of `IContentFactory`.
     */
    var ContentFactory = (function () {
        /**
         * Create a new content factory.
         */
        function ContentFactory(options) {
            var editorFactory = options.editorFactory;
            var outputAreaContentFactory = (options.outputAreaContentFactory ||
                outputarea_1.OutputAreaWidget.defaultContentFactory);
            this.codeCellContentFactory = (options.codeCellContentFactory ||
                new cells_1.CodeCellWidget.ContentFactory({
                    editorFactory: editorFactory,
                    outputAreaContentFactory: outputAreaContentFactory
                }));
            this.rawCellContentFactory = (options.rawCellContentFactory ||
                new cells_1.RawCellWidget.ContentFactory({ editorFactory: editorFactory }));
        }
        /**
         * The history manager for a console widget.
         */
        ContentFactory.prototype.createConsoleHistory = function (options) {
            return new history_1.ConsoleHistory(options);
        };
        /**
         * The foreign handler for a console widget.
         */
        ContentFactory.prototype.createForeignHandler = function (options) {
            return new foreign_1.ForeignHandler(options);
        };
        /**
         * Create a new banner widget.
         */
        ContentFactory.prototype.createBanner = function (options, parent) {
            return new cells_1.RawCellWidget(options);
        };
        /**
         * Create a new prompt widget.
         */
        ContentFactory.prototype.createPrompt = function (options, parent) {
            return new cells_1.CodeCellWidget(options);
        };
        /**
         * Create a new code cell widget for an input from a foreign session.
         */
        ContentFactory.prototype.createForeignCell = function (options, parent) {
            return new cells_1.CodeCellWidget(options);
        };
        return ContentFactory;
    }());
    CodeConsole.ContentFactory = ContentFactory;
    /**
     * The default implementation of an `IModelFactory`.
     */
    var ModelFactory = (function () {
        /**
         * Create a new cell model factory.
         */
        function ModelFactory(options) {
            this.codeCellContentFactory = (options.codeCellContentFactory ||
                cells_1.CodeCellModel.defaultContentFactory);
        }
        /**
         * Create a new code cell.
         *
         * @param source - The data to use for the original source data.
         *
         * @returns A new code cell. If a source cell is provided, the
         *   new cell will be intialized with the data from the source.
         *   If the contentFactory is not provided, the instance
         *   `codeCellContentFactory` will be used.
         */
        ModelFactory.prototype.createCodeCell = function (options) {
            if (!options.contentFactory) {
                options.contentFactory = this.codeCellContentFactory;
            }
            return new cells_1.CodeCellModel(options);
        };
        /**
         * Create a new raw cell.
         *
         * @param source - The data to use for the original source data.
         *
         * @returns A new raw cell. If a source cell is provided, the
         *   new cell will be intialized with the data from the source.
         */
        ModelFactory.prototype.createRawCell = function (options) {
            return new cells_1.RawCellModel(options);
        };
        return ModelFactory;
    }());
    CodeConsole.ModelFactory = ModelFactory;
    /**
     * The default `ModelFactory` instance.
     */
    CodeConsole.defaultModelFactory = new ModelFactory({});
})(CodeConsole = exports.CodeConsole || (exports.CodeConsole = {}));
exports.CodeConsole = CodeConsole;
/**
 * A namespace for console widget private data.
 */
var Private;
(function (Private) {
    /**
     * Jump to the bottom of a node.
     *
     * @param node - The scrollable element.
     */
    function scrollToBottom(node) {
        node.scrollTop = node.scrollHeight - node.clientHeight;
    }
    Private.scrollToBottom = scrollToBottom;
})(Private || (Private = {}));

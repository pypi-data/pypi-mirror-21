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
var widgets_1 = require("@phosphor/widgets");
var widgets_2 = require("@phosphor/widgets");
var codeeditor_1 = require("@jupyterlab/codeeditor");
var rendermime_1 = require("@jupyterlab/rendermime");
var outputarea_1 = require("@jupyterlab/outputarea");
/**
 * The class name added to cell widgets.
 */
var CELL_CLASS = 'jp-Cell';
/**
 * The class name added to the prompt area of cell.
 */
var PROMPT_CLASS = 'jp-Cell-prompt';
/**
 * The class name added to input area widgets.
 */
var INPUT_CLASS = 'jp-InputArea';
/**
 * The class name added to the editor area of the cell.
 */
var EDITOR_CLASS = 'jp-InputArea-editor';
/**
 * The class name added to the cell when collapsed.
 */
var COLLAPSED_CLASS = 'jp-mod-collapsed';
/**
 * The class name added to the cell when readonly.
 */
var READONLY_CLASS = 'jp-mod-readOnly';
/**
 * The class name added to code cells.
 */
var CODE_CELL_CLASS = 'jp-CodeCell';
/**
 * The class name added to markdown cells.
 */
var MARKDOWN_CELL_CLASS = 'jp-MarkdownCell';
/**
 * The class name added to rendered markdown output widgets.
 */
var MARKDOWN_OUTPUT_CLASS = 'jp-MarkdownOutput';
/**
 * The class name added to raw cells.
 */
var RAW_CELL_CLASS = 'jp-RawCell';
/**
 * The class name added to cell editor widget nodes.
 */
var CELL_EDITOR_CLASS = 'jp-CellEditor';
/**
 * The class name added to a rendered input area.
 */
var RENDERED_CLASS = 'jp-mod-rendered';
/**
 * The text applied to an empty markdown cell.
 */
var DEFAULT_MARKDOWN_TEXT = 'Type Markdown and LaTeX: $ α^2 $';
/**
 * A base cell widget.
 */
var BaseCellWidget = (function (_super) {
    __extends(BaseCellWidget, _super);
    /**
     * Construct a new base cell widget.
     */
    function BaseCellWidget(options) {
        var _this = _super.call(this) || this;
        _this._input = null;
        _this._editor = null;
        _this._model = null;
        _this._readOnly = false;
        _this.addClass(CELL_CLASS);
        _this.layout = new widgets_1.PanelLayout();
        var model = _this._model = options.model;
        var factory = _this.contentFactory = options.contentFactory;
        var editorOptions = { model: model, factory: factory.editorFactory };
        var editor = _this._editor = factory.createCellEditor(editorOptions);
        editor.addClass(CELL_EDITOR_CLASS);
        _this._input = factory.createInputArea({ editor: editor });
        _this.layout.addWidget(_this._input);
        return _this;
    }
    Object.defineProperty(BaseCellWidget.prototype, "promptNode", {
        /**
         * Get the prompt node used by the cell.
         */
        get: function () {
            return this._input.promptNode;
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(BaseCellWidget.prototype, "editorWidget", {
        /**
         * Get the editor widget used by the cell.
         */
        get: function () {
            return this._editor;
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(BaseCellWidget.prototype, "editor", {
        /**
         * Get the editor used by the cell.
         */
        get: function () {
            return this._editor.editor;
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(BaseCellWidget.prototype, "model", {
        /**
         * Get the model used by the cell.
         */
        get: function () {
            return this._model;
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(BaseCellWidget.prototype, "readOnly", {
        /**
         * The read only state of the cell.
         */
        get: function () {
            return this._readOnly;
        },
        set: function (value) {
            if (value === this._readOnly) {
                return;
            }
            this._readOnly = value;
            this.update();
        },
        enumerable: true,
        configurable: true
    });
    /**
     * Set the prompt for the widget.
     */
    BaseCellWidget.prototype.setPrompt = function (value) {
        this._input.setPrompt(value);
    };
    /**
     * Dispose of the resources held by the widget.
     */
    BaseCellWidget.prototype.dispose = function () {
        // Do nothing if already disposed.
        if (this.isDisposed) {
            return;
        }
        this._model = null;
        this._input = null;
        this._editor = null;
        _super.prototype.dispose.call(this);
    };
    /**
     * Handle `after-attach` messages.
     */
    BaseCellWidget.prototype.onAfterAttach = function (msg) {
        this.update();
    };
    /**
     * Handle `'activate-request'` messages.
     */
    BaseCellWidget.prototype.onActivateRequest = function (msg) {
        this._editor.editor.focus();
    };
    /**
     * Handle `update-request` messages.
     */
    BaseCellWidget.prototype.onUpdateRequest = function (msg) {
        if (!this._model) {
            return;
        }
        // Handle read only state.
        this._editor.editor.readOnly = this._readOnly;
        this.toggleClass(READONLY_CLASS, this._readOnly);
    };
    /**
     * Render an input instead of the text editor.
     */
    BaseCellWidget.prototype.renderInput = function (widget) {
        this.addClass(RENDERED_CLASS);
        this._input.renderInput(widget);
    };
    /**
     * Show the text editor.
     */
    BaseCellWidget.prototype.showEditor = function () {
        this.removeClass(RENDERED_CLASS);
        this._input.showEditor();
    };
    return BaseCellWidget;
}(widgets_2.Widget));
exports.BaseCellWidget = BaseCellWidget;
/**
 * The namespace for the `BaseCellWidget` class statics.
 */
(function (BaseCellWidget) {
    /**
     * The default implementation of an `IContentFactory`.
     */
    var ContentFactory = (function () {
        /**
         * Creates a new renderer.
         */
        function ContentFactory(options) {
            this.editorFactory = options.editorFactory;
        }
        /**
         * Create a new cell editor for the widget.
         */
        ContentFactory.prototype.createCellEditor = function (options) {
            return new codeeditor_1.CodeEditorWidget(options);
        };
        /**
         * Create a new input area for the widget.
         */
        ContentFactory.prototype.createInputArea = function (options) {
            return new InputAreaWidget(options);
        };
        return ContentFactory;
    }());
    BaseCellWidget.ContentFactory = ContentFactory;
})(BaseCellWidget = exports.BaseCellWidget || (exports.BaseCellWidget = {}));
exports.BaseCellWidget = BaseCellWidget;
/**
 * A widget for a code cell.
 */
var CodeCellWidget = (function (_super) {
    __extends(CodeCellWidget, _super);
    /**
     * Construct a code cell widget.
     */
    function CodeCellWidget(options) {
        var _this = _super.call(this, options) || this;
        _this._rendermime = null;
        _this._output = null;
        _this.addClass(CODE_CELL_CLASS);
        var rendermime = _this._rendermime = options.rendermime;
        var factory = options.contentFactory;
        var model = _this.model;
        _this._output = factory.createOutputArea({
            model: model.outputs,
            rendermime: rendermime,
            contentFactory: factory.outputAreaContentFactory
        });
        _this.layout.addWidget(_this._output);
        _this.setPrompt("" + (model.executionCount || ''));
        model.stateChanged.connect(_this.onStateChanged, _this);
        model.metadata.changed.connect(_this.onMetadataChanged, _this);
        return _this;
    }
    /**
     * Dispose of the resources used by the widget.
     */
    CodeCellWidget.prototype.dispose = function () {
        if (this.isDisposed) {
            return;
        }
        this._output = null;
        _super.prototype.dispose.call(this);
    };
    /**
     * Execute the cell given a client session.
     */
    CodeCellWidget.prototype.execute = function (session) {
        var _this = this;
        var model = this.model;
        var code = model.value.text;
        if (!code.trim() || !session.kernel) {
            model.executionCount = null;
            model.outputs.clear();
            return Promise.resolve(null);
        }
        model.executionCount = null;
        this.setPrompt('*');
        this.model.trusted = true;
        return this._output.execute(code, session).then(function (reply) {
            var status = reply.content.status;
            if (status === 'abort') {
                model.executionCount = null;
                _this.setPrompt(' ');
            }
            else {
                model.executionCount = reply.content.execution_count;
            }
            return reply;
        });
    };
    /**
     * Handle `update-request` messages.
     */
    CodeCellWidget.prototype.onUpdateRequest = function (msg) {
        var value = this.model.metadata.get('collapsed');
        this.toggleClass(COLLAPSED_CLASS, value);
        if (this._output) {
            // TODO: handle scrolled state.
        }
        _super.prototype.onUpdateRequest.call(this, msg);
    };
    /**
     * Handle changes in the model.
     */
    CodeCellWidget.prototype.onStateChanged = function (model, args) {
        switch (args.name) {
            case 'executionCount':
                this.setPrompt("" + model.executionCount);
                break;
            default:
                break;
        }
    };
    /**
     * Handle changes in the metadata.
     */
    CodeCellWidget.prototype.onMetadataChanged = function (model, args) {
        switch (args.key) {
            case 'collapsed':
            case 'scrolled':
                this.update();
                break;
            default:
                break;
        }
    };
    return CodeCellWidget;
}(BaseCellWidget));
exports.CodeCellWidget = CodeCellWidget;
/**
 * The namespace for the `CodeCellWidget` class statics.
 */
(function (CodeCellWidget) {
    /**
     * The default implementation of an `IContentFactory`.
     */
    var ContentFactory = (function (_super) {
        __extends(ContentFactory, _super);
        /**
         * Construct a new code cell content factory
         */
        function ContentFactory(options) {
            var _this = _super.call(this, options) || this;
            _this.outputAreaContentFactory = (options.outputAreaContentFactory ||
                outputarea_1.OutputAreaWidget.defaultContentFactory);
            return _this;
        }
        /**
         * Create an output area widget.
         */
        ContentFactory.prototype.createOutputArea = function (options) {
            return new outputarea_1.OutputAreaWidget(options);
        };
        return ContentFactory;
    }(BaseCellWidget.ContentFactory));
    CodeCellWidget.ContentFactory = ContentFactory;
})(CodeCellWidget = exports.CodeCellWidget || (exports.CodeCellWidget = {}));
exports.CodeCellWidget = CodeCellWidget;
/**
 * A widget for a Markdown cell.
 *
 * #### Notes
 * Things get complicated if we want the rendered text to update
 * any time the text changes, the text editor model changes,
 * or the input area model changes.  We don't support automatically
 * updating the rendered text in all of these cases.
 */
var MarkdownCellWidget = (function (_super) {
    __extends(MarkdownCellWidget, _super);
    /**
     * Construct a Markdown cell widget.
     */
    function MarkdownCellWidget(options) {
        var _this = _super.call(this, options) || this;
        _this._rendermime = null;
        _this._output = null;
        _this._rendered = true;
        _this._prevText = '';
        _this._prevTrusted = false;
        _this.addClass(MARKDOWN_CELL_CLASS);
        _this._rendermime = options.rendermime;
        _this.editor.wordWrap = true;
        return _this;
    }
    Object.defineProperty(MarkdownCellWidget.prototype, "rendered", {
        /**
         * Whether the cell is rendered.
         */
        get: function () {
            return this._rendered;
        },
        set: function (value) {
            if (value === this._rendered) {
                return;
            }
            this._rendered = value;
            this._handleRendered();
        },
        enumerable: true,
        configurable: true
    });
    /**
     * Dispose of the resource held by the widget.
     */
    MarkdownCellWidget.prototype.dispose = function () {
        if (this.isDisposed) {
            return;
        }
        this._output = null;
        _super.prototype.dispose.call(this);
    };
    /*
     * Handle `update-request` messages.
     */
    MarkdownCellWidget.prototype.onUpdateRequest = function (msg) {
        // Make sure we are properly rendered.
        this._handleRendered();
        _super.prototype.onUpdateRequest.call(this, msg);
    };
    /**
     * Handle the rendered state.
     */
    MarkdownCellWidget.prototype._handleRendered = function () {
        if (!this._rendered) {
            this.showEditor();
        }
        else {
            this._updateOutput();
            this.renderInput(this._output);
        }
    };
    /**
     * Update the output.
     */
    MarkdownCellWidget.prototype._updateOutput = function () {
        var model = this.model;
        var text = model && model.value.text || DEFAULT_MARKDOWN_TEXT;
        var trusted = this.model.trusted;
        // Do not re-render if the text has not changed and the trusted
        // has not changed.
        if (text !== this._prevText || trusted !== this._prevTrusted) {
            var data = { 'text/markdown': text };
            var bundle = new rendermime_1.MimeModel({ data: data, trusted: trusted });
            var widget = this._rendermime.render(bundle);
            this._output = widget || new widgets_2.Widget();
            this._output.addClass(MARKDOWN_OUTPUT_CLASS);
        }
        this._prevText = text;
        this._prevTrusted = trusted;
    };
    return MarkdownCellWidget;
}(BaseCellWidget));
exports.MarkdownCellWidget = MarkdownCellWidget;
/**
 * A widget for a raw cell.
 */
var RawCellWidget = (function (_super) {
    __extends(RawCellWidget, _super);
    /**
     * Construct a raw cell widget.
     */
    function RawCellWidget(options) {
        var _this = _super.call(this, options) || this;
        _this.addClass(RAW_CELL_CLASS);
        return _this;
    }
    return RawCellWidget;
}(BaseCellWidget));
exports.RawCellWidget = RawCellWidget;
/**
 * An input area widget, which hosts a prompt and an editor widget.
 */
var InputAreaWidget = (function (_super) {
    __extends(InputAreaWidget, _super);
    /**
     * Construct an input area widget.
     */
    function InputAreaWidget(options) {
        var _this = _super.call(this) || this;
        _this.addClass(INPUT_CLASS);
        var editor = _this._editor = options.editor;
        editor.addClass(EDITOR_CLASS);
        _this.layout = new widgets_1.PanelLayout();
        var prompt = _this._prompt = new widgets_2.Widget();
        prompt.addClass(PROMPT_CLASS);
        var layout = _this.layout;
        layout.addWidget(prompt);
        layout.addWidget(editor);
        return _this;
    }
    Object.defineProperty(InputAreaWidget.prototype, "promptNode", {
        /**
         * Get the prompt node used by the cell.
         */
        get: function () {
            return this._prompt.node;
        },
        enumerable: true,
        configurable: true
    });
    /**
     * Render an input instead of the text editor.
     */
    InputAreaWidget.prototype.renderInput = function (widget) {
        var layout = this.layout;
        if (this._rendered) {
            layout.removeWidget(this._rendered);
        }
        else {
            layout.removeWidget(this._editor);
        }
        this._rendered = widget;
        layout.addWidget(widget);
    };
    /**
     * Show the text editor.
     */
    InputAreaWidget.prototype.showEditor = function () {
        var layout = this.layout;
        if (this._rendered) {
            layout.removeWidget(this._rendered);
            layout.addWidget(this._editor);
        }
    };
    /**
     * Set the prompt of the input area.
     */
    InputAreaWidget.prototype.setPrompt = function (value) {
        if (value === 'null') {
            value = ' ';
        }
        var text = "In [" + (value || ' ') + "]:";
        this._prompt.node.textContent = text;
    };
    return InputAreaWidget;
}(widgets_2.Widget));
exports.InputAreaWidget = InputAreaWidget;

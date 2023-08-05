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
var coreutils_1 = require("@phosphor/coreutils");
var signaling_1 = require("@phosphor/signaling");
var widgets_1 = require("@phosphor/widgets");
var apputils_1 = require("@jupyterlab/apputils");
var widget_1 = require("./widget");
/**
 * The class name added to notebook panels.
 */
var NB_PANEL = 'jp-Notebook-panel';
/**
 * The class name added to a dirty widget.
 */
var DIRTY_CLASS = 'jp-mod-dirty';
/**
 * A widget that hosts a notebook toolbar and content area.
 *
 * #### Notes
 * The widget keeps the document metadata in sync with the current
 * kernel on the context.
 */
var NotebookPanel = (function (_super) {
    __extends(NotebookPanel, _super);
    /**
     * Construct a new notebook panel.
     */
    function NotebookPanel(options) {
        var _this = _super.call(this) || this;
        _this._context = null;
        _this._activated = new signaling_1.Signal(_this);
        _this._contextChanged = new signaling_1.Signal(_this);
        _this.addClass(NB_PANEL);
        _this.rendermime = options.rendermime;
        var layout = _this.layout = new widgets_1.PanelLayout();
        var factory = _this.contentFactory = options.contentFactory;
        var nbOptions = {
            rendermime: _this.rendermime,
            languagePreference: options.languagePreference,
            contentFactory: factory.notebookContentFactory,
            mimeTypeService: options.mimeTypeService
        };
        var toolbar = factory.createToolbar();
        _this.notebook = factory.createNotebook(nbOptions);
        layout.addWidget(toolbar);
        layout.addWidget(_this.notebook);
        return _this;
    }
    Object.defineProperty(NotebookPanel.prototype, "activated", {
        /**
         * A signal emitted when the panel has been activated.
         */
        get: function () {
            return this._activated;
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(NotebookPanel.prototype, "contextChanged", {
        /**
         * A signal emitted when the panel context changes.
         */
        get: function () {
            return this._contextChanged;
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(NotebookPanel.prototype, "session", {
        /**
         * The client session used by the panel.
         */
        get: function () {
            return this._context ? this._context.session : null;
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(NotebookPanel.prototype, "toolbar", {
        /**
         * Get the toolbar used by the widget.
         */
        get: function () {
            return this.layout.widgets[0];
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(NotebookPanel.prototype, "model", {
        /**
         * The model for the widget.
         */
        get: function () {
            return this.notebook ? this.notebook.model : null;
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(NotebookPanel.prototype, "context", {
        /**
         * The document context for the widget.
         *
         * #### Notes
         * Changing the context also changes the model on the
         * `content`.
         */
        get: function () {
            return this._context;
        },
        set: function (newValue) {
            newValue = newValue || null;
            if (newValue === this._context) {
                return;
            }
            var oldValue = this._context;
            this._context = newValue;
            this.rendermime.resolver = newValue;
            // Trigger private, protected, and public changes.
            this._onContextChanged(oldValue, newValue);
            this.onContextChanged(oldValue, newValue);
            this._contextChanged.emit(void 0);
        },
        enumerable: true,
        configurable: true
    });
    /**
     * Dispose of the resources used by the widget.
     */
    NotebookPanel.prototype.dispose = function () {
        this._context = null;
        this.notebook.dispose();
        _super.prototype.dispose.call(this);
    };
    /**
     * Handle `'activate-request'` messages.
     */
    NotebookPanel.prototype.onActivateRequest = function (msg) {
        this.notebook.activate();
        this._activated.emit(void 0);
    };
    /**
     * Handle a change to the document context.
     *
     * #### Notes
     * The default implementation is a no-op.
     */
    NotebookPanel.prototype.onContextChanged = function (oldValue, newValue) {
        // This is a no-op.
    };
    /**
     * Handle a change in the model state.
     */
    NotebookPanel.prototype.onModelStateChanged = function (sender, args) {
        if (args.name === 'dirty') {
            this._handleDirtyState();
        }
    };
    /**
     * Handle a change to the document path.
     */
    NotebookPanel.prototype.onPathChanged = function (sender, path) {
        this.title.label = path.split('/').pop();
    };
    /**
     * Handle a change in the context.
     */
    NotebookPanel.prototype._onContextChanged = function (oldValue, newValue) {
        var _this = this;
        if (oldValue) {
            oldValue.pathChanged.disconnect(this.onPathChanged, this);
            oldValue.session.kernelChanged.disconnect(this._onKernelChanged, this);
            if (oldValue.model) {
                oldValue.model.stateChanged.disconnect(this.onModelStateChanged, this);
            }
        }
        if (!newValue) {
            this._onKernelChanged(null, null);
            return;
        }
        var context = newValue;
        this.notebook.model = newValue.model;
        this._handleDirtyState();
        newValue.model.stateChanged.connect(this.onModelStateChanged, this);
        context.session.kernelChanged.connect(this._onKernelChanged, this);
        // Clear the cells when the context is initially populated.
        if (!newValue.isReady) {
            newValue.ready.then(function () {
                if (_this.isDisposed) {
                    return;
                }
                var model = newValue.model;
                // Clear the undo state of the cells.
                if (model) {
                    model.cells.clearUndo();
                    algorithm_1.each(_this.notebook.widgets, function (widget) {
                        widget.editor.clearHistory();
                    });
                }
            });
        }
        // Handle the document title.
        this.onPathChanged(context, context.path);
        context.pathChanged.connect(this.onPathChanged, this);
    };
    /**
     * Handle a change in the kernel by updating the document metadata.
     */
    NotebookPanel.prototype._onKernelChanged = function (sender, kernel) {
        var _this = this;
        if (!this.model || !kernel) {
            return;
        }
        kernel.ready.then(function () {
            if (_this.model) {
                _this._updateLanguage(kernel.info.language_info);
            }
        });
        this._updateSpec(kernel);
    };
    /**
     * Update the kernel language.
     */
    NotebookPanel.prototype._updateLanguage = function (language) {
        this.model.metadata.set('language_info', language);
    };
    /**
     * Update the kernel spec.
     */
    NotebookPanel.prototype._updateSpec = function (kernel) {
        var _this = this;
        kernel.getSpec().then(function (spec) {
            if (_this.isDisposed) {
                return;
            }
            _this.model.metadata.set('kernelspec', {
                name: kernel.name,
                display_name: spec.display_name,
                language: spec.language
            });
        });
    };
    /**
     * Handle the dirty state of the model.
     */
    NotebookPanel.prototype._handleDirtyState = function () {
        if (!this.model) {
            return;
        }
        if (this.model.dirty) {
            this.title.className += " " + DIRTY_CLASS;
        }
        else {
            this.title.className = this.title.className.replace(DIRTY_CLASS, '');
        }
    };
    return NotebookPanel;
}(widgets_1.Widget));
exports.NotebookPanel = NotebookPanel;
/**
 * A namespace for `NotebookPanel` statics.
 */
(function (NotebookPanel) {
    /**
     * The default implementation of an `IContentFactory`.
     */
    var ContentFactory = (function () {
        /**
         * Creates a new renderer.
         */
        function ContentFactory(options) {
            this.editorFactory = options.editorFactory;
            this.notebookContentFactory = (options.notebookContentFactory ||
                new widget_1.Notebook.ContentFactory({
                    editorFactory: this.editorFactory,
                    outputAreaContentFactory: options.outputAreaContentFactory,
                    codeCellContentFactory: options.codeCellContentFactory,
                    rawCellContentFactory: options.rawCellContentFactory,
                    markdownCellContentFactory: options.markdownCellContentFactory
                }));
        }
        /**
         * Create a new content area for the panel.
         */
        ContentFactory.prototype.createNotebook = function (options) {
            return new widget_1.Notebook(options);
        };
        /**
         * Create a new toolbar for the panel.
         */
        ContentFactory.prototype.createToolbar = function () {
            return new apputils_1.Toolbar();
        };
        return ContentFactory;
    }());
    NotebookPanel.ContentFactory = ContentFactory;
    /* tslint:disable */
    /**
     * The notebook renderer token.
     */
    NotebookPanel.IContentFactory = new coreutils_1.Token('jupyter.services.notebook.content-factory');
    /* tslint:enable */
})(NotebookPanel = exports.NotebookPanel || (exports.NotebookPanel = {}));
exports.NotebookPanel = NotebookPanel;

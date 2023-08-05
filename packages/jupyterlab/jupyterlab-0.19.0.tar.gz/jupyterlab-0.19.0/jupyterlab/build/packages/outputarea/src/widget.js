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
var services_1 = require("@jupyterlab/services");
var coreutils_1 = require("@phosphor/coreutils");
var dragdrop_1 = require("@phosphor/dragdrop");
var widgets_1 = require("@phosphor/widgets");
var widgets_2 = require("@phosphor/widgets");
/**
 * The threshold in pixels to start a drag event.
 */
var DRAG_THRESHOLD = 5;
/**
 * The factory MIME type supported by phosphor dock panels.
 */
var FACTORY_MIME = 'application/vnd.phosphor.widget-factory';
/**
 * The class name added to an output area widget.
 */
var OUTPUT_AREA_CLASS = 'jp-OutputAreaWidget';
/**
 * The class name added to a "mirrored" output area widget created by a drag.
 */
var MIRRORED_OUTPUT_AREA_CLASS = 'jp-MirroredOutputArea';
/**
 * The class name added to an child widget.
 */
var CHILD_CLASS = 'jp-OutputAreaWidget-child';
/**
 * The class name added to output area gutters.
 */
var GUTTER_CLASS = 'jp-OutputAreaWidget-gutter';
/**
 * The class name added to output area outputs.
 */
var OUTPUT_CLASS = 'jp-OutputAreaWidget-output';
/**
 * The class name added to an execution result.
 */
var EXECTUTE_CLASS = 'jp-OutputAreaWidget-executeResult';
/**
 * The class name added to stdin data.
 */
var STDIN_CLASS = 'jp-OutputAreaWidget-stdin';
/**
 * The class name added to stdin data prompt nodes.
 */
var STDIN_PROMPT_CLASS = 'jp-StdinWidget-prompt';
/**
 * The class name added to stdin data input nodes.
 */
var STDIN_INPUT_CLASS = 'jp-StdinWidget-input';
/**
 * The class name added to stdin rendered text nodes.
 */
var STDIN_RENDERED_CLASS = 'jp-StdinWidget-rendered';
/**
 * The class name added to fixed height output areas.
 */
var FIXED_HEIGHT_CLASS = 'jp-mod-fixedHeight';
/**
 * The class name added to collaped output areas.
 */
var COLLAPSED_CLASS = 'jp-mod-collapsed';
/**
 * An output area widget.
 *
 * #### Notes
 * The widget model must be set separately and can be changed
 * at any time.  Consumers of the widget must account for a
 * `null` model, and may want to listen to the `modelChanged`
 * signal.
 */
var OutputAreaWidget = (function (_super) {
    __extends(OutputAreaWidget, _super);
    /**
     * Construct an output area widget.
     */
    function OutputAreaWidget(options) {
        var _this = _super.call(this) || this;
        _this._fixedHeight = false;
        _this._collapsed = false;
        _this._minHeightTimeout = null;
        var model = _this.model = options.model;
        _this.addClass(OUTPUT_AREA_CLASS);
        _this.rendermime = options.rendermime;
        _this.contentFactory = (options.contentFactory || OutputAreaWidget.defaultContentFactory);
        _this.layout = new widgets_1.PanelLayout();
        for (var i = 0; i < model.length; i++) {
            var output = model.get(i);
            _this._insertOutput(i, output);
        }
        model.changed.connect(_this.onModelChanged, _this);
        return _this;
    }
    /**
     * Create a mirrored output area widget.
     */
    OutputAreaWidget.prototype.mirror = function () {
        var rendermime = this.rendermime;
        var contentFactory = this.contentFactory;
        var model = this.model;
        var widget = new OutputAreaWidget({ model: model, rendermime: rendermime, contentFactory: contentFactory });
        widget.title.label = 'Mirrored Output';
        widget.title.closable = true;
        widget.addClass(MIRRORED_OUTPUT_AREA_CLASS);
        return widget;
    };
    Object.defineProperty(OutputAreaWidget.prototype, "widgets", {
        /**
         * A read-only sequence of the widgets in the output area.
         */
        get: function () {
            return this.layout.widgets;
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(OutputAreaWidget.prototype, "collapsed", {
        /**
         * The collapsed state of the widget.
         */
        get: function () {
            return this._collapsed;
        },
        set: function (value) {
            if (this._collapsed === value) {
                return;
            }
            this._collapsed = value;
            this.update();
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(OutputAreaWidget.prototype, "fixedHeight", {
        /**
         * The fixed height state of the widget.
         */
        get: function () {
            return this._fixedHeight;
        },
        set: function (value) {
            if (this._fixedHeight === value) {
                return;
            }
            this._fixedHeight = value;
            this.update();
        },
        enumerable: true,
        configurable: true
    });
    /**
     * Execute code on a client session and handle response messages.
     */
    OutputAreaWidget.prototype.execute = function (code, session) {
        var _this = this;
        // Bail if the model is disposed.
        if (this.model.isDisposed) {
            return Promise.reject('Model is disposed');
        }
        // Bail if there is no kernel.
        var kernel = session.kernel;
        if (!kernel) {
            return Promise.reject('No kernel exists on the session');
        }
        // Override the default for `stop_on_error`.
        var content = {
            code: code,
            stop_on_error: true
        };
        this.model.clear();
        // Make sure there were no input widgets.
        if (this.widgets.length) {
            this._clear();
        }
        return new Promise(function (resolve, reject) {
            var future = kernel.requestExecute(content);
            // Handle published messages.
            future.onIOPub = function (msg) {
                _this._onIOPub(msg);
            };
            // Handle the execute reply.
            future.onReply = function (msg) {
                _this._onExecuteReply(msg);
                resolve(msg);
            };
            // Handle stdin.
            future.onStdin = function (msg) {
                if (services_1.KernelMessage.isInputRequestMsg(msg)) {
                    _this._onInputRequest(msg, session);
                }
            };
        });
    };
    /**
     * Handle `update-request` messages.
     */
    OutputAreaWidget.prototype.onUpdateRequest = function (msg) {
        this.toggleClass(COLLAPSED_CLASS, this.collapsed);
        this.toggleClass(FIXED_HEIGHT_CLASS, this.fixedHeight);
    };
    /**
     * Follow changes on the model state.
     */
    OutputAreaWidget.prototype.onModelChanged = function (sender, args) {
        switch (args.type) {
            case 'add':
                this._insertOutput(args.newIndex, args.newValues[0]);
                break;
            case 'remove':
                // Only clear is supported by the model.
                if (this.widgets.length) {
                    this._clear();
                }
                break;
            case 'set':
                this._setOutput(args.newIndex, args.newValues[0]);
                break;
            default:
                break;
        }
    };
    /**
     * Clear the widget inputs and outputs.
     */
    OutputAreaWidget.prototype._clear = function () {
        var _this = this;
        // Bail if there is no work to do.
        if (!this.widgets.length) {
            return;
        }
        // Remove all of our widgets.
        var length = this.widgets.length;
        for (var i = 0; i < length; i++) {
            var widget = this.widgets[0];
            widget.parent = null;
            widget.dispose();
        }
        // When an output area is cleared and then quickly replaced with new
        // content (as happens with @interact in widgets, for example), the
        // quickly changing height can make the page jitter.
        // We introduce a small delay in the minimum height
        // to prevent this jitter.
        var rect = this.node.getBoundingClientRect();
        this.node.style.minHeight = rect.height + "px";
        if (this._minHeightTimeout) {
            clearTimeout(this._minHeightTimeout);
        }
        this._minHeightTimeout = window.setTimeout(function () {
            if (_this.isDisposed) {
                return;
            }
            _this.node.style.minHeight = '';
        }, 50);
    };
    /**
     * Handle an iopub message.
     */
    OutputAreaWidget.prototype._onIOPub = function (msg) {
        var model = this.model;
        var msgType = msg.header.msg_type;
        switch (msgType) {
            case 'execute_result':
            case 'display_data':
            case 'stream':
            case 'error':
                var output = msg.content;
                output.output_type = msgType;
                model.add(output);
                break;
            case 'clear_output':
                var wait = msg.content.wait;
                model.clear(wait);
                break;
            default:
                break;
        }
    };
    /**
     * Handle an execute reply message.
     */
    OutputAreaWidget.prototype._onExecuteReply = function (msg) {
        // API responses that contain a pager are special cased and their type
        // is overriden from 'execute_reply' to 'display_data' in order to
        // render output.
        var model = this.model;
        var content = msg.content;
        var payload = content && content.payload;
        if (!payload || !payload.length) {
            return;
        }
        var pages = payload.filter(function (i) { return i.source === 'page'; });
        if (!pages.length) {
            return;
        }
        var page = JSON.parse(JSON.stringify(pages[0]));
        var output = {
            output_type: 'display_data',
            data: page.data,
            metadata: {}
        };
        model.add(output);
    };
    /**
     * Handle an input request from a kernel.
     */
    OutputAreaWidget.prototype._onInputRequest = function (msg, session) {
        // Add an output widget to the end.
        var factory = this.contentFactory;
        var prompt = msg.content.prompt;
        var password = msg.content.password;
        var panel = new widgets_1.Panel();
        panel.addClass(CHILD_CLASS);
        panel.addClass(STDIN_CLASS);
        var gutter = factory.createGutter();
        gutter.addClass(GUTTER_CLASS);
        panel.addWidget(gutter);
        var kernel = session.kernel;
        var input = factory.createStdin({ prompt: prompt, password: password, kernel: kernel });
        input.addClass(STDIN_CLASS);
        panel.addWidget(input);
        var layout = this.layout;
        layout.addWidget(panel);
    };
    /**
     * Insert an output to the layout.
     */
    OutputAreaWidget.prototype._insertOutput = function (index, model) {
        var panel = new widgets_1.Panel();
        panel.addClass(CHILD_CLASS);
        panel.addClass(OUTPUT_CLASS);
        var gutter = this.contentFactory.createGutter();
        gutter.executionCount = model.executionCount;
        gutter.addClass(GUTTER_CLASS);
        panel.addWidget(gutter);
        var output = this._createOutput(model);
        output.toggleClass(EXECTUTE_CLASS, model.executionCount !== null);
        panel.addWidget(output);
        var layout = this.layout;
        layout.insertWidget(index, panel);
    };
    /**
     * Update an output in place.
     */
    OutputAreaWidget.prototype._setOutput = function (index, model) {
        var layout = this.layout;
        var widgets = this.widgets;
        // Skip any stdin widgets to find the correct index.
        for (var i = 0; i < index; i++) {
            if (widgets[i].hasClass(STDIN_CLASS)) {
                index++;
            }
        }
        layout.widgets[index].dispose();
        this._insertOutput(index, model);
    };
    /**
     * Create an output.
     */
    OutputAreaWidget.prototype._createOutput = function (model) {
        var widget = this.rendermime.render(model);
        widget.addClass(CHILD_CLASS);
        widget.addClass(OUTPUT_CLASS);
        return widget;
    };
    return OutputAreaWidget;
}(widgets_2.Widget));
exports.OutputAreaWidget = OutputAreaWidget;
/**
 * A namespace for OutputAreaWidget statics.
 */
(function (OutputAreaWidget) {
    /**
     * The default implementation of `IContentFactory`.
     */
    var ContentFactory = (function () {
        function ContentFactory() {
        }
        /**
         * Create the gutter for the widget.
         */
        ContentFactory.prototype.createGutter = function () {
            return new GutterWidget();
        };
        /**
         * Create an stdin widget.
         */
        ContentFactory.prototype.createStdin = function (options) {
            return new StdinWidget(options);
        };
        return ContentFactory;
    }());
    OutputAreaWidget.ContentFactory = ContentFactory;
    /**
     * The default `ContentFactory` instance.
     */
    OutputAreaWidget.defaultContentFactory = new ContentFactory();
    /**
     * The default stdin widget.
     */
    var StdinWidget = (function (_super) {
        __extends(StdinWidget, _super);
        /**
         * Construct a new input widget.
         */
        function StdinWidget(options) {
            var _this = _super.call(this, { node: Private.createInputWidgetNode() }) || this;
            _this._kernel = null;
            _this._input = null;
            var text = _this.node.firstChild;
            text.textContent = options.prompt;
            _this._input = _this.node.lastChild;
            if (options.password) {
                _this._input.type = 'password';
            }
            _this._kernel = options.kernel;
            return _this;
        }
        /**
         * Handle the DOM events for the widget.
         *
         * @param event - The DOM event sent to the widget.
         *
         * #### Notes
         * This method implements the DOM `EventListener` interface and is
         * called in response to events on the dock panel's node. It should
         * not be called directly by user code.
         */
        StdinWidget.prototype.handleEvent = function (event) {
            var input = this._input;
            if (event.type === 'keydown') {
                if (event.keyCode === 13) {
                    this._kernel.sendInputReply({
                        value: input.value
                    });
                    var rendered = document.createElement('span');
                    rendered.className = STDIN_RENDERED_CLASS;
                    if (input.type === 'password') {
                        rendered.textContent = Array(input.value.length + 1).join('·');
                    }
                    else {
                        rendered.textContent = input.value;
                    }
                    this.node.replaceChild(rendered, input);
                }
            }
        };
        /**
         * Handle `after-attach` messages sent to the widget.
         */
        StdinWidget.prototype.onAfterAttach = function (msg) {
            this._input.addEventListener('keydown', this);
            this.update();
        };
        /**
         * Handle `update-request` messages sent to the widget.
         */
        StdinWidget.prototype.onUpdateRequest = function (msg) {
            this._input.focus();
        };
        /**
         * Handle `before-detach` messages sent to the widget.
         */
        StdinWidget.prototype.onBeforeDetach = function (msg) {
            this._input.removeEventListener('keydown', this);
        };
        return StdinWidget;
    }(widgets_2.Widget));
    OutputAreaWidget.StdinWidget = StdinWidget;
    /**
     * The default output gutter.
     */
    var GutterWidget = (function (_super) {
        __extends(GutterWidget, _super);
        function GutterWidget() {
            var _this = _super !== null && _super.apply(this, arguments) || this;
            _this._drag = null;
            _this._dragData = null;
            _this._executionCount = null;
            return _this;
        }
        Object.defineProperty(GutterWidget.prototype, "executionCount", {
            /**
             * The execution count for the widget.
             */
            get: function () {
                return this._executionCount;
            },
            set: function (value) {
                this._executionCount = value;
                if (value === null) {
                    this.node.textContent = '';
                }
                else {
                    this.node.textContent = "Out[" + value + "]:";
                }
            },
            enumerable: true,
            configurable: true
        });
        /**
         * Handle the DOM events for the output gutter widget.
         *
         * @param event - The DOM event sent to the widget.
         *
         * #### Notes
         * This method implements the DOM `EventListener` interface and is
         * called in response to events on the panel's DOM node. It should
         * not be called directly by user code.
         */
        GutterWidget.prototype.handleEvent = function (event) {
            switch (event.type) {
                case 'mousedown':
                    this._evtMousedown(event);
                    break;
                case 'mouseup':
                    this._evtMouseup(event);
                    break;
                case 'mousemove':
                    this._evtMousemove(event);
                    break;
                default:
                    break;
            }
        };
        /**
         * A message handler invoked on an `'after-attach'` message.
         */
        GutterWidget.prototype.onAfterAttach = function (msg) {
            _super.prototype.onAfterAttach.call(this, msg);
            this.node.addEventListener('mousedown', this);
        };
        /**
         * A message handler invoked on a `'before-detach'` message.
         */
        GutterWidget.prototype.onBeforeDetach = function (msg) {
            _super.prototype.onBeforeDetach.call(this, msg);
            var node = this.node;
            node.removeEventListener('mousedown', this);
        };
        /**
         * Handle the `'mousedown'` event for the widget.
         */
        GutterWidget.prototype._evtMousedown = function (event) {
            // Left mouse press for drag start.
            if (event.button === 0) {
                this._dragData = { pressX: event.clientX, pressY: event.clientY };
                document.addEventListener('mouseup', this, true);
                document.addEventListener('mousemove', this, true);
            }
        };
        /**
         * Handle the `'mouseup'` event for the widget.
         */
        GutterWidget.prototype._evtMouseup = function (event) {
            if (event.button !== 0 || !this._drag) {
                document.removeEventListener('mousemove', this, true);
                document.removeEventListener('mouseup', this, true);
                return;
            }
            event.preventDefault();
            event.stopPropagation();
        };
        /**
         * Handle the `'mousemove'` event for the widget.
         */
        GutterWidget.prototype._evtMousemove = function (event) {
            event.preventDefault();
            event.stopPropagation();
            // Bail if we are the one dragging.
            if (this._drag) {
                return;
            }
            // Check for a drag initialization.
            var data = this._dragData;
            var dx = Math.abs(event.clientX - data.pressX);
            var dy = Math.abs(event.clientY - data.pressY);
            if (dx < DRAG_THRESHOLD && dy < DRAG_THRESHOLD) {
                return;
            }
            this._startDrag(event.clientX, event.clientY);
        };
        /**
         * Start a drag event.
         */
        GutterWidget.prototype._startDrag = function (clientX, clientY) {
            var _this = this;
            // Set up the drag event.
            this._drag = new dragdrop_1.Drag({
                mimeData: new coreutils_1.MimeData(),
                supportedActions: 'copy',
                proposedAction: 'copy'
            });
            this._drag.mimeData.setData(FACTORY_MIME, function () {
                var outputArea = _this.parent.parent;
                return outputArea.mirror();
            });
            // Remove mousemove and mouseup listeners and start the drag.
            document.removeEventListener('mousemove', this, true);
            document.removeEventListener('mouseup', this, true);
            this._drag.start(clientX, clientY).then(function (action) {
                _this._drag = null;
            });
        };
        /**
         * Dispose of the resources held by the widget.
         */
        GutterWidget.prototype.dispose = function () {
            this._dragData = null;
            this._drag = null;
            _super.prototype.dispose.call(this);
        };
        return GutterWidget;
    }(widgets_2.Widget));
    OutputAreaWidget.GutterWidget = GutterWidget;
})(OutputAreaWidget = exports.OutputAreaWidget || (exports.OutputAreaWidget = {}));
exports.OutputAreaWidget = OutputAreaWidget;
/**
 * A namespace for private data.
 */
var Private;
(function (Private) {
    /**
     * Create the node for an InputWidget.
     */
    function createInputWidgetNode() {
        var node = document.createElement('div');
        var prompt = document.createElement('span');
        prompt.className = STDIN_PROMPT_CLASS;
        var input = document.createElement('input');
        input.className = STDIN_INPUT_CLASS;
        node.appendChild(prompt);
        node.appendChild(input);
        return node;
    }
    Private.createInputWidgetNode = createInputWidgetNode;
})(Private || (Private = {}));

// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var coreutils_1 = require("@jupyterlab/coreutils");
var algorithm_1 = require("@phosphor/algorithm");
var coreutils_2 = require("@phosphor/coreutils");
var signaling_1 = require("@phosphor/signaling");
var _1 = require(".");
/**
 * The default implementation of client session object.
 */
var ClientSession = (function () {
    /**
     * Construct a new client session.
     */
    function ClientSession(options) {
        this._path = '';
        this._name = '';
        this._type = '';
        this._prevKernelName = '';
        this._isDisposed = false;
        this._session = null;
        this._ready = new coreutils_2.PromiseDelegate();
        this._initializing = false;
        this._isReady = false;
        this._terminated = new signaling_1.Signal(this);
        this._kernelChanged = new signaling_1.Signal(this);
        this._statusChanged = new signaling_1.Signal(this);
        this._iopubMessage = new signaling_1.Signal(this);
        this._unhandledMessage = new signaling_1.Signal(this);
        this._propertyChanged = new signaling_1.Signal(this);
        this.manager = options.manager;
        this._path = options.path || coreutils_1.uuid();
        this._type = options.type || '';
        this._name = options.name || '';
        this._kernelPreference = options.kernelPreference || {};
    }
    Object.defineProperty(ClientSession.prototype, "terminated", {
        /**
         * A signal emitted when the session is shut down.
         */
        get: function () {
            return this._terminated;
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(ClientSession.prototype, "kernelChanged", {
        /**
         * A signal emitted when the kernel changes.
         */
        get: function () {
            return this._kernelChanged;
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(ClientSession.prototype, "statusChanged", {
        /**
         * A signal emitted when the status changes.
         */
        get: function () {
            return this._statusChanged;
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(ClientSession.prototype, "iopubMessage", {
        /**
         * A signal emitted for iopub kernel messages.
         */
        get: function () {
            return this._iopubMessage;
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(ClientSession.prototype, "unhandledMessage", {
        /**
         * A signal emitted for an unhandled kernel message.
         */
        get: function () {
            return this._unhandledMessage;
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(ClientSession.prototype, "propertyChanged", {
        /**
         * A signal emitted when a session property changes.
         */
        get: function () {
            return this._propertyChanged;
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(ClientSession.prototype, "kernel", {
        /**
         * The current kernel of the session.
         */
        get: function () {
            return this._session ? this._session.kernel : null;
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(ClientSession.prototype, "path", {
        /**
         * The current path of the session.
         */
        get: function () {
            return this._path;
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(ClientSession.prototype, "name", {
        /**
         * The current name of the session.
         */
        get: function () {
            return this._name;
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(ClientSession.prototype, "type", {
        /**
         * The type of the client session.
         */
        get: function () {
            return this._type;
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(ClientSession.prototype, "kernelPreference", {
        /**
         * The kernel preference of the session.
         */
        get: function () {
            return this._kernelPreference;
        },
        set: function (value) {
            this._kernelPreference = value;
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(ClientSession.prototype, "status", {
        /**
         * The current status of the session.
         */
        get: function () {
            if (!this.isReady) {
                return 'starting';
            }
            return this._session ? this._session.status : 'dead';
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(ClientSession.prototype, "isReady", {
        /**
         * Whether the session is ready.
         */
        get: function () {
            return this._isReady;
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(ClientSession.prototype, "ready", {
        /**
         * A promise that is fulfilled when the session is ready.
         */
        get: function () {
            return this._ready.promise;
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(ClientSession.prototype, "kernelDisplayName", {
        /**
         * The display name of the current kernel.
         */
        get: function () {
            var kernel = this.kernel;
            if (!kernel) {
                return 'No Kernel!';
            }
            if (!this.manager.isReady) {
                return 'Unknown!';
            }
            var spec = this.manager.specs.kernelspecs[kernel.name];
            return spec ? spec.display_name : kernel.name;
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(ClientSession.prototype, "isDisposed", {
        /**
         * Test whether the context is disposed.
         */
        get: function () {
            return this._isDisposed;
        },
        enumerable: true,
        configurable: true
    });
    /**
     * Dispose of the resources held by the context.
     */
    ClientSession.prototype.dispose = function () {
        if (this._isDisposed) {
            return;
        }
        this._isDisposed = true;
        if (this._session) {
            this._session.dispose();
            this._session = null;
        }
        signaling_1.Signal.clearData(this);
    };
    /**
     * Change the current kernel associated with the document.
     */
    ClientSession.prototype.changeKernel = function (options) {
        var _this = this;
        return this.ready.then(function () {
            if (_this.isDisposed) {
                return;
            }
            return _this._changeKernel(options);
        });
    };
    /**
     * Select a kernel for the session.
     */
    ClientSession.prototype.selectKernel = function () {
        var _this = this;
        return this.ready.then(function () {
            if (_this.isDisposed) {
                return;
            }
            return _this._selectKernel();
        });
    };
    /**
     * Kill the kernel and shutdown the session.
     *
     * @returns A promise that resolves when the session is shut down.
     */
    ClientSession.prototype.shutdown = function () {
        if (this.isDisposed || !this._session) {
            return Promise.resolve(void 0);
        }
        var session = this._session;
        this._session = null;
        if (session) {
            return session.shutdown();
        }
    };
    /**
     * Restart the session.
     *
     * @returns A promise that resolves with the kernel model.
     *
     * #### Notes
     * If there is a running kernel, present a dialog.
     * If there is no kernel, we start a kernel with the last run
     * kernel name.
     * If no kernel has been started, this is a no-op.
     */
    ClientSession.prototype.restart = function () {
        var _this = this;
        return this.ready.then(function () {
            if (_this.isDisposed) {
                return;
            }
            var kernel = _this.kernel;
            if (!kernel) {
                if (_this._prevKernelName) {
                    return _this.changeKernel({ name: _this._prevKernelName });
                }
                // Bail if there is no previous kernel to start.
                return;
            }
            return ClientSession.restartKernel(kernel);
        });
    };
    /**
     * Change the session path.
     *
     * @param path - The new session path.
     *
     * @returns A promise that resolves when the session has renamed.
     *
     * #### Notes
     * This uses the Jupyter REST API, and the response is validated.
     * The promise is fulfilled on a valid response and rejected otherwise.
     */
    ClientSession.prototype.setPath = function (path) {
        if (this.isDisposed || this._path === path) {
            return Promise.resolve(void 0);
        }
        this._path = path;
        this._propertyChanged.emit('path');
        if (this._session) {
            return this._session.rename(path);
        }
        return Promise.resolve(void 0);
    };
    /**
     * Change the session name.
     */
    ClientSession.prototype.setName = function (name) {
        if (this.isDisposed || this._name === name) {
            return Promise.resolve(void 0);
        }
        this._name = name;
        // no-op until supported.
        this._propertyChanged.emit('name');
        return Promise.resolve(void 0);
    };
    /**
     * Change the session type.
     */
    ClientSession.prototype.setType = function (type) {
        if (this.isDisposed || this._type === type) {
            return Promise.resolve(void 0);
        }
        this._type = type;
        // no-op until supported.
        this._propertyChanged.emit('type');
        return Promise.resolve(void 0);
    };
    /**
     * Initialize the session.
     *
     * #### Notes
     * If a server session exists on the current path, we will connect to it.
     * If preferences include disabling `canStart` or `shouldStart`, no
     * server session will be started.
     * If a kernel id is given, we attempt to start a session with that id.
     * If a default kernel is available, we connect to it.
     * Otherwise we ask the user to select a kernel.
     */
    ClientSession.prototype.initialize = function () {
        var _this = this;
        if (this._initializing) {
            return this._ready.promise;
        }
        this._initializing = true;
        var manager = this.manager;
        return manager.ready.then(function () {
            var model = algorithm_1.find(manager.running(), function (item) {
                return item.notebook.path === _this._path;
            });
            if (!model) {
                return;
            }
            return manager.connectTo(model.id).then(function (session) {
                _this._handleNewSession(session);
            }).catch(function (err) {
                _this._handleSessionError(err);
            });
        }).then(function () {
            return _this._startIfNecessary();
        }).then(function () {
            _this._isReady = true;
            _this._ready.resolve(void 0);
        });
    };
    /**
     * Start the session if necessary.
     */
    ClientSession.prototype._startIfNecessary = function () {
        var _this = this;
        var preference = this.kernelPreference;
        if (this.isDisposed ||
            this.kernel || preference.shouldStart === false ||
            preference.canStart === false) {
            return Promise.resolve(void 0);
        }
        // Try to use an existing kernel.
        if (preference.id) {
            return this._changeKernel({ id: preference.id }).then(function () { return void 0; }, function () { return _this._selectKernel(); });
        }
        var name = ClientSession.getDefaultKernel({
            specs: this.manager.specs,
            sessions: this.manager.running(),
            preference: preference
        });
        if (name) {
            return this._changeKernel({ name: name }).then(function () { return void 0; }, function () { return _this._selectKernel(); });
        }
        return this._selectKernel();
    };
    /**
     * Change the kernel.
     */
    ClientSession.prototype._changeKernel = function (options) {
        if (this.isDisposed) {
            return Promise.resolve(void 0);
        }
        var session = this._session;
        if (session) {
            return session.changeKernel(options);
        }
        else {
            return this._startSession(options);
        }
    };
    /**
     * Select a kernel.
     */
    ClientSession.prototype._selectKernel = function () {
        var _this = this;
        if (this.isDisposed) {
            return Promise.resolve(void 0);
        }
        return Private.selectKernel(this).then(function (model) {
            if (_this.isDisposed || model === void 0) {
                return;
            }
            if (model === null && _this._session) {
                return _this.shutdown();
            }
            return _this._changeKernel(model).then(function () { return void 0; });
        }).then(function () { return void 0; });
    };
    /**
     * Start a session and set up its signals.
     */
    ClientSession.prototype._startSession = function (model) {
        var _this = this;
        if (this.isDisposed) {
            return Promise.resolve(void 0);
        }
        return this.manager.startNew({
            path: this._path,
            kernelName: model.name,
            kernelId: model.id
        }).then(function (session) { return _this._handleNewSession(session); })
            .catch(function (err) { return _this._handleSessionError(err); });
    };
    /**
     * Handle a new session object.
     */
    ClientSession.prototype._handleNewSession = function (session) {
        if (this.isDisposed) {
            return null;
        }
        if (this._session) {
            this._session.dispose();
        }
        this._session = session;
        this._onPathChanged(session, session.path);
        session.terminated.connect(this._onTerminated, this);
        session.pathChanged.connect(this._onPathChanged, this);
        session.kernelChanged.connect(this._onKernelChanged, this);
        session.statusChanged.connect(this._onStatusChanged, this);
        session.iopubMessage.connect(this._onIopubMessage, this);
        session.unhandledMessage.connect(this._onUnhandledMessage, this);
        this._kernelChanged.emit(session.kernel);
        this._prevKernelName = session.kernel.name;
        return session.kernel;
    };
    /**
     * Handle an error in session startup.
     */
    ClientSession.prototype._handleSessionError = function (err) {
        var response = String(err.xhr.response);
        try {
            response = JSON.parse(err.xhr.response)['traceback'];
        }
        catch (err) {
            // no-op
        }
        var body = document.createElement('pre');
        body.textContent = response;
        return _1.showDialog({
            title: 'Error Starting Kernel',
            body: body,
            buttons: [_1.Dialog.okButton()]
        }).then(function () { return void 0; });
    };
    /**
     * Handle a session termination.
     */
    ClientSession.prototype._onTerminated = function () {
        if (this._session) {
            this._session.dispose();
        }
        this._session = null;
        this._terminated.emit(void 0);
    };
    /**
     * Handle a change to a session path.
     */
    ClientSession.prototype._onPathChanged = function (sender, path) {
        if (path !== this._path) {
            this._path = path;
            this._propertyChanged.emit('path');
        }
    };
    /**
     * Handle a change to the kernel.
     */
    ClientSession.prototype._onKernelChanged = function (sender) {
        this._kernelChanged.emit(sender.kernel);
    };
    /**
     * Handle a change to the session status.
     */
    ClientSession.prototype._onStatusChanged = function () {
        this._statusChanged.emit(this.status);
    };
    /**
     * Handle an iopub message.
     */
    ClientSession.prototype._onIopubMessage = function (sender, message) {
        this._iopubMessage.emit(message);
    };
    /**
     * Handle an unhandled message.
     */
    ClientSession.prototype._onUnhandledMessage = function (sender, message) {
        this._unhandledMessage.emit(message);
    };
    return ClientSession;
}());
exports.ClientSession = ClientSession;
/**
 * A namespace for `ClientSession` statics.
 */
(function (ClientSession) {
    /**
     * Restart a kernel if the user accepts the risk.
     */
    function restartKernel(kernel) {
        var restartBtn = _1.Dialog.warnButton({ label: 'RESTART ' });
        return _1.showDialog({
            title: 'Restart Kernel?',
            body: 'Do you want to restart the current kernel? All variables will be lost.',
            buttons: [_1.Dialog.cancelButton(), restartBtn]
        }).then(function (result) {
            if (kernel.isDisposed) {
                return null;
            }
            if (result.accept) {
                return kernel.restart().then(function () {
                    return kernel;
                });
            }
            return kernel;
        });
    }
    ClientSession.restartKernel = restartKernel;
    /**
     * Get the default kernel name given select options.
     */
    function getDefaultKernel(options) {
        return Private.getDefaultKernel(options);
    }
    ClientSession.getDefaultKernel = getDefaultKernel;
    /**
     * Populate a kernel dropdown list.
     *
     * @param node - The node to populate.
     *
     * @param options - The options used to populate the kernels.
     *
     * #### Notes
     * Populates the list with separated sections:
     *   - Kernels matching the preferred language (display names).
     *   - "None" signifying no kernel.
     *   - The remaining kernels.
     *   - Sessions matching the preferred language (file names).
     *   - The remaining sessions.
     * If no preferred language is given or no kernels are found using
     * the preferred language, the default kernel is used in the first
     * section.  Kernels are sorted by display name.  Sessions display the
     * base name of the file with an ellipsis overflow and a tooltip with
     * the explicit session information.
     */
    function populateKernelSelect(node, options) {
        return Private.populateKernelSelect(node, options);
    }
    ClientSession.populateKernelSelect = populateKernelSelect;
})(ClientSession = exports.ClientSession || (exports.ClientSession = {}));
exports.ClientSession = ClientSession;
/**
 * The namespace for module private data.
 */
var Private;
(function (Private) {
    /**
     * Select a kernel for the session.
     */
    function selectKernel(session) {
        // Create the dialog body.
        var body = document.createElement('div');
        var text = document.createElement('label');
        text.innerHTML = "Select kernel for: \"" + session.name + "\"";
        body.appendChild(text);
        var options = getKernelSearch(session);
        var selector = document.createElement('select');
        ClientSession.populateKernelSelect(selector, options);
        body.appendChild(selector);
        var select = _1.Dialog.okButton({ label: 'SELECT' });
        return _1.showDialog({
            title: 'Select Kernel',
            body: body,
            buttons: [_1.Dialog.cancelButton(), select]
        }).then(function (result) {
            if (!result.accept) {
                return void 0;
            }
            return JSON.parse(selector.value);
        });
    }
    Private.selectKernel = selectKernel;
    /**
     * Get the default kernel name given select options.
     */
    function getDefaultKernel(options) {
        var specs = options.specs, preference = options.preference;
        var name = preference.name, language = preference.language, shouldStart = preference.shouldStart, canStart = preference.canStart;
        if (shouldStart === false || canStart === false) {
            return null;
        }
        if (!name && !language) {
            return null;
        }
        // Look for an exact match of a spec name.
        for (var specName in specs.kernelspecs) {
            if (specName === name) {
                return name;
            }
        }
        // Bail if there is no language.
        if (!language) {
            return null;
        }
        // Check for a single kernel matching the language.
        var matches = [];
        for (var specName in specs.kernelspecs) {
            var kernelLanguage = specs.kernelspecs[specName].language;
            if (language === kernelLanguage) {
                matches.push(specName);
            }
        }
        if (matches.length === 1) {
            var specName = matches[0];
            console.log('No exact match found for ' + specName +
                ', using kernel ' + specName + ' that matches ' +
                'language=' + language);
            return specName;
        }
        // No matches found.
        return null;
    }
    Private.getDefaultKernel = getDefaultKernel;
    /**
     * Populate a kernel select node for the session.
     */
    function populateKernelSelect(node, options) {
        while (node.firstChild) {
            node.removeChild(node.firstChild);
        }
        var maxLength = 10;
        var preference = options.preference, sessions = options.sessions, specs = options.specs;
        var name = preference.name, id = preference.id, language = preference.language, canStart = preference.canStart, shouldStart = preference.shouldStart;
        if (canStart === false) {
            node.appendChild(optionForNone());
            node.value = 'null';
            node.disabled = true;
            return;
        }
        node.disabled = false;
        // Create mappings of display names and languages for kernel name.
        var displayNames = Object.create(null);
        var languages = Object.create(null);
        for (var name_1 in specs.kernelspecs) {
            var spec = specs.kernelspecs[name_1];
            displayNames[name_1] = spec.display_name;
            maxLength = Math.max(maxLength, displayNames[name_1].length);
            languages[name_1] = spec.language;
        }
        // Handle a kernel by name.
        var names = [];
        if (name && name in specs.kernelspecs) {
            names.push(name);
        }
        // Then look by language.
        if (language) {
            for (var specName in specs.kernelspecs) {
                if (name !== specName && languages[specName] === language) {
                    names.push(name);
                }
            }
        }
        // Use the default kernel if no kernels were found.
        if (!names.length) {
            names.push(specs.default);
        }
        // Handle a preferred kernels in order of display name.
        var preferred = document.createElement('optgroup');
        preferred.label = 'Start Preferred Kernel';
        names.sort(function (a, b) { return displayNames[a].localeCompare(displayNames[b]); });
        for (var _i = 0, names_1 = names; _i < names_1.length; _i++) {
            var name_2 = names_1[_i];
            preferred.appendChild(optionForName(name_2, displayNames[name_2]));
        }
        if (preferred.firstChild) {
            node.appendChild(preferred);
        }
        // Add an option for no kernel
        node.appendChild(optionForNone());
        var other = document.createElement('optgroup');
        other.label = 'Start Other Kernel';
        // Add the rest of the kernel names in alphabetical order.
        var otherNames = [];
        for (var specName in specs.kernelspecs) {
            if (names.indexOf(specName) !== -1) {
                continue;
            }
            otherNames.push(specName);
        }
        otherNames.sort(function (a, b) { return displayNames[a].localeCompare(displayNames[b]); });
        for (var _a = 0, otherNames_1 = otherNames; _a < otherNames_1.length; _a++) {
            var otherName = otherNames_1[_a];
            other.appendChild(optionForName(otherName, displayNames[otherName]));
        }
        // Add a separator option if there were any other names.
        if (otherNames.length) {
            node.appendChild(other);
        }
        // Handle the default value.
        if (shouldStart === false) {
            node.value = 'null';
        }
        else {
            node.selectedIndex = 0;
        }
        // Bail if there are no sessions.
        if (!sessions) {
            return;
        }
        // Add the sessions using the preferred language first.
        var matchingSessions = [];
        var otherSessions = [];
        algorithm_1.each(sessions, function (session) {
            if (language &&
                languages[session.kernel.name] === language &&
                session.kernel.id !== id) {
                matchingSessions.push(session);
            }
            else if (session.kernel.id !== id) {
                otherSessions.push(session);
            }
        });
        var matching = document.createElement('optgroup');
        matching.label = 'Use Kernel from Preferred Session';
        node.appendChild(matching);
        if (matchingSessions.length) {
            matchingSessions.sort(function (a, b) {
                return a.notebook.path.localeCompare(b.notebook.path);
            });
            algorithm_1.each(matchingSessions, function (session) {
                var name = displayNames[session.kernel.name];
                matching.appendChild(optionForSession(session, name, maxLength));
            });
        }
        var otherSessionsNode = document.createElement('optgroup');
        otherSessionsNode.label = 'Use Kernel from Other Session';
        node.appendChild(otherSessionsNode);
        if (otherSessions.length) {
            otherSessions.sort(function (a, b) {
                return a.notebook.path.localeCompare(b.notebook.path);
            });
            algorithm_1.each(otherSessions, function (session) {
                var name = displayNames[session.kernel.name] || session.kernel.name;
                otherSessionsNode.appendChild(optionForSession(session, name, maxLength));
            });
        }
    }
    Private.populateKernelSelect = populateKernelSelect;
    /**
     * Get the kernel search options given a client session and sesion manager.
     */
    function getKernelSearch(session) {
        return {
            specs: session.manager.specs,
            sessions: session.manager.running(),
            preference: session.kernelPreference
        };
    }
    /**
     * Create an option element for a kernel name.
     */
    function optionForName(name, displayName) {
        var option = document.createElement('option');
        option.text = displayName;
        option.value = JSON.stringify({ name: name });
        return option;
    }
    /**
     * Create an option for no kernel.
     */
    function optionForNone() {
        var group = document.createElement('optgroup');
        group.label = 'Use No Kernel';
        var option = document.createElement('option');
        option.text = 'No Kernel';
        option.value = 'null';
        group.appendChild(option);
        return group;
    }
    /**
     * Create an option element for a session.
     */
    function optionForSession(session, displayName, maxLength) {
        var option = document.createElement('option');
        var sessionName = session.notebook.path.split('/').pop();
        var CONSOLE_REGEX = /^console-(\d)+-[0-9a-f]+$/;
        if (CONSOLE_REGEX.test(sessionName)) {
            sessionName = "Console " + sessionName.match(CONSOLE_REGEX)[1];
        }
        if (sessionName.length > maxLength) {
            sessionName = sessionName.slice(0, maxLength - 3) + '...';
        }
        option.text = sessionName;
        option.value = JSON.stringify({ id: session.kernel.id });
        option.title = "Path: " + session.notebook.path + "\n" +
            ("Kernel Name: " + displayName + "\n") +
            ("Kernel Id: " + session.kernel.id);
        return option;
    }
})(Private || (Private = {}));

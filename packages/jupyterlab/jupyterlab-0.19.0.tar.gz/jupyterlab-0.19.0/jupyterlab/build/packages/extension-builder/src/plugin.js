// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var path = require("path");
/**
 * A WebPack plugin that generates custom bundles that use version and
 * semver-mangled require semantics.
 */
var JupyterLabPlugin = (function () {
    /**
     * Construct a new JupyterLabPlugin.
     */
    function JupyterLabPlugin(options) {
        this._name = '';
        this._publicPath = '';
        options = options || {};
        this._name = options.name || 'jupyter';
    }
    /**
     * Plugin installation, called by WebPack.
     *
     * @param compiler - The WebPack compiler object.
     */
    JupyterLabPlugin.prototype.apply = function (compiler) {
        var publicPath = compiler.options.output.publicPath;
        if (!publicPath) {
            throw new Error('Must define a public path');
        }
        if (publicPath[publicPath.length - 1] !== '/') {
            publicPath += '/';
        }
        this._publicPath = publicPath;
        // Notes
        // We use the emit phase because it allows other plugins to act on the
        // output first.
        // We can't replace the module ids during compilation, because there are
        // places in the compilation that assume a numeric id.
        compiler.plugin('emit', this._onEmit.bind(this));
    };
    JupyterLabPlugin.prototype._onEmit = function (compilation, callback) {
        var _this = this;
        // Explore each chunk (build output):
        compilation.chunks.forEach(function (chunk) {
            var sources = [];
            // A mapping for each module name and its dependencies.
            var modules = {};
            // Explore each module within the chunk (built inputs):
            chunk.modules.forEach(function (mod) {
                // We don't allow externals.
                if (mod.external) {
                    throw Error("Cannot use externals: " + mod.userRequest);
                }
                // Parse each module.
                var source = _this._parseModule(compilation, mod);
                sources.push(source);
                // Add dependencies to the manifest.
                var deps = [];
                for (var i = 0; i < mod.dependencies.length; i++) {
                    var dep = mod.dependencies[i];
                    if (dep.module && dep.module.id && dep.module.id !== mod.id) {
                        deps.push(Private.getRequirePath(mod, dep.module));
                    }
                }
                modules[Private.getDefinePath(mod)] = deps;
            });
            var code = sources.join('\n\n');
            // Replace the original chunk file.
            // Use the first file name, because the mangling of the chunk
            // file names are private to WebPack.
            var fileName = chunk.files[0];
            compilation.assets[fileName] = {
                source: function () {
                    return code;
                },
                size: function () {
                    return code.length;
                }
            };
            // Create a manifest for the chunk.
            var manifest = {};
            if (chunk.entryModule) {
                manifest['entry'] = Private.getDefinePath(chunk.entryModule);
            }
            manifest['hash'] = chunk.hash;
            manifest['id'] = chunk.id;
            manifest['name'] = chunk.name || chunk.id;
            manifest['files'] = chunk.files;
            manifest['modules'] = modules;
            var manifestSource = JSON.stringify(manifest, null, '\t');
            compilation.assets[fileName + ".manifest"] = {
                source: function () {
                    return manifestSource;
                },
                size: function () {
                    return manifestSource.length;
                }
            };
        });
        callback();
    };
    /**
     * Parse a WebPack module to generate a custom version.
     *
     * @param compilation - The Webpack compilation object.
     *
     * @param module - A parsed WebPack module object.
     *
     * @returns The new module contents.
     */
    JupyterLabPlugin.prototype._parseModule = function (compilation, mod) {
        var pluginName = this._name;
        var publicPath = this._publicPath;
        var requireName = "__" + pluginName + "_require__";
        // There is no public API in WebPack to get the raw module source
        // The method used below is known to work in almost all cases
        // The base prototype of the module source() method takes no arguments,
        // but the normal module source() takes three arguments and is intended
        // to be called by its module factory.
        // We can call the normal module source() because it has already been
        // run in the compilation process and will return the cached value,
        // without relying on the provided arguments.
        // https://github.com/webpack/webpack/blob/a53799c0ac58983860a27648cdc8519b6a562b89/lib/NormalModule.js#L224-L229
        var source = mod.source().source();
        // Regular modules.
        if (mod.userRequest) {
            // Handle ensure blocks with and without inline comments.
            // From WebPack dependencies/DepBlockHelpers
            source = this._handleEnsure(compilation, source, /__webpack_require__.e\/\*.*?\*\/\((\d+)/);
            source = this._handleEnsure(compilation, source, /__webpack_require__.e\((\d+)/);
            // Replace the require statements with the semver-mangled name.
            var deps = Private.getAllModuleDependencies(mod);
            for (var i = 0; i < deps.length; i++) {
                var dep = deps[i];
                var target = "__webpack_require__(" + dep.id + ")";
                var modPath = Private.getRequirePath(mod, dep);
                var replacer = "__webpack_require__('" + modPath + "')";
                source = source.split(target).join(replacer);
            }
            // Context modules.
        }
        else if (mod.context) {
            // Context modules have to be assembled ourselves
            // because they are not clearly delimited in the text.
            source = Private.createContextModule(mod);
            source = source.split('webpackContext').join(pluginName + "Context");
        }
        // Handle public requires.
        var requireP = '__webpack_require__.p +';
        var newRequireP = "'" + publicPath + "' +";
        source = source.split(requireP).join(newRequireP);
        // Replace the require name with the custom one.
        source = source.split('__webpack_require__').join(requireName);
        // Handle ES6 exports
        source = source.split('__webpack_exports__').join('exports');
        // Create our header and footer with a version-mangled defined name.
        var definePath = Private.getDefinePath(mod);
        var header = "/** START DEFINE BLOCK for " + definePath + " **/\n" + pluginName + ".define('" + definePath + "', function (module, exports, " + requireName + ") {\n\t";
        var footer = "\n})\n/** END DEFINE BLOCK for " + definePath + " **/\n";
        // Combine code and indent.
        return header + source.split('\n').join('\n\t') + footer;
    };
    /**
     * Handle an ensure block.
     *
     * @param compilation - The Webpack compilation object.
     *
     * @param source - The raw module source.
     *
     * @param publicPath - The public path of the plugin.
     *
     * @param regex - The ensure block regex.
     *
     * @returns The new ensure block contents.
     */
    JupyterLabPlugin.prototype._handleEnsure = function (compilation, source, regex) {
        var publicPath = this._publicPath;
        var _loop_1 = function () {
            var match = source.match(regex);
            var chunkId = match[1];
            var fileName = '';
            // Use the first file name, because the mangling of the chunk
            // file name is private to WebPack.
            compilation.chunks.forEach(function (chunk) {
                if (String(chunk.id) === chunkId) {
                    fileName = chunk.files[0];
                }
            });
            var replacement = "__webpack_require__.e('" + publicPath + fileName + "'";
            source = source.replace(regex, replacement);
        };
        while (regex.test(source)) {
            _loop_1();
        }
        return source;
    };
    return JupyterLabPlugin;
}());
exports.JupyterLabPlugin = JupyterLabPlugin;
/**
 * A namespace for module private data.
 */
var Private;
(function (Private) {
    /**
     * Get the define path for a WebPack module.
     *
     * @param module - A parsed WebPack module object.
     *
     * @returns A version-mangled define path for the module.
     *    For example, 'foo@1.0.1/lib/bar/baz.js'.
     */
    function getDefinePath(mod) {
        if (!mod.context) {
            return '__ignored__';
        }
        var request = mod.userRequest || mod.context;
        var parts = request.split('!');
        var names = [];
        for (var i = 0; i < parts.length; i++) {
            names.push(getModuleVersionPath(parts[i]));
        }
        return names.join('!');
    }
    Private.getDefinePath = getDefinePath;
    /**
     * Get the require path for a WebPack module.
     *
     * @param mod - A parsed WebPack module that is requiring a dependency.
     * @param dep - A parsed WebPack module object representing the dependency.
     *
     * @returns A semver-mangled define path for the dependency.
     *    For example, 'foo@^1.0.0/lib/bar/baz.js'.
     */
    function getRequirePath(mod, dep) {
        if (!dep.context) {
            return '__ignored__';
        }
        var issuer = mod.userRequest || mod.context;
        var request = dep.userRequest || dep.context;
        var requestParts = request.split('!');
        var parts = [];
        // Handle the loaders.
        for (var i = 0; i < requestParts.length - 1; i++) {
            parts.push(getModuleSemverPath(requestParts[i], requestParts[i]));
        }
        // Handle the last part.
        var base = requestParts[requestParts.length - 1];
        parts.push(getModuleSemverPath(base, issuer));
        return parts.join('!');
    }
    Private.getRequirePath = getRequirePath;
    /**
     * Create custom context module source.
     *
     * @param module - A parsed WebPack module object.
     *
     * @returns The new contents of the context module output.
     */
    function createContextModule(mod) {
        // Modeled after Webpack's ContextModule.js.
        var map = {};
        var dependencies = mod.dependencies || [];
        dependencies.slice().sort(function (a, b) {
            if (a.userRequest === b.userRequest) {
                return 0;
            }
            return a.userRequest < b.userRequest ? -1 : 1;
        }).forEach(function (dep) {
            if (dep.module) {
                map[dep.userRequest] = getRequirePath(mod, dep.module);
            }
        });
        var mapString = JSON.stringify(map, null, '\t');
        return generateContextModule(mapString, getDefinePath(mod));
    }
    Private.createContextModule = createContextModule;
    /**
     * Get all of the module dependencies for a module.
     */
    function getAllModuleDependencies(mod) {
        // Extracted from https://github.com/webpack/webpack/blob/ee1b8c43b474b22a20bfc25daf0ee153dfb2ef9f/lib/NormalModule.js#L227
        var list = [];
        function doDep(dep) {
            if (dep.module && list.indexOf(dep.module) < 0) {
                list.push(dep.module);
            }
        }
        function doVariable(variable) {
            variable.dependencies.forEach(doDep);
        }
        function doBlock(block) {
            block.variables.forEach(doVariable);
            block.dependencies.forEach(doDep);
            block.blocks.forEach(doBlock);
        }
        doBlock(mod);
        return list;
    }
    Private.getAllModuleDependencies = getAllModuleDependencies;
    /**
     * Find a package root path from a request.
     *
     * @param request - The request path.
     *
     * @returns The path to the package root.
     */
    function findRoot(request) {
        var orig = request;
        if (path.extname(request)) {
            request = path.dirname(request);
        }
        while (true) {
            try {
                var pkgPath = require.resolve(path.join(request, 'package.json'));
                var pkg = require(pkgPath);
                // Use public packages except for the local package.
                if (!pkg.private || request === process.cwd()) {
                    return request;
                }
            }
            catch (err) {
                // no-op
            }
            var prev = request;
            request = path.dirname(request);
            if (request === prev) {
                throw Error("Could not find package for " + orig);
            }
        }
    }
    /**
     * Get the package.json associated with a file.
     *
     * @param request - The request path.
     *
     * @returns The package.json object for the package.
     */
    function getPackage(request) {
        var rootPath = findRoot(request);
        return require(path.join(rootPath, 'package.json'));
    }
    /**
     * Get a mangled path for a path using the exact version.
     *
     * @param modPath - The absolute path of the module.
     *
     * @returns A version-mangled path (e.g. 'foo@1.0.0/lib/bar/baz.js')
     */
    function getModuleVersionPath(modPath) {
        var rootPath = findRoot(modPath);
        var pkg = getPackage(rootPath);
        modPath = modPath.slice(rootPath.length + 1);
        var name = pkg.name + "@" + pkg.version;
        if (modPath) {
            modPath = modPath.split(path.sep).join('/');
            name += "/" + modPath;
        }
        return name;
    }
    /**
     * Get the semver-mangled path for a request.
     *
     * @param request - The requested module path.
     *
     * @param issuer - The path of the issuer of the module request.
     *
     * @returns A semver-mangled path (e.g. 'foo@^1.0.0/lib/bar/baz.js')
     *
     * #### Notes
     * Files in the same package are locked to the exact version number
     * of the package. Files in local packages (i.e., `file://` packages) are
     * allowed to vary by patch number (the `~` semver range specifier is added).
     */
    function getModuleSemverPath(request, issuer) {
        var rootPath = findRoot(request);
        var rootPackage = getPackage(rootPath);
        var issuerPackage = getPackage(issuer);
        var modPath = request.slice(rootPath.length + 1);
        var name = rootPackage.name;
        var semver = ((issuerPackage.dependencies &&
            issuerPackage.dependencies[name]) || rootPackage.version);
        if (issuerPackage.name === rootPackage.name) {
            semver = "" + rootPackage.version;
        }
        else if (semver.indexOf('file:') === 0) {
            var sourcePath = path.resolve(rootPath, semver.slice('file:'.length));
            var sourcePackage = getPackage(sourcePath);
            // Allow patch version increments of local packages.
            semver = "~" + sourcePackage.version;
        }
        var id = name + "@" + semver;
        if (modPath) {
            modPath = modPath.split(path.sep).join('/');
            id += "/" + modPath;
        }
        return id;
    }
    /**
     * Generate a context module given a mapping and an id.
     */
    function generateContextModule(mapString, id) {
        return "\n      var map = " + mapString + ";\n      function webpackContext(req) {\n        return __webpack_require__(webpackContextResolve(req));\n      };\n      function webpackContextResolve(req) {\n        return map[req] || (function() { throw new Error(\"Cannot find module '\" + req + \"'.\") }());\n      };\n      webpackContext.keys = function webpackContextKeys() {\n        return Object.keys(map);\n      };\n      webpackContext.resolve = webpackContextResolve;\n      module.exports = webpackContext;\n      webpackContext.id = \"" + id + "\";\n    ";
    }
})(Private || (Private = {}));

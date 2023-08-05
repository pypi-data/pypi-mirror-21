// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var ExtractTextPlugin = require("extract-text-webpack-plugin");
var path = require("path");
var webpack = require("webpack");
var webpack_config_1 = require("webpack-config");
var plugin_1 = require("./plugin");
/**
 * The default file loaders.
 */
var DEFAULT_LOADERS = [
    { test: /\.json$/, use: 'json-loader' },
    { test: /\.html$/, use: 'file-loader' },
    { test: /\.(jpg|png|gif)$/, use: 'file-loader' },
    { test: /\.js.map$/, use: 'file-loader' },
    { test: /\.woff2(\?v=\d+\.\d+\.\d+)?$/, use: 'url-loader?limit=10000&mimetype=application/font-woff' },
    { test: /\.woff(\?v=\d+\.\d+\.\d+)?$/, use: 'url-loader?limit=10000&mimetype=application/font-woff' },
    { test: /\.ttf(\?v=\d+\.\d+\.\d+)?$/, use: 'url-loader?limit=10000&mimetype=application/octet-stream' },
    { test: /\.eot(\?v=\d+\.\d+\.\d+)?$/, use: 'file-loader' },
    { test: /\.svg(\?v=\d+\.\d+\.\d+)?$/, use: 'url-loader?limit=10000&mimetype=image/svg+xml' }
];
/**
 * Build a JupyterLab extension.
 *
 * @param options - The options used to build the extension.
 */
function buildExtension(options) {
    var name = options.name;
    if (!name) {
        throw Error('Must specify a name for the extension');
    }
    if (!options.entry) {
        throw Error('Must specify an entry module');
    }
    if (!options.outputDir) {
        throw Error('Must specify an output directory');
    }
    // Create the named entry point to the entryPath.
    var entry = {};
    entry[name] = options.entry;
    var config = new webpack_config_1.Config().merge({
        // The default options.
        entry: entry,
        output: {
            path: path.resolve(options.outputDir),
            filename: '[name].bundle.js',
            publicPath: "labextension/" + name
        },
        node: {
            fs: 'empty'
        },
        bail: true,
        plugins: [new plugin_1.JupyterLabPlugin()]
        // Add the override options.
    }).merge(options.config || {});
    // Add the CSS extractors unless explicitly told otherwise.
    if (options.extractCSS !== false) {
        // Note that we have to use an explicit local public path
        // otherwise the urls in the extracted CSS will point to the wrong
        // location.
        // See https://github.com/webpack-contrib/extract-text-webpack-plugin/tree/75cb09eed13d15cec8f974b1210920a7f249f8e2
        var cssLoader = ExtractTextPlugin.extract({
            use: 'css-loader',
            fallback: 'style-loader',
            publicPath: './'
        });
        config.merge({
            module: {
                rules: [
                    {
                        test: /\.css$/,
                        use: cssLoader
                    }
                ]
            },
            plugins: [new ExtractTextPlugin('[name].css')]
        });
    }
    // Add the rest of the default loaders unless explicitly told otherwise.
    if (options.useDefaultLoaders !== false) {
        config.merge({
            module: {
                rules: DEFAULT_LOADERS
            }
        });
    }
    // Set up and run the WebPack compilation.
    var compiler = webpack(config);
    compiler.name = name;
    return new Promise(function (resolve, reject) {
        compiler.run(function (err, stats) {
            if (err) {
                console.error(err.stack || err);
                if (err.details) {
                    console.error(err.details);
                }
                reject(err);
            }
            else {
                console.log("\n\nSuccessfully built \"" + name + "\":\n");
                process.stdout.write(stats.toString({
                    chunks: true,
                    modules: false,
                    chunkModules: false,
                    colors: require('supports-color')
                }) + '\n');
                resolve();
            }
        });
    });
}
exports.buildExtension = buildExtension;

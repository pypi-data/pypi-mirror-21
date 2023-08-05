import * as webpack from 'webpack';
/**
 * A WebPack plugin that generates custom bundles that use version and
 * semver-mangled require semantics.
 */
export declare class JupyterLabPlugin {
    /**
     * Construct a new JupyterLabPlugin.
     */
    constructor(options?: JupyterLabPlugin.IOptions);
    /**
     * Plugin installation, called by WebPack.
     *
     * @param compiler - The WebPack compiler object.
     */
    apply(compiler: webpack.compiler.Compiler): void;
    private _onEmit(compilation, callback);
    /**
     * Parse a WebPack module to generate a custom version.
     *
     * @param compilation - The Webpack compilation object.
     *
     * @param module - A parsed WebPack module object.
     *
     * @returns The new module contents.
     */
    private _parseModule(compilation, mod);
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
    private _handleEnsure(compilation, source, regex);
    private _name;
    private _publicPath;
}
/**
 * A namespace for `JupyterLabPlugin` statics.
 */
export declare namespace JupyterLabPlugin {
    interface IOptions {
        /**
         * The name of the plugin.
         */
        name?: string;
    }
}

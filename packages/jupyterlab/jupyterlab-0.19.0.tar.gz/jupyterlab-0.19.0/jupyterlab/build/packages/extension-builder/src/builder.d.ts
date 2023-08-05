import * as webpack from 'webpack';
/**
 * Build a JupyterLab extension.
 *
 * @param options - The options used to build the extension.
 */
export declare function buildExtension(options: IBuildOptions): Promise<void>;
/**
 * The options used to build a JupyterLab extension.
 */
export interface IBuildOptions {
    /**
     * The name of the extension.
     */
    name: string;
    /**
     * The module to load as the entry point.
     *
     * The module should export a plugin configuration or array of
     * plugin configurations.
     */
    entry: string;
    /**
     * The directory in which to put the generated bundle files.
     *
     * Relative directories are resolved relative to the current
     * working directory of the process.
     */
    outputDir: string;
    /**
     * Whether to extract CSS from the bundles (default is True).
     *
     * Note: no other CSS loaders should be used if not set to False.
     */
    extractCSS?: boolean;
    /**
     * Whether to use the default loaders for some common file types.
     *
     * See [[DEFAULT_LOADERS]].  The default is True.
     */
    useDefaultLoaders?: boolean;
    /**
     * Extra webpack configuration.
     */
    config?: webpack.Configuration;
}

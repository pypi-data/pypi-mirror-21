import { Application, IPlugin } from '@phosphor/application';
import { ModuleLoader } from './loader';
import { ApplicationShell } from './shell';
export { ModuleLoader } from './loader';
export { ApplicationShell } from './shell';
/**
 * The type for all JupyterLab plugins.
 */
export declare type JupyterLabPlugin<T> = IPlugin<JupyterLab, T>;
/**
 * JupyterLab is the main application class. It is instantiated once and shared.
 */
export declare class JupyterLab extends Application<ApplicationShell> {
    /**
     * Construct a new JupyterLab object.
     */
    constructor(options?: JupyterLab.IOptions);
    /**
     * The information about the application.
     */
    readonly info: JupyterLab.IInfo;
    /**
     * The module loader used by the application.
     */
    readonly loader: ModuleLoader | null;
    /**
     * Promise that resolves when state is restored, returning layout description.
     *
     * #### Notes
     * This is just a reference to `shell.restored`.
     */
    readonly restored: Promise<ApplicationShell.ILayout>;
    /**
     * Register plugins from a plugin module.
     *
     * @param mod - The plugin module to register.
     */
    registerPluginModule(mod: JupyterLab.IPluginModule): void;
    /**
     * Register the plugins from multiple plugin modules.
     *
     * @param mods - The plugin modules to register.
     */
    registerPluginModules(mods: JupyterLab.IPluginModule[]): void;
    private _info;
    private _loader;
}
/**
 * The namespace for `JupyterLab` class statics.
 */
export declare namespace JupyterLab {
    /**
     * The options used to initialize a JupyterLab object.
     */
    interface IOptions {
        /**
         * The git description of the JupyterLab application.
         */
        gitDescription?: string;
        /**
         * The module loader used by the application.
         */
        loader?: ModuleLoader;
        /**
         * The namespace/prefix plugins may use to denote their origin.
         *
         * #### Notes
         * This field may be used by persistent storage mechanisms such as state
         * databases, cookies, session storage, etc.
         *
         * If unspecified, the default value is `'jupyterlab'`.
         */
        namespace?: string;
        /**
         * The version of the JupyterLab application.
         */
        version?: string;
    }
    /**
     * The information about a JupyterLab application.
     */
    interface IInfo {
        /**
         * The git description of the JupyterLab application.
         */
        readonly gitDescription: string;
        /**
         * The namespace/prefix plugins may use to denote their origin.
         */
        readonly namespace: string;
        /**
         * The version of the JupyterLab application.
         */
        readonly version: string;
    }
    /**
     * The interface for a module that exports a plugin or plugins as
     * the default value.
     */
    interface IPluginModule {
        /**
         * The default export.
         */
        default: JupyterLabPlugin<any> | JupyterLabPlugin<any>[];
    }
}

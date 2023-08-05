import { ModuleLoader } from '@jupyterlab/application';
/**
 * Define a module that can be synchronously required.
 *
 * @param path - The version-mangled fully qualified path of the module.
 *   For example, "foo@1.0.1/lib/bar/baz.js".
 *
 * @param callback - The callback function for invoking the module.
 */
export declare function define(path: string, callback: ModuleLoader.DefineCallback): void;
export declare const loader: ModuleLoader;

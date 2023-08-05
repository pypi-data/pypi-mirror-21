import 'es6-promise/auto';
import { JupyterLab, ModuleLoader } from '@jupyterlab/application';
import 'font-awesome/css/font-awesome.min.css';
import '@jupyterlab/default-theme/style/index.css';
/**
 * Create an application object.
 *
 * @param loader - The module loader for the application.
 *
 * @returns A new application object.
 */
export declare function createLab(loader: ModuleLoader): JupyterLab;

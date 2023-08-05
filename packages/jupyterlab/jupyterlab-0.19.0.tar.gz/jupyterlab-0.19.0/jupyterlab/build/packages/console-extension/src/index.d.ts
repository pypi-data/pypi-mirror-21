import { JupyterLabPlugin } from '@jupyterlab/application';
import { IConsoleTracker, ConsolePanel } from '@jupyterlab/console';
/**
 * The console widget tracker provider.
 */
export declare const trackerPlugin: JupyterLabPlugin<IConsoleTracker>;
/**
 * The console widget content factory.
 */
export declare const contentFactoryPlugin: JupyterLabPlugin<ConsolePanel.IContentFactory>;
/**
 * Export the plugins as the default.
 */
declare const plugins: JupyterLabPlugin<any>[];
export default plugins;

import { JupyterLabPlugin } from '@jupyterlab/application';
import { INotebookTracker, NotebookPanel } from '@jupyterlab/notebook';
/**
 * The notebook widget tracker provider.
 */
export declare const trackerPlugin: JupyterLabPlugin<INotebookTracker>;
/**
 * The notebook cell factory provider.
 */
export declare const contentFactoryPlugin: JupyterLabPlugin<NotebookPanel.IContentFactory>;
/**
 * Export the plugins as default.
 */
declare const plugins: JupyterLabPlugin<any>[];
export default plugins;

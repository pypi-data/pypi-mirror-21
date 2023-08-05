import { JupyterLabPlugin } from '@jupyterlab/application';
import { IEditorServices } from '@jupyterlab/codeeditor';
/**
 * The editor services.
 */
export declare const servicesPlugin: JupyterLabPlugin<IEditorServices>;
/**
 * The editor commands.
 */
export declare const commandsPlugin: JupyterLabPlugin<void>;
/**
 * Export the plugins as default.
 */
declare const plugins: JupyterLabPlugin<any>[];
export default plugins;

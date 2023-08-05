import { JupyterLabPlugin } from '@jupyterlab/application';
import { IPathTracker } from '@jupyterlab/filebrowser';
/**
 * The default file browser provider.
 */
declare const plugin: JupyterLabPlugin<IPathTracker>;
export default plugin;

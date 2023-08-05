import { Message } from '@phosphor/messaging';
import { VirtualNode } from '@phosphor/virtualdom';
import { VDomModel, VDomWidget } from '@jupyterlab/apputils';
/**
 * AboutModel holds data which the AboutWidgetwill render.
 */
export declare class AboutModel extends VDomModel {
    /**
     * Create an about model.
     */
    constructor(options: AboutModel.IOptions);
    /**
     * Title of About page.
     */
    readonly title: string;
    /**
     * The current JupyterLab version.
     */
    readonly version: string;
    /**
     * Text on the first page that gives a high level overview of JupyterLab.
     */
    readonly headerText: string[];
    /**
     * Contains the plugin names.
     */
    readonly pluginHeaders: string[];
    /**
     * Description of the main area and its functionality.
     */
    readonly mainAreaDesc: string[];
    /**
     * Description of the file browser and its functionality.
     */
    readonly filebrowserDesc: string[];
    /**
     * Description of the command palette and its functionality.
     */
    readonly commandPaletteDesc: string[];
    /**
     * Description of the notebook and its functionality.
     */
    readonly notebookDesc: string[];
}
/**
 * A namespace for `AboutModel` statics.
 */
export declare namespace AboutModel {
    /**
     * Instantiation options for an about model.
     */
    interface IOptions {
        /**
         * The lab application version.
         */
        version: string;
    }
}
/**
 * A virtual-DOM-based widget for the About plugin.
 */
export declare class AboutWidget extends VDomWidget<AboutModel> {
    /**
     * Handle `'activate-request'` messages.
     */
    protected onActivateRequest(msg: Message): void;
    /**
     * Handle `'close-request'` messages.
     */
    protected onCloseRequest(msg: Message): void;
    /**
     * Render the about plugin to virtual DOM nodes.
     */
    protected render(): VirtualNode;
}

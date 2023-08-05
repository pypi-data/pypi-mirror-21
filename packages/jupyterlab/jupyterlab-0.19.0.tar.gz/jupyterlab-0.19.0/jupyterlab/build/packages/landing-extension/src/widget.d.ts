import { Message } from '@phosphor/messaging';
import { VirtualNode } from '@phosphor/virtualdom';
import { JupyterLab } from '@jupyterlab/application';
import { VDomModel, VDomWidget } from '@jupyterlab/apputils';
/**
 * LandingModel keeps track of the path to working directory and has text data,
 * which the LandingWidget will render.
 */
export declare class LandingModel extends VDomModel {
    /**
     * Preview messages.
     */
    readonly previewMessage: string;
    /**
     * The `Start a new activity` text.
     */
    readonly headerText: string;
    /**
     * The names of activities and their associated commands.
     */
    readonly activities: string[][];
    /**
     * Construct a new landing model.
     */
    constructor(terminalsAvailable?: boolean);
    /**
     * Get the path of the current working directory.
     */
    /**
     * Set the path of the current working directory.
     */
    path: string;
    private _path;
}
/**
 * A virtual-DOM-based widget for the Landing plugin.
 */
export declare class LandingWidget extends VDomWidget<LandingModel> {
    /**
     * Construct a new landing widget.
     */
    constructor(app: JupyterLab);
    /**
     * Handle `'activate-request'` messages.
     */
    protected onActivateRequest(msg: Message): void;
    /**
     * Handle `'close-request'` messages.
     */
    protected onCloseRequest(msg: Message): void;
    /**
     * Render the landing plugin to virtual DOM nodes.
     */
    protected render(): VirtualNode;
    private _app;
}

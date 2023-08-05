import { Message } from '@phosphor/messaging';
import { VirtualNode } from '@phosphor/virtualdom';
import { ICommandLinker, VDomModel, VDomWidget } from '@jupyterlab/apputils';
/**
 * FaqModel holds data which the FaqWidget will render.
 */
export declare class FaqModel extends VDomModel {
    /**
     * Title of the FAQ plugin.
     */
    readonly title: string;
    /**
     * Contain subheadings for each section.
     */
    readonly subheadings: string[];
    /**
     * Contain questions for `the basics` section.
     */
    readonly basicsQuestions: string[];
    /**
     * Contain questions for the `features` section.
     */
    readonly featuresQuestions: string[];
    /**
     * Contain questions for the `developer` section.
     */
    readonly developerQuestions: string[];
}
/**
 * A virtual-DOM-based widget for the FAQ plugin.
 */
export declare class FaqWidget extends VDomWidget<FaqModel> {
    /**
     * Construct a new faq widget.
     */
    constructor(options: FaqWidget.IOptions);
    /**
     * Render the faq plugin to virtual DOM nodes.
     */
    protected render(): VirtualNode[];
    /**
     * Handle `'activate-request'` messages.
     */
    protected onActivateRequest(msg: Message): void;
    /**
     * Handle `'close-request'` messages.
     */
    protected onCloseRequest(msg: Message): void;
    private _linker;
}
/**
 * A namespace for `FaqWidget` statics.
 */
export declare namespace FaqWidget {
    /**
     * Instantiation options for the FAQ widget.
     */
    interface IOptions {
        /**
         * A command linker instance.
         */
        linker: ICommandLinker;
    }
}

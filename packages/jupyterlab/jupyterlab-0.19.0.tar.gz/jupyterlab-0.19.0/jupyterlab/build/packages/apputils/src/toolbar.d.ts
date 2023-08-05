import { IIterator } from '@phosphor/algorithm';
import { Message } from '@phosphor/messaging';
import { Widget } from '@phosphor/widgets';
import { IClientSession } from '.';
/**
 * A class which provides a toolbar widget.
 */
export declare class Toolbar<T extends Widget> extends Widget {
    /**
     * Construct a new toolbar widget.
     */
    constructor();
    /**
     * Get an iterator over the ordered toolbar item names.
     *
     * @returns An iterator over the toolbar item names.
     */
    names(): IIterator<string>;
    /**
     * Add an item to the end of the toolbar.
     *
     * @param name - The name of the widget to add to the toolbar.
     *
     * @param widget - The widget to add to the toolbar.
     *
     * @param index - The optional name of the item to insert after.
     *
     * @returns Whether the item was added to toolbar.  Returns false if
     *   an item of the same name is already in the toolbar.
     */
    addItem(name: string, widget: T): boolean;
    /**
     * Insert an item into the toolbar at the specified index.
     *
     * @param index - The index at which to insert the item.
     *
     * @param name - The name of the item.
     *
     * @param widget - The widget to add.
     *
     * @returns Whether the item was added to the toolbar. Returns false if
     *   an item of the same name is already in the toolbar.
     *
     * #### Notes
     * The index will be clamped to the bounds of the items.
     */
    insertItem(index: number, name: string, widget: T): boolean;
    /**
     * Remove an item in the toolbar by value.
     *
     *  @param name - The name of the widget to remove from the toolbar.
     */
    removeItem(widget: T): void;
    /**
     * Handle the DOM events for the widget.
     *
     * @param event - The DOM event sent to the widget.
     *
     * #### Notes
     * This method implements the DOM `EventListener` interface and is
     * called in response to events on the dock panel's node. It should
     * not be called directly by user code.
     */
    handleEvent(event: Event): void;
    /**
     * Handle `after-attach` messages for the widget.
     */
    protected onAfterAttach(msg: Message): void;
    /**
     * Handle `before-detach` messages for the widget.
     */
    protected onBeforeDetach(msg: Message): void;
}
/**
 * The namespace for Toolbar class statics.
 */
export declare namespace Toolbar {
    /**
     * Create an interrupt toolbar item.
     */
    function createInterruptButton(session: IClientSession): ToolbarButton;
    /**
     * Create a restart toolbar item.
     */
    function createRestartButton(session: IClientSession): ToolbarButton;
    /**
     * Create a kernel name indicator item.
     *
     * #### Notes
     * It will display the `'display_name`' of the current kernel,
     * or `'No Kernel!'` if there is no kernel.
     * It can handle a change in context or kernel.
     */
    function createKernelNameItem(session: IClientSession): Widget;
    /**
     * Create a kernel status indicator item.
     *
     * #### Notes
     * It show display a busy status if the kernel status is
     * not idle.
     * It will show the current status in the node title.
     * It can handle a change to the context or the kernel.
     */
    function createKernelStatusItem(session: IClientSession): Widget;
}
/**
 * A widget which acts as a button in a toolbar.
 */
export declare class ToolbarButton extends Widget {
    /**
     * Construct a new toolbar button.
     */
    constructor(options?: ToolbarButton.IOptions);
    /**
     * Dispose of the resources held by the widget.
     */
    dispose(): void;
    /**
     * Handle the DOM events for the widget.
     *
     * @param event - The DOM event sent to the widget.
     *
     * #### Notes
     * This method implements the DOM `EventListener` interface and is
     * called in response to events on the dock panel's node. It should
     * not be called directly by user code.
     */
    handleEvent(event: Event): void;
    /**
     * Handle `after-attach` messages for the widget.
     */
    protected onAfterAttach(msg: Message): void;
    /**
     * Handle `before-detach` messages for the widget.
     */
    protected onBeforeDetach(msg: Message): void;
    private _onClick;
}
/**
 * A namespace for `ToolbarButton` statics.
 */
export declare namespace ToolbarButton {
    /**
     * The options used to construct a toolbar button.
     */
    interface IOptions {
        /**
         * The callback for a click event.
         */
        onClick?: () => void;
        /**
         * The class name added to the button.
         */
        className?: string;
        /**
         * The tooltip added to the button node.
         */
        tooltip?: string;
    }
}

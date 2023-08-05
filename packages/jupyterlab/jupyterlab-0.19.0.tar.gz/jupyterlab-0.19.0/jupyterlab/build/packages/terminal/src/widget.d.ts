import { TerminalSession } from '@jupyterlab/services';
import { Message } from '@phosphor/messaging';
import { Widget } from '@phosphor/widgets';
/**
 * A widget which manages a terminal session.
 */
export declare class TerminalWidget extends Widget {
    /**
     * Construct a new terminal widget.
     *
     * @param options - The terminal configuration options.
     */
    constructor(options?: TerminalWidget.IOptions);
    /**
     * The terminal session associated with the widget.
     */
    session: TerminalSession.ISession;
    /**
     * Get the font size of the terminal in pixels.
     */
    /**
     * Set the font size of the terminal in pixels.
     */
    fontSize: number;
    /**
     * Get the background color of the terminal.
     */
    /**
     * Set the background color of the terminal.
     */
    background: string;
    /**
     * Get the text color of the terminal.
     */
    /**
     * Set the text color of the terminal.
     */
    color: string;
    /**
     * Dispose of the resources held by the terminal widget.
     */
    dispose(): void;
    /**
     * Refresh the terminal session.
     */
    refresh(): Promise<void>;
    /**
     * Process a message sent to the widget.
     *
     * @param msg - The message sent to the widget.
     *
     * #### Notes
     * Subclasses may reimplement this method as needed.
     */
    processMessage(msg: Message): void;
    /**
     * Set the size of the terminal when attached if dirty.
     */
    protected onAfterAttach(msg: Message): void;
    /**
     * Set the size of the terminal when shown if dirty.
     */
    protected onAfterShow(msg: Message): void;
    /**
     * Dispose of the terminal when closing.
     */
    protected onCloseRequest(msg: Message): void;
    /**
     * On resize, use the computed row and column sizes to resize the terminal.
     */
    protected onResize(msg: Widget.ResizeMessage): void;
    /**
     * A message handler invoked on an `'update-request'` message.
     */
    protected onUpdateRequest(msg: Message): void;
    /**
     * A message handler invoked on an `'fit-request'` message.
     */
    protected onFitRequest(msg: Message): void;
    /**
     * Handle `'activate-request'` messages.
     */
    protected onActivateRequest(msg: Message): void;
    /**
     * Create the terminal object.
     */
    private _initializeTerm();
    /**
     * Handle a message from the terminal session.
     */
    private _onMessage(sender, msg);
    /**
     * Use the dummy terminal to measure the row and column sizes.
     */
    private _snapTermSizing();
    /**
     * Resize the terminal based on computed geometry.
     */
    private _resizeTerminal();
    /**
     * Send the size to the session.
     */
    private _setSessionSize();
    /**
     * Set the stylesheet.
     */
    private _setStyle();
    private _term;
    private _sheet;
    private _dummyTerm;
    private _fontSize;
    private _needsSnap;
    private _needsResize;
    private _needsStyle;
    private _rowHeight;
    private _colWidth;
    private _offsetWidth;
    private _offsetHeight;
    private _sessionSize;
    private _background;
    private _color;
    private _box;
    private _session;
}
/**
 * The namespace for `TerminalWidget` class statics.
 */
export declare namespace TerminalWidget {
    /**
     * Options for the terminal widget.
     */
    interface IOptions {
        /**
         * The font size of the terminal in pixels.
         */
        fontSize?: number;
        /**
         * The background color of the terminal.
         */
        background?: string;
        /**
         * The text color of the terminal.
         */
        color?: string;
        /**
         * Whether to blink the cursor.  Can only be set at startup.
         */
        cursorBlink?: boolean;
    }
    /**
     * The default options used for creating terminals.
     */
    const defaultOptions: IOptions;
}

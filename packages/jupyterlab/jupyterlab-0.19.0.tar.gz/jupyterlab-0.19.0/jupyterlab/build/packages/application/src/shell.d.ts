import { ISignal } from '@phosphor/signaling';
import { DockLayout, FocusTracker, Widget } from '@phosphor/widgets';
/**
 * The application shell for JupyterLab.
 */
export declare class ApplicationShell extends Widget {
    /**
     * Construct a new application shell.
     */
    constructor();
    /**
     * A signal emitted when main area's current focus changes.
     */
    readonly currentChanged: ISignal<this, ApplicationShell.IChangedArgs>;
    /**
     * A signal emitted when main area's active focus changes.
     */
    readonly activeChanged: ISignal<this, ApplicationShell.IChangedArgs>;
    /**
     * The current widget in the shell's main area.
     */
    readonly currentWidget: Widget | null;
    /**
     * The active widget in the shell's main area.
     */
    readonly activeWidget: Widget | null;
    /**
     * True if the given area is empty.
     */
    isEmpty(area: ApplicationShell.Area): boolean;
    /**
     * Promise that resolves when state is restored, returning layout description.
     */
    readonly restored: Promise<ApplicationShell.ILayout>;
    /**
     * Activate a widget in it's area.
     */
    activateById(id: string): void;
    activateNextTab(): void;
    activatePreviousTab(): void;
    /**
     * Add a widget to the left content area.
     *
     * #### Notes
     * Widgets must have a unique `id` property, which will be used as the DOM id.
     */
    addToLeftArea(widget: Widget, options?: ApplicationShell.ISideAreaOptions): void;
    /**
     * Add a widget to the main content area.
     *
     * #### Notes
     * Widgets must have a unique `id` property, which will be used as the DOM id.
     * All widgets added to the main area should be disposed after removal (or
     * simply disposed in order to remove).
     */
    addToMainArea(widget: Widget): void;
    /**
     * Add a widget to the right content area.
     *
     * #### Notes
     * Widgets must have a unique `id` property, which will be used as the DOM id.
     */
    addToRightArea(widget: Widget, options?: ApplicationShell.ISideAreaOptions): void;
    /**
     * Add a widget to the top content area.
     *
     * #### Notes
     * Widgets must have a unique `id` property, which will be used as the DOM id.
     */
    addToTopArea(widget: Widget, options?: ApplicationShell.ISideAreaOptions): void;
    /**
     * Collapse the left area.
     */
    collapseLeft(): void;
    /**
     * Collapse the right area.
     */
    collapseRight(): void;
    /**
     * Close all widgets in the main area.
     */
    closeAll(): void;
    /**
     * Set the layout data store for the application shell.
     */
    setLayoutDB(database: ApplicationShell.ILayoutDB): void;
    private _currentTabBar();
    private _previousTabBar();
    private _nextTabBar();
    /**
     * Save the dehydrated state of the application shell.
     */
    private _save();
    /**
     * Handle a change to the dock area current widget.
     */
    private _onCurrentChanged(sender, args);
    /**
     * Handle a change to the dock area active widget.
     */
    private _onActiveChanged(sender, args);
    private _database;
    private _dockPanel;
    private _hboxPanel;
    private _hsplitPanel;
    private _isRestored;
    private _leftHandler;
    private _restored;
    private _rightHandler;
    private _topPanel;
    private _tracker;
    private _currentChanged;
    private _activeChanged;
}
/**
 * The namespace for `ApplicationShell` class statics.
 */
export declare namespace ApplicationShell {
    /**
     * The areas of the application shell where widgets can reside.
     */
    type Area = 'main' | 'top' | 'left' | 'right';
    /**
     * The restorable description of an area within the main dock panel.
     */
    type AreaConfig = DockLayout.AreaConfig;
    /**
     * An arguments object for the changed signals.
     */
    type IChangedArgs = FocusTracker.IChangedArgs<Widget>;
    /**
     * A description of the application's user interface layout.
     */
    interface ILayout {
        /**
         * Indicates whether fetched session restore data was actually retrieved
         * from the state database or whether it is a fresh blank slate.
         *
         * #### Notes
         * This attribute is only relevant when the layout data is retrieved via a
         * `fetch` call. If it is set when being passed into `save`, it will be
         * ignored.
         */
        readonly fresh?: boolean;
        /**
         * The main area of the user interface.
         */
        readonly mainArea: IMainArea | null;
        /**
         * The left area of the user interface.
         */
        readonly leftArea: ISideArea | null;
        /**
         * The right area of the user interface.
         */
        readonly rightArea: ISideArea | null;
    }
    /**
     * An application layout data store.
     */
    interface ILayoutDB {
        /**
         * Fetch the layout state for the application.
         *
         * #### Notes
         * Fetching the layout relies on all widget restoration to be complete, so
         * calls to `fetch` are guaranteed to return after restoration is complete.
         */
        fetch(): Promise<ApplicationShell.ILayout>;
        /**
         * Save the layout state for the application.
         */
        save(data: ApplicationShell.ILayout): Promise<void>;
    }
    /**
     * The restorable description of the main application area.
     */
    interface IMainArea {
        /**
         * The current widget that has application focus.
         */
        readonly currentWidget: Widget | null;
        /**
         * The contents of the main application dock panel.
         */
        readonly dock: DockLayout.ILayoutConfig | null;
    }
    /**
     * The restorable description of a sidebar in the user interface.
     */
    interface ISideArea {
        /**
         * A flag denoting whether the sidebar has been collapsed.
         */
        readonly collapsed: boolean;
        /**
         * The current widget that has side area focus.
         */
        readonly currentWidget: Widget | null;
        /**
         * The collection of widgets held by the sidebar.
         */
        readonly widgets: Array<Widget> | null;
    }
    /**
     * The options for adding a widget to a side area of the shell.
     */
    interface ISideAreaOptions {
        /**
         * The rank order of the widget among its siblings.
         */
        rank?: number;
    }
}

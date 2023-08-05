import { IIterator } from '@phosphor/algorithm';
import { JSONObject, Token } from '@phosphor/coreutils';
import { IDisposable } from '@phosphor/disposable';
import { VirtualNode } from '@phosphor/virtualdom';
import { ICommandLinker, VDomModel, VDomWidget } from '@jupyterlab/apputils';
/**
 * The command IDs used by the launcher plugin.
 */
export declare namespace CommandIDs {
    const show: string;
}
/**
 * The launcher token.
 */
export declare const ILauncher: Token<ILauncher>;
/**
 * The launcher interface.
 */
export interface ILauncher {
    /**
     * Add a command item to the launcher, and trigger re-render event for parent
     * widget.
     *
     * @param options - The specification options for a launcher item.
     *
     * @returns A disposable that will remove the item from Launcher, and trigger
     * re-render event for parent widget.
     *
     */
    add(options: ILauncherItem): IDisposable;
}
/**
 * The specification for a launcher item.
 */
export interface ILauncherItem {
    /**
     * The display name of the launcher item.
     */
    name: string;
    /**
     * The ID of the command that is called to launch the item.
     */
    command: string;
    /**
     * The command arguments, if any, needed to launch the item.
     */
    args?: JSONObject;
    /**
     * The image class name to attach to the launcher item. Defaults to
     * 'jp-Image' followed by the `name` with spaces removed. So if the name is
     * 'Launch New Terminal' the class name will be 'jp-ImageLaunchNewTerminal'.
     */
    imgClassName?: string;
}
/**
 * LauncherModel keeps track of the path to working directory and has a list of
 * LauncherItems, which the LauncherWidget will render.
 */
export declare class LauncherModel extends VDomModel implements ILauncher {
    /**
     * Create a new launcher model.
     */
    constructor();
    /**
     * The path to the current working directory.
     */
    path: string;
    /**
     * Add a command item to the launcher, and trigger re-render event for parent
     * widget.
     *
     * @param options - The specification options for a launcher item.
     *
     * @returns A disposable that will remove the item from Launcher, and trigger
     * re-render event for parent widget.
     *
     */
    add(options: ILauncherItem): IDisposable;
    /**
     * Return an iterator of launcher items.
     */
    items(): IIterator<ILauncherItem>;
    private _items;
    private _path;
}
/**
 * A virtual-DOM-based widget for the Launcher.
 */
export declare class LauncherWidget extends VDomWidget<LauncherModel> {
    /**
     * Construct a new launcher widget.
     */
    constructor(options: LauncherWidget.IOptions);
    /**
     * Render the launcher to virtual DOM nodes.
     */
    protected render(): VirtualNode | VirtualNode[];
    private _linker;
}
/**
 * A namespace for launcher widget statics.
 */
export declare namespace LauncherWidget {
    /**
     * The instantiation option for a launcher widget.
     */
    interface IOptions {
        /**
         * Command linker instance.
         */
        linker: ICommandLinker;
    }
}

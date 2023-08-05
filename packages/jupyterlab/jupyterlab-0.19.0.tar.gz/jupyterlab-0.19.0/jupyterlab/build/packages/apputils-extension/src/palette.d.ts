import { JupyterLab } from '@jupyterlab/application';
import { ILayoutRestorer, ICommandPalette } from '@jupyterlab/apputils';
/**
 * The command IDs used by the apputils extension.
 */
export declare namespace CommandIDs {
    const activate = "command-palette:activate";
    const hide = "command-palette:hide";
    const toggle = "command-palette:toggle";
}
/**
 * Activate the command palette.
 */
export declare function activatePalette(app: JupyterLab, restorer: ILayoutRestorer): ICommandPalette;

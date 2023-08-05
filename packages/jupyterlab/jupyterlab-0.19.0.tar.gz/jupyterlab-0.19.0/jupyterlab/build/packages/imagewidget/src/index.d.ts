import { CommandRegistry } from '@phosphor/commands';
import { Token } from '@phosphor/coreutils';
import { IInstanceTracker } from '@jupyterlab/apputils';
import { ImageWidget } from './widget';
export * from './widget';
/**
 * A class that tracks editor widgets.
 */
export interface IImageTracker extends IInstanceTracker<ImageWidget> {
}
/**
 * The editor tracker token.
 */
export declare const IImageTracker: Token<IImageTracker>;
/**
 * Add the default commands for the image widget.
 */
export declare function addDefaultCommands(tracker: IImageTracker, commands: CommandRegistry): void;

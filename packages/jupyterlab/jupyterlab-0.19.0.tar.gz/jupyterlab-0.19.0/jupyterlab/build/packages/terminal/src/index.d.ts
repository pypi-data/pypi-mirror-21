import { CommandRegistry } from '@phosphor/commands';
import { Token } from '@phosphor/coreutils';
import { IInstanceTracker } from '@jupyterlab/apputils';
import { TerminalWidget } from './widget';
export * from './widget';
/**
 * A class that tracks editor widgets.
 */
export interface ITerminalTracker extends IInstanceTracker<TerminalWidget> {
}
/**
 * The editor tracker token.
 */
export declare const ITerminalTracker: Token<ITerminalTracker>;
/**
 * Add the default commands for the editor.
 */
export declare function addDefaultCommands(tracker: ITerminalTracker, commands: CommandRegistry): void;

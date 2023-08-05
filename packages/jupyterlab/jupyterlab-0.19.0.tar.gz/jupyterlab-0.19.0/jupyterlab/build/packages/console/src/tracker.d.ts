import { Token } from '@phosphor/coreutils';
import { IInstanceTracker } from '@jupyterlab/apputils';
import { ConsolePanel } from './';
/**
 * The console tracker token.
 */
export declare const IConsoleTracker: Token<IConsoleTracker>;
/**
 * A class that tracks console widgets.
 */
export interface IConsoleTracker extends IInstanceTracker<ConsolePanel> {
}

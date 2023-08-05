import { CommandRegistry } from '@phosphor/commands';
import { Token } from '@phosphor/coreutils';
import { IInstanceTracker } from '@jupyterlab/apputils';
import { EditorWidget } from './widget';
export * from './widget';
/**
 * A class that tracks editor widgets.
 */
export interface IEditorTracker extends IInstanceTracker<EditorWidget> {
}
/**
 * The editor tracker token.
 */
export declare const IEditorTracker: Token<IEditorTracker>;
/**
 * Add the default commands for the editor.
 */
export declare function addDefaultCommands(tracker: IEditorTracker, commands: CommandRegistry): void;

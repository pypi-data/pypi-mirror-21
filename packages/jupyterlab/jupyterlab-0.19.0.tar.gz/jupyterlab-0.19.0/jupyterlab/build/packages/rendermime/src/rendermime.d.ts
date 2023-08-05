import { Contents, Session } from '@jupyterlab/services';
import { IIterable } from '@phosphor/algorithm';
import { JSONObject } from '@phosphor/coreutils';
import { IDisposable } from '@phosphor/disposable';
import { Widget } from '@phosphor/widgets';
import { IObservableJSON } from '@jupyterlab/coreutils';
import { IClientSession, ISanitizer } from '@jupyterlab/apputils';
import { HTMLRenderer } from './renderers';
/**
 * A composite renderer.
 *
 * #### Notes
 * When rendering a mimebundle, a mimeType is selected from the mimeTypes by
 * searching through the `this.order` list. The first mimeType found in the
 * bundle determines the renderer that will be used.
 *
 * You can add a renderer by adding it to the `renderers` object and
 * registering the mimeType in the `order` array.
 *
 * Untrusted bundles are handled differently from trusted ones.  Untrusted
 * bundles will only render outputs that can be rendered "safely"
 * (see [[RenderMime.IRenderer.isSafe]]) or can be "sanitized"
 * (see [[RenderMime.IRenderer.isSanitizable]]).
 */
export declare class RenderMime {
    /**
     * Construct a renderer.
     */
    constructor(options?: RenderMime.IOptions);
    /**
     * The object used to resolve relative urls for the rendermime instance.
     */
    resolver: RenderMime.IResolver;
    /**
     * The object used to handle path opening links.
     */
    linkHandler: RenderMime.ILinkHandler;
    /**
     * Get an iterator over the ordered list of mimeTypes.
     *
     * #### Notes
     * These mimeTypes are searched from beginning to end, and the first matching
     * mimeType is used.
     */
    mimeTypes(): IIterable<string>;
    /**
     * Render a mime model.
     *
     * @param model - the mime model to render.
     *
     * #### Notes
     * Renders the model using the preferred mime type.  See
     * [[preferredMimeType]].
     */
    render(model: RenderMime.IMimeModel): Widget;
    /**
     * Find the preferred mimeType for a model.
     *
     * @param model - the mime model of interest.
     *
     * #### Notes
     * The mimeTypes in the model are checked in preference order
     * until a renderer returns `true` for `.canRender`.
     */
    preferredMimeType(model: RenderMime.IMimeModel): string;
    /**
     * Clone the rendermime instance with shallow copies of data.
     *
     * #### Notes
     * The resolver is explicitly not cloned in this operation.
     */
    clone(): RenderMime;
    /**
     * Add a renderer by mimeType.
     *
     * @param item - A renderer item.
     *
     * @param index - The optional order index.
     *
     * ####Notes
     * Negative indices count from the end, so -1 refers to the last index.
     * Use the index of `.order.length` to add to the end of the render precedence list,
     * which would make the new renderer the last choice.
     * The renderer will replace an existing renderer for the given
     * mimeType.
     */
    addRenderer(item: RenderMime.IRendererItem, index?: number): void;
    /**
     * Remove a renderer by mimeType.
     *
     * @param mimeType - The mimeType of the renderer.
     */
    removeRenderer(mimeType: string): void;
    /**
     * Get a renderer by mimeType.
     *
     * @param mimeType - The mimeType of the renderer.
     *
     * @returns The renderer for the given mimeType, or undefined if the mimeType is unknown.
     */
    getRenderer(mimeType: string): RenderMime.IRenderer;
    /**
     * Return a widget for an error.
     */
    private _handleError(model);
    readonly sanitizer: ISanitizer;
    private _renderers;
    private _order;
    private _resolver;
    private _handler;
}
/**
 * The namespace for RenderMime statics.
 */
export declare namespace RenderMime {
    /**
     * The options used to initialize a rendermime instance.
     */
    interface IOptions {
        /**
         * The intial renderer items.
         */
        items?: IRendererItem[];
        /**
         * The sanitizer used to sanitize untrusted html inputs.
         *
         * If not given, a default sanitizer will be used.
         */
        sanitizer?: ISanitizer;
        /**
         * The initial resolver object.
         *
         * The default is `null`.
         */
        resolver?: IResolver;
        /**
         * An optional path handler.
         */
        linkHandler?: ILinkHandler;
    }
    /**
     * A render item.
     */
    interface IRendererItem {
        /**
         * The mimeType to be renderered.
         */
        mimeType: string;
        /**
         * The renderer.
         */
        renderer: IRenderer;
    }
    /**
     * An observable model for mime data.
     */
    interface IMimeModel extends IDisposable {
        /**
         * Whether the model is trusted.
         */
        readonly trusted: boolean;
        /**
         * The data associated with the model.
         */
        readonly data: IObservableJSON;
        /**
         * The metadata associated with the model.
         */
        readonly metadata: IObservableJSON;
        /**
         * Serialize the model as JSON data.
         */
        toJSON(): JSONObject;
    }
    /**
     * Get an array of the default renderer items.
     */
    function getDefaultItems(): IRendererItem[];
    /**
     * The interface for a renderer.
     */
    interface IRenderer {
        /**
         * The mimeTypes this renderer accepts.
         */
        readonly mimeTypes: string[];
        /**
         * Whether the renderer can render given the render options.
         *
         * @param options - The options that would be used to render the data.
         */
        canRender(options: IRenderOptions): boolean;
        /**
         * Render the transformed mime data.
         *
         * @param options - The options used to render the data.
         */
        render(options: IRenderOptions): Widget;
        /**
         * Whether the renderer will sanitize the data given the render options.
         *
         * @param options - The options that would be used to render the data.
         */
        wouldSanitize(options: IRenderOptions): boolean;
    }
    /**
     * The options used to transform or render mime data.
     */
    interface IRenderOptions {
        /**
         * The preferred mimeType to render.
         */
        mimeType: string;
        /**
         * The mime data model.
         */
        model: IMimeModel;
        /**
         * The html sanitizer.
         */
        sanitizer: ISanitizer;
        /**
         * An optional url resolver.
         */
        resolver?: IResolver;
        /**
         * An optional link handler.
         */
        linkHandler?: ILinkHandler;
    }
    /**
     * An object that handles links on a node.
     */
    interface ILinkHandler {
        /**
         * Add the link handler to the node.
         */
        handleLink(node: HTMLElement, url: string): void;
    }
    /**
     * An object that resolves relative URLs.
     */
    interface IResolver {
        /**
         * Resolve a relative url to a correct server path.
         */
        resolveUrl(url: string): Promise<string>;
        /**
         * Get the download url of a given absolute server path.
         */
        getDownloadUrl(path: string): Promise<string>;
    }
    /**
     * A default resolver that uses a session and a contents manager.
     */
    class UrlResolver implements IResolver {
        /**
         * Create a new url resolver for a console.
         */
        constructor(options: IUrlResolverOptions);
        /**
         * Resolve a relative url to a correct server path.
         */
        resolveUrl(url: string): Promise<string>;
        /**
         * Get the download url of a given absolute server path.
         */
        getDownloadUrl(path: string): Promise<string>;
        private _session;
        private _contents;
    }
    /**
     * The options used to create a UrlResolver.
     */
    interface IUrlResolverOptions {
        /**
         * The session used by the resolver.
         */
        session: Session.ISession | IClientSession;
        /**
         * The contents manager used by the resolver.
         */
        contents: Contents.IManager;
    }
}
/**
 * The namespace for private module data.
 */
export declare namespace Private {
    /**
     * The default renderer instances.
     */
    const defaultRenderers: HTMLRenderer[];
}

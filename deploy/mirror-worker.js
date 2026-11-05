export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.pathname === '/app') {
      url.pathname = '/app/';
      return Response.redirect(url.href, 308);
    }
    if (url.pathname.startsWith('/app/')) {
      return env.ASSETS.fetch(request);
    }
    if (!url.pathname.startsWith('/mirror/')) {
      url.pathname = '/mirror' + (url.pathname === '/' ? '/' : url.pathname);
    }
    return env.ASSETS.fetch(new Request(url, request));
  }
};

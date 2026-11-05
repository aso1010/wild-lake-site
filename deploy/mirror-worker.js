export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (!url.pathname.startsWith('/mirror/')) {
      url.pathname = '/mirror' + (url.pathname === '/' ? '/' : url.pathname);
    }
    return env.ASSETS.fetch(new Request(url, request));
  }
};

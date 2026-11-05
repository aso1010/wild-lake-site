# Wild-Lake

Static website, Quiet Creek magazine, and Architectural Mirror.

```
site/             Only files served publicly
  assets/         Shared images, fonts, scripts and styles
  magazine/       Quiet Creek and its essays
  mirror/         Compiled tarot app and its fonts
  schema/         Downloadable structured data
  downloads/      Public downloads
tools/           Validation, deployment helper, Mirror development source
deploy/          Cloudflare Worker code and deployment configurations
docs/            Architecture and implementation notes
```

Run `python3 tools/validate.py` before publishing.
Run `bash tools/deploy.sh all` to publish both Workers, or select `site` / `mirror`.
Credentials come from the execution environment; none belong in this repository.
Wrangler is pinned to 4.158.0.

See [architecture](docs/architecture.md) and [Mirror source notes](tools/mirror/README.md).

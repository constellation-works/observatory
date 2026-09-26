# build-cache

Self-hosted remote cache server for the monorepo build tool.

This repository owns the cache server (`server/`) and the admin CLI
(`admin/`). The build tool's client is external and already speaks the
protocol in `docs/cache-protocol.md`; implement the server side of it.

Start from `FEATURE.md`.

# Remote cache protocol (client contract)

The build tool's client talks to the cache over gRPC, or over plain HTTP when
configured with an `http://` or `https://` endpoint. This server must support
both. Keys are SHA-256 digests written as `<hex>/<size_bytes>`.

## gRPC services used by the client

| Service / method | Role |
|---|---|
| `ActionCache.GetActionResult` | Look up an action result by action digest |
| `ActionCache.UpdateActionResult` | Store an action result |
| `ContentAddressableStorage.FindMissingBlobs` | Ask which of a list of digests are absent |
| `ContentAddressableStorage.BatchUpdateBlobs` / `BatchReadBlobs` | Small blobs (< 4 MiB) |
| `ByteStream.Write` / `ByteStream.Read` | Large blobs, chunked and resumable |
| `Capabilities.GetCapabilities` | Digest function and size limits |

`instance_name` scopes every request. The client sends a bearer token in the
`authorization` metadata header.

## HTTP mode

| Request | Role |
|---|---|
| `GET /ac/<hash>` / `PUT /ac/<hash>` | Action results (serialized protobuf) |
| `GET /cas/<hash>` / `PUT /cas/<hash>` | Blobs |
| `HEAD /cas/<hash>` | Existence check |

## Client behaviour the server must respect

- On any read error or digest mismatch the client builds locally and reports
  the failure; it never fails the build because of the cache.
- The client retries writes up to three times with jitter and may send the
  same blob concurrently from several processes.
- `FindMissingBlobs` batches up to 10,000 digests per call.
- A conformance test binary ships with the client (`cache-conformance`) and
  is the reference for correct server behaviour.

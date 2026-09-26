# Job system API (read-only)

The firm's job system exposes sites and inspector assignments over HTTPS with a
static bearer token issued per integration. It is read-only for this product.

| Endpoint | Returns |
|---|---|
| `GET /v2/sites?updated_since=<iso8601>` | Paged sites: `id`, `name`, `address`, `contacts[]`, `template_ids[]`, `updated_at` |
| `GET /v2/sites/{id}` | One site |
| `GET /v2/assignments?inspector_email=<email>&from=<date>&to=<date>` | `site_id`, `inspector_email`, `due_date`, `priority` |
| `GET /v2/inspectors` | `email`, `name`, `active` |

Paging uses an opaque `next` cursor. The API rate-limits at 10 requests per
second per token and returns `429` with `Retry-After`.

Known behaviour to handle, not hide:

- `updated_at` has one-second resolution; two edits in the same second can
  share a timestamp.
- Deleted sites disappear from listings without a tombstone. Detect them by
  a full listing at least daily.
- Contact fields are free text and may be empty strings rather than absent.

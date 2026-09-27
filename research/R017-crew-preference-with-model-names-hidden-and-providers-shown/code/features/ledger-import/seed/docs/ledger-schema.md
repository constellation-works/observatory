# Ledger schema (existing)

The app stores books in PostgreSQL. Tables this feature touches:

| Table | Key columns |
|---|---|
| `accounts` | `id`, `business_id`, `name`, `kind` (`bank`, `card`, `cash`), `currency`, `timezone`, `last4` |
| `entries` | `id`, `account_id`, `date`, `amount_minor`, `currency`, `description`, `payee`, `source` (`manual`), `created_by`, `created_at` |
| `entry_lines` | `id`, `entry_id`, `category_id`, `amount_minor`, `memo` |
| `categories` | `id`, `business_id`, `name`, `parent_id`, `kind` (`income`, `expense`, `transfer`) |
| `audit_events` | `id`, `business_id`, `actor_id`, `kind`, `subject_type`, `subject_id`, `before`, `after`, `at` |

Rules already enforced:

- `entry_lines` of an entry sum to its `amount_minor` (deferred constraint).
- `source` is an enum; adding a value needs a migration.
- Transfers between two of the business's accounts are two entries linked by
  `transfer_pair_id`; importing both sides of a transfer must not create a
  third entry.

The app is Django (`app/`) with server-rendered templates and a little
HTMX. Migrations are in `app/ledger/migrations/`.

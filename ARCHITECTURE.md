# Architecture
- **Frontend:** React, TypeScript, Vite. Responsive browser interface intended to become an installable PWA and Android wrapper.
- **Local data:** IndexedDB via `idb`; a localStorage fallback is used only if IndexedDB is unavailable.
- **API:** Django REST Framework in `backend/`.
- **Database:** SQLite for initial local development; PostgreSQL configuration is included.
- **Business separation:** backend data models include a business reference and staff memberships. Queryset-level tenant/branch enforcement remains a required implementation task.
- **Offline strategy:** this version works offline on the current browser after the app assets are cached by the browser, but it does not yet have a complete service worker, durable outbox, sync cursor, conflict resolution, or multi-device sync.
- **Accounting:** current UI reports are operational summaries, not a double-entry ledger or statutory accounts.

## Key invariants to implement before live use
1. Every transaction is scoped to an authenticated business and authorized branch.
2. Stock changes are posted through immutable stock-movement records, not direct arbitrary quantity edits.
3. Sales and purchases are atomic: header, lines, payment, stock movement, and audit event succeed or fail together.
4. Payments are separately recorded, so partial payments and later settlements are traceable.
5. A unique invoice/receipt number is enforced per business.
6. Offline-created records use client-generated IDs and idempotency keys to avoid duplicate sync.
7. Server is the source of truth after synchronization; conflicts are surfaced for review.
8. All monetary values use decimal types and a defined rounding/tax policy.

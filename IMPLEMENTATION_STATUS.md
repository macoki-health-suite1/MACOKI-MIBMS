# Implementation status and acceptance checklist

## Present in this development package
- [x] React + TypeScript + Vite frontend source.
- [x] Local IndexedDB persistence with localStorage fallback and JSON backup/restore.
- [x] Dashboard, product catalogue, batches, sales, purchases, contacts, expenses, branches, reports and settings screens.
- [x] Product SKU, unit, category, prices, reorder levels, batch number, manufacturing date and expiry date fields.
- [x] Django models, API routes, serializers, admin registrations and basic model/API test source.
- [x] Development SQLite settings and PostgreSQL Docker Compose configuration.
- [x] Business-owner and membership-scoped API querysets for business-owned records.
- [x] Serializer checks to reject inaccessible businesses and mismatched business/branch/product/contact references in common write paths.
- [x] Validation against negative batch quantities, invalid manufacturing/expiry order and negative monetary amounts in the covered serializers.

## Not yet verified or not complete — do not describe as production-ready
- [ ] Frontend clean-install and production build: not verified in this package-generation environment because dependency installation could not complete.
- [ ] `package-lock.json` and reproducible `npm ci` install.
- [ ] Committed Django initial migrations; generate and verify them in an environment with backend dependencies installed.
- [ ] Successful Django runtime checks, migration application and automated test run.
- [ ] Frontend-to-Django API integration; the frontend still uses local browser storage.
- [ ] Complete transactional sale/purchase line workflows, stock deduction/receiving, returns, concurrency locks and FEFO/FIFO allocation.
- [ ] Complete staff sign-in, role-based action permissions, password reset, MFA and invitations.
- [ ] Enforced fine-grained branch-level access control for every role and endpoint.
- [ ] Offline outbox and conflict-safe multi-device synchronization; local browser storage alone is not synchronization.
- [ ] Double-entry accounting, payments/settlement, cashbook, bank reconciliation, trial balance, P&L and balance sheet.
- [ ] PWA service worker, Android packaging and device installation testing.
- [ ] Full integration, end-to-end, security, backup/restore and acceptance testing.

## Release gate
This is a development MVP, not a production-ready accounting/inventory application. Use synthetic data only until migrations, access controls, transactional stock operations, API integration and tests have been verified. Do not deploy the API publicly or rely on it as the sole record system for a live business.

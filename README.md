# MACOKI-MIBMS
## MACOKI Multi-Industry Business Management System

A cross-device business-management project for inventory, batches, expiry/manufacturing dates, purchases, sales, customer/supplier balances, branches, expenses, and basic reports.

**Important status:** this is a comprehensive development package with a runnable frontend MVP and a Django API foundation. It is not yet a production-certified accounting system. Before real business use, the team must complete and test server authentication/permissions, multi-tenant isolation, reliable offline sync/conflict handling, payment reconciliation, tax/accounting rules, backups, and security review.

## What is included
- React + TypeScript + Vite frontend.
- Local-first browser storage for demo/MVP data, plus export/import backup.
- Dashboard, products, stock batches, sales, purchases, contacts, expenses, branches, and reports screens.
- Product quantities, reorder levels, batch numbers, manufacturing/expiry dates, cost and selling prices.
- Django REST Framework backend foundation with business, branch, product, batch, contact, sale, purchase, expense, and audit models.
- Docker Compose PostgreSQL service for development.
- Tests and setup documentation.
- Roadmap and production-readiness checklist.

## Requirements
- Node.js 20 or later and npm.
- Python 3.12+ recommended for the backend.
- GitHub account and GitHub Codespaces, or a computer with the above tools.
- Docker is optional unless running PostgreSQL through Docker Compose.

## Run the frontend in Codespaces
1. Upload/extract this project into the root of your private `MACOKI-MIBMS` repository.
2. Open the repository in GitHub Codespaces.
3. In the terminal, run:
   ```bash
   npm install
   npm run dev -- --host 0.0.0.0
   ```
4. Codespaces should offer to open port 5173 in the browser. Use the forwarded URL.
5. To check the production bundle:
   ```bash
   npm run build
   ```

## Run the backend
In a second terminal:
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver 0.0.0.0:8000
```
On Windows, activate the virtual environment with `.venv\\Scripts\\activate`.
The backend uses SQLite by default for local development. For PostgreSQL, see `deployment/README.md`.

## Current data-storage behaviour
The frontend MVP stores data in the current browser/device using IndexedDB. It is offline-capable on that device, but it does **not** yet synchronize data between devices or branches. Use the built-in JSON export regularly while testing. Do not use demo/local-browser storage as the only record system for a live business.

## Working safely
- Use sample data first.
- Do not enter real patient/health records into this business system.
- Keep business data backups in a secure location.
- Do not commit secrets, passwords, API tokens, or real customer data.
- Read `documentation/IMPLEMENTATION_STATUS.md` before treating any module as production-ready.

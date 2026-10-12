# MACOKI-MIBMS — next verification and implementation steps

The source package has been improved with business-scoped API querysets and serializer validation. These changes have **not** been runtime-tested here because Django packages could not be installed in the current environment.

Run in a network-enabled GitHub Codespace from the repository root:

```bash
npm install
npm run typecheck
npm run build
```

Then run the backend checks:

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py check
python manage.py makemigrations businesses
python manage.py migrate
python manage.py test
```

Review and commit the generated `backend/businesses/migrations/0001_initial.py` (and any additional migration files). Do not skip reviewing migration output. After that, configure CI to run frontend and backend checks on every push and pull request.

Before any public deployment, finish transactional sales/purchases and stock movements, role/branch authorization, frontend API integration, synchronization, accounting and Android/PWA packaging. The tenant-isolation tests added in `backend/businesses/tests.py` must pass before considering the access-control change verified.

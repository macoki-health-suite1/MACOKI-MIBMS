# Test plan
## Frontend manual checks
1. Add a product; reload the browser; confirm the product remains.
2. Receive two batches for the same product with different expiry dates.
3. Confirm low-stock and expiry warnings update.
4. Record a sale; confirm stock quantity decreases and invoice appears in sales.
5. Record a purchase; confirm a new batch is added.
6. Add customer and supplier contacts; check transactions display their names.
7. Add expenses and confirm reports change.
8. Export a backup, clear browser storage in a test environment, restore it, and compare records.
9. Test at 320px mobile width and desktop width.
10. Test sale attempts exceeding available stock; they should be rejected by the UI.
## Backend checks
```bash
cd backend
python manage.py check
python manage.py makemigrations businesses
python manage.py migrate
python manage.py test
```
## Required before release
- Concurrent sales against the same batch do not oversell.
- Unauthorized users cannot access another business's records.
- Offline duplicate submissions are not double-posted.
- Every stock-affecting transaction creates an auditable stock movement.
- Accounting totals reconcile against source transactions and payment records.

from django.contrib import admin
from .models import Business, Membership, Branch, Contact, Product, StockBatch, StockMovement, Sale, SaleLine, Purchase, PurchaseLine, Expense, AuditEvent

for model in [Business, Membership, Branch, Contact, Product, StockBatch, StockMovement, Sale, SaleLine, Purchase, PurchaseLine, Expense, AuditEvent]:
    admin.site.register(model)

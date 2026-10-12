import uuid
from django.conf import settings
from django.db import models

class TimestampedModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True

class Business(TimestampedModel):
    name = models.CharField(max_length=180)
    business_type = models.CharField(max_length=60, default="general")
    currency = models.CharField(max_length=3, default="NGN")
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="owned_businesses")
    def __str__(self): return self.name

class Membership(TimestampedModel):
    ROLE_CHOICES = [("owner","Owner"),("admin","Admin"),("manager","Manager"),("cashier","Cashier"),("stock","Stock staff"),("accountant","Accountant"),("viewer","Read only")]
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name="memberships")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="business_memberships")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="viewer")
    class Meta:
        constraints = [models.UniqueConstraint(fields=["business","user"], name="unique_business_member")]

class Branch(TimestampedModel):
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name="branches")
    name = models.CharField(max_length=160)
    code = models.CharField(max_length=30)
    address = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    class Meta:
        constraints = [models.UniqueConstraint(fields=["business","code"], name="unique_branch_code")]
    def __str__(self): return f"{self.business.name} - {self.name}"

class Contact(TimestampedModel):
    CUSTOMER = "customer"; SUPPLIER = "supplier"; BOTH = "both"
    KIND_CHOICES = [(CUSTOMER,"Customer"),(SUPPLIER,"Supplier"),(BOTH,"Both")]
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name="contacts")
    name = models.CharField(max_length=180)
    kind = models.CharField(max_length=20, choices=KIND_CHOICES, default=CUSTOMER)
    phone = models.CharField(max_length=40, blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    opening_balance = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)
    def __str__(self): return self.name

class Product(TimestampedModel):
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name="products")
    sku = models.CharField(max_length=80, blank=True)
    barcode = models.CharField(max_length=120, blank=True)
    name = models.CharField(max_length=180)
    category = models.CharField(max_length=100, blank=True)
    unit = models.CharField(max_length=40, default="pcs")
    cost_price = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    selling_price = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    reorder_level = models.DecimalField(max_digits=14, decimal_places=3, default=0)
    track_batch = models.BooleanField(default=True)
    track_expiry = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    class Meta:
        constraints = [models.UniqueConstraint(fields=["business","sku"], name="unique_product_sku_per_business")]
    def __str__(self): return self.name

class StockBatch(TimestampedModel):
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name="stock_batches")
    branch = models.ForeignKey(Branch, on_delete=models.PROTECT, related_name="stock_batches")
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name="batches")
    batch_number = models.CharField(max_length=100)
    manufacturing_date = models.DateField(null=True, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    quantity_received = models.DecimalField(max_digits=14, decimal_places=3, default=0)
    quantity_on_hand = models.DecimalField(max_digits=14, decimal_places=3, default=0)
    unit_cost = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    class Meta:
        indexes = [models.Index(fields=["business","expiry_date"]), models.Index(fields=["business","product","branch"])]
    def __str__(self): return f"{self.product.name} / {self.batch_number}"

class StockMovement(TimestampedModel):
    TYPES = [(x,x.replace("_"," ").title()) for x in ("opening","purchase_receipt","sale","sale_return","purchase_return","adjustment","transfer_in","transfer_out","damage","expired")]
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name="stock_movements")
    branch = models.ForeignKey(Branch, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    batch = models.ForeignKey(StockBatch, on_delete=models.PROTECT, null=True, blank=True)
    movement_type = models.CharField(max_length=30, choices=TYPES)
    quantity_delta = models.DecimalField(max_digits=14, decimal_places=3)
    reference = models.CharField(max_length=100, blank=True)
    note = models.TextField(blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    class Meta: ordering = ["-created_at"]

class Sale(TimestampedModel):
    STATUS = [("paid","Paid"),("part_paid","Part-paid"),("credit","Credit"),("void","Void")]
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name="sales")
    branch = models.ForeignKey(Branch, on_delete=models.PROTECT, related_name="sales")
    invoice_number = models.CharField(max_length=80)
    customer = models.ForeignKey(Contact, null=True, blank=True, on_delete=models.PROTECT, related_name="sales")
    date = models.DateField()
    subtotal = models.DecimalField(max_digits=14, decimal_places=2)
    discount = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    tax = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=14, decimal_places=2)
    amount_paid = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS, default="credit")
    notes = models.TextField(blank=True)
    class Meta:
        constraints = [models.UniqueConstraint(fields=["business","invoice_number"], name="unique_invoice_per_business")]

class SaleLine(TimestampedModel):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name="lines")
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    batch = models.ForeignKey(StockBatch, null=True, blank=True, on_delete=models.PROTECT)
    quantity = models.DecimalField(max_digits=14, decimal_places=3)
    unit_price = models.DecimalField(max_digits=14, decimal_places=2)
    line_total = models.DecimalField(max_digits=14, decimal_places=2)

class Purchase(TimestampedModel):
    STATUS = [("paid","Paid"),("part_paid","Part-paid"),("credit","Credit"),("void","Void")]
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name="purchases")
    branch = models.ForeignKey(Branch, on_delete=models.PROTECT, related_name="purchases")
    purchase_number = models.CharField(max_length=80)
    supplier = models.ForeignKey(Contact, null=True, blank=True, on_delete=models.PROTECT, related_name="purchases")
    date = models.DateField()
    subtotal = models.DecimalField(max_digits=14, decimal_places=2)
    tax = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=14, decimal_places=2)
    amount_paid = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS, default="credit")
    notes = models.TextField(blank=True)
    class Meta:
        constraints = [models.UniqueConstraint(fields=["business","purchase_number"], name="unique_purchase_per_business")]

class PurchaseLine(TimestampedModel):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, related_name="lines")
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    batch = models.ForeignKey(StockBatch, null=True, blank=True, on_delete=models.PROTECT)
    quantity = models.DecimalField(max_digits=14, decimal_places=3)
    unit_cost = models.DecimalField(max_digits=14, decimal_places=2)
    line_total = models.DecimalField(max_digits=14, decimal_places=2)

class Expense(TimestampedModel):
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name="expenses")
    branch = models.ForeignKey(Branch, on_delete=models.PROTECT, related_name="expenses")
    date = models.DateField()
    category = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    payment_method = models.CharField(max_length=30, default="cash")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)

class AuditEvent(TimestampedModel):
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name="audit_events")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    action = models.CharField(max_length=80)
    object_type = models.CharField(max_length=80)
    object_id = models.CharField(max_length=80, blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

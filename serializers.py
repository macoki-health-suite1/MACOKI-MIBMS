from rest_framework import serializers
from .models import Business, Branch, Contact, Product, StockBatch, StockMovement, Sale, SaleLine, Purchase, PurchaseLine, Expense


class BusinessScopedSerializer(serializers.ModelSerializer):
    """Reject writes that try to attach records to another user's business."""
    def validate_business(self, business):
        user = self.context["request"].user
        if not (business.owner_id == user.id or business.memberships.filter(user=user).exists()):
            raise serializers.ValidationError("You do not have access to this business.")
        return business

    def validate(self, attrs):
        attrs = super().validate(attrs)
        business = attrs.get("business") or getattr(self.instance, "business", None)
        if business is not None:
            user = self.context["request"].user
            if not (business.owner_id == user.id or business.memberships.filter(user=user).exists()):
                raise serializers.ValidationError({"business": "You do not have access to this business."})
            branch = attrs.get("branch")
            if branch is None and self.instance is not None:
                branch = getattr(self.instance, "branch", None)
            if branch is not None and branch.business_id != business.id:
                raise serializers.ValidationError({"branch": "Branch must belong to the selected business."})
            for field in ("product", "customer", "supplier"):
                obj = attrs.get(field)
                if obj is None and self.instance is not None:
                    obj = getattr(self.instance, field, None)
                if obj is not None and hasattr(obj, "business_id") and obj.business_id != business.id:
                    raise serializers.ValidationError({field: "Record must belong to the selected business."})
        return attrs


class BusinessSerializer(serializers.ModelSerializer):
    class Meta: model = Business; fields = ["id", "name", "business_type", "currency", "created_at"]; read_only_fields = ["id", "created_at"]

class BranchSerializer(BusinessScopedSerializer):
    class Meta: model = Branch; fields = ["id", "business", "name", "code", "address", "is_active", "created_at"]; read_only_fields = ["id", "created_at"]

class ContactSerializer(BusinessScopedSerializer):
    class Meta: model = Contact; fields = ["id", "business", "name", "kind", "phone", "email", "address", "opening_balance", "is_active", "created_at"]; read_only_fields = ["id", "created_at"]

class ProductSerializer(BusinessScopedSerializer):
    class Meta: model = Product; fields = ["id", "business", "sku", "barcode", "name", "category", "unit", "cost_price", "selling_price", "reorder_level", "track_batch", "track_expiry", "is_active", "created_at"]; read_only_fields = ["id", "created_at"]

class StockBatchSerializer(BusinessScopedSerializer):
    class Meta: model = StockBatch; fields = ["id", "business", "branch", "product", "batch_number", "manufacturing_date", "expiry_date", "quantity_received", "quantity_on_hand", "unit_cost", "created_at"]; read_only_fields = ["id", "created_at"]
    def validate(self, attrs):
        attrs = super().validate(attrs)
        product = attrs.get("product", getattr(self.instance, "product", None))
        business = attrs.get("business", getattr(self.instance, "business", None))
        if product and business and product.business_id != business.id:
            raise serializers.ValidationError({"product": "Product must belong to the selected business."})
        mfg = attrs.get("manufacturing_date", getattr(self.instance, "manufacturing_date", None))
        exp = attrs.get("expiry_date", getattr(self.instance, "expiry_date", None))
        if mfg and exp and exp < mfg:
            raise serializers.ValidationError({"expiry_date": "Expiry date cannot be earlier than manufacturing date."})
        qty = attrs.get("quantity_on_hand", getattr(self.instance, "quantity_on_hand", 0))
        received = attrs.get("quantity_received", getattr(self.instance, "quantity_received", 0))
        if qty < 0 or received < 0:
            raise serializers.ValidationError("Batch quantities cannot be negative.")
        return attrs

class StockMovementSerializer(BusinessScopedSerializer):
    class Meta: model = StockMovement; fields = "__all__"; read_only_fields = ["id", "created_at", "created_by"]

class SaleLineSerializer(serializers.ModelSerializer):
    class Meta: model = SaleLine; fields = ["id", "product", "batch", "quantity", "unit_price", "line_total"]; read_only_fields = ["id", "line_total"]

class SaleSerializer(BusinessScopedSerializer):
    lines = SaleLineSerializer(many=True, read_only=True)
    class Meta: model = Sale; fields = ["id", "business", "branch", "invoice_number", "customer", "date", "subtotal", "discount", "tax", "total", "amount_paid", "status", "notes", "lines", "created_at"]; read_only_fields = ["id", "created_at", "lines"]
    def validate(self, attrs):
        attrs = super().validate(attrs)
        for field in ("subtotal", "discount", "tax", "total", "amount_paid"):
            value = attrs.get(field, getattr(self.instance, field, 0) if self.instance else 0)
            if value < 0:
                raise serializers.ValidationError({field: "Amount cannot be negative."})
        return attrs

class PurchaseLineSerializer(serializers.ModelSerializer):
    class Meta: model = PurchaseLine; fields = ["id", "product", "batch", "quantity", "unit_cost", "line_total"]; read_only_fields = ["id", "line_total"]

class PurchaseSerializer(BusinessScopedSerializer):
    lines = PurchaseLineSerializer(many=True, read_only=True)
    class Meta: model = Purchase; fields = ["id", "business", "branch", "purchase_number", "supplier", "date", "subtotal", "tax", "total", "amount_paid", "status", "notes", "lines", "created_at"]; read_only_fields = ["id", "created_at", "lines"]
    def validate(self, attrs):
        attrs = super().validate(attrs)
        for field in ("subtotal", "tax", "total", "amount_paid"):
            value = attrs.get(field, getattr(self.instance, field, 0) if self.instance else 0)
            if value < 0:
                raise serializers.ValidationError({field: "Amount cannot be negative."})
        return attrs

class ExpenseSerializer(BusinessScopedSerializer):
    class Meta: model = Expense; fields = ["id", "business", "branch", "date", "category", "description", "amount", "payment_method", "created_by", "created_at"]; read_only_fields = ["id", "created_by", "created_at"]
    def validate_amount(self, value):
        if value < 0: raise serializers.ValidationError("Expense amount cannot be negative.")
        return value

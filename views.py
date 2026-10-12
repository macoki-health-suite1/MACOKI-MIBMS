from django.db.models import Q
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Business, Membership, Branch, Contact, Product, StockBatch, StockMovement, Sale, Purchase, Expense
from .serializers import BusinessSerializer, BranchSerializer, ContactSerializer, ProductSerializer, StockBatchSerializer, StockMovementSerializer, SaleSerializer, PurchaseSerializer, ExpenseSerializer


def accessible_businesses(user):
    """Businesses owned by the user or where the user has an explicit membership."""
    return Business.objects.filter(Q(owner=user) | Q(memberships__user=user)).distinct()


class AuthenticatedViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_accessible_business_ids(self):
        return accessible_businesses(self.request.user).values_list("id", flat=True)

    def perform_create(self, serializer):
        # All business-scoped serializers must supply a business the user can access.
        serializer.save()


class BusinessViewSet(AuthenticatedViewSet):
    serializer_class = BusinessSerializer

    def get_queryset(self):
        return accessible_businesses(self.request.user)

    def perform_create(self, serializer):
        business = serializer.save(owner=self.request.user)
        Membership.objects.get_or_create(business=business, user=self.request.user, defaults={"role": "owner"})


class BranchViewSet(AuthenticatedViewSet):
    serializer_class = BranchSerializer
    def get_queryset(self): return Branch.objects.filter(business_id__in=self.get_accessible_business_ids())

class ContactViewSet(AuthenticatedViewSet):
    serializer_class = ContactSerializer
    def get_queryset(self): return Contact.objects.filter(business_id__in=self.get_accessible_business_ids())

class ProductViewSet(AuthenticatedViewSet):
    serializer_class = ProductSerializer
    def get_queryset(self): return Product.objects.filter(business_id__in=self.get_accessible_business_ids())

class StockBatchViewSet(AuthenticatedViewSet):
    serializer_class = StockBatchSerializer
    def get_queryset(self): return StockBatch.objects.filter(business_id__in=self.get_accessible_business_ids())

class StockMovementViewSet(AuthenticatedViewSet):
    serializer_class = StockMovementSerializer
    def get_queryset(self): return StockMovement.objects.filter(business_id__in=self.get_accessible_business_ids())

class SaleViewSet(AuthenticatedViewSet):
    serializer_class = SaleSerializer
    def get_queryset(self): return Sale.objects.filter(business_id__in=self.get_accessible_business_ids())

class PurchaseViewSet(AuthenticatedViewSet):
    serializer_class = PurchaseSerializer
    def get_queryset(self): return Purchase.objects.filter(business_id__in=self.get_accessible_business_ids())

class ExpenseViewSet(AuthenticatedViewSet):
    serializer_class = ExpenseSerializer
    def get_queryset(self): return Expense.objects.filter(business_id__in=self.get_accessible_business_ids())

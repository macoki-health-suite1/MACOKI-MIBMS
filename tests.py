from django.contrib.auth import get_user_model
from django.test import TestCase
from .models import Business, Branch, Product

class CoreModelTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="owner-test", password="not-a-real-password")
        self.business = Business.objects.create(name="Test Shop", owner=self.user)
    def test_business_defaults_to_ngn(self):
        self.assertEqual(self.business.currency, "NGN")
    def test_branch_code_is_saved(self):
        branch = Branch.objects.create(business=self.business, name="Main", code="MAIN")
        self.assertEqual(branch.code, "MAIN")
    def test_product_can_track_batch_and_expiry(self):
        product = Product.objects.create(business=self.business, name="Sample item", sku="TEST-001", track_batch=True, track_expiry=True)
        self.assertTrue(product.track_batch)
        self.assertTrue(product.track_expiry)

from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Membership, Contact

class TenantIsolationAPITests(APITestCase):
    def setUp(self):
        User = get_user_model()
        self.owner = User.objects.create_user(username="tenant-owner", password="Strong-test-password-123")
        self.other = User.objects.create_user(username="other-owner", password="Strong-test-password-456")
        self.business = Business.objects.create(name="Owner Shop", owner=self.owner)
        self.other_business = Business.objects.create(name="Other Shop", owner=self.other)
        self.product = Product.objects.create(business=self.business, name="Private product", sku="PRIVATE-1")
        self.other_product = Product.objects.create(business=self.other_business, name="Other product", sku="OTHER-1")

    def test_user_cannot_list_another_business_products(self):
        self.client.force_authenticate(user=self.other)
        response = self.client.get("/api/products/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data.get("results", response.data)
        returned_ids = {str(item["id"]) for item in results}
        self.assertNotIn(str(self.product.id), returned_ids)
        self.assertIn(str(self.other_product.id), returned_ids)

    def test_user_cannot_retrieve_another_business_product_by_id(self):
        self.client.force_authenticate(user=self.other)
        response = self.client.get(f"/api/products/{self.product.id}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_member_can_access_business_records(self):
        Membership.objects.create(business=self.business, user=self.other, role="viewer")
        self.client.force_authenticate(user=self.other)
        response = self.client.get("/api/products/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data.get("results", response.data)
        self.assertIn(str(self.product.id), {str(item["id"]) for item in results})

    def test_user_cannot_create_contact_for_unrelated_business(self):
        self.client.force_authenticate(user=self.other)
        response = self.client.post("/api/contacts/", {
            "business": str(self.business.id), "name": "Attempted cross-tenant contact", "kind": "customer"
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

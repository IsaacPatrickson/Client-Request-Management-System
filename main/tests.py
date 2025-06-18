from django.test import TestCase
from django.utils.timezone import make_aware
from datetime import datetime
from .models import Client, ClientRequest, RequestType


class ClientModelTest(TestCase):
    def test_create_client_with_valid_data(self):
        created_at = make_aware(datetime(2025, 6, 18, 14, 0))
        client = Client.objects.create(
            name="Test Client",
            email="client@example.com",
            contact_number="123456789",
            company_url="https://example.com",
            created_at=created_at
        )
        self.assertEqual(client.name, "Test Client")
        self.assertEqual(client.email, "client@example.com")
        self.assertEqual(client.contact_number, "123456789")
        self.assertEqual(client.company_url, "https://example.com")
        self.assertEqual(client.created_at, created_at)
        
class RequestTypeModelTest(TestCase):
    def test_create_request_type_with_valid_data(self):
        request_type = RequestType.objects.create(
            name="SEO Tech Check",
            description="Generic description of the request type. SEO Tech Check Description.",
        )
        self.assertEqual(request_type.name, "SEO Tech Check")
        self.assertIn("SEO Tech Check", request_type.description)        

class ClientRequestModelTest(TestCase):
    def test_create_client_request_with_dependencies(self):
        timestamp = make_aware(datetime(2025, 6, 18, 15, 0))
        client = Client.objects.create(
            name="Test Client",
            email="client@example.com",
            contact_number="123456789",
            company_url="https://example.com",
            created_at=timestamp
        )

        request_type = RequestType.objects.create(
            name="SEO Tech Check",
            description="SEO Tech Check Description."
        )

        client_request = ClientRequest.objects.create(
            client=client,
            request_type=request_type,
            description="Run an SEO Check for VetPartners.",
            status="In Progress",
            created_at=timestamp,
            updated_at=timestamp
        )

        self.assertEqual(client_request.client.name, "Test Client")
        self.assertEqual(client_request.request_type.name, "SEO Tech Check")
        self.assertEqual(client_request.status, "In Progress")
        self.assertIn("VetPartners", client_request.description)
        self.assertEqual(client_request.created_at, timestamp)




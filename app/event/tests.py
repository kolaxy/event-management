from django.test import TestCase
from django.utils import timezone
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model

from .models import Organization, Event


class OrganizationModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="testuser@example.com", password="testpassword"
        )
        self.organization = Organization.objects.create(
            founder=self.user,
            title="Test Organization",
            description="Test Organization Description",
            address="Test Address",
            postcode="12345",
        )

    def test_organization_str(self):
        self.assertEqual(str(self.organization), "Test Organization")

    def test_organization_members(self):
        self.assertEqual(self.organization.members.count(), 0)
        new_member = get_user_model().objects.create_user(
            email="newuser@example.com", password="newpassword"
        )
        self.organization.members.add(new_member)
        self.assertEqual(self.organization.members.count(), 1)


class EventModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="testuser@example.com", password="testpassword"
        )
        self.organization = Organization.objects.create(
            founder=self.user,
            title="Test Organization",
            description="Test Organization Description",
            address="Test Address",
            postcode="12345",
        )
        self.event = Event.objects.create(
            title="Test Event",
            description="Test Event Description",
            date=timezone.now(),
        )
        self.event.organizations.add(self.organization)

    def test_event_str(self):
        self.assertEqual(str(self.event), "Test Event")

    def test_event_organizations(self):
        self.assertEqual(self.event.organizations.count(), 1)
        new_organization = Organization.objects.create(
            founder=self.user,
            title="New Test Organization",
            description="New Test Organization Description",
            address="New Test Address",
            postcode="54321",
        )
        self.event.organizations.add(new_organization)
        self.assertEqual(self.event.organizations.count(), 2)

    def test_event_image_upload(self):
        image = SimpleUploadedFile(
            "test_image.jpg", b"content", content_type="image/jpeg"
        )
        self.event.image = image
        self.event.save()
        self.assertIsNotNone(self.event.image)

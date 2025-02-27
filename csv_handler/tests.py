from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import UserModel

# Create your tests here.


class CSVUploadTests(APITestCase):

    def test_upload_valid_csv(self):
        # Arrange
        csv_data = """name,email,age
                        John Doe,john@example.com,30
                        Jane Smith,jane@example.com,25
                        Alice Johnson,alice@example.com,40"""
        csv_file = SimpleUploadedFile("valid_users.csv", csv_data.encode('utf-8'), content_type="text/csv")

        # Act
        url = reverse('csv_upload')
        response = self.client.post(url, {'file': csv_file}, format='multipart')

        # Assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['total_saved'], 3)
        self.assertEqual(response.data['total_rejected'], 0)
        self.assertEqual(UserModel.objects.count(), 3)  # Verify data saved to database

    def test_upload_invalid_csv(self):
        # Arrange
        csv_data = """name,email,age
                      Bob Brown,john@example.com,35
                      John Doe,john@example.com,30"""
        csv_file = SimpleUploadedFile("invalid_users.csv", csv_data.encode('utf-8'), content_type="text/csv")

        # Act
        url = reverse('csv_upload')
        response = self.client.post(url, {'file': csv_file}, format='multipart')

        # Assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['total_saved'], 1)
        self.assertEqual(response.data['total_rejected'], 1)
        self.assertEqual(UserModel.objects.count(), 1)  # Only 1 user should be added

    def test_upload_empty_name(self):
         # Arrange
        csv_data = """name,email,age
,test@example.com,20"""
        csv_file = SimpleUploadedFile("invalid_users.csv", csv_data.encode('utf-8'), content_type="text/csv")

        # Act
        url = reverse('csv_upload')
        response = self.client.post(url, {'file': csv_file}, format='multipart')

        # Assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['total_saved'], 0)
        self.assertEqual(response.data['total_rejected'], 1)
        self.assertEqual(UserModel.objects.count(), 0)  # Only 1 user should be added
        self.assertIn("Name must be a non-empty string", str(response.data['rejected_records']))

    def test_upload_invalid_age(self):
        # Arrange
        csv_data = """name,email,age
test,test@example.com,200"""
        csv_file = SimpleUploadedFile("invalid_users.csv", csv_data.encode('utf-8'), content_type="text/csv")

        # Act
        url = reverse('csv_upload')
        response = self.client.post(url, {'file': csv_file}, format='multipart')

        # Assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['total_saved'], 0)
        self.assertEqual(response.data['total_rejected'], 1)
        self.assertEqual(UserModel.objects.count(), 0)  # Only 1 user should be added
        self.assertIn("Age must be an integer between 0 and 120", str(response.data['rejected_records']))

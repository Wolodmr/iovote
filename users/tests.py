from django.test import TestCase
from django.test import TestCase
from django.contrib.auth.models import User

class UserListAccessTests(TestCase):
    """Test access control for the User List page."""

    def setUp(self):
        """Create a superuser and a regular user."""
        self.superuser = User.objects.create_superuser(username="admin", password="admin123")
        self.regular_user = User.objects.create_user(username="user", password="user123")

    def test_superuser_can_access_user_list(self):
        """Ensure superusers can access the user list."""
        self.client.login(username="admin", password="admin123")
        response = self.client.get("/users/list/")
        self.assertEqual(response.status_code, 200)

    def test_regular_user_cannot_access_user_list(self):
        """Ensure regular users cannot access the user list."""
        self.client.login(username="user", password="user123")
        response = self.client.get("/users/list/")
        self.assertNotEqual(response.status_code, 200)  # Should redirect or deny access

# Create your tests here.


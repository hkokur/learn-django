from django.contrib.auth import get_user_model
from django.test import TestCase

# Create your tests here.
class CustomUserTests(TestCase):
    # test the creating user successfully
    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            username = 'adam',
            email = 'adam@email.com',
            password = 'password'
        )
        self.assertEqual(user.username, 'adam')
        self.assertEqual(user.email, 'adam@email.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    # test the creating superuser successfully
    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(
            username = 'admin',
            email = 'admin@email.com',
            password = 'password'
        )
        self.assertEqual(admin_user.username , 'admin')
        self.assertEqual(admin_user.email , 'admin@email.com')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)

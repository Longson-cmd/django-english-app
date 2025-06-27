from django.test import TestCase
from django.contrib.auth.models import User


class CustomerProfileTestCase(TestCase):
    def setUp(self):
        User.objects.create_user(username='default', email='default@example.com', password='dummy')
        # This will trigger the signal to auto-create CustomerProfile
        self.user = User.objects.create_user(username='user1')

    def test_is_paying_customer(self):
        # Check the default value of is_paying_customer
        self.assertFalse(self.user.customerprofile.is_paying_customer)

        # Update the value
        # self.user.customerprofile.is_paying_customer = True
        # self.user.customerprofile.save()

        # Re-fetch to make sure the change is saved
        # updated_user = User.objects.get(username='user1')
        # self.assertTrue(updated_user.customerprofile.is_paying_customer)



# Create your tests here.

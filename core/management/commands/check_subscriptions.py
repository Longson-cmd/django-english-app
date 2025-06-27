# core/management/commands/check_subscriptions.py


from django.core.management.base import BaseCommand
from core.models import CustomerProfile

class Command(BaseCommand):
    help = "Disable expired paying customers"

    def handle(self, *args, **kwargs):
        for profile in CustomerProfile.objects.filter(is_paying_customer=True):
            profile.check_payment_status()

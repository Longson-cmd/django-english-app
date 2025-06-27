from django.db import models
from django.contrib.auth.models import User

from datetime import timedelta
from django.utils import timezone

class CustomerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_paying_customer = models.BooleanField(default=False)
    payment_date = models.DateTimeField(null=True, blank=True)
    paid_until = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {'Paying' if self.is_paying_customer else 'Free'}"
    def activate_monthly_payment(self):
        self.is_paying_customer = True
        self.payment_date = timezone.now()
        self.paid_until = timezone.now() + timedelta(days=30)
        self.save()

    def check_payment_status(self):
        if self.paid_until and self.paid_until < timezone.now():
            self.is_paying_customer = False
            self.save()





class Sentences(models.Model):
    word = models.ForeignKey('Words', on_delete=models.CASCADE)
    sentence = models.TextField()
    audio = models.CharField(max_length=255)

    class Meta:
        db_table = 'sentences'


class Words(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    word_key = models.CharField(max_length=100, blank=True, null=True)
    number = models.IntegerField()
    audio = models.CharField(max_length=255,  blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'words'

class SelfIntroduce(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sentence = models.TextField()
    class Meta:
        db_table = "self_introduce"


class DefaultCategories(models.Model):
    category_key = models.CharField(max_length=100)
    introduction_phrase = models.TextField()

    class Meta:
        db_table = 'default_categories'


class DefaultOptions(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey("DefaultCategories", on_delete=models.DO_NOTHING)
    option = models.CharField(max_length=255)
    is_user_choice = models.BooleanField(default=False)

    class Meta:
        db_table = 'default_options'

class Topics(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    topic_name = models.CharField(max_length=100)
    is_user_choice = models.BooleanField(default=False)

    class Meta:
        db_table = 'topics'

# python manage.py inspectdb words sentences | Out-File -Encoding utf8 core/models.py
# python manage.py migrate appname --fake
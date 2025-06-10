from django.db import models


class Sentences(models.Model):
    word = models.ForeignKey('Words', on_delete=models.CASCADE)
    sentence = models.TextField()
    audio = models.CharField(max_length=255)

    class Meta:
        db_table = 'sentences'


class Words(models.Model):
    word_key = models.CharField(max_length=100, blank=True, null=True)
    number = models.IntegerField()
    audio = models.CharField(max_length=255,  blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'words'

class SelfIntroduce(models.Model):
    sentence = models.TextField()
    class Meta:
        db_table = "self_introduce"


class DefaultCategories(models.Model):
    category_key = models.CharField(max_length=100)
    introduction_phrase = models.TextField()

    class Meta:
        db_table = 'default_categories'


class DefaultOptions(models.Model):
    category = models.ForeignKey("DefaultCategories", on_delete=models.DO_NOTHING)
    option = models.CharField(max_length=255)
    is_user_choice = models.BooleanField(default=False)

    class Meta:
        db_table = 'default_options'

class Topics(models.Model):
    topic_name = models.CharField(max_length=100)
    is_user_choise = models.BooleanField(default=False)

    class Meta:
        db_table = 'topics'

# python manage.py inspectdb words sentences | Out-File -Encoding utf8 core/models.py
# python manage.py migrate appname --fake
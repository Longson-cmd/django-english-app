from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from core.models import Words, SelfIntroduce, DefaultOptions, Sentences, Topics, CustomerProfile

@receiver(post_save, sender=User)
def create_customer_profile(sender, instance, created, **kwargs):
    if created:
        CustomerProfile.objects.create(user=instance)

@receiver(post_save, sender = User)
def create_user_default_data(sender, instance, created, **kwargs):
    if created and instance.username != "default":
        print(f"Cloning default data for: {instance.username}")
        default_user = User.objects.get(username = "default")

        for word in Words.objects.filter(user = default_user):
            new_word = Words.objects.create(
                user = instance,
                word_key = word.word_key,
                number = word.number,
                audio = word.audio,
                notes = word.notes
            )

            for s in Sentences.objects.filter(word = word):
                Sentences.objects.create(
                    word = new_word,
                    sentence = s.sentence,
                    audio = s.audio
                )

        for s in SelfIntroduce.objects.filter(user = default_user):
            SelfIntroduce.objects.create(
                user = instance,
                sentence = s.sentence
            )

        for topic in Topics.objects.filter(user = default_user):
            Topics.objects.create(
                user = instance,
                topic_name = topic.topic_name,
                is_user_choice = topic.is_user_choice
            )

        for defaultOption in DefaultOptions.objects.filter(user = default_user):
            DefaultOptions.objects.create(
                user = instance,
                category = defaultOption.category,
                option = defaultOption.option,
                is_user_choice = defaultOption.is_user_choice
            )
        print(f"finished Cloning default data for: {instance.username}")
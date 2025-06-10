from django.core.management.base import BaseCommand
from core.models import Words, Sentences, SelfIntroduce, DefaultCategories, DefaultOptions, Topics
import json
import os

class Command(BaseCommand):
    help = "Import words from JSON file"

    def handle(self, *args, **options):
        official_path = os.path.join("core", "management", "data", "official.json")

        with open(official_path, 'r', encoding="utf-8") as f:
            words_data = json.load(f)

        if Words.objects.exists():
            print("words table was already imported.")
        else:
            for item in words_data:
                word = Words.objects.create(
                    word_key=item['key'],
                    number=item["number"],
                    audio=item["audio"],
                    notes='no notes'
                )

                for s in item["sentences"]:
                    Sentences.objects.create(
                        word=word,
                        sentence=s["sentence"],
                        audio=s['audio']
                    )

        self.stdout.write(self.style.SUCCESS(
            f"Imported {Words.objects.count()} words successfully"
        ))

        self_path = os.path.join("core", "management", "data", "self.json")
        with open(self_path, 'r', encoding="utf-8") as f:           
            self_data = json.load(f)
        self_introduce = self_data["self_introduce"]
        default_introduction = self_data["default_introduction"]
        topics = self_data["topics"]
    
        if Topics.objects.exists():
            print("data self tables was already imported")
        else: 
            for s in self_introduce:
                SelfIntroduce.objects.create(sentence = s) 
            for item in default_introduction:
                category_key = DefaultCategories.objects.create(
                    category_key = item["key"],
                    introduction_phrase = item["introduction_phrace"]
                )

                for op in item["options"]:
                    DefaultOptions.objects.create(
                        category = category_key,
                        option = op,
                        is_user_choice = op in item["UserChoices"]
                    )

            for topic in topics["daily_conversation_topics"]:
                Topics.objects.create(
                    topic_name = topic,
                    is_user_choise = topic in topics['userChoises']
                )
            
            self.stdout.write(self.style.SUCCESS(
                f"Imported self.json words successfully"
            ))
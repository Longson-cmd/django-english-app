import os

from gtts import gTTS
from django.core.management.base import BaseCommand
from django.conf import settings
from core.models import Words, Sentences

class Command(BaseCommand):
    help = "Generate audio files for words and sentences"
    def handle(self, *args, **kwargs):

        print(settings.BASE_DIR)
        for w in Words.objects.all():
            word_key = w.word_key
            w_relative_path = w.audio.replace("backend/", "")   
            w_absolute_path = os.path.join(settings.BASE_DIR, w_relative_path)
            if not os.path.exists(w_absolute_path):
                tts = gTTS(text = word_key, lang='en')
                tts.save(w_absolute_path)
        
        for s in Sentences.objects.all():
            sentence = s.sentence
            s_relative_audio = s.audio.replace("backend/", "")
            s_absolute_audio = os.path.join(settings.BASE_DIR, s_relative_audio)
            if not os.path.exists(s_absolute_audio):
                tts = gTTS(text = sentence, lang= "en")
                tts.save(s_absolute_audio)
        
        self.stdout.write(self.style.SUCCESS(
                "create demo audios cessfully"
            ))
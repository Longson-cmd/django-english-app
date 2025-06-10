from django.http import JsonResponse
from core.models import Sentences, Words
import json
import os 
from django.views.decorators.csrf import csrf_exempt

from utils.paths import sentences_dir
from utils.file_utils import safe_filename
from gtts import gTTS
from core.forms import AddSentenceForm

@csrf_exempt
def add_sentences(request):
    if request.method == "POST":
        data = json.loads(request.body)

        form = AddSentenceForm(data)
        if not form.is_valid():
            return JsonResponse({"message": form.errors}, status= 400)


        frontend_word = form.cleaned_data['word']
        frontend_sentence = form.cleaned_data['sentence']

        word = Words.objects.get(word_key = frontend_word)
        word.number -= 1
        word.save()

        Sentences.objects.create(
            word = word,
            sentence = frontend_sentence,
            audio = f"backend/audios/sentences/{safe_filename(frontend_sentence)}"
        )

        if not os.path.exists(os.path.join(sentences_dir, safe_filename(frontend_sentence))):
            tts = gTTS(text = frontend_sentence, lang = 'en')
            tts.save(os.path.join(sentences_dir, safe_filename(frontend_sentence)))

        return JsonResponse({"message": "added sentence"}, status = 201)
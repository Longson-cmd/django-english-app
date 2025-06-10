# add_words, get_words, delete_word, get_list_words


from django.http import JsonResponse, FileResponse
import json
from django.views.decorators.csrf import csrf_exempt
from gtts import gTTS
import os
from django.conf import settings
from core.models import Words, Sentences
from utils.paths import words_dir
from django.core.paginator import Paginator

@csrf_exempt
def add_words(request):
    if request.method =="POST":
        data = json.loads(request.body)

        if Words.objects.filter(word_key = data['word']).exists() : 
            word = Words.objects.get(word_key = data['word'])
            word.number += 1
            word.save()
            return JsonResponse({"message": f"add more number on {data['word']}"}, status = 201)
        else:
            word = Words.objects.create(
                word_key = data['word'],
                number = 4,
                notes = 'no notes',
                audio = f"backend/audios/words/{data['word']}.mp3"
            )

            if not os.path.exists(os.path.join(words_dir, f"{data['word']}.mp3")):
                tts = gTTS(text = data["word"], lang='en')
                tts.save(os.path.join(words_dir, f"{data['word']}.mp3"))
             
            return JsonResponse({"message": "added new word"}, status = 201)
        
@csrf_exempt
def delete_word(request):
    if request.method == 'DELETE':
        data = json.loads(request.body)

        try: 
            w= Words.objects.get(word_key = data['word'])
            audio_path = w.audio.replace("backend/", "")
            word_audio_path = os.path.join(settings.BASE_DIR, audio_path)
            print("Word audio path:", word_audio_path)
            if os.path.exists(word_audio_path):
                os.remove(word_audio_path)
            for s in Sentences.objects.filter(word = w):
                s_audio_path = s.audio.replace("backend/", "")
                print("sentence audio path:", s_audio_path)
                if os.path.exists(s_audio_path):
                    os.remove(s_audio_path)
            w.delete()
            return JsonResponse({"message": "deleted word"})
        except: 
            return JsonResponse({"message": 'there is an error'}, status = 405)



@csrf_exempt
def add_notes(request):
    if request.method == "PUT":
        data = json.loads(request.body)
        word = data['word']
        notes = data['text']
        w = Words.objects.get(word_key = word)
        w.notes = notes
        w.save()
        return JsonResponse({"message": "added notes"})
    

def get_list_words(request):
    currentPage = request.GET.get("page", 1)
    page_size = request.GET.get("size", 10)


    words = Words.objects.all().order_by('-id')

    paginator = Paginator(words, page_size)
    page = paginator.page(currentPage)

    result = []

    for word in page.object_list:
        sentences = Sentences.objects.filter(word = word)
        result.append({
            "key": word.word_key,
            "number": word.number,
            "audio": word.audio,
            "notes": word.notes,
            "sentences": [
                {'sentence': s.sentence, "audio": s.audio} for s in sentences
            ]
        })

    print(page_size)
    print(page.has_next())
    return JsonResponse({
        "words": result,
        "has_next": page.has_next(),
        "has_previous": page.has_previous(),
        "totalPages": paginator.num_pages
    }, safe= False)


def get_words(request):
    words = Words.objects.all()

    result = []

    for word in words:
        sentences = Sentences.objects.filter(word = word)
        result.append({
            "key": word.word_key,
            "number": word.number,
            "audio": word.audio,
            "sentences": [
                {'sentence': s.sentence, "audio": s.audio} for s in sentences
            ]
        })

    return JsonResponse(result, safe= False)
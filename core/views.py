from django.http import JsonResponse, FileResponse, Http404
from .models import Words, Sentences, SelfIntroduce, DefaultCategories, DefaultOptions, Topics
from django.views.decorators.csrf import csrf_exempt
import json
import os
from gtts import gTTS


from django.conf import settings
from django.core.paginator import Paginator


from utils.paths import words_dir, sentences_dir
from utils.file_utils import safe_filename

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
                audio = f"backend/audios/words/{data['word']}.mp3"
            )

            if not os.path.exists(os.path.join(words_dir, f"{data['word']}.mp3")):
                tts = gTTS(text = data["word"], lang='en')
                tts.save(os.path.join(words_dir, f"{data['word']}.mp3"))
             
            return JsonResponse({"message": "added new word"}, status = 201)


@csrf_exempt
def add_sentences(request):
    if request.method == "POST":
        data = json.loads(request.body)
        frontend_word = data['word']
        frontend_sentence = data['sentence']

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

@csrf_exempt
def delete_word(request):
    if request.method == 'DELETE':
        data = json.loads(request.body)

        try: 
            Words.objects.get(word_key = data['word']).delete()
            return JsonResponse({"message": "deleted word"})
        except: 
            return JsonResponse({"message": 'there is an error'}, status = 405)


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


def get_self(request):
    self_introduce = []
    default_introduction = []
    topics = []
    for sentence in SelfIntroduce.objects.all():
        self_introduce.append(sentence.sentence)

    for category in DefaultCategories.objects.all():
        options = []
        UserChoices = []
        for op in DefaultOptions.objects.filter(category = category):
            options.append(op.option)
            if op.is_user_choice == 1:
                UserChoices.append(op.option)

        default_introduction.append({
            "key": category.category_key, 
            "introduction_phrace": category.introduction_phrase,
            "options" : options,
            "UserChoices": UserChoices
        })


    daily_conversation_topics = []
    UserChoices = []
    for topic in Topics.objects.all():
        daily_conversation_topics.append(topic.topic_name)
        if topic.is_user_choise == 1:
            UserChoices.append(topic.topic_name)
    topics = {
        "daily_conversation_topics": daily_conversation_topics,
        "userChoises": UserChoices
    }
    

    return JsonResponse({
        "self_introduce": self_introduce,
        "default_introduction": default_introduction, 
        "topics": topics
    }, safe=False)


def get_self_promt(request):
    self_introduce = []
    topics = []
    for sentence in SelfIntroduce.objects.all():
        self_introduce.append(sentence.sentence)

    for category in DefaultCategories.objects.all():
        ops = DefaultOptions.objects.filter(category = category,  is_user_choice = 1)
        for op in ops:
            self_introduce.append(category.introduction_phrase + " " + op.option)


    for topic in Topics.objects.filter(is_user_choise = 1):
        topics.append(topic.topic_name)

    return JsonResponse({
        "self_introduce": self_introduce,
        "topics":  topics
    }, safe=False)

@csrf_exempt
def update_self(request):
    if request.method == "PUT":
        data = json.loads(request.body)
        key = data['key']

        if key == 'default_introduction':
            for item in data['default_introduction']:
                for option in item['options']:
                    defaultOption_obj = DefaultOptions.objects.get(option = option)
                    defaultOption_obj.is_user_choice = option in item['UserChoices']
                    defaultOption_obj.save()
        if key == "self_introduce":
            SelfIntroduce.objects.all().delete()
            for sentence in data["self_introduce"]:
                SelfIntroduce.objects.create(
                    sentence = sentence
                )

        if key == "topics":
            for topic in data['topics']["daily_conversation_topics"]:
                topic_obj = Topics.objects.get(topic_name = topic)
                topic_obj.is_user_choise = topic in data['topics']["userChoises"]
                topic_obj.save()

        return JsonResponse({"message": "updated self introdutions and topics"}, status = 201)
            
def serve_audio(request, filename):
    audio_path = os.path.join(settings.BASE_DIR, 'audios', filename)

    if os.path.exists(audio_path):
        return FileResponse(open(audio_path, 'rb'))
    else:
        raise Http404("Audio file not found")

# Create your views here.

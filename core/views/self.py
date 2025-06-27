from django.http import JsonResponse
from core.models import SelfIntroduce, DefaultCategories, DefaultOptions, Topics
from django.views.decorators.csrf import csrf_exempt
import json

def get_self(request):
    self_introduce = []
    default_introduction = []
    topics = []
    for sentence in SelfIntroduce.objects.filter(user = request.user):

        self_introduce.append(sentence.sentence)

    for category in DefaultCategories.objects.all():
        options = []
        UserChoices = []
        for op in DefaultOptions.objects.filter(category = category, user = request.user):
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
    for topic in Topics.objects.filter(user = request.user):
        daily_conversation_topics.append(topic.topic_name)
        if topic.is_user_choice == 1:
            UserChoices.append(topic.topic_name)
    topics = {
        "daily_conversation_topics": daily_conversation_topics,
        "userchoices": UserChoices
    }
    

    return JsonResponse({
        "self_introduce": self_introduce,
        "default_introduction": default_introduction, 
        "topics": topics
    }, safe=False)


def get_self_promt(request):
    self_introduce = []
    topics = []
    for sentence in SelfIntroduce.objects.filter(user = request.user):
        self_introduce.append(sentence.sentence)

    for category in DefaultCategories.objects.all():
        ops = DefaultOptions.objects.filter(category = category,  is_user_choice = 1)
        for op in ops:
            self_introduce.append(category.introduction_phrase + " " + op.option)


    for topic in Topics.objects.filter(is_user_choice = 1, user = request.user):
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
                    defaultOption_obj = DefaultOptions.objects.get(option = option, user = request.user)
                    defaultOption_obj.is_user_choice = option in item['UserChoices']
                    defaultOption_obj.save()
        if key == "self_introduce":
            SelfIntroduce.objects.filter(user = request.user).delete()
            for sentence in data["self_introduce"]:
                SelfIntroduce.objects.create(
                    user = request.user,
                    sentence = sentence
                )

        if key == "topics":
            for topic in data['topics']["daily_conversation_topics"]:
                topic_obj = Topics.objects.get(topic_name = topic, user = request.user)
                topic_obj.is_user_choice = topic in data['topics']["userchoices"]
                topic_obj.save()

        return JsonResponse({"message": "updated self introdutions and topics"}, status = 201)
            
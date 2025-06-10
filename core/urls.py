from django.urls import path
from core.views.sentences import add_sentences
from core.views.self import  get_self, get_self_promt, update_self
from core.views.words import add_words, get_words, delete_word, get_list_words, add_notes
from core.views.audios import serve_audio

urlpatterns = [
    path("list_words/", get_list_words, name = 'get_list_words'),
    path("words/", get_words, name = 'get_words'),
    path("words/add/", add_words, name = 'add_words'),
    path("add_notes/", add_notes, name = 'add_notes'),
    path("words/add_sentence/", add_sentences, name = 'add_sentences'),
    path("words/delete", delete_word, name = 'delete_word'),
    path("self/", get_self, name = 'get_self'),
    path("update_self/", update_self, name = 'update_self'),
    path("self_prompt/", get_self_promt, name = 'get_self_promt'),
    path('backend/audios/<path:filename>', serve_audio, name = 'serve_audio'),
]


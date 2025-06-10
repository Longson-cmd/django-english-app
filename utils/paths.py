import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)

AUDIO_BASE = os.path.join(PROJECT_ROOT, 'audios')
words_dir = os.path.join(AUDIO_BASE, 'words')
sentences_dir = os.path.join(AUDIO_BASE, 'sentences')

os.makedirs(words_dir, exist_ok=True)
os.makedirs(sentences_dir, exist_ok=True)

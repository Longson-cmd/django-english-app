# Django English App

This is a full-stack app built with Django (backend), MySQL (database), and Vue.js (frontend).

# Django English Backend

This is the backend for the English Speaking App. It is built with:

- Django 5.2
- MySQL (external or Railway-hosted)
- gTTS for text-to-speech
- Docker support for easy deployment

---
pip install -r requirements.txt

# MIRGRATE, IMPORT JSON FILE AND CREATE AUDIO

python manage.py migrate
python manage.py import_jsons
python manage.py create_audios

# RUN PROJECT

python manage.py runserver




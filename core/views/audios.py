
from django.http import FileResponse, Http404
import os
from django.conf import settings

def serve_audio(request, filename):
    audio_path = os.path.join(settings.BASE_DIR, 'audios', filename)

    if os.path.exists(audio_path):
        return FileResponse(open(audio_path, 'rb'))
    else:
        raise Http404("Audio file not found")

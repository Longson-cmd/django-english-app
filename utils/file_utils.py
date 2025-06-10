import re

def safe_filename(sentence):
    filename = re.sub(r'[^\w\s]', '', sentence)
    filename = filename.replace(' ', '_')
    return filename + '.mp3'

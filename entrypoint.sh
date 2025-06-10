
#!/bin/sh
set -e
sh ./wait-for-it.sh db 3306

python manage.py migrate
python manage.py import_jsons
python manage.py runserver 0.0.0.0:8000
if (Test-Path "core\migrations") { Remove-Item "core\migrations" -Recurse -Force }
python manage.py makemigrations core
python manage.py migrate
python manage.py import_jsons


python manage.py createsuperuser
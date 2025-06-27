from django.http import JsonResponse
from django.contrib.auth.models import User
from  django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
import json


@csrf_exempt
def resigter_user(request):
    if request.method == "POST":
        data = json.loads(request.body)
        email = data["email"]
        username = email
        password = data["password"]

        if User.objects.filter(email = email).exists():
            return JsonResponse({"message": "this account already exists"}, status = 400)

        user = User.objects.create_user(
            email = email,
            username = username,
            password = password
        )

        user.save()
        return JsonResponse({"message": "created new account successfully"}, status = 201)

    return JsonResponse({"message": "Invalid method"}, status = 405)
        
@csrf_exempt
def login_user(request):
    if request.method == "POST":
        data = json.loads(request.body)
        email = data["email"]
        password = data["password"]

        user = authenticate(request, username = email, password = password)
        if user is not None:
            login(request, user)
            print("User after login:", request.user)  # ✅ Print here
            print("Session key:", request.session.session_key)

            return JsonResponse({"message" : "logged in successfully"})

        return JsonResponse({"message": "invalid credentials"}, status=401)
    return JsonResponse({"message": "invalid method"}, status = 405)
    # if request.method == "PUT":
    #     data = json.loads(request.body)

# Remove-Item -Path "core/migrations" -Recurse
# python manage.py makemigrations core; python manage.py migrate; python manage.py import_jsons
# curl -X POST http://localhost:8000/register/ ^
#  -H "Content-Type: application/json" ^
#  -d "{\"email\":\"test@example.com\", \"password\":\"1234abcd\"}"
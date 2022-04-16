import json

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token

User = get_user_model()


@csrf_exempt
def login_view(request):
    data = json.loads(request.body.decode("utf-8"))
    email = data.get("email", "")
    password = data.get("password", "")
    print(email, password)
    try:
        user = User.objects.get(email=email)
        matchcheck = check_password(password, user.password)
        if matchcheck:
            token, newly_created = Token.objects.get_or_create(user=user)
            return JsonResponse({"logged_in": True, "token": token.key})
        return JsonResponse({"logged_in": False})
    except User.DoesNotExist:
        return JsonResponse({"logged_in": False})

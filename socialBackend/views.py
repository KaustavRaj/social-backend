from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.utils.http import urlencode
from django.contrib.auth import logout as auth_logout
import environ

# Environment variables
env = environ.Env()

@login_required
def home(request):
  user = request.user
  auth_provider = request.session.get("social_auth_last_login_backend")

  print("auth_provider : ", auth_provider)

  social = user.social_auth.get(provider=auth_provider)

  appResponse = {
    "name" : user.username,
    "email": user.email,
    "access_token": social.extra_data['access_token'],
    "expires" : social.extra_data['expires'],
    "auth_time": social.extra_data['auth_time'],
    "provider" : auth_provider
  }

  print("appResponse : ", appResponse)

  redirectUrl = f'{env("EXPO_REDIRECT_URL")}/?{urlencode(appResponse)}'

  response = HttpResponse("", status=302)
  response['Location'] = redirectUrl
  return response

def logout(request):
  try:
    auth_logout(request)
    return JsonResponse({ "success": True })
  except:
    return JsonResponse({ "success": False })
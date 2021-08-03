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
  social = None

  existing_providers = ["google-oauth2", "facebook"]

  for each_provider in existing_providers:
    if user.social_auth.filter(provider=each_provider):
      social = user.social_auth.get(provider=each_provider)

  appResponse = {
    "name" : user.username,
    "email": user.email,
    "access_token": social.extra_data['access_token'],
    "expires" : social.extra_data['expires'],
    "auth_time": social.extra_data['auth_time'],
    "provider" : social.provider
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
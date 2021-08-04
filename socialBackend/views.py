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
  connected_providers = list(user.social_auth.values_list('provider', 'modified'))
  recently_used_provider = sorted(connected_providers, key=lambda x: x[1], reverse=True)[0][0]

  print("connected_providers : ", connected_providers)
  print("recently used provider : ", recently_used_provider)

  social = user.social_auth.get(provider=recently_used_provider)

  appResponse = {
    "name" : f'{user.first_name} {user.last_name}',
    "email": user.email,
    "access_token": social.extra_data['access_token'],
    "expires" : social.extra_data['expires'],
    "auth_time": social.extra_data['auth_time'],
    "provider" : recently_used_provider
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
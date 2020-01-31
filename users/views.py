from django.shortcuts import render, redirect
import google.oauth2.credentials
import google_auth_oauthlib.flow
import os
from oauth2client.client import OAuth2WebServerFlow
from django.conf import settings

# Create your views here.
SCOPES = ['https://www.googleapis.com/auth/fitness.body.read']
def authenticate(request):
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
    os.path.abspath('E:/research/heartRate/users/client_secret.json'),
    ['https://www.googleapis.com/auth/fitness.body.read'])
    
    flow.redirect_uri = 'http://localhost:8000/redirect'

    authorization_url, state = flow.authorization_url(access_type='offline', include_granted_scopes='true')
    request.session['STATE'] = state
    return redirect(authorization_url) 

def redirectView(request):
    state = request.session['STATE']
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
    os.path.abspath('E:/research/heartRate/users/client_secret.json'), scopes=SCOPES, state=state)
    flow.redirect_uri = 'http://localhost:8000/home'

    authorization_response = request.build_absolute_uri()
    flow.fetch_token(authorization_response = authorization_response)
    
    credentials = flow.CredentialsModel
    request.session['credentials'] = credentials_to_dict(credentials)

    return redirect('home-view') 

def home(request): 
    return render(request, 'users/index.html') 

def credentials_to_dict(credentials):
  return {'token': credentials.token,
          'refresh_token': credentials.refresh_token,
          'token_uri': credentials.token_uri,
          'client_id': credentials.client_id,
          'client_secret': credentials.client_secret,
          'scopes': credentials.scopes}
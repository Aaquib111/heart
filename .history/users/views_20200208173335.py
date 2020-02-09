from django.shortcuts import render, redirect
import google.oauth2.credentials
import google_auth_oauthlib.flow
import os
from oauth2client.client import OAuth2WebServerFlow
from django.conf import settings
from googleapiclient.discovery import build
import json
from django.http import JsonResponse

from rest_framework.views import APIView
from rest_framework.response import Response
# Create your views here.
#E:/research/heartRate/users/client_secret.json
#C:/Users/Saquib/research-proj/users/client_secret.json

SCOPES = ['https://www.googleapis.com/auth/fitness.body.read']
API_SERVICE_NAME = 'fitness'
API_VERSION = 'v1'
DATA_SET = "3051700038292387000-1451700038292387000"
LIMIT = 30

def authenticate(request):
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
    os.path.abspath('E:/research/heartRate/users/client_secret.json'),
    ['https://www.googleapis.com/auth/fitness.body.read'])
    
    flow.redirect_uri = 'http://localhost:8000/redirect/'

    authorization_url, state = flow.authorization_url(access_type='offline', include_granted_scopes='true')
    request.session['STATE'] = state
    return redirect(authorization_url) 

def redirectView(request):
    state = request.session['STATE']
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
    os.path.abspath('E:/research/heartRate/users/client_secret.json'), scopes=SCOPES, state=state)
    flow.redirect_uri = 'http://localhost:8000/redirect/'
    authorization_response = request.get_full_path() #build_absolute_uri()
    flow.fetch_token(authorization_response = authorization_response)
    credentials = flow.credentials
    request.session['credentials'] = credentials_to_dict(credentials)
    return redirect('home-view')

class ChartData(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None, *args, **kwargs):
        if 'credentials' not in request.session:
            return redirect('auth-view') 
        credentials = google.oauth2.credentials.Credentials(
            **request.session['credentials']
        )
        service = build(
            API_SERVICE_NAME, API_VERSION, credentials=credentials
        )
        result = service.users().dataSources(). \
            datasets(). \
            get(userId='me', dataSourceId='derived:com.google.heart_rate.bpm:com.google.android.gms:merge_heart_rate_bpm', datasetId=DATA_SET, limit = LIMIT). \
            execute()
        
        request.session['credentials'] = credentials_to_dict(credentials)
        #print(json.dumps(result, indent=4, sort_keys=True))
        defaultData = []
        label = []

        for pt in result['point']:
            print(pt)
            defaultData.append(pt['value'][0]['fpVal'])

        for i in range(LIMIT):
            label.append(i)
        #print(json.dumps(defaultData, indent=4, sort_keys=True))

        data = {
            'context': defaultData,
            'label': label
        }
        #print(json.dumps(context, indent=4, sort_keys=True))
        return Response(data) 

def credentials_to_dict(credentials):
  return {
          'token': credentials.token,
          'refresh_token': credentials.refresh_token,
          'token_uri': credentials.token_uri,
          'client_id': credentials.client_id,
          'client_secret': credentials.client_secret,
          'scopes': credentials.scopes
        }

def home(request):
    return render(request, 'users/index.html')
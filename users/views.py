from django.shortcuts import render, redirect
import google.oauth2.credentials
import google_auth_oauthlib.flow
import os
from oauth2client.client import OAuth2WebServerFlow
import heartRate.settings

# Create your views here.

def authenticate(request):
    FLOW = OAuth2WebServerFlow(
    'client_secrets.json',
    scope='https://www.googleapis.com/auth/fitness.body.read',
    redirect_uri='http://localhost:8000/redirect',
    prompt='consent')

    storage = DjangoORMStorage(CredentialsModel, 'id', request.user, 'credential') 
    credential = storage.get() 
  
    if credential is None or credential.invalid: 
        FLOW.params['state'] = xsrfutil.generate_token(settings.SECRET_KEY, 
                                                              request.user) 
        authorize_url = FLOW.step1_get_authorize_url() 
        return redirect(authorize_url) 
    else: 
        #http = httplib2.Http() 
        #http = credential.authorize(http) 
        #service = build('gmail', 'v1', http = http) #this
        print('access_token = ', credential.access_token) 
        status = True

    return render(request, 'index.html', {'status': status}) 

def redirectView(request):
    get_state = bytes(request.GET.get('state'), 'utf8') 
    if not xsrfutil.validate_token(settings.SECRET_KEY, get_state, 
                                   request.user): 
        return HttpResponseBadRequest() 
  
    credential = FLOW.step2_exchange(request.GET.get('code')) 
    storage = DjangoORMStorage(CredentialsModel, 'id', request.user, 'credential') 
    storage.put(credential) 
  
    print("access_token: % s" % credential.access_token) 
    return redirect("/") 

def home(request): 
    status = True
  
    if not request.user.is_authenticated: 
        return HttpResponseRedirect('admin') 
  
    storage = DjangoORMStorage(CredentialsModel, 'id', request.user, 'credential') 
    credential = storage.get() 
  
    try: 
        access_token = credential.access_token 
        resp, cont = Http().request("https://www.googleapis.com/auth/fitness.body.read", 
                                     headers ={'Host': 'www.googleapis.com', 
                                             'Authorization': access_token}) 
    except: 
        status = False
        print('Not Found') 
  
    return render(request, 'index.html', {'status': status}) 
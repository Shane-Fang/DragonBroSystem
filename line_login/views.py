from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .forms import CustomSignupForm
import requests
from django.http import HttpResponse
from urllib.parse import urlencode

@login_required
def enter_phone_number(request):
    if request.method == 'POST':
        form = CustomSignupForm(request.POST)
        if form.is_valid():
            request.user.phone_number = form.cleaned_data['phone_number']       
            request.user.save()
            return redirect('home') 
    else:
        form = CustomSignupForm()
    return render(request, 'enter_phone_number.html', {'form': form})

def line_notify_login(request):
    line_auth_url = "https://notify-bot.line.me/oauth/authorize"
    client_id = 'b4YL9iLIP4DRRbgV7HKW2j'
    redirect_uri = 'https://22bf-124-109-116-168.ngrok-free.app'
    state = 'NO_STATE'  # Optional, for CSRF protection

    params = {
        'response_type': 'code',
        'client_id': client_id,
        'redirect_uri': redirect_uri,
        'scope': 'notify',
        'state': state,  # Adjust scopes as needed
    }

    url = f"{line_auth_url}?{urlencode(params)}"
    return redirect(url)

@login_required
def line_notify_callback(request):
    code = request.GET.get('code')
    if not code:
        return HttpResponse("Error: No code provided", status=400)

    print('code: ', code)
    
    url = "https://notify-bot.line.me/oauth/token"
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': 'https://22bf-124-109-116-168.ngrok-free.app',
        'client_id': 'b4YL9iLIP4DRRbgV7HKW2j',
        'client_secret': 'AuXAMDZbU5RRTkmBGH3ZcgG1KAgG9eqgKzFMf8Eo6wz'
    }
    
    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        response_data = response.json()
        print(f"200: {response.status_code} - {response.text}")
        print(f"response_data: {response_data}")
        return response_data.get('access_token')
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None
    
def LINE_notify_send_msg(user_LINE_token, msg):

    headers = {
        "Authorization": "Bearer " + user_LINE_token, 
        "Content-Type" : "application/x-www-form-urlencoded"
    }

    payload = {'message': msg}
    r = requests.post("https://notify-api.line.me/api/notify", headers = headers, params = payload)
    print(f"LINE notify message return: {r}")
    

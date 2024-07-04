from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from allauth.socialaccount.models import SocialAccount
from .forms import CustomSignupForm
from allauth.socialaccount.models import SocialLogin
from member.models import User

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
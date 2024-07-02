from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from allauth.socialaccount.models import SocialAccount
from .forms import CustomSignupForm
from allauth.socialaccount.models import SocialLogin
from member.models import User


# Create your views here.
@login_required(login_url='log-in')
def main(request):
    """首頁
    """
    
    social_auth_user = SocialAccount.objects.get(user=request.user)
    provider = social_auth_user.provider
    extra_data = social_auth_user.extra_data

    print('item: ', extra_data.get('sub'))
    user = User.objects.get(line_token=extra_data.get('sub'))
    if not user.phone_number:
        return redirect('enter_phone_number')

    return render(request, 'member/login.html')


def log_in(request):
    """登入頁面
    """
    if request.user.is_authenticated:
        return redirect('/')
    return render(request, 'login.html')


def log_out(request):
    """登出
    """
    logout(request)
    return redirect('/')

@login_required
def enter_phone_number(request):
    if request.method == 'POST':
        form = CustomSignupForm(request.POST)
        if form.is_valid():
            request.user.phone_number = form.cleaned_data['phone_number']
            request.user.save()
            return render(request, 'member/login.html')
    else:
        form = CustomSignupForm()
    return render(request, 'enter_phone_number.html', {'form': form})
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from .models import User
from .forms import RegisterModelForm,UserUpdateForm
# Create your views here.
def index(request):
    return render(request, 'index/index.html')
def memberprofile(request):
    if not request.user.is_authenticated:
        return redirect('member:login.html')

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)

        if user_form.is_valid():
            user = user_form.save()
            return redirect('home')  # 重定向到确认页面

    else:
        user_form = UserUpdateForm(instance=request.user)


    return render(request, 'member/memberprofile.html', {
        'user_form': user_form,

        'title':'會員資訊'
    })
def memberlogin(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            # 重定向到主页或其他页面
            return redirect('home')
        else:
            # 如果用户不存在或密码错误，显示错误信息
            messages.error(request, 'Email或密碼錯誤')

    # 如果不是 POST 请求，则显示登录表单
    return render(request, 'member/login.html')
    

def user_logout(request):
    logout(request)
    messages.info(request, '已成功登出')
    return redirect('member:login')


def register(request):
    if request.method == 'POST':
        form = RegisterModelForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            # 密碼已在表單的 save 方法中設置，所以這裡不需要再設置
            # user.password = make_password(form.cleaned_data['password1'])
            if User.objects.filter(email=user.email).exists():
                return render(request, "member/register.html", {"error_message": "Email已存在"})
            user.save()
            # 根据需要处理其他逻辑，例如登录用户、发送邮件等
            return render(request, "member/register.html", {"success": '註冊成功'})
    else:
        form = RegisterModelForm()
    context={
        'form': form,
        'title':'註冊'
    }
    return render(request, "member/register.html",context )

from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from .models import User,Address
from .forms import RegisterModelForm,UserUpdateForm, RegisterAddressForm, AddressFormSet
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    context={
        'title':'榮哥海鮮'
    }
    return render(request, 'index/index.html',context)
def memberprofile(request):
    if not request.user.is_authenticated:
        return redirect('member:login')

    user_form = UserUpdateForm(request.POST or None, instance=request.user)
    address_formset = AddressFormSet(request.POST or None, instance=request.user)

    if request.method == 'POST':
        if user_form.is_valid() and address_formset.is_valid():
            user_form.save()
            address_formset.save()
            return redirect('home')  # 重定向到确认页面或其他适当页面

    return render(request, 'member/memberprofile.html', {
        'user_form': user_form,
        'address_formset': address_formset,
        'title': '會員資訊'
    })
def memberlogin(request):
    if request.method == 'POST':
        phone_number = request.POST['phone_number']
        password = request.POST['password']
        user = authenticate(request, phone_number=phone_number, password=password)

        if user is not None:
            login(request, user)
            # 重定向到主页或其他页面
            return redirect('home')
        else:
            # 如果用户不存在或密码错误，显示错误信息
            messages.error(request, '電話或密碼錯誤')

    # 如果不是 POST 请求，则显示登录表单
    return render(request, 'member/login.html')
    

def user_logout(request):
    logout(request)
    messages.info(request, '已成功登出')
    return redirect('member:login')


def register(request):
    if request.method == 'POST':
        form = RegisterModelForm(request.POST, request.FILES)
        address_form = RegisterAddressForm(request.POST, request.FILES)
        if form.is_valid() and address_form.is_valid():
            user = form.save(commit=False)
            address = address_form.save(commit=False)
            # 密碼已在表單的 save 方法中設置，所以這裡不需要再設置
            # user.password = make_password(form.cleaned_data['password1'])
            if User.objects.filter(email=user.phone_number).exists():
                return render(request, "member/register.html", {"error_message": "電話已存在"})
            user.save()
            address.user_id = user.id
            address.save()
            # 根据需要处理其他逻辑，例如登录用户、发送邮件等
            return render(request, "member/register.html", {"success": '註冊成功'})
    else:
        form = RegisterModelForm()
        address_form = RegisterAddressForm()
    context={
        'form': form,
        'address_form': address_form,
        'title':'註冊'
    }
    return render(request, "member/register.html",context )
# @login_required
@require_POST
def update_address(request):
    action = request.POST.get('action')
    address_id = request.POST.get('address_id', None)  # 获取地址 ID
    if action == 'add':
        Address.objects.create(user=request.user, address=request.POST.get('address'))
    elif action == 'remove' and address_id:
        Address.objects.filter(id=address_id, user=request.user).delete()

    return JsonResponse({'status': 'success'})
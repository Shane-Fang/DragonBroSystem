from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import Branch_Inventory,Products
from OrderManagement.models import ShoppingCart,ShoppingCartDetails
from member.models import Branchs
from django.http import JsonResponse

def products_view(request,branch=None):
    branch=Branchs.objects.filter(pk=branch).first()
    products = Branch_Inventory.objects.filter(Branch_id=branch)
    context={
        'products':products,
        'branch':branch,
        'title':f"榮哥海鮮-{branch.Name}",
    }
    return render(request, 'products_view.html',context)

def get_branches(request):
    branches = Branchs.objects.all().values('id', 'Name')  # 使用 'Name' 而不是 'name'
    return JsonResponse(list(branches), safe=False) 

def detail(request,branch=None,detail=None):
    if request.user.is_authenticated:
        # current_user = request.user
        # loginuser = current_user.username
        product=Branch_Inventory.objects.get(Products=detail)
        context={
            'product':product,
            'branch':branch,
            'detail':detail,
        }
        return render(request,'detail.html',context)

@login_required 
def add_to_cart_view(request, product_id):
    if request.method == 'POST':
        quantity = request.POST.get('quantity', 1)
        user = request.user

        # 添加到购物车的逻辑
        add_to_cart(user, product_id, quantity)

        # 添加成功后重定向到某个页面，例如购物车页面或商品页面
        return redirect('some-view-name')

    # 如果不是 POST 请求，重定向到其他页面
    return redirect('another-view-name')
def add_to_cart(user, product_id, quantity):
    # 获取或创建购物车
    cart, cart_created = ShoppingCart.objects.get_or_create(User=user, defaults={'Total': 0})

    # 获取或创建购物车明细项
    product = Products.objects.get(id=product_id)  # 获取商品对象
    detail, created = ShoppingCartDetails.objects.get_or_create(ShoppingCart=cart, Product=product)
    if created:
        # 新商品，设置数量
        detail.Number = int(quantity)
    else:
        # 商品已存在，增加数量
        if detail.Number is None:
            detail.Number = 0
        detail.Number += int(quantity)

    # 更新商品明细的价格和总价
    detail.Price = product.Price  # 假设 Products 模型有一个 Price 字段
    detail.save()

    # 更新购物车总价
    update_cart_total(cart)

def update_cart_total(cart):
    total = 0
    for detail in cart.details.all():
        number = detail.Number or 0
        price = detail.Price or 0
        total += number * price
    cart.Total = total
    cart.save()
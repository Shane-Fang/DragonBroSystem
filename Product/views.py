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

        product=Branch_Inventory.objects.get(pk=detail)
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
        # 新增購物車function
        add_to_cart(user, product_id, quantity)

        return redirect('OrderManagement:cart')

    return redirect('OrderManagement:cart')
def add_to_cart(user, product_id, quantity):
    cart, cart_created = ShoppingCart.objects.get_or_create(User=user, defaults={'Total': 0})

    product = Branch_Inventory.objects.get(id=product_id) 
    detail, created = ShoppingCartDetails.objects.get_or_create(ShoppingCart=cart, Branch_Inventory=product)
    if created:
        detail.Number = int(quantity)
        detail.Price = product.Products.Price
    else:
        # 商品已存在，增加数量
        if detail.Number is None:
            detail.Number = 0
        detail.Number += int(quantity)

    # 更新商品明细的价格和总价
    detail.Price = product.Products.Price
    detail.Total = detail.Number * detail.Price
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
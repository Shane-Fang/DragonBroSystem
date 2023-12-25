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
    branches = Branchs.objects.all().values('id', 'Name')
    return JsonResponse(list(branches), safe=False) 

def detail(request,branch=None,detail=None):
    if request.user.is_authenticated:
        # current_user = request.user
        # loginuser = current_user.username
        branch=Branch_Inventory.objects.get(pk=detail)
        context={
            'branch':branch,
            'detail':detail,
            'title':'商品介紹'
        }
        return render(request,'detail.html',context)

@login_required 
def add_to_cart_view(request,branch ,product_id):
    if request.method == 'POST':
        quantity = request.POST.get('quantity', 1)
        user = request.user 
        # 新增購物車function

        add_to_cart(user, branch,product_id, quantity)

        return redirect('OrderManagement:cart')

    return redirect('OrderManagement:cart')
def add_to_cart(user, branch,product_id, quantity):
    Branchs_instance=Branchs.objects.get(id=branch)
    cart, cart_created = ShoppingCart.objects.get_or_create(User=user,branch=Branchs_instance ,defaults={'Total': 0})
    product = Products.objects.get(id=product_id) 
    detail, created = ShoppingCartDetails.objects.get_or_create(ShoppingCart=cart, Products=product)
    if created:
        detail.Number = int(quantity)
        detail.Price = product.Price
    else:
        if detail.Number is None:
            detail.Number = 0
        detail.Number += int(quantity)

    # 更新商品明细的价格和总价
    detail.Price = product.Price
    detail.Total = detail.Number * detail.Price
    detail.save()
 
    update_cart_total(cart)

def update_cart_total(cart):
    total = 0
    for detail in cart.details.all():
        number = detail.Number or 0
        price = detail.Price or 0
        total += number * price
    cart.Total = total
    cart.save()
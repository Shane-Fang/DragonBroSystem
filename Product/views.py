import logging
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import Branch_Inventory,Products,ItemImage, Categories,RestockDetail
from OrderManagement.models import ShoppingCart,ShoppingCartDetails
from member.models import Branchs
from django.http import JsonResponse
from django.core.paginator import Paginator

def products_view(request,branch=None,detail=None):
    
    branch=Branchs.objects.get(pk=branch)
    products = Branch_Inventory.objects.filter(Branch_id=branch)
    products_detail = {}
    categories = Categories.objects.all()
    for inventory_item in products:
        product = inventory_item.Products
        product_info = {}
        product_info['Product'] = product
        product_info['Number'] = inventory_item.Number
        product_info['Price'] = product.Price
        product_info['Specification'] = product.Specification
        product_info['id'] = inventory_item.id
        product_info['Category_id'] = product.Category_id
        product_images = ItemImage.objects.filter(Products=product)
        image_paths = []
        for image in product_images:
            image_paths.append(image.Image_path.url)
        product_info['Picture'] = image_paths
        products_detail[product.Item_name] = product_info
        products_detail_list = list(products_detail.values())
        paginator = Paginator(products_detail_list, 24) #每页显示 2 条数据
        # paginator = Paginator(products_detail_list, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    context={
        'branch':branch,
        'title':f"榮哥海鮮-{branch.Name}",
        'products_detail':products_detail,
        'categories': categories,
        'page_number': page_number,
        'page_obj': page_obj,
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
        product_images = ItemImage.objects.filter(Products=branch.Products)
        image_paths = []
        for image in product_images:
            image_paths.append(image.Image_path.url)
        context={
            'branch':branch,
            'detail':detail,
            'title':'商品介紹',
            'image_paths':image_paths
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
def get_products_by_branch(request, branch_id):
    data = list(RestockDetail.objects.filter(Branch_id=branch_id, Remain__gt=0)
                .values('id', 'Product__Item_name', 'ExpiryDate', 'Remain','Product'))
    return JsonResponse(data, safe=False)
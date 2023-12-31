from django.shortcuts import render,redirect
from .models import ShoppingCart,ShoppingCartDetails,Orders,OrderDetails
from django.contrib.auth.models import User
from member.models import Address
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db import transaction
from django.views.decorators.csrf import csrf_exempt
from collections import defaultdict
from django.contrib import messages
# Create your views here.
def cart(request):
    carts_by_branch = defaultdict(list)
    current_user = request.user  
    member_cart = ShoppingCart.objects.filter(User=current_user)
    if member_cart:
        for cart_item in member_cart:
            total=cart_item.Total
            cart_details = cart_item.details.all()
            branch = cart_item.branch
            carts_by_branch[branch].append({'details': cart_details, 'total': total})
            print(cart_details)
    else:
        cart_details=None
        total=0
    context={
        'title':'榮哥海鮮',
        'cartlist':dict(carts_by_branch),
    }
    return render(request, 'cart.html',context)

def cartorder(request):

    if request.user.is_authenticated:
        current_user = request.user
        member_carts = ShoppingCart.objects.filter(User=current_user)
    
        if member_carts.count() > 1:
            messages.error(request, '一次只能選一個店家，請把多的店家商品刪除')
            return redirect('OrderManagement:cart')
        if member_carts.count() == 1:
            # print(member_cart)
            member_cart = member_carts.first()
            cart_details = member_cart.details.all()
            total=member_cart.Total
        else:
            cart_details=None
            total=0
        addresses=Address.objects.filter(user=current_user)
        context={
            'title':'訂單確認',
            'user':current_user,
            'addresses':addresses,
            'cartlist':cart_details,
            'total':total
        }
        return render(request, 'cartorder.html',context )
def cartok(request):
    if request.user.is_authenticated:
        current_user = request.user
        latest_order = Orders.objects.latest('id')
        order_detail = OrderDetails.objects.filter(Order=latest_order)
        Payment_method_display = latest_order.get_Payment_method_display()
        Delivery_method_display = latest_order.get_Delivery_method_display()
        context={
            'title':'訂單完成',
            'user':current_user,
            'Payment_method':Payment_method_display,
            'Delivery_method':Delivery_method_display,
            'order_detail':order_detail,
            'order':latest_order
        }
        return render(request, 'cartok.html',context )
@csrf_exempt
def submit_order(request):
    if request.method == 'POST':

        current_user = request.user
        address = request.POST.get('address')
        delivery_method = request.POST.get('Delivery')
        payment_method = request.POST.get('Payment_method')
        shopping_cart = ShoppingCart.objects.get(User=current_user)
        try:
            with transaction.atomic():
                order = Orders(
                    User=current_user,
                    Delivery_method=request.POST['Delivery'],
                    Delivery_state=0,
                    Payment_method=request.POST['Payment_method'],
                    Address=request.POST['address'],
                    Total=shopping_cart.Total,
                    branch=shopping_cart.branch
                )
                order.save()
                # 你的数据库操作代码
                for item in ShoppingCartDetails.objects.filter(ShoppingCart=shopping_cart):
                    OrderDetails(
                        Products=item.Products,
                        Number=item.Number,
                        Price=item.Price,
                        Total=item.Total,
                        Order=order  
                    ).save()
                ShoppingCartDetails.objects.filter(ShoppingCart=shopping_cart).delete()
                shopping_cart.delete()
                latest_order = Orders.objects.latest('id')
                order_detail = OrderDetails.objects.filter(Order=latest_order)
                Payment_method_display = latest_order.get_Payment_method_display()
                Delivery_method_display = latest_order.get_Delivery_method_display()
                return JsonResponse({'status': 'success', 'message': 'Order submitted successfully.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})
@require_POST
def delete_from_cart(request):
    detail_id = request.POST.get('detail_id')

    try:
        detail = ShoppingCartDetails.objects.get(id=detail_id)
        detail.delete()
        return JsonResponse({'status': 'success'})
    except ShoppingCartDetails.DoesNotExist:
        return JsonResponse({'status': 'failed', 'error': 'Item not found'})
    
@require_POST
def update_cart_item(request):
    detail_id = request.POST.get('detail_id')
    new_quantity = request.POST.get('quantity', 0)

    try:
        detail = ShoppingCartDetails.objects.get(id=detail_id)
        detail.Number = new_quantity
        detail.Total = int(detail.Price) * int(detail.Number)
        detail.save()
        cart=ShoppingCart.objects.get(id=detail.ShoppingCart.pk)
        carttotal=cart.Total
        cartbranch=cart.branch.pk
        return JsonResponse({'status': 'success', 'new_total': detail.Total,'carttotal':carttotal,'branch_id':cartbranch})
    except ShoppingCartDetails.DoesNotExist:
        return JsonResponse({'status': 'failed', 'error': 'Item not found'})
    except ValueError:
        return JsonResponse({'status': 'failed', 'error': 'Invalid quantity'})

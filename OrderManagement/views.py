from django.shortcuts import render
from .models import ShoppingCart,ShoppingCartDetails,Orders,OrderDetails
from django.contrib.auth.models import User
from member.models import Address
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db import transaction
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
def cart(request):
    current_user = request.user  
    member_cart = ShoppingCart.objects.filter(User=current_user).first() or None
    if member_cart:
        cart_details = member_cart.details.all()
        total=member_cart.Total
    else:
        cart_details=None
        total=0
    context={
        'title':'榮哥海鮮',
        'cartlist':cart_details,
        'total':total
    }
    return render(request, 'cart.html',context)

def cartorder(request):

    if request.user.is_authenticated:
        current_user = request.user
        member_Orders = Orders.objects.filter(User=current_user).first() or None
        print(member_Orders)
        print(member_Orders.get_Payment_method_display())
        member_cart = ShoppingCart.objects.filter(User=current_user).first() or None
        if member_cart:
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
        print(latest_order.Address)
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
                    Total=shopping_cart.Total
                )
                order.save()
                for item in ShoppingCartDetails.objects.filter(ShoppingCart=shopping_cart):
                    OrderDetails(
                        Product=item.Product,
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
        carttotal=ShoppingCart.objects.get(id=detail.ShoppingCart.pk).Total
        return JsonResponse({'status': 'success', 'new_total': detail.Total,'carttotal':carttotal})
    except ShoppingCartDetails.DoesNotExist:
        return JsonResponse({'status': 'failed', 'error': 'Item not found'})
    except ValueError:
        return JsonResponse({'status': 'failed', 'error': 'Invalid quantity'})

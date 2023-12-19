from django.shortcuts import render
from .models import ShoppingCart,ShoppingCartDetails,Orders,OrderDetails
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.http import require_POST
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

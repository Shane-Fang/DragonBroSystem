from django.shortcuts import render
from .models import Branch_Inventory
from member.models import Branchs
from django.http import JsonResponse

def products_view(request):
    # 处理商品浏览页面的逻辑
    # 可能包括从数据库获取商品信息等等
    branch_name = request.GET.get('branch')
    branch=Branchs.objects.filter(pk=branch_name).first()

    products = Branch_Inventory.objects.filter(Branch_id=branch_name)

    
    context={
        'products':products,
        'title':f"榮哥海鮮-{branch.Name}",
    }
    return render(request, 'products_view.html',context)

def get_branches(request):
    branches = Branchs.objects.all().values('id', 'Name')  # 使用 'Name' 而不是 'name'
    return JsonResponse(list(branches), safe=False) 
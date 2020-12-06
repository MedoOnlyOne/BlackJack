from django.shortcuts import render
from products.models import Product
from django.db.models import Q 


# Create your views here.
def search(request):
    if request.GET.get('product_name',None) is None:
        print('HHEEEEEEEEEEEEEEEEEEEEREEEEEEEEEEEEEEEEEE')
        return render(request,'search/index.html')
    else:
        print("#####################################")
        query = request.GET['product_name']
        print(f"###########     {query}   ###############")
        results = Product.objects.filter(Q(name__icontains=query))
        print(f'###############     {results}   ##############')
        return render(request, 'search/searchResults.html',{
            'products': results
        })
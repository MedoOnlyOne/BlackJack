from django.shortcuts import render
from products.models import Product
from shop.models import Shop
from django.core.paginator import Paginator
import os,requests

currency_symbols={
    'EGP':'EGP',
    'EUR':'€',
    'USD':'$',
    'GBP':'£'
}

def get_currency_ratio(request):
    preferred_currency=get_preffered_currency(request)
    if preferred_currency=='EGP':
        return 1
    else:
        return requests.get('https://free.currconv.com/api/v7/convert',{'apiKey':os.environ.get('API_KEY'),'q':'EGP'+'_'+preferred_currency,'compact':'ultra'}).json()['EGP'+'_'+preferred_currency]

def get_preffered_currency(request):
    if not request.user.is_authenticated:
        return 'EGP'
    if request.user.preferred_currency=='':
        return 'EGP'
    return request.user.preferred_currency


# Create your views here.
def search(request):
    query = request.GET['search_name']
    search_by = request.GET['search_for']
    sort_by = request.GET.get('sort_by',None)
    preferred_currency=get_preffered_currency(request)
    currency_ratio=get_currency_ratio(request)
    url=request.build_absolute_uri()
    if '&page=' in url:
        last=-1
        for index in range(len(url)-1,-1,-1):
            if url[index]=='=':
                last=index
                break
        url=url[:last-5]
    if search_by=='products':
        results = Product.objects.filter(name__icontains=query)
        if sort_by=='name':
            results=sorted(results,key=lambda item:item.name)
        else:
            results=sorted(results,key=lambda item:item.price)
        paginator=Paginator(results,5)
        page_num=request.GET.get('page',1)
        page_obj=paginator.get_page(page_num)
        return render(request, 'search/searchResults.html',{
            'results': page_obj,
            'currency_ratio':currency_ratio,
            'currency_symbol':currency_symbols[preferred_currency],
            'is_products_search':True,
            'current_path':url
        })
    else:
        results=Shop.objects.filter(name__icontains=query)
        results=sorted(results,key=lambda item:item.name)
        paginator=Paginator(results,5)
        page_num=request.GET.get(['page'],1)
        page_obj=paginator.get_page(page_num)    
        return render(request, 'search/searchResults.html',{
            'results': page_obj,
            'currency_ratio':currency_ratio,
            'currency_symbol':currency_symbols[preferred_currency],
            'is_products_search':False
        })
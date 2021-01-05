from django.shortcuts import render
from products.models import Product
from shop.models import Shop
from django.db.models import Q 


currency_symbols={
    'EGP':'L.E.',
    'EUR':'€',
    'USD':'$',
    'GBP':'£'
}

def get_currency_ratio(request):
    if not request.user.is_authenticated:
        return 1
    preferred_currency=request.user.preferred_currency
    if preferred_currency=='EGP':
        return 1
    else:
        return requests.get('https://free.currconv.com/api/v7/convert',{'apiKey':config('API_KEY'),'q':'EGP'+'_'+preferred_currency,'compact':'ultra'}).json()['EGP'+'_'+preferred_currency]

def get_preffered_currency(request):
    if not request.user.is_authenticated:
        return 'EGP'
    return request.user.preferred_currency


# Create your views here.
def search(request):
    query = request.GET['search_name']
    search_by = request.GET['search_for']
    sort_by = request.GET.get('sort_by',None)
    preferred_currency=get_preffered_currency(request)
    currency_ratio=get_currency_ratio(request)
    if search_by=='products':
        results = Product.objects.filter(name__icontains=query)
        if sort_by=='name':
            results=sorted(results,key=lambda item:item.name)
        else:
            results=sorted(results,key=lambda item:item.price)
        return render(request, 'search/searchResults.html',{
            'results': results,
            'currency_ratio':currency_ratio,
            'currency_symbol':currency_symbols[preferred_currency],
            'is_products_search':True
        })
    else:
        results=Shop.objects.filter(name__icontains=query)
        results=sorted(results,key=lambda item:item.name)
        return render(request, 'search/searchResults.html',{
            'results': results,
            'currency_ratio':currency_ratio,
            'currency_symbol':currency_symbols[preferred_currency],
            'is_products_search':False
        })
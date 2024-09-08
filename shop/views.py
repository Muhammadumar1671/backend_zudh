from django.shortcuts import render, get_object_or_404
from .models import Product, Category

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    return render(request, 'shop/product_list.html', {
        'category': category,
        'categories': categories,
        'products': products,
    })



def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, available=True)

    return render(request, 'shop/product_detail.html', {
        'product': product,
    })
    
    
def product_search(request):
    query = request.GET.get('q')
    products = Product.objects.filter(name__icontains=query)

    return render(request, 'shop/product_search.html', {
        'products': products,
        'query': query,
    })
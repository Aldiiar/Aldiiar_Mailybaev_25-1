from django.shortcuts import render
from products.models import Product, Hashtag

# Create your views here.

def main_page_view(request):
    if request.method == 'GET':
        return render(request, 'layouts/index.html')

def products_view(request):
    if request.method == 'GET':
        tovary = Product.objects.all()

        context = {
            'products': [
                {
                    'id': tovar,
                    'title': tovar.title,
                    'image': tovar.image,
                    'rating': tovar.rating,
                    'price': tovar.price,
                    'hashtags': tovar.hashtags.all()
                } for tovar in tovary
            ]
        }

        return render(request, 'products/products.html', context=context)

def hashtag_view(request):
    if request.method == 'GET':
        hashtags = Hashtag.objects.all()

        context = {
            'hashtags': hashtags
        }

        return render(request, 'products/hashtags.html', context=context)



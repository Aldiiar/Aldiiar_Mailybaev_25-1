from django.shortcuts import render, redirect
from products.models import Product, Hashtag, Comment
from products.forms import ProductCreateForm, CommentsCreateForm
from products.constans import PAGINATION_LIMIT

# Create your views here.

def main_page_view(request):
    if request.method == 'GET':
        return render(request, 'layouts/index.html')

def products_view(request):
    if request.method == 'GET':
        tovary = Product.objects.all()
        search = request.GET.get('search')
        page = int(request.GET.get('page', 1))

        max_page = tovary.__len__() / PAGINATION_LIMIT
        if round(max_page) < max_page:
            max_page = round(max_page) + 1
        else:
            max_page = round(max_page)

        if search:
            tovary = tovary.filter(title__contains=search) | tovary.filter(description__contains=search)

        tovary = tovary[PAGINATION_LIMIT * (page-1):PAGINATION_LIMIT*page]


        context = {
            'products': [
                {
                    'id': tovar.id,
                    'title': tovar.title,
                    'image': tovar.image,
                    'rating': tovar.rating,
                    'price': tovar.price,
                    'hashtags': tovar.hashtags.all()
                } for tovar in tovary
            ],
            'user': request.user,
            'pages': range(1, max_page+1)
        }

        return render(request, 'products/products.html', context=context)

def hashtag_view(request):
    if request.method == 'GET':
        hashtags = Hashtag.objects.all()

        context = {
            'hashtags': hashtags
        }

        return render(request, 'products/hashtags.html', context=context)

def product_detail_view(request, id):
    if request.method == 'GET':
        product = Product.objects.get(id=id)

        context = {
            'product': product,
            'comments': product.comment_set.all(),
            'form': CommentsCreateForm
        }

        return render(request, 'products/detail.html', context=context)

    if request.method == 'POST':
        product = Product.objects.get(id=id)
        data = request.POST
        form = CommentsCreateForm(data=data)

        if form.is_valid():
            Comment.objects.create(
                text=form.cleaned_data.get('text'),
                product=product
            )

        context = {
            'product': product,
            'comments': product.comment_set.all(),
            'form': form
        }

        return render(request, 'products/detail.html', context=context)


def create_product_view(request):
    if request.method == 'GET':

        context = {
            'form': ProductCreateForm
        }

        return render(request, 'products/create.html', context=context)

    if request.method == 'POST':
        data, files = request.POST, request.FILES

        form = ProductCreateForm(data, files)

        if form.is_valid():
            Product.objects.create(
                image=form.cleaned_data.get('image'),
                title=form.cleaned_data.get('title'),
                description=form.cleaned_data.get('description'),
                rating=form.cleaned_data.get('rating'),
                price=form.cleaned_data.get('price')
            )
            return redirect('/products')

        return render(request, 'products/create.html', context={
            'form': form
        })

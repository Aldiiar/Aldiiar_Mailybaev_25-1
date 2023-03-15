from django.shortcuts import render, redirect
from products.models import Product, Hashtag, Comment
from products.forms import ProductCreateForm, CommentsCreateForm
from products.constans import PAGINATION_LIMIT
from django.views.generic import ListView, DetailView, CreateView

# Create your views here.

class MainPageCBV(ListView):

    model = Product
    template_name = 'layouts/index.html'


class ProductsCBV(ListView, CreateView):
    model = Product
    template_name = 'products/products.html'
    context_object_name = 'products'

    def get(self, request, **kwargs):
        tovary = self.get_queryset()
        search = request.GET.get('search')
        page = int(request.GET.get('page', 1))

        max_page = tovary.__len__() / PAGINATION_LIMIT
        if round(max_page) < max_page:
            max_page = round(max_page) + 1
        else:
            max_page = round(max_page)

        if search:
            tovary = tovary.filter(title__contains=search) | tovary.filter(description__contains=search)

        tovary = tovary[PAGINATION_LIMIT * (page - 1):PAGINATION_LIMIT * page]

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
            'pages': range(1, max_page + 1)
        }

        return render(request, self.template_name, context=context)



class HashtagCBV(ListView):
    model = Hashtag
    template_name = 'products/hashtags.html'

    def get(self, request, **kwargs):
        hashtags = self.get_queryset()

        context = {
            'hashtags': hashtags
        }

        return render(request, self.template_name, context=context)



class ProductDetailCBV(DetailView, CreateView):
    model = Product
    template_name = 'products/detail.html'
    context_object_name = 'product'
    form_class = CommentsCreateForm

    def get_context_data(self,  *, object_list=None, **kwargs):
        product = Product.objects.get(pk=self.kwargs.get('pk'))
        return {
            'form': self.form_class if not kwargs.get('form') else kwargs['form'],
            'product': product,
            'comments': product.comment_set.all()
        }

    def get(self, request, **kwargs):
        return render(request, self.template_name, context=self.get_context_data())

    def post(self, request, **kwargs):
        product = Product.objects.get(pk=self.kwargs.get('pk'))
        data = request.POST
        form = CommentsCreateForm(data=data)

        if form.is_valid():
            Comment.objects.create(
                text=form.cleaned_data.get('text'),
                product=product
            )

        return render(request, self.template_name, context=self.get_context_data(form=form))



class CreateProductsCBV(ListView, CreateView):
    model = Product
    template_name = 'products/create.html'
    form_class = ProductCreateForm

    def get_context_data(self, *, object_list=None, **kwargs):
        return {
            'form': self.form_class if not kwargs.get('form') else kwargs['form']
        }

    def get(self, request, **kwargs):
        return render(request, self.template_name, context=self.get_context_data())

    def post(self, request, **kwargs):
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

        return render(request, self.template_name, context=self.get_context_data(
            form=form
        ))
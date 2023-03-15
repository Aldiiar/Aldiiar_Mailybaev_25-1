from django.contrib import admin
from django.urls import path
from products.views import MainPageCBV, ProductsCBV, HashtagCBV, \
    ProductDetailCBV, CreateProductsCBV
from django.conf.urls.static import static
from django_hw.settings import MEDIA_URL, MEDIA_ROOT
from users.views import RegisterView, LoginView, LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', MainPageCBV.as_view()),
    path('products/', ProductsCBV.as_view()),
    path('products/<int:pk>/', ProductDetailCBV.as_view()),
    path('hashtags/', HashtagCBV.as_view()),
    path('products/create/', CreateProductsCBV.as_view()),
    path('users/register/', RegisterView.as_view()),
    path('users/login/', LoginView.as_view()),
    path('users/logout/', LogoutView.as_view())
]

urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)
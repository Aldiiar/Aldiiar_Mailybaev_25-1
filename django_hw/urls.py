from django.contrib import admin
from django.urls import path
from posts.views import hello_view, nowdate_view, goodby_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello/', hello_view),
    path('now_date/', nowdate_view),
    path('goodby/', goodby_view)
]

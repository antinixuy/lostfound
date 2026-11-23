from django.contrib import admin
from django.urls import path, include
from listings import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.listing_list, name='listing_list'),
    path('add/', views.add_listing, name='add_listing'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register/', views.register, name='register'),
]
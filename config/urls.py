from django.contrib import admin
from django.urls import path, include
from listings import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.listing_list, name='listing_list'),
    path('add/', views.add_listing, name='add_listing'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register/', views.register, name='register'),
    
    # API для объявлений
    path('api/listings/', views.ListingListCreateAPIView.as_view(), name='api_listings'),
    path('api/listings/<int:pk>/', views.ListingDetailAPIView.as_view(), name='api_listing_detail'),
    
    # API для аутентификации (ВОТ ЭТИ ДВЕ СТРОКИ НУЖНО ДОБАВИТЬ)
    path('api/auth/register/', views.api_register, name='api_register'),
    path('api/auth/login/', views.api_login, name='api_login'),
]
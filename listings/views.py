from django.shortcuts import render
from .models import Listing

def listing_list(request):
    # Берем все объявления из базы (сортируем по дате создания)
    listings = Listing.objects.all() 
    return render(request, 'listings/list.html', {'listings': listings})
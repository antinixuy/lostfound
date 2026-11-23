from django.shortcuts import render, redirect
from .models import Listing
from .forms import ListingForm

def listing_list(request):
    listings = Listing.objects.all()
    return render(request, 'listings/list.html', {'listings': listings})

def add_listing(request):
    if request.method == 'POST':
        form = ListingForm(request.POST)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.user = request.user  # Автоматически назначаем автором текущего пользователя
            listing.save()
            return redirect('listing_list')  # Возвращаемся на главную
    else:
        form = ListingForm()
    
    return render(request, 'listings/add_listing.html', {'form': form})
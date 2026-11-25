from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from .models import Listing
from .forms import ListingForm

# --- Обычные страницы (HTML) ---

def listing_list(request):
    listings = Listing.objects.all()
    return render(request, 'listings/list.html', {'listings': listings})

@login_required
def add_listing(request):
    if request.method == 'POST':
        form = ListingForm(request.POST)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.user = request.user
            listing.save()
            return redirect('listing_list')
    else:
        form = ListingForm()
    return render(request, 'listings/add_listing.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('listing_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

# --- REST API (Объявления) ---

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ListingSerializer

class ListingListCreateAPIView(APIView):
    def get(self, request):
        listings = Listing.objects.all()
        serializer = ListingSerializer(listings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ListingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

class ListingDetailAPIView(APIView):
    def get_object(self, pk):
        return get_object_or_404(Listing, pk=pk)

    def get(self, request, pk):
        listing = self.get_object(pk)
        serializer = ListingSerializer(listing)
        return Response(serializer.data, status=status.HTTP_200_OK)

# --- REST API (Аутентификация) ---

from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

@api_view(['POST'])
@permission_classes([AllowAny])
def api_register(request):
    username = request.data.get('username')
    password = request.data.get('password')
    if not username or not password:
        return Response({'error': 'Username and password required'}, status=status.HTTP_400_BAD_REQUEST)
    
    if User.objects.filter(username=username).exists():
        return Response({'error': 'User already exists'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    
    user = User.objects.create_user(username=username, password=password)
    return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([AllowAny])
def api_login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user:
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_200_OK)
    return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
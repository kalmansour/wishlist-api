from django.shortcuts import render, redirect
from items.models import Item, FavoriteItem
from .serializers import UserRegisterSerialzer, ItemListSerializer, ItemDetailSerializer
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.filters import SearchFilter, OrderingFilter
from .permissions import IsItemOwnerOrStaff

class ItemListView(ListAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemListSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name', 'description']
    permission_classes = [AllowAny]
    
class ItemDetailView(RetrieveAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemDetailSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'item_id'
    permission_classes = [IsItemOwnerOrStaff]

class UserRegister(CreateAPIView):
    serializer_class = UserRegisterSerialzer

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
def item_favorite(request, item_id):
    item_object = Item.objects.get(id=item_id)
    if request.user.is_anonymous:
        return redirect('user-login')
    
    favorite, created = FavoriteItem.objects.get_or_create(user=request.user, item=item_object)
    if created:
        action = "favorite"
    else:
        favorite.delete()
        action="unfavorite"
    
    response = {
        "action": action,
    }
    return JsonResponse(response, safe=False)

@csrf_exempt
def wishlist(request):
    wishlist = []
    items = Item.objects.all()
    query = request.GET.get('q')
    if query:
        items = Item.objects.filter(name__contains=query)
    if request.user.is_authenticated:
        favorite_objects = request.user.favoriteitem_set.all()
    for item in items:
        for favorite in favorite_objects:
            if item.id == favorite.item_id:
                wishlist.append(item)
    context = {
        "wishlist": wishlist
    }
    return render(request, 'wishlist.html', context)

from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Item, FavoriteItem

class UserRegisterSerialzer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['username','first_name', 'last_name', 'password']
    
    def create(self, validated_data):
        username = validated_data['username']
        first_name = validated_data['first_name']
        last_name = validated_data['last_name']
        password = validated_data['password']
        new_user = User(username=username, first_name=first_name, last_name=last_name)
        new_user.set_password(password)
        new_user.save()
        return validated_data

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']

class ItemListSerializer(serializers.ModelSerializer):
    added_by = UserSerializer()
    detail = serializers.HyperlinkedIdentityField(
        view_name = "item-detail",
        lookup_field = "id",
        lookup_url_kwarg = "item_id"
        )
    class Meta:
        model = Item
        fields = ['image', 'name', 'description', 'detail','added_by']

# class FavoriteItemSerializer(serializers.ModelSerializer): #####
#     user  = UserSerializer()
#     item = ItemListSerializer()
#     class Meta:
#         model = FavoriteItem
#         fields = ['user', 'item']


class ItemDetailSerializer(serializers.ModelSerializer):
    favorited_by = 'lol'
    class Meta:
        model = Item
        fields = ['image', 'name', 'description', 'favorited_by']

        


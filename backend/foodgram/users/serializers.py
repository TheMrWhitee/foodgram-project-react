from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers

from recipes.models import Recipe

from .models import Follow

User = get_user_model()


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'password')


class CustomUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed', )

    def get_is_subscribed(self, obj):
        if self.context['request'].user.is_anonymous:
            return False
        return Follow.objects.filter(
            user=self.context['request'].user, following=obj
        ).exists()


class FollowRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class FollowSerializer(CustomUserSerializer):
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'recipes', 'recipes_count')

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj).count()

    def get_recipes(self, obj):
        recipes_limit = self.context.get('recipes_limit')
        if recipes_limit is None:
            recipes = Recipe.objects.filter(author=obj)
        else:
            recipes = Recipe.objects.filter(author=obj)[:int(recipes_limit)]
        serializer = FollowRecipeSerializer(recipes, many=True)
        return serializer.data

    # def validate(self, data):
    #     user = self.context['request'].user
    #     following = data['following']
    #
    #     if Follow.objects.filter(
    #             user=user, following=following
    #     ).exists() or following == user:
    #         raise ValidationError('Подписка уже существует или попытка '
    #                               'подписаться на себя.')
    #     return data

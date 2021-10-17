from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import transaction
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from users.serializers import CustomUserSerializer

from .models import Component, Favorites, Ingredient, Recipe, ShoppingCart, Tag


def add_ingredients(instance, values):
    for ingredient in values:
        ingredient_id = ingredient['ingredient']['id']
        amount = ingredient['amount']
        component = Component.objects.bulk_create(Component(
            ingredient=ingredient_id,
            amount=amount)
        )
        instance.ingredients.add(component[0])
    return instance


class ComponentSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = Component
        fields = ('id', 'name', 'measurement_unit', 'amount', )


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit', )


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug', )

    def to_internal_value(self, data):
        try:
            tag = Tag.objects.get(id=data)
        except ObjectDoesNotExist:
            raise ValidationError('Wrong tag id')
        return tag


class RecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    ingredients = ComponentSerializer(many=True)
    author = CustomUserSerializer(read_only=True)
    image = Base64ImageField(max_length=None, use_url=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients', 'is_favorited',
                  'is_in_shopping_cart', 'name', 'image', 'text',
                  'cooking_time')

    def get_is_favorited(self, obj):
        if self.context['request'].user.is_anonymous:
            return False
        return Favorites.objects.filter(
            owner=self.context['request'].user, recipes=obj
        ).exists()

    def get_is_in_shopping_cart(self, obj):
        if self.context['request'].user.is_anonymous:
            return False
        return ShoppingCart.objects.filter(
                owner=self.context['request'].user, recipes=obj
        ).exists()

    @transaction.atomic
    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data,
                                       author=self.context['request'].user)
        for tag in tags:
            recipe.tags.add(tag)

        return add_ingredients(recipe, ingredients)

    @transaction.atomic
    def update(self, recipe, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')

        Recipe.objects.filter(pk=recipe.pk).update(**validated_data)
        recipe = Recipe.objects.get(pk=recipe.pk)

        recipe.tags.set(tags)
        recipe.ingredients.set('')

        return add_ingredients(recipe, ingredients)


class FavoritesSerializer(RecipeSerializer):
    class Meta(RecipeSerializer.Meta):
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time', )

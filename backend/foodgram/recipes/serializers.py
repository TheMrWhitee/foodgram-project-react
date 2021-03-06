from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import transaction
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from users.serializers import CustomUserSerializer

from .models import Component, Favorites, Ingredient, Recipe, ShoppingCart, Tag


def add_ingredients(instance, values):
    components = []
    for ingredient in values:
        ingredient_id = ingredient['ingredient']['id']
        amount = ingredient['amount']
        components.append(
            Component.objects.get_or_create(
                ingredient=Ingredient(pk=ingredient_id),
                amount=amount)[0]
        )
    instance.ingredients.add(*components)
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
            Tag.objects.get(id=data)
        except ObjectDoesNotExist:
            raise ValidationError('Wrong tag id')
        return Tag.objects.get(id=data)


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
        recipe.name = validated_data.pop('name')
        recipe.text = validated_data.pop('text')
        if validated_data.get('image') is not None:
            recipe.image = validated_data.pop('image')
        recipe.cooking_time = validated_data.pop('cooking_time')
        recipe.save()
        recipe.tags.set(tags)
        recipe.ingredients.set('')
        return add_ingredients(recipe, ingredients)


class FavoritesSerializer(RecipeSerializer):
    class Meta(RecipeSerializer.Meta):
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time', )

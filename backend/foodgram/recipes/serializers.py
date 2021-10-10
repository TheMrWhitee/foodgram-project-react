from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from users.serializers import CustomUserSerializer

from .models import Component, Ingredient, Recipe, Tag


class ComponentSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
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
        fields = ('id', 'name', 'measurement_unit', 'amount', )


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug', )


class RecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    ingredients = ComponentSerializer(many=True, read_only=True)
    author = CustomUserSerializer(read_only=True)
    image = Base64ImageField(max_length=None, use_url=True)

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients', 'is_favorited',
                  'is_in_shopping_cart', 'name', 'image', 'text',
                  'cooking_time')

    def create(self, validated_data):
        tags = self.initial_data.pop('tags')
        ingredients = self.initial_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data,
                                       author=self.context['request'].user)
        for tag in tags:
            recipe.tags.add(tag)

        for ingredient in ingredients:
            ingredient_id = ingredient['id']
            amount = ingredient['amount']
            component = Component.objects.create(
                ingredient=Ingredient.objects.get(pk=ingredient_id),
                amount=amount
            )
            recipe.ingredients.add(component)

        return recipe

    def update(self, recipe, validated_data):
        tags = self.initial_data.pop('tags')
        ingredients = self.initial_data.pop('ingredients')

        Recipe.objects.filter(pk=recipe.pk).update(**validated_data)
        recipe = Recipe.objects.get(pk=recipe.pk)

        recipe.tags.set(tags)
        recipe.ingredients.set('')

        for ingredient in ingredients:
            ingredient_id = ingredient['id']
            amount = ingredient['amount']
            component = Component.objects.create(
                ingredient=Ingredient.objects.get(pk=ingredient_id),
                amount=amount
            )
            recipe.ingredients.add(component)

        return recipe

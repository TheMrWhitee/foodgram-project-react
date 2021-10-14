from django.apps import apps
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.response import Response

from .models import Favorites, Ingredient, Recipe, Tag
from .serializers import (FavoritesSerializer, IngredientSerializer,
                          RecipeSerializer, TagSerializer)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None


class FavoritesViewSet(viewsets.ModelViewSet):
    def create(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            data = {'detail': 'Учетные данные не были предоставлены.'}
            return Response(data, status=status.HTTP_401_UNAUTHORIZED)

        model = apps.get_model('recipes', kwargs['model'])

        recipe = get_object_or_404(Recipe, pk=kwargs['id'])
        favorite = model.objects.get_or_create(owner=request.user)

        if model.objects.filter(
                owner=request.user, recipes=recipe
        ).exists():
            data = {'errors': 'Уже есть в избранном.'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        favorite[0].recipes.add(recipe)
        serializer = FavoritesSerializer(recipe,
                                         context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            data = {'detail': 'Учетные данные не были предоставлены.'}
            return Response(data, status=status.HTTP_401_UNAUTHORIZED)

        model = apps.get_model('recipes', kwargs['model'])

        recipe = get_object_or_404(Recipe, pk=kwargs['id'])

        if not model.objects.filter(
                owner=request.user, recipes=recipe
        ).exists():
            data = {'errors': 'Отсутствует в избранном.'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        favorites = model.objects.get(owner=request.user)
        favorites.recipes.remove(recipe)
        return Response(status=status.HTTP_204_NO_CONTENT)

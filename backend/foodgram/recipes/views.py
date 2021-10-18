from django.apps import apps
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from prettytable import PrettyTable
from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .filters import IngredientFilter, RecipeFilter
from .models import Ingredient, Recipe, Tag
from .permissions import AdminOrAuthorOrReadOnly
from .serializers import (FavoritesSerializer, IngredientSerializer,
                          RecipeSerializer, TagSerializer)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all().order_by('-pk')
    serializer_class = RecipeSerializer
    permission_classes = [AdminOrAuthorOrReadOnly]
    # filter_backends = [DjangoFilterBackend]
    filterset_class = RecipeFilter


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    # filter_backends = [DjangoFilterBackend]
    filterset_class = IngredientFilter
    pagination_class = None


class FavoritesViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    # filter_backends = [DjangoFilterBackend]
    filterset_class = RecipeFilter

    # def list(self, request, *args, **kwargs):
    #     model = apps.get_model('recipes', kwargs['model'])
    #     queryset = self.filter_queryset(model.objects.all())
    #     serializer = FavoritesSerializer(queryset, many=True)
    #     return Response(serializer.data)
    #
    # def filter_queryset(self, queryset):
    #     filter_backends = [DjangoFilterBackend]
    #     for backend in list(filter_backends):
    #         queryset = backend().filter_queryset(self.request, queryset,
    #                                              view=self)
    #     return queryset

    def create(self, request, *args, **kwargs):
        model = apps.get_model('recipes', kwargs['model'])

        recipe = get_object_or_404(Recipe, pk=kwargs['id'])
        favorite = model.objects.get_or_create(owner=request.user)[0]

        if model.objects.filter(
                owner=request.user, recipes=recipe
        ).exists():
            data = {'errors': 'Уже есть в избранном.'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        favorite.recipes.add(recipe)
        serializer = FavoritesSerializer(recipe,
                                         context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
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


@api_view(['GET'])
def download_shopping_cart(request):
    if request.user.is_anonymous:
        data = {'detail': 'Пользователь не авторизован.'}
        return Response(data, status=status.HTTP_401_UNAUTHORIZED)

    shopping_cart = Recipe.objects.filter(
        shopping_cart__owner=request.user
    ).order_by(
        'ingredients__ingredient__name'
    ).values(
        'ingredients__ingredient__name',
        'ingredients__ingredient__measurement_unit'
    ).annotate(
        total=Sum('ingredients__amount')
    )

    table = PrettyTable()
    table.field_names = ['Ингредиент', 'Ед-ца', 'Количество']
    for item in shopping_cart:
        table.add_row([item['ingredients__ingredient__name'],
                       item['total'],
                       item['ingredients__ingredient__measurement_unit']])

    response = HttpResponse(table, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename="shop.txt"'
    return response

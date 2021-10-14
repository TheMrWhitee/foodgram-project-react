from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (FavoritesViewSet, IngredientViewSet, RecipeViewSet,
                    TagViewSet, download_shopping_cart)

router = DefaultRouter()
router.register('recipes', RecipeViewSet)
router.register('tags', TagViewSet)
router.register('ingredients', IngredientViewSet)

favorite = FavoritesViewSet.as_view({'get': 'create',
                                     'delete': 'destroy'})

urlpatterns = [
    path('recipes/<int:id>/favorite/', favorite, {'model': 'Favorites'}),
    path(
        'recipes/<int:id>/shopping_cart/', favorite, {'model': 'ShoppingCart'}
    ),
    path('recipes/download_shopping_cart/', download_shopping_cart),
    path('', include(router.urls)),
]

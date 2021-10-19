from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (IngredientViewSet, RecipeViewSet, TagViewSet,
                    download_shopping_cart, favorites)

router = DefaultRouter()
router.register('recipes', RecipeViewSet)
router.register('tags', TagViewSet)
router.register('ingredients', IngredientViewSet)

urlpatterns = [
    path('recipes/<int:id>/favorite/', favorites, {'model': 'Favorites'}),
    path(
        'recipes/<int:id>/shopping_cart/', favorites, {'model': 'ShoppingCart'}
    ),
    path('recipes/download_shopping_cart/', download_shopping_cart),
    path('', include(router.urls)),
]

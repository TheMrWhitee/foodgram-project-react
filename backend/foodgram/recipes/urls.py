from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (IngredientViewSet, RecipeViewSet, TagViewSet,
                    create_or_delete_favorite, download_shopping_cart)

router = DefaultRouter()
router.register('recipes', RecipeViewSet)
router.register('tags', TagViewSet)
router.register('ingredients', IngredientViewSet)

urlpatterns = [
    path('recipes/<int:id>/favorite/', create_or_delete_favorite,
         {'model': 'Favorites'}),
    path(
        'recipes/<int:id>/shopping_cart/', create_or_delete_favorite,
        {'model': 'ShoppingCart'}
    ),
    path('recipes/download_shopping_cart/', download_shopping_cart),
    path('', include(router.urls)),
]

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (FavoritesViewSet, IngredientViewSet, RecipeViewSet,
                    TagViewSet)

router = DefaultRouter()
router.register('recipes', RecipeViewSet)
router.register('tags', TagViewSet)
router.register('ingredients', IngredientViewSet)

favorite_create = FavoritesViewSet.as_view({'get': 'create'})

urlpatterns = [
    path('recipes/<int:id>/favorite/', favorite_create),
    path('', include(router.urls)),
]

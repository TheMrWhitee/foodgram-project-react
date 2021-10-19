from django.urls import include, path

from .views import FollowViewSet, subscriptions

follow_list = FollowViewSet.as_view({'get': 'list'})

urlpatterns = [
    path('users/subscriptions/', follow_list),
    path('users/<int:id>/subscribe/', subscriptions),
    path('', include('djoser.urls')),
    path(r'auth/', include('djoser.urls.authtoken')),
]

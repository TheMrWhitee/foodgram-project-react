from django.urls import include, path

from .views import FollowViewSet

follow_list = FollowViewSet.as_view({'get': 'list'})
follow_create = FollowViewSet.as_view({'get': 'create',
                                       'delete': 'destroy'})
urlpatterns = [
    path('users/subscriptions/', follow_list),
    path('users/<int:id>/subscribe/', follow_create),
    path('', include('djoser.urls')),
    path(r'auth/', include('djoser.urls.authtoken')),
]

from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.response import Response

from .models import Follow
from .serializers import FollowSerializer

User = get_user_model()


class FollowViewSet(viewsets.ModelViewSet):
    def list(self, request, *args, **kwargs):
        followings = User.objects.filter(following__user=request.user)
        serializer = FollowSerializer(followings,
                                      context={'request': request},
                                      many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        user = request.user
        following = User.objects.get(pk=kwargs['id'])
        Follow.objects.create(user=user, following=following)
        serializer = FollowSerializer([following],
                                      context={'request': request},
                                      many=True)
        return Response(serializer.data)

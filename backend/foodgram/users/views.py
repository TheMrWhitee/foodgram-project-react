from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.response import Response

from .models import Follow
from .serializers import FollowSerializer

User = get_user_model()


class FollowViewSet(viewsets.ModelViewSet):
    def list(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        followings = User.objects.filter(following__user=request.user)
        serializer = FollowSerializer(followings,
                                      context={'request': request},
                                      many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        following = get_object_or_404(User, pk=kwargs['id'])

        if Follow.objects.filter(
                user=request.user, following=following
        ).exists() or following == request.user:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        Follow.objects.create(user=request.user, following=following)
        serializer = FollowSerializer(following,
                                      context={'request': request})
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        following = User.objects.get(pk=kwargs['id'])
        instance = Follow.objects.get(user=request.user, following=following)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Follow
from .serializers import FollowSerializer

User = get_user_model()


class FollowViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        recipes_limit = self.request.query_params.get('recipes_limit')
        followings = User.objects.filter(following__user=request.user)
        page = self.paginate_queryset(followings)
        serializer = FollowSerializer(page,
                                      context={'request': request,
                                               'recipes_limit': recipes_limit},
                                      many=True)
        return self.get_paginated_response(serializer.data)

    def create(self, request, *args, **kwargs):
        following = get_object_or_404(User, pk=kwargs['id'])

        if Follow.objects.filter(
                user=request.user, following=following
        ).exists() or following == request.user:
            data = {'errors': 'Подписка уже существует или попытка '
                              'подписаться на самого себя!'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        Follow.objects.create(user=request.user, following=following)
        serializer = FollowSerializer(following,
                                      context={'request': request})
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        following = User.objects.get(pk=kwargs['id'])

        if not Follow.objects.filter(
                user=request.user, following=following
        ).exists():
            data = {'errors': 'Подписки не существует.'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        instance = Follow.objects.get(user=request.user, following=following)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()

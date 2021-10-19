from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Follow
from .serializers import FollowCreateSerializer, FollowSerializer

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


@api_view(['GET', 'DELETE'])
@permission_classes([IsAuthenticated])
def subscriptions(request, **kwargs):
    following_user = get_object_or_404(User, pk=kwargs['id'])
    if request.method == 'GET':
        data = {'user': request.user.id, 'following': kwargs['id']}
        serializer = FollowCreateSerializer(data=data,
                                            context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        serializer = FollowSerializer(following_user,
                                      context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    subscribe = get_object_or_404(Follow, user=request.user,
                                  following=following_user)
    subscribe.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

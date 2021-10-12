from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.response import Response

from .serializers import FollowSerializer

User = get_user_model()


class FollowViewSet(viewsets.ModelViewSet):
    def list(self, request, *args, **kwargs):
        followings = User.objects.filter(following__user=request.user)
        serializer = FollowSerializer(followings, many=True)
        return Response(serializer.data)

from rest_framework import viewsets

from authentication.models import CustomUser
from authentication.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
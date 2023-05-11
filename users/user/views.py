from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView

from users.models import User
from users.user.serializers import UserSerializer, UsersCreateSerializer, UserUpdateSerializer


class UsersListView(ListAPIView):
    queryset = User.objects.all().order_by('username')
    serializer_class = UserSerializer


class UsersDetailView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UsersCreateView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UsersCreateSerializer


class UsersUpdateView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer


class UsersDeleteView(DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer



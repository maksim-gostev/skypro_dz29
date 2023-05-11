from rest_framework import serializers
from users.models import User, Location


class UserSerializer(serializers.ModelSerializer):
    location = serializers.SlugRelatedField(read_only=True,
                                            many=True,
                                            slug_field='name')
    class Meta:
        model = User
        exclude = ['password']


class UsersCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    location =serializers.SlugRelatedField(required=False,
                                           many=True,
                                           queryset=Location.objects.all(),
                                           slug_field='name')

    class Meta:
        model = User
        fields = '__all__'

    def is_valid(self, *, raise_exception=False):
        self._location = self.initial_data.pop('location')
        return super().is_valid(raise_exception=raise_exception)


    def create(self, validated_data):
        user = User.objects.create(**validated_data)

        for location in self._location:
            location_obj, _ = Location.objects.get_or_create(name=location)
            user.location.add(location_obj)
        user.save()
        return user

class UserUpdateSerializer(serializers.ModelSerializer):
    location = serializers.SlugRelatedField(required=False,
                                            many=True,
                                            queryset=Location.objects.all(),
                                            slug_field='name')

    class Meta:
        model = User
        fields = '__all__'

    def is_valid(self, *, raise_exception=False):
        self._location = self.initial_data.pop('location')
        return super().is_valid(raise_exception=raise_exception)

    def save(self, **kwargs):
        user = super().save()

        for location in self._location:
            location_obj, _ = Location.objects.get_or_create(name=location)
            user.location.add(location_obj)
        user.save()
        return user
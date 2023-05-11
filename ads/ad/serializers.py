from rest_framework import serializers
from ads.models import Ad, Category
from users.models import User


class AdSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(read_only=True,
                                          slug_field='username')
    category = serializers.SlugRelatedField(read_only=True,
                                            slug_field='name')

    location = serializers.SlugRelatedField(read_only=True,
                                            many=True,
                                            slug_field='name')

    class Meta:
        model = Ad
        fields = '__all__'


class AdCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    category = serializers.SlugRelatedField(required=False,
                                            queryset=Category.objects.all(),
                                            slug_field='name')
    author = serializers.SlugRelatedField(queryset=User.objects.all(),
                                          slug_field='username')
    class Meta:
        model = Ad
        exclude = ['image']


class AdUpdateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    category = serializers.SlugRelatedField(required=False,
                                            queryset=Category.objects.all(),
                                            slug_field='name')
    author = serializers.SlugRelatedField(queryset=User.objects.all(),
                                          slug_field='username')
    class Meta:
        model = Ad
        exclude = ['image']


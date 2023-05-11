from rest_framework.viewsets import ModelViewSet

from users.location.serializers import LocationSerializer
from users.models import Location


class LocationViewSet(ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
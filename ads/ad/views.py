from django.db.models import Q
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import UpdateView
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView

from ads.models import Ad
from ads.ad.serializers import AdSerializer, AdCreateSerializer, AdUpdateSerializer


class AdListView(ListAPIView):
    queryset = Ad.objects.all().order_by('-price')
    serializer_class = AdSerializer

    def get(self, request, *args, **kwargs):
        text_search = request.GET.get('text', None)

        if text_search:
            self.queryset = self.queryset.filter(
                name__icontains=text_search
            )

        categoryes_search = request.GET.getlist('cat', None)
        cat_q = None
        for cat in categoryes_search:
            if cat_q is None:
                cat_q = Q(category_id=cat)
            else:
                cat_q |= Q(category_id=cat)
        if cat_q:
            self.queryset = self.queryset.filter(cat_q)

        location_search = request.GET.get('location', None)

        if location_search:
            self.queryset = self.queryset.filter(
                author__location__name__icontains=location_search
            )

        price_from = request.GET.get('price_from', None)

        if price_from:
            self.queryset = self.queryset.filter(
                price__gte=price_from
            )

        price_to = request.GET.get('price_to', None)

        if price_to:
            self.queryset = self.queryset.filter(
                price__lte=price_to
            )

        return super().get(request, *args, **kwargs)


class AdDetailView(RetrieveAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer


class AdCreateView(CreateAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdCreateSerializer


class AdUpdateView(UpdateAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdUpdateSerializer


class AdDeleteView(DestroyAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer


@method_decorator(csrf_exempt, name='dispatch')
class AdImageView(UpdateView):
    model = Ad

    fields = ['name', 'author_id', 'price', 'description', 'is_published', 'image', 'category_id']

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        self.object.image = request.FILES["image"]

        self.object.save()

        return JsonResponse({
            "id": self.object.id,
            'name': self.object.name,
            'author_id': self.object.author_id.username,
            'author': self.object.author_id.id,
            'price': self.object.price,
            'description': self.object.description,
            'is_published': self.object.is_published,
            'image': self.object.image.url if self.object.image else None,
            'category_id': self.object.category_id.id
        }, status=200)
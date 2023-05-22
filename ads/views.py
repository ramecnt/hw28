import json

from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView

from ads.models import Ads


class RootView(View):
    def get(self, request):
        response = {"status": "ok"}
        return JsonResponse(response, status=200)


@method_decorator(csrf_exempt, name="dispatch")
class AdViewDataLoad(View):
    def get(self, request):
        with open(file="datasets/ads.json", encoding='utf-8') as file:
            data = json.load(file)
            for item in data:
                ad = Ads(name=item['name'],
                         author=item['author'],
                         price=item['price'],
                         description=item['description'],
                         address=item['address'],
                         is_published=item['is_published'])

                ad.save()
        return JsonResponse({"downloading": "completed"}, 200)


@method_decorator(csrf_exempt, name="dispatch")
class AdView(View):
    def get(self, request):
        ads = Ads.objects.all()
        response = []

        for ad in ads:
            response.append({
                "id": ad.id,
                "name": ad.name,
                "author": ad.author,
                "price": ad.price,
                "description": ad.description,
                "address": ad.address,
                "is_published": ad.is_published,
            })

        return JsonResponse(response, safe=False, json_dumps_params={'ensure_ascii': False})

    def post(self, request):
        ads_data = json.loads(request.body)
        ads = Ads()

        ads.id = ads_data.get("id")
        ads.name = ads_data.get("name")
        ads.author = ads_data.get("author")
        ads.price = ads_data.get("price")
        ads.description = ads_data.get("description")
        ads.is_published = ads_data.get("is_published", False)

        try:
            ads.full_clean()
        except ValidationError as e:
            return JsonResponse(e.message_dict, status=422)

        ads.save()

        return JsonResponse({
            "name": ads.name,
            "author": ads.author,
            "price": ads.price,
            "description": ads.description,
            "address": ads.address,
            "is_published": ads.is_published,
        }, safe=False, json_dumps_params={'ensure_ascii': False})


@method_decorator(csrf_exempt, name="dispatch")
class AdDetailView(DetailView):
    model = Ads

    def get(self, request, *args, **kwargs):
        ad = self.get_object()

        return JsonResponse({
            "id": ad.id,
            "name": ad.name
        }, safe=False, json_dumps_params={'ensure_ascii': False})
import json

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from ads.models import Location


@method_decorator(csrf_exempt, name="dispatch")
class LocationViewDataLoad(View):
    def get(self, request):
        with open(file="datasets/location.json", encoding="utf-8") as file:
            data = json.load(file)
            for item in data:
                location = Location(name=item['name'],
                                    lat=item['lat'],
                                    lng=item['lng'])

                location.save()
        return JsonResponse({"downloading": "completed"}, status=200)
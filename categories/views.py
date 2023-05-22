import json

from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView

from categories.models import Cat


@method_decorator(csrf_exempt, name="dispatch")
class CatViewDataLoad(View):
    def get(self, request):
        with open(file="datasets/categories.json", encoding="utf-8") as file:
            data = json.load(file)
            for item in data:
                category = Cat(name=item['name'])

                category.save()
        return JsonResponse({"downloading": "completed"}, 200)


@method_decorator(csrf_exempt, name="dispatch")
class CatView(View):
    def get(self, request):
        catd = Cat.objects.all()
        response = []

        for category in catd:
            response.append({
                "id": category.id,
                "name": category.name
            })

        return JsonResponse(response, safe=False, json_dumps_params={'ensure_ascii': False})

    def post(self, request):
        categories_data = json.loads(request.body)
        categories = Cat()

        categories.id = categories_data.get("id")
        categories.name = categories_data.get("name")

        try:
            categories.full_clean()
        except ValidationError as e:
            return JsonResponse(e.message_dict, status=422)

        categories.save()

        return JsonResponse({
            "name": categories.name
        }, safe=False, json_dumps_params={'ensure_ascii': False})


@method_decorator(csrf_exempt, name="dispatch")
class CatDetailView(DetailView):
    model = Cat

    def get(self, request, *args, **kwargs):
        category = self.get_object()

        return JsonResponse({
            "id": category.id,
            "name": category.name
        }, safe=False, json_dumps_params={'ensure_ascii': False})

import json

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView

from ads.models import Cat


@method_decorator(csrf_exempt, name="dispatch")
class CatViewDataLoad(View):
    def get(self, request):
        with open(file="datasets/categories.json", encoding="utf-8") as file:
            data = json.load(file)
            for item in data:
                category = Cat(name=item['name'])

                category.save()
        return JsonResponse({"downloading": "completed"}, status=200)


@method_decorator(csrf_exempt, name="dispatch")
class CatListView(ListView):
    model = Cat

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        categories = self.object_list.order_by("name")
        response = []

        for category in categories:
            response.append({
                "id": category.id,
                "name": category.name
            })

        return JsonResponse(response, safe=False, json_dumps_params={'ensure_ascii': False})


@method_decorator(csrf_exempt, name="dispatch")
class CatCreateView(CreateView):
    model = Cat
    fields = ["name"]

    def post(self, request, *args, **kwargs):
        categories_data = json.loads(request.body)
        categories = Cat.objects.create(
            name=categories_data.get("name")
        )

        return JsonResponse({
            "name": categories.name
        }, safe=False, json_dumps_params={'ensure_ascii': False})


@method_decorator(csrf_exempt, name="dispatch")
class CatDetailView(DetailView):
    model = Cat

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        return JsonResponse({
            "id": self.object.id,
            "name": self.object.name
        }, safe=False, json_dumps_params={'ensure_ascii': False})


@method_decorator(csrf_exempt, name="dispatch")
class CatDeleteView(DeleteView):
    model = Cat
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({"status": "ok"}, status=200)


@method_decorator(csrf_exempt, name="dispatch")
class CatUpdateView(UpdateView):
    model = Cat
    fields = ["name"]

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        categories_data = json.loads(request.body)
        self.object.name = categories_data.get("name")

        self.object.save()

        return JsonResponse({
            "id": self.object.id,
            "name": self.object.name
        }, safe=False, json_dumps_params={'ensure_ascii': False}, status=200)

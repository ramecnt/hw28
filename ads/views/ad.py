import json

from django.core.paginator import Paginator
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, DeleteView, UpdateView

from ads.models import Ads, Cat, User, Location
from hw27 import settings


class RootView(View):
    def get(self, request):
        response = {"status": "ok"}
        return JsonResponse(response, status=200)


@method_decorator(csrf_exempt, name="dispatch")
class AdViewDataLoad(View):
    def get(self, request):
        with open(file="datasets/ad.json", encoding='utf-8') as file:
            data = json.load(file)
            for item in data:
                ad = Ads(name=item['name'],
                         author_id=item['author_id'],
                         price=item['price'],
                         description=item['description'],
                         is_published=item['is_published'],
                         category_id=item['category_id'],
                         image=item['image'])

                ad.save()
        return JsonResponse({"downloading": "completed"}, status=200)


@method_decorator(csrf_exempt, name="dispatch")
class AdListView(ListView):
    model = Ads

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        ads = self.object_list.order_by("-price")

        paginator = Paginator(ads, settings.TOTAL_ON_PAGE)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        pre_resp = []
        for ad in page_obj:
            pre_resp.append({
                "id": ad.id,
                "name": ad.name,
                "author_id": ad.author_id,
                "author": str(User.objects.get(pk=ad.author_id)),
                "price": ad.price,
                "description": ad.description,
                "is_published": ad.is_published,
                "category_id": ad.category_id,
                "image": ad.image.url if ad.image else None
            })

        response = {
            "items": pre_resp,
            "num_pages": paginator.num_pages,
            "total": paginator.count
        }
        return JsonResponse(response, safe=False, json_dumps_params={'ensure_ascii': False})


@method_decorator(csrf_exempt, name="dispatch")
class AdCreateView(CreateView):
    model = Ads
    fields = ["name", "author_id", "price", "description", "is_published", "category_id", "image"]

    def post(self, request, *args, **kwargs):
        ads_data = json.loads(request.body)
        ads = Ads.objects.create(
            name=ads_data.get("name"),
            author_id=ads_data.get("author_id"),
            price=ads_data.get("price"),
            description=ads_data.get("description"),
            is_published=ads_data.get("is_published", False),
            category_id=ads_data.get("category_id")
        )

        return JsonResponse({
            "name": ads.name,
            "author_id": ads.author_id,
            "author": str(User.objects.get(pk=ads.author_id)),
            "price": ads.price,
            "description": ads.description,
            "is_published": ads.is_published,
            "category_id": ads.category_id,
            "image": ads.image.url if ads.image else None
        }, safe=False, json_dumps_params={'ensure_ascii': False})


@method_decorator(csrf_exempt, name="dispatch")
class AdDetailView(DetailView):
    model = Ads

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        return JsonResponse({
            "id": self.object.id,
            "name": self.object.name,
            "author_id": self.object.author_id,
            "author": str(User.objects.get(pk=self.object.author_id)),
            "price": self.object.price,
            "description": self.object.description,
            "is_published": self.object.is_published,
            "category_id": self.object.category_id,
            "image": self.object.image.url if self.object.image else None
        }, safe=False, json_dumps_params={'ensure_ascii': False})


@method_decorator(csrf_exempt, name="dispatch")
class AdDeleteView(DeleteView):
    model = Ads
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({"status": "ok"}, status=200)


@method_decorator(csrf_exempt, name="dispatch")
class AdUpdateView(UpdateView):
    model = Ads
    fields = ["name", "author_id", "price", "description", "is_published", "category_id", "image"]

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        ads_data = json.loads(request.body)
        if ads_data.get("name"):
            self.object.name = ads_data.get("name")
        if ads_data.get("author_id"):
            self.object.author_id = ads_data.get("author_id")
        if ads_data.get("price"):
            self.object.price = ads_data.get("price")
        if ads_data.get("description"):
            self.object.description = ads_data.get("description")
        if ads_data.get("category_id"):
            self.object.category_id = ads_data.get("category_id")

        self.object.save()

        return JsonResponse({
            "id": self.object.id,
            "name": self.object.name,
            "author_id": self.object.author_id,
            "author": str(User.objects.get(pk=self.object.author_id)),
            "price": self.object.price,
            "description": self.object.description,
            "is_published": self.object.is_published,
            "category_id": self.object.category_id,
            "image": self.object.image.url if self.object.image else None
        }, safe=False, json_dumps_params={'ensure_ascii': False}, status=200)


@method_decorator(csrf_exempt, name="dispatch")
class AdImageView(UpdateView):
    model = Ads
    fields = ["name", "author_id", "price", "description", "is_published", "category_id", "image"]

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        self.object.image = request.FILES['image']
        self.object.save()

        return JsonResponse({
            "id": self.object.id,
            "name": self.object.name,
            "author_id": self.object.author_id,
            "author": str(User.objects.get(pk=self.object.author_id)),
            "price": self.object.price,
            "description": self.object.description,
            "is_published": self.object.is_published,
            "category_id": self.object.category_id,
            "image": self.object.image.url if self.object.image else None
        }, safe=False, json_dumps_params={'ensure_ascii': False}, status=200)

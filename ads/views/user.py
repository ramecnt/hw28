import json

from django.core.paginator import Paginator
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView

from ads.models import User, Location, Ads
from hw27 import settings


@method_decorator(csrf_exempt, name="dispatch")
class UserViewDataLoad(View):
    def get(self, request):
        with open(file="datasets/user.json", encoding="utf-8") as file:
            data = json.load(file)
            for item in data:
                user = User(first_name=item["first_name"],
                            last_name=item["last_name"],
                            username=item["username"],
                            password=item["password"],
                            role=item["role"],
                            age=item["age"],
                            location_id=item["location_id"])

                user.save()
        return JsonResponse({"downloading": "completed"}, status=200)


@method_decorator(csrf_exempt, name="dispatch")
class UserListView(ListView):
    model = User

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        users = self.object_list

        paginator = Paginator(users, settings.TOTAL_ON_PAGE)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        pre_resp = []
        for user in page_obj:
            ad_amount = Ads.objects.filter(author_id=user.id).count()
            pre_resp.append({
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "username": user.username,
                "password": user.password,
                "role": user.role,
                "age": user.age,
                "locations": [
                    str(Location.objects.get(pk=int(user.location_id)))
                ] if not user.added_by_user else [user.location_id],
                "total_ads": ad_amount
            })

        response = {
            "items": pre_resp,
            "num_pages": paginator.num_pages,
            "total": paginator.count
        }
        return JsonResponse(response, safe=False, json_dumps_params={'ensure_ascii': False})


@method_decorator(csrf_exempt, name='dispatch')
class UserDetailView(DetailView):
    model = User

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        ad_amount = Ads.objects.filter(author_id=self.object.id).count()

        return JsonResponse({
            "id": self.object.id,
            "first_name": self.object.first_name,
            "last_name": self.object.last_name,
            "username": self.object.username,
            "password": self.object.password,
            "role": self.object.role,
            "age": self.object.age,
            "locations": [
                str(Location.objects.get(pk=int(self.object.location_id)))
            ] if not self.object.added_by_user else [self.object.location_id],
            "total_ads": ad_amount
        }, safe=False, json_dumps_params={'ensure_ascii': False})


@method_decorator(csrf_exempt, name="dispatch")
class UserCreateView(CreateView):
    model = User
    fields = ["first_name", "last_name", "username", "password", "role", "age", "location_id", "added_by_user"]

    def post(self, request, *args, **kwargs):
        user_data = json.loads(request.body)
        user = User.objects.create(
            first_name=user_data.get("first_name"),
            last_name=user_data.get("last_name", None),
            username=user_data.get("username"),
            password=user_data.get("password"),
            role=user_data.get("role"),
            age=user_data.get("age"),
            location_id=", ".join(user_data.get("locations")),
            added_by_user=True
        )

        return JsonResponse({
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "username": user.username,
            "password": user.password,
            "role": user.role,
            "age": user.age,
            "locations": [user.location_id],
        }, safe=False, json_dumps_params={'ensure_ascii': False})


@method_decorator(csrf_exempt, name="dispatch")
class UserDeleteView(DeleteView):
    model = User
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({"status": "ok"}, status=200)


@method_decorator(csrf_exempt, name="dispatch")
class UserUpdateView(UpdateView):
    model = User
    fields = ["first_name", "last_name", "username", "password", "role", "age", "location_id"]

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        user_data = json.loads(request.body)

        ad_amount = Ads.objects.filter(author_id=self.object.id).count()

        if user_data.get("first_name"):
            self.object.name = user_data.get("first_name")
        if user_data.get("last_name"):
            self.object.author_id = user_data.get("last_name")
        if user_data.get("username"):
            self.object.price = user_data.get("username")
        if user_data.get("password"):
            self.object.description = user_data.get("password")
        if user_data.get("role"):
            self.object.category_id = user_data.get("role")
        if user_data.get('age'):
            self.object.age = user_data.get('age')
        if user_data.get('locations'):
            self.object.location_id = user_data.get("locations")
        self.object.added_by_user = True

        self.object.save()

        return JsonResponse({
            "first_name": self.object.first_name,
            "last_name": self.object.last_name,
            "username": self.object.username,
            "password": self.object.password,
            "role": self.object.role,
            "age": self.object.age,
            "locations": [
                str(Location.objects.get(pk=int(self.object.location_id)))
            ] if not self.object.added_by_user else [self.object.location_id],
            "total_ads": ad_amount
        }, safe=False, json_dumps_params={'ensure_ascii': False}, status=200)

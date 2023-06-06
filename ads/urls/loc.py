from django.urls import path

from ads.views.loc import LocationViewDataLoad

urlpatterns = [
    path('download/', LocationViewDataLoad.as_view())
]
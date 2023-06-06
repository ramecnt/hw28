from django.urls import path

from ads.views.cat import CatListView, CatViewDataLoad, CatDetailView, CatDeleteView, CatUpdateView, CatCreateView

urlpatterns = [
    path('download/', CatViewDataLoad.as_view()),

    path('', CatListView.as_view()),

    path('create/', CatCreateView.as_view()),

    path('<int:pk>', CatDetailView.as_view()),

    path('<int:pk>/delete', CatDeleteView.as_view()),

    path('<int:pk>/create', CatUpdateView.as_view())
]

from django.urls import path

from ads.views.ad import AdViewDataLoad, AdListView, AdDetailView, AdDeleteView, AdUpdateView, AdImageView, AdCreateView

urlpatterns = [
    path('download/', AdViewDataLoad.as_view()),

    path('', AdListView.as_view()),

    path('create/', AdCreateView.as_view()),

    path('<int:pk>', AdDetailView.as_view()),

    path('<int:pk>/delete', AdDeleteView.as_view()),

    path('<int:pk>/update', AdUpdateView.as_view()),

    path('<int:pk>/upload_image', AdImageView.as_view())
]

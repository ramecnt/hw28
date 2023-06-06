from django.urls import path

from ads.views.user import UserViewDataLoad, UserListView, UserCreateView, UserDetailView, UserDeleteView, \
    UserUpdateView

urlpatterns = [
    path('download/', UserViewDataLoad.as_view()),

    path('', UserListView.as_view()),

    path('create/', UserCreateView.as_view()),

    path('<int:pk>', UserDetailView.as_view()),

    path('<int:pk>/delete', UserDeleteView.as_view()),

    path('<int:pk>/update', UserUpdateView.as_view()),
]
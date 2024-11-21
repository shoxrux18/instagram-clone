from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [
    path('api/token/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("", views.AccountListView.as_view()),
    path("<int:pk>/", views.AccountDetailView.as_view()),
    path("follow/<int:pk>/", views.FollowCreateOrDeleteView.as_view()),
    path("connection/<int:pk>/", views.FollowRequestUpdateOrDeleteView.as_view()),
    path("requests/", views.RequestListView.as_view()),
    path("followers/", views.FollowerListView.as_view()),
    path("following/", views.FollowingListView.as_view()),
    path("<int:pk>/followers/", views.FollowerListView.as_view()),
    path("<int:pk>/following/", views.FollowingListView.as_view()),

]

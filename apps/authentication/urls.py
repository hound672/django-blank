from django.urls import path
from rest_framework_jwt.views import refresh_jwt_token, obtain_jwt_token

from apps.authentication import apis


urlpatterns = [
    path('login/', view=apis.LoginApi.as_view(), name='login'),
    path('me/', view=apis.UserDetailApi.as_view(), name='user-detail'),
    path('token-refresh/', view=refresh_jwt_token),
    path('logout/', view=apis.LogoutApi.as_view(), name='logout'),
    path('change-password/', view=apis.ChangePasswordApi.as_view(), name='change-password'),
]

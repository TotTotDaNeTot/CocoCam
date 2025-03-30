from django.urls import path, include
from . import views


from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)


app_name = 'accounts'


urlpatterns = [
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.authtoken")),
    path("auth/", include("djoser.urls.jwt")),
    path('auth/users/activation/<str:uid>/<str:token>/', views.activate_user, name='activate'),  # Маршрут для активации
    path('auth/jwt/create/', TokenObtainPairView.as_view(), name='jwt-create'),  # JWT-токен
    path('auth/jwt/refresh/', TokenRefreshView.as_view(), name='jwt-refresh'),  # Обновление JWT
    path('auth/jwt/verify/', TokenVerifyView.as_view(), name='jwt-verify'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', views.reg_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout, name='logout'),
    path('verify-token/', views.verify_token, name='verify_token'),
    #path('api/auth/logout/', LogoutView.as_view(), name='logout'),
]


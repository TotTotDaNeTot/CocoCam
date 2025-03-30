from django.contrib import admin
from django.urls import path, include
from core import views




urlpatterns = [
    path("", include('core.urls')),
    path("", include('accounts.urls')),
    path("links/", include('link.urls')),
    path("dashboard/", include('dashboard.urls')),
    path("admin/", admin.site.urls),
    path("", include("payments.urls")),
    path("stripe/", include("djstripe.urls", namespace="djstripe")),
]

handler404 = 'core.views.pageNotFound'
# handler404 = views.pageNotFound

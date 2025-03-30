from django.urls import path
from . import views
from .stripe_webhook import stripe_webhook


app_name = 'payments'


urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path("create-sub/", views.create_sub, name="create sub"),
    path("complete/", views.complete, name="complete"),
    path('stripe_webhook/', stripe_webhook, name='stripe_webhook'),
    
    path("cancel/", views.cancel, name="cancel"),
    # path("cancel-subscription/", views.cancel_subscription, name="cancel_subscription"),
]
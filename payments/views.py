from cococam.JWTdecorators import jwt_login_required
from accounts.models import *

from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.views.decorators.http import require_http_methods

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication
from rest_framework.response import Response
from rest_framework import status

from djstripe.models import Product, Subscription

import djstripe
import stripe
import json
import logging
import urllib3




urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

logger = logging.getLogger(__name__)

# Используйте секретный ключ API
stripe.api_key = settings.STRIPE_TEST_SECRET_KEY



@require_http_methods(["GET"])
@jwt_login_required
@permission_classes([IsAuthenticated])
def checkout(request):
    products = Product.objects.all().prefetch_related('plan_set')
    
    return render(request, "payments/checkout.html", {
        'products': products,
        'stripe_public_key': settings.STRIPE_TEST_PUBLIC_KEY
    })
    
    

@api_view(['POST'])
@jwt_login_required
@permission_classes([IsAuthenticated])
def create_sub(request):
    
  if request.method == 'POST':
      data = json.loads(request.body)
    #   logger.info(f"Received data: {data}")
      payment_method = data['payment_method']
      price_id = data['price_id']
      stripe.api_key = settings.STRIPE_TEST_SECRET_KEY

      payment_method_obj = stripe.PaymentMethod.retrieve(payment_method)
      djstripe.models.PaymentMethod.sync_from_stripe_data(payment_method_obj)


      try:
          customer = stripe.Customer.create(
              payment_method=payment_method,
              email=request.user.email,
              invoice_settings={
                  'default_payment_method': payment_method
              }
          )

          djstripe_customer = djstripe.models.Customer.sync_from_stripe_data(customer)

          user = request.user
          user.customer = djstripe_customer
          
          subscription = stripe.Subscription.create(
              customer=customer.id,
              items=[
                  {'price': price_id}
              ],
              expand=["latest_invoice.payment_intent"]
          )
        
        #   logger.info(f"Subscription created: {subscription}")
          
          djstripe_subscription = djstripe.models.Subscription.sync_from_stripe_data(subscription)
          
        #   stripe_plan = stripe.Plan.retrieve(subscription.plan.id)
        #   djstripe_plan = djstripe.models.Plan.sync_from_stripe_data(stripe_plan)
        
        #   price_id = subscription.items.data[0].price.id
        #   price = stripe.Price.retrieve(price_id)
        #   product = stripe.Product.retrieve(price.product)
          
          user.subscription = djstripe_subscription
        #   user.plan_id = 2  # Обновляем план пользователя
          user.save()
          logger.info(f"User plan updated: {request.user.plan}")
          return JsonResponse(subscription)
      
      except Exception as e:
        #   logger.error(f"Error: {e}")
          return JsonResponse({'error': str(e)}, status=403)
      
  else:  
    return HttpResponse('requet method not allowed')



@require_http_methods(["GET"])
@jwt_login_required
@permission_classes([IsAuthenticated])
def complete(request):
  return render(request, "payments/complete.html")



@require_http_methods(["GET"])
@jwt_login_required
@permission_classes([IsAuthenticated])
def cancel(request):

    sub_id = request.user.subscription.id  # Получаем subscription_id из модели пользователя
    stripe.api_key = settings.STRIPE_TEST_SECRET_KEY  # Используем ключ из dj-stripe
    
    user = request.user
    
    try:
        
        # Отменяем подписку с окончанием текущего периода
        stripe.Subscription.modify(
            sub_id,
            cancel_at_period_end=True
        )
        
        user.sub_status = 'canceled'
        user.save()
        
        return redirect("/links/subscription/")  # Перенаправляем на главную страницу
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=403)  # Возвращаем ошибку, если что-то пошло не так






# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def create_sub(request):
#     if request.method == 'POST':
#         try:
#             # Получаем реального пользователя из БД
#             user = User.objects.get(pk=request.user.pk)
            
#             data = json.loads(request.body)
#             stripe.api_key = settings.STRIPE_TEST_SECRET_KEY

#             # Создаем customer в Stripe
#             customer = stripe.Customer.create(
#                 payment_method=data['payment_method'],
#                 email=user.email,
#                 invoice_settings={
#                     'default_payment_method': data['payment_method']
#                 }
#             )

#             # Создаем подписку
#             subscription = stripe.Subscription.create(
#                 customer=customer.id,
#                 items=[{'price': data['price_id']}],
#                 expand=["latest_invoice.payment_intent"]
#             )

#             # Обновляем пользователя
#             user.stripe_customer_id = customer.id
#             user.stripe_subscription_id = subscription.id
#             user.is_subscribed = True
#             user.save()

#             return Response({'status': 'success'}, status=status.HTTP_200_OK)

#         except User.DoesNotExist:
#             return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
#     return Response({'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)



# @jwt_login_required
# @permission_classes([IsAuthenticated])
# def checkout(request):
    
#     logger.debug("Rendering checkout page")
#     products = Product.objects.all()
#     return render(request, "payments/checkout.html", {"products": products})




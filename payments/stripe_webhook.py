from accounts.models import User

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from djstripe.models import Subscription
from djstripe.models import Subscription as DjstripeSubscription

from rest_framework.decorators import api_view, permission_classes

import json
import logging
import stripe




logger = logging.getLogger(__name__)

stripe.api_key = settings.STRIPE_WEBHOOK_SECRET



@csrf_exempt 
def stripe_webhook(request):
    logger.info("Получен запрос на вебхук.")
    
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET
    
    
    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
        
    except ValueError:
        # logger.error(f"Ошибка при декодировании события: {e}")
        return HttpResponse(status=400)
    
    except stripe.error.SignatureVerificationError :
        # logger.error(f"Ошибка верификации подписи: {e}")
        return HttpResponse(status=400)
    
    
    
    if event['type'] == 'customer.subscription.created':
        
        # Извлекаем customer_id из события
        stripe_subscription_id = event['data']['object']['id']  # Идентификатор подписки (sub_xxx)
        
        try:
            stripe_subscription = stripe.Subscription.retrieve(stripe_subscription_id)
            subscription = Subscription.sync_from_stripe_data(stripe_subscription)
            
            # Находим подписку по stripe_subscription_id
            subscription = DjstripeSubscription.objects.get(id=stripe_subscription_id)
            
            # Находим пользователя по subscription_id
            user = User.objects.get(subscription_id=subscription.djstripe_id)
            user.plan_id = 2  # Обновляем план пользователя
            user.sub_status = 'active'
            user.save()
            
            print(event)
            print(f"User {user.email} plan updated to pro.")
            
        except DjstripeSubscription.DoesNotExist:
            print(f"Subscription with id {stripe_subscription_id} does not exist.")
            return HttpResponse(status=404)
        
        except User.DoesNotExist:
            print(f"User with subscription_id {subscription.djstripe_id} does not exist.")
            return HttpResponse(status=404)
    


    if event['type'] == 'customer.subscription.deleted':
        
        # Извлекаем customer_id из события
        stripe_subscription_id = event['data']['object']['customer']  # Идентификатор подписки (sub_xxx)
        
        try:
            # Находим подписку по stripe_subscription_id
            subscription = DjstripeSubscription.objects.get(customer_id=stripe_subscription_id)
            
            # Находим пользователя по subscription_id
            user = User.objects.get(subscription_id=subscription.djstripe_id)
            user.plan_id = 1  # Обновляем план пользователя
            user.save()
            print(event)
            print(f"User {user.email} plan updated to free.")
            
        except DjstripeSubscription.DoesNotExist:
            print(f"Subscription with id {stripe_subscription_id} does not exist.")
            return HttpResponse(status=404)
        
        except User.DoesNotExist:
            print(f"User with subscription_id {subscription.djstripe_id} does not exist.")
            return HttpResponse(status=404)

    return HttpResponse(status=200)






# @csrf_exempt
# def stripe_webhook(request):
#     if request.method != 'POST':
#         return HttpResponseBadRequest("Invalid method")

#     payload = request.body
#     sig_header = request.META.get('HTTP_STRIPE_SIGNATURE', '')

#     if not sig_header:
#         logger.error("Missing Stripe-Signature header")
#         return HttpResponseBadRequest("Missing signature header")

#     try:
#         event = stripe.Webhook.construct_event(
#             payload,
#             sig_header,
#             settings.STRIPE_WEBHOOK_SECRET
#         )
#     except ValueError as e:
#         logger.error(f"Invalid payload: {str(e)}")
#         return HttpResponseBadRequest("Invalid payload")
#     except stripe.error.SignatureVerificationError as e:
#         logger.error(f"Invalid signature: {str(e)}")
#         return HttpResponseBadRequest("Invalid signature")
#     except Exception as e:
#         logger.error(f"Webhook error: {str(e)}")
#         return HttpResponseBadRequest("Webhook error")

#     logger.info(f"Received event: {event['type']}")

#     # Обработка событий
#     if event['type'] == 'customer.subscription.created':
#         return handle_subscription_created(event)
#     elif event['type'] == 'customer.subscription.deleted':
#         return handle_subscription_deleted(event)

#     return HttpResponse(status=200)

# def handle_subscription_created(event):
#     subscription = event['data']['object']
#     try:
#         # Синхронизация с dj-stripe
#         dj_subscription = DjstripeSubscription.sync_from_stripe_data(subscription)
        
#         user = User.objects.get(stripe_customer_id=subscription['customer'])
#         user.subscription_id = dj_subscription.id
#         user.plan_id = 2  # Pro plan
#         user.sub_status = 'active'
#         user.save()
        
#         logger.info(f"Updated user {user.email} to Pro plan")
#         return HttpResponse(status=200)
        
#     except User.DoesNotExist:
#         logger.error(f"User not found for customer: {subscription['customer']}")
#         return HttpResponse(status=404)
#     except Exception as e:
#         logger.error(f"Subscription created error: {str(e)}")
#         return HttpResponse(status=400)

# def handle_subscription_deleted(event):
#     subscription = event['data']['object']
#     try:
#         user = User.objects.get(stripe_customer_id=subscription['customer'])
#         user.plan_id = 1  # Free plan
#         user.sub_status = 'canceled'
#         user.save()
        
#         logger.info(f"Updated user {user.email} to Free plan")
#         return HttpResponse(status=200)
        
#     except User.DoesNotExist:
#         logger.error(f"User not found for customer: {subscription['customer']}")
#         return HttpResponse(status=404)
#     except Exception as e:
#         logger.error(f"Subscription deleted error: {str(e)}")
#         return HttpResponse(status=400)


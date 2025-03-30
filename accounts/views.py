from django.contrib.auth import authenticate, login as user_login, logout as user_logout

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from .models import *

from django.conf import settings
import djstripe
import stripe
import json
from djstripe.models import Product
from django.contrib.auth.decorators import login_required

from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.tokens import RefreshToken
import logging


from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import (
    api_view, permission_classes, authentication_classes)

from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model

from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from django.conf import settings
import jwt

import requests
import logging
import time 

from django.urls import reverse



User = get_user_model()



logger = logging.getLogger(__name__)




# Функция для проверки срока действия токена
def check_token_expiry(token):
    try:
        decoded_token = AccessToken(token)
        return decoded_token.payload  # Возвращает данные токена, включая срок действия
    except Exception as e:
        return str(e)  # Возвращает ошибку, если токен недействителен

# Функция для проверки, находится ли токен в черном списке
def is_token_blacklisted(token):
    try:
        outstanding_token = OutstandingToken.objects.get(token=token)
        return BlacklistedToken.objects.filter(token=outstanding_token).exists()
    except OutstandingToken.DoesNotExist:
        return False
    
    

# Функция для проверки валидности токена
def validate_token(request):
    access_token = request.session.get('access_token')
    if not access_token:
        return False

    try:
        # Декодируем токен, чтобы проверить его валидность
        token = AccessToken(access_token)
        if is_token_blacklisted(access_token):
            return False
        # Проверяем срок действия токена
        if token.payload['exp'] < time.time():
            return False
        return True
    except TokenError:
        return False


# Функция для обновления access-токена
def refresh_access_token(request):
    refresh_token = request.session.get('refresh_token')
    if not refresh_token:
        # logger.error("Refresh token отсутствует в сессии")
        return None

    try:
        response = requests.post(
            'http://127.0.0.1:8000/auth/jwt/refresh/',
            json={'refresh': refresh_token},
        )

        if response.status_code == 200:
            access_token = response.json().get('access')
            if access_token:
                # logger.info("Новый access token успешно получен")
                request.session['access_token'] = access_token
                return access_token
            else:
                logger.error("Новый access token отсутствует в ответе")
        else:
            logger.error(f"Ошибка при обновлении токена: {response.status_code}, {response.text}")
    except Exception as e:
        logger.error(f"Ошибка при обновлении токена: {e}")
    return None




def reg_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        re_password = request.POST.get('re_password')

        if password == re_password:
            response = requests.post(
                'http://127.0.0.1:8000/auth/users/',
                data={
                    'username': username,
                    'email': email,
                    'password': password,
                    're_password': re_password,
                }
            )

            if response.status_code == 201:  # Успешная регистрация
                return HttpResponseRedirect('/login')
            else:
                error_message = response.json().get('non_field_errors', ['Ошибка регистрации'])[0]
                return render(request, 'accounts/auth/register.html', {
                    'error': error_message
                })
        else:
            return render(request, 'accounts/auth/register.html', {
                'error': 'Пароли не совпадают'
            })

    return render(request, 'accounts/auth/register.html')



def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Отправляем запрос к JWT endpoint
        response = requests.post(
            'http://127.0.0.1:8000/auth/jwt/create/',
            data={
                'username': username,
                'password': password
            }
        )
        

        if response.status_code == 200:
            tokens = response.json()
            response = HttpResponseRedirect(reverse('core:index'))
            
            # Устанавливаем токены и в куки, и в localStorage через JavaScript
            response.set_cookie('access_token', tokens['access'], httponly=False, samesite='Lax')
            response.set_cookie('refresh_token', tokens['refresh'], httponly=False, samesite='Lax')
            
            # Добавляем JavaScript для сохранения в localStorage
            response.write(
                f"""
                <script>
                    localStorage.setItem('accessToken', '{tokens['access']}');
                    localStorage.setItem('refreshToken', '{tokens['refresh']}');
                    window.location.href = '{reverse('core:index')}';
                </script>
                """
            )
            return response
        
        else:
            error_message = response.json().get('detail', 'Invalid username or password')
            return render(request, 'accounts/auth/login.html', {'error': error_message})

    return render(request, 'accounts/auth/login.html')



def logout(request):
    if request.method == 'POST':
        response = redirect('login')
        
        # Очищаем все токены
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        
        # Пытаемся добавить refresh token в черный список
        refresh_token = request.COOKIES.get('refresh_token')
        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
            except Exception as e:
                print(f"Ошибка при добавлении токена в черный список: {e}")
        
        return response
    
    return JsonResponse({'error': 'Метод не разрешен'}, status=405)
    
    
    
def activate_user(request, uid, token):
    try:
        uid = urlsafe_base64_decode(uid).decode()
        user = get_object_or_404(User, pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.is_verified = True
        user.save()
        
        access_token = AccessToken.for_user(user)
        return redirect(f'/login?token={access_token}')  # Перенаправление на страницу входа
    else:
        # Обработка случая, когда токен недействителен
        return redirect('invalid_token')  # Перенаправление на страницу с ошибкой


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def verify_token(request):
    return Response({'status': 'valid'})



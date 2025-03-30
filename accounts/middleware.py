from django.contrib.auth import logout
from django.contrib.auth import get_user_model
from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import resolve

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

from urllib.parse import urlencode

import re 
import logging




logger = logging.getLogger(__name__)


User = get_user_model()



class JWTAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.exempt_paths = [
            '/login/',
            '/auth/',
            '/static/',
            '/api/'
            '/checkout/',
            '/create-sub/'
        ]

    def __call__(self, request):
        # Пропускаем проверку для исключенных путей
        if any(request.path.startswith(p) for p in self.exempt_paths):
            return self.get_response(request)
            
        # Проверяем JWT токен
        jwt_token = request.COOKIES.get('access_token')
        if jwt_token:
            try:
                from rest_framework_simplejwt.authentication import JWTAuthentication
                jwt_auth = JWTAuthentication()
                validated_token = jwt_auth.get_validated_token(jwt_token)
                request.user = jwt_auth.get_user(validated_token)
            except Exception as e:
                logger.error(f"JWT error: {str(e)}")
                return self._handle_unauthorized(request)
                
        return self.get_response(request)

    def _handle_unauthorized(self, request):
        response = HttpResponseRedirect('/login/')
        response.delete_cookie('access_token')
        return response
    
    
    
    
    # class JWTAuthenticationMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response
#         self.login_url = '/login/'  # Убедитесь, что этот URL существует!
        
#         # Пути, которые не требуют аутентификации
#         self.exempt_paths = [
#             self.login_url,
#             '/static/',
#             '/media/',
#             '/api/auth/',
#             '/login/',  # На всякий случай
#         ]

#     def __call__(self, request):
#         # Пропускаем проверку для исключенных путей
#         if any(request.path.startswith(p) for p in self.exempt_paths):
#             return self.get_response(request)
        
        
#         # Проверяем атрибут is_public у View
#         try:
#             resolved = resolve(request.path)
#             view_func = resolved.func
            
#             if self._is_view_public(view_func):
#                 return self.get_response(request)
#         except:
#             pass


#         # Проверяем токен
#         jwt_token = (
#             request.COOKIES.get('access_token') or 
#             request.headers.get('Authorization', '').split(' ')[-1]
#         )

#         try:
#             if jwt_token:
#                 jwt_auth = JWTAuthentication()
#                 validated_token = jwt_auth.get_validated_token(jwt_token)
#                 user = jwt_auth.get_user(validated_token)
#                 request.user = user
#             else:
#                 return self._handle_unauthorized(request)
                
#         except (InvalidToken, TokenError):
#             return self._handle_unauthorized(request)

#         return self.get_response(request)
    
    
#     def _is_view_public(self, view_func):
#         """
#         Проверяет, является ли View публичной через:
#         1. Декоратор @public_view (для FBV)
#         2. Миксин PublicViewMixin (для CBV)
#         """
#         # Для Function-Based Views
#         if getattr(view_func, 'is_public', False):
#             return True
            
#         # Для Class-Based Views
#         view_class = getattr(view_func, 'view_class', None)
#         if view_class and getattr(view_class, 'is_public', False):
#             return True
            
#         return False
    
    

#     def _handle_unauthorized(self, request):
#         """Обработка неавторизованных запросов"""
#         from django.contrib.auth import logout
#         logout(request)
        
#         # Проверяем, не пытаемся ли мы уже редиректить на login
#         if not request.path.startswith(self.login_url):
#             response = HttpResponseRedirect(self.login_url)
#             response.delete_cookie('access_token')
#             return response
        
#         # Если уже на странице входа - возвращаем 401
#         return HttpResponse('Unauthorized', status=401)
    

# class JWTAuthenticationMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response
        

#     def __call__(self, request):
        
#         print(f"Request path: {request.path}")  # Логируем запрос
#         if request.path == '/accounts/login/':
#             print("WARNING: Someone is trying to access /accounts/login/")
#             return HttpResponseRedirect('/login/')
        
#         # Пропускаем проверку для статических файлов и API
#         if request.path.startswith('/static/') or request.path.startswith('/api/') or request.path.startswith('/create-sub/'):
#             return self.get_response(request)

#         jwt_token = (
#             request.COOKIES.get('access_token') or 
#             request.headers.get('Authorization', '').split(' ')[-1]
#         )
        
#         if jwt_token:
#             try:
#                 jwt_auth = JWTAuthentication()
#                 validated_token = jwt_auth.get_validated_token(jwt_token)
#                 user = jwt_auth.get_user(validated_token)
#                 request.user = user
#             except (InvalidToken, TokenError):
#                 response = HttpResponseRedirect('/login/')
#                 response.delete_cookie('access_token')
#                 return response
            
#         elif hasattr(request, 'user') and request.user.is_authenticated:
#             # Если нет JWT, но есть сессия - очищаем
#             response = HttpResponseRedirect('/login/')
#             response.delete_cookie('access_token')
#             return response

#         return self.get_response(request)


    
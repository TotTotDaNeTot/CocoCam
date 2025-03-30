import jwt
from django.conf import settings

# Укажите ваш токен здесь
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQyNjY1NzAyLCJpYXQiOjE3NDI2NjIxMDIsImp0aSI6IjIxODI0ODdkOTY3NzRhNDI4ODU4OTU3MDFkMzAyMjkzIiwidXNlcl9pZCI6MzB9.4yA72qqOEoIagEUczF01hGGUIC1H_hLHeBqv3Yik_dI"

try:
    # Декодируем токен
    decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
    print("Токен валиден:", decoded)
except jwt.ExpiredSignatureError:
    print("Токен истек")
except jwt.InvalidTokenError:
    print("Токен недействителен")
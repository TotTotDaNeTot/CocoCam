from django.http import JsonResponse

def jwt_login_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:  # Проверяет user, установленного JWT-мидлварью
            return JsonResponse({"error": "Authentication required"}, status=401)
        return view_func(request, *args, **kwargs)
    return wrapper
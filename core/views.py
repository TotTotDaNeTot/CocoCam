from django.shortcuts import render
from django.http import HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from .PublicDecorator import public_view  

    
# @public_view
def index(request):
    return render(request, 'core/index.html')

# @public_view
def about(request):
    return render(request, 'core/about.html')

# @public_view
def pricing(request):
    return render(request, 'core/pricing.html')

# @public_view
def service(request):
    return render(request, 'core/service.html')


def pageNotFound(request, exception):
    """Обработчик 404 ошибки"""
    return render(request, 'core/404.html', status=404)

# def pageNotFound(request, exception):
#     return HttpResponseNotFound('<h1>Page not found</h1>')

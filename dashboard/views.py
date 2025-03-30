from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods

from link.models import Link
from cococam.JWTdecorators import jwt_login_required

from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication



@require_http_methods(["GET"])
@jwt_login_required
@permission_classes([IsAuthenticated])
def dashboard(request):
    
    newest_links = Link.objects.filter(created_by=request.user)[:5]

    return render(request, 'dashboard/dashboard.html', {
    'newest_links': newest_links,
    })
        
    
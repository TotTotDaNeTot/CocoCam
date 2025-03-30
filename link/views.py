from django.contrib.auth.decorators import login_required   
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse, HttpResponseNotAllowed
from django.views.decorators.http import require_http_methods

from .forms import CategoryForm, LinkForm
from .models import Category, Link
from accounts.models import *
from cococam.JWTdecorators import jwt_login_required

from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication


from rest_framework.exceptions import AuthenticationFailed
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status




#LINKS
@require_http_methods(["GET"])
@jwt_login_required
@permission_classes([IsAuthenticated])
def links(request):
    
    category = request.GET.get('category', '')
    links = Link.objects.filter(created_by=request.user)
    
    if category:
        try:
            category_obj = Category.objects.get(name=category, created_by=request.user)
            links = links.filter(category=category_obj)
            
        except Category.DoesNotExist:
            links = Link.objects.none()
    
    return render(request, 'link/links.html', {
        'links': links,
        'category': category,
    })



@require_http_methods(["GET", "POST"])
@jwt_login_required
@permission_classes([IsAuthenticated])
def create_link(request):

    # Обработка POST-запроса
    if request.method == 'POST':
        form = LinkForm(request.POST)
        if form.is_valid():
            link = form.save(commit=False)
            link.created_by = request.user
            link.save()
            return JsonResponse({'success': True, 'redirect': '/dashboard/'})
        return JsonResponse({'errors': form.errors}, status=400)

     # Обработка GET-запроса
    elif request.method == 'GET':
        form = LinkForm()
        form.fields['category'].queryset = Category.objects.filter(created_by=request.user)
        
        links_count = request.user.links.count()
        plan_max_links = request.user.plan.max_num_links if hasattr(request.user, 'plan') else 0
        
        return render(request, 'link/create_link.html', {
            'form': form,
            'title': 'Create link',
            'links_count': links_count,
            'plan_max_links': plan_max_links,
        })
    
    

@require_http_methods(["GET", "POST"])
@jwt_login_required
@permission_classes([IsAuthenticated])
def edit_link(request, pk):
    
    link = get_object_or_404(Link, created_by=request.user, pk=pk)
    
    if request.method == 'POST':
        form = LinkForm(request.POST, instance=link)
        
        if form.is_valid():
            link.save()
            return JsonResponse({'success': True, 'redirect': '/links/'})
        
    else:
         form = LinkForm(instance=link)   
         form.fields['category'].queryset = Category.objects.filter(created_by = request.user)
        
    return render(request, 'link/create_link.html', {
        'form': form,
        'title': 'Edit link',
        })
    


@require_http_methods(["GET"])
@jwt_login_required
@permission_classes([IsAuthenticated])
def delete_link(request, pk):
    
    link = get_object_or_404(Link, created_by=request.user, pk=pk)
    link.delete()
    
    return redirect('/links/')




#CATEGORIES
@require_http_methods(["GET"])
@jwt_login_required
@permission_classes([IsAuthenticated])
def categories(request):

    categories = Category.objects.filter(created_by=request.user)

    return render(request, 'link/categories.html', {
        'categories': categories,
    })
    
    

@require_http_methods(["GET", "POST"])
@jwt_login_required
@permission_classes([IsAuthenticated])
def create_category(request):

    if request.method == 'POST':
        form = CategoryForm(request.POST)
        
        if form.is_valid():
            category = form.save(commit=False)
            category.created_by = request.user
            category.save()
            
            return HttpResponseRedirect('/dashboard/')
        
    form = CategoryForm()   
    return render(request, 'link/create_category.html', {
        'form': form,
        'title': 'Create category',
        })


# @login_required
# def create_category(request):
#     if request.method == 'POST':
#         form = CategoryForm(request.POST)
        
#         if form.is_valid():
#             category = form.save(commit=False)
#             category.created_by = request.user
#             category.save()
            
#             return redirect('/dashboard/')
#     else:
#          form = CategoryForm()   
        
#     return render(request, 'link/create_category.html', {
#         'form': form,
#         'title': 'Create category',
#         })
    
    
    
@require_http_methods(["GET", "POST"])
@jwt_login_required
@permission_classes([IsAuthenticated])
def edit_category(request, pk):
    
    category = get_object_or_404(Category, created_by=request.user, pk=pk)
    
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        
        if form.is_valid():
            form.save()
            
            return redirect('/links/categories/')
    else:
        form = CategoryForm(instance=category)
    
    return render(request, 'link/create_category.html', {
        'form': form,
        'title': 'Edit Category',
        })



@require_http_methods(["GET"])
@jwt_login_required
@permission_classes([IsAuthenticated])
def delete_category(request, pk):
    
    category = get_object_or_404(Category, created_by=request.user, pk=pk)
    category.delete()
    
    return redirect('/links/categories/')



# SUBSCRIPTION 
@require_http_methods(["GET"])
@jwt_login_required
@permission_classes([IsAuthenticated])
def subscription(request):
    
    plan = request.user.plan
    sub = request.user.sub_status
    # plan = User.objects.get(plan_id=request.user)
    # sub = get_object_or_404(User, sub_status=request.user)
    # plan = get_object_or_404(User, plan_id=request.user)
    print(plan)
    return render(request, 'link/subscription.html', {
        'plan': plan,
        'sub': sub,
    })


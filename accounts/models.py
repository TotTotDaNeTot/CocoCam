from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager

from djstripe.models import Customer, Subscription




class Role(models.Model):
    title = models.CharField(max_length=100, verbose_name='Роль', 
                             default=None, null=False)
    
    def __str__(self):
        return f'{self.title}'
    
    class Meta:
        verbose_name = 'Роль'
        verbose_name_plural = 'Роли'



class Plan(models.Model):
    name = models.CharField(max_length=255)
    max_num_links = models.IntegerField()
    
    def __str__(self):
        return self.name



class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=30, unique=True, blank=False)
    email = models.EmailField(unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    
    sub_status = models.CharField(max_length=255, null=True, blank=True) 
    
    role = models.ForeignKey(Role, on_delete=models.PROTECT, null=True, 
                             default=None, blank=True, verbose_name='Роль')
    
    plan = models.ForeignKey(Plan, related_name='users', 
                             default=1, on_delete=models.CASCADE)
    
    customer = models.ForeignKey(Customer, null=True, blank=True, on_delete=models.SET_NULL)
    subscription = models.ForeignKey(Subscription, null=True, blank=True,on_delete=models.SET_NULL)

    
    # is_verified = models.BooleanField(default=False)

        
    objects = CustomUserManager()
    
    # EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        unique_together = ['username', 'email']
    
    def __str__(self):
        return f'{self.email}'
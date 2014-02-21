from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.TextField(blank=True, null=True)
    expiration = models.DateField()
    manager = models.ForeignKey(User, related_name='product_manager')
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='created_products', blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, related_name='updated_products', blank=True, null=True)
    def __unicode__(self):
        return self.name
    
class Project(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField(blank=True, null=True)
    product = models.ForeignKey(Product, blank=True, null=True)
    participants = models.ManyToManyField(User, related_name='project_participants')
    expiration = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='created_project', blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, related_name='updated_project', blank=True, null=True)
    
    def __unicode__(self):
        return self.name
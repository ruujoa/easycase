from django.db import models
from django.contrib.auth.models import User
from products.models import Project

# Create your models here.
class Page(models.Model):
    name = models.CharField(max_length=30)
    project = models.ForeignKey(Project, blank=True, null=True)
    created_by = models.ForeignKey(User, related_name='created_pages', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, related_name='updated_pages', blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return self.name
    
class ElementType(models.Model):
    name = models.CharField(max_length=10)
    
    def __unicode__(self):
        return self.name
    
class LocatorType(models.Model):
    name = models.CharField(max_length=10)
    
    def __unicode__(self):
        return self.name
    
class Element(models.Model):
    page = models.ForeignKey(Page, blank=True, null=True)
    name = models.CharField(max_length=30)
    type = models.ForeignKey(ElementType)
    locator = models.CharField(max_length=100)
    locatorType = models.ForeignKey(LocatorType)
    created_by = models.ForeignKey(User, related_name='created_elements', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, related_name='updated_elements', blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return self.name

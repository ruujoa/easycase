from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Task(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.TextField(blank=True, null=True)
    schedule = models.CharField(max_length=30, blank=True, null=True)
    after_trigger = models.ForeignKey('self', blank=True, null=True)
    last_success = models.CharField(max_length=30, blank=True, null=True)
    last_failure = models.CharField(max_length=30, blank=True, null=True)
    last_duration = models.CharField(max_length=30, blank=True, null=True)
    created_by = models.ForeignKey(User, related_name='created_task', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, related_name='updated_task', blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=30, blank=True, null=True)
    operator = models.CharField(max_length=30, blank=True, null=True)
    cases_set = models.FilePathField()
    
    def __unicode__(self):
        return self.name
'''
Created on 2013-8-30

@author: luyao
'''
from django.forms import ModelForm
from pages.models import Page, Element
from products.models import Project
from django.forms import TextInput
from django.forms.widgets import Select
from django import forms
from django.utils.datastructures import MultiValueDictKeyError
import re
from django.conf import settings

pattern = re.compile(settings.REGEXP)

class PageForm(ModelForm):
    class Meta:
        model = Page
        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 
                                     'id': 'name',
                                     'placeholder': 'Enter Name'}),
        }
    def clean_name(self):
        name = self.cleaned_data['name']
        if not pattern.match(name):
            raise forms.ValidationError('Please enter 2-30 characters,' 
                "\"A-Z, a-z, 0-9, _, -, ., \" are valid." )
        project_id = ''
        try:
            project_id = self.data['project_id']
        except MultiValueDictKeyError:
            return name
        pages = Page.objects.filter(name__exact=name)
        pages = pages.filter(project_id__exact=project_id)
        project = Project.objects.get(id=project_id)
        if pages:
            raise forms.ValidationError('There is already a page that has same name in the project named %s'
                                        % project)
        return name

class ElementForm(ModelForm):
    class Meta:
        model = Element
        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 
                                     'id': 'name',
                                     'placeholder': 'Enter Name'}),
            'locator': TextInput(attrs={'class': 'form-control',
                                        'id': 'locator',
                                        'placeholder': 'Enter Locator'}),
            'type': Select(attrs={'class': 'form-control',
                                  'id': 'type'}),
            'locatorType': Select(attrs={'class': 'form-control',
                                         'id': 'locatorType'})
        }
    def clean_name(self):
        name = self.cleaned_data['name']
        if not pattern.match(name):
            raise forms.ValidationError('Please enter 2-30 characters,' 
                "\"A-Z, a-z, 0-9, _, -, ., \" are valid." )
        page_id = ''
        try:
            page_id = self.data['page_id']
        except MultiValueDictKeyError:
            return name
        page = Page.objects.get(id=page_id)
        elements = Element.objects.filter(name__exact=name)
        elements = elements.filter(page_id__exact=page_id)
        if elements:
            raise forms.ValidationError('There is already a element that has same name in the page named %s'
                                        % page)
        return name
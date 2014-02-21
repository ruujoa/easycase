from django.forms import ModelForm
from products.models import Product, Project
from django.forms import TextInput,DateInput
from django.forms.widgets import Textarea, Select, SelectMultiple
from django import forms
from django.utils.datastructures import MultiValueDictKeyError
import datetime
import re
from django.conf import settings

pattern = re.compile(settings.REGEXP)

class ProductForm(ModelForm):
    class Meta:
        model = Product
        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 
                                     'id': 'name',
                                     'placeholder': 'Enter Name'}),
            'description': Textarea(attrs={'class': 'form-control',
                                            'id': 'description',
                                            'rows': 3}),
            'manager': Select(attrs={'class': 'form-control',
                                     'id': 'manager'}),
            'expiration': DateInput(attrs={'class': 'form-control',
                                           'id': 'expiration'}),
        }
    def clean_name(self):
        name = self.cleaned_data['name']
        if not name:
            raise forms.ValidationError('This field is required.')
        if not pattern.match(name):
            raise forms.ValidationError('Please enter 2-30 characters,' 
                "\"A-Z, a-z, 0-9, _, -, ., \" are valid." )
        return name
    def clean_expiration(self):
        expiration = self.cleaned_data['expiration']
        if expiration <= datetime.date.today() + datetime.timedelta(days=10):
            raise forms.ValidationError('Please set the expiration to at least 10 days later.')
        return expiration

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 
                                     'id': 'name',
                                     'placeholder': 'Enter Name'}),
            'description': Textarea(attrs={'class': 'form-control',
                                            'id': 'description',
                                            'rows': 3}),
            'expiration': DateInput(attrs={'class': 'form-control',
                                           'id': 'expiration'}),
            'participants': SelectMultiple(attrs={'class': 'form-control',
                                        'id': 'participants'}),
        }
     
    def clean_expiration(self):
        expiration = self.cleaned_data['expiration']
        product_name = self.data['product_name']
        product = Product.objects.get(name=product_name)
        
        if expiration > product.expiration:
            raise forms.ValidationError('The expiration of the project can not be later than the product that it belongs to.')
        return expiration
    
    def clean_name(self):
        name = self.cleaned_data['name']
        if not name:
            raise forms.ValidationError('This field is required.')
        if not pattern.match(name):
            raise forms.ValidationError('Please enter 2-30 characters,' 
                "\"A-Z, a-z, 0-9, _, -, ., \" are valid." )
        project_id = ''
        try:
            product_id = self.data['product_id']
        except MultiValueDictKeyError:
            return name
        projects = Project.objects.filter(name__exact=name)
        projects = projects.filter(product_id__exact=product_id)
        product = Product.objects.get(id=product_id)
        if projects:
            raise forms.ValidationError('There is already a project that has same name in the product named %s'
                                        % product )
        return name

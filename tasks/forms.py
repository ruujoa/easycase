from django.forms import ModelForm
from tasks.models import *
from django.forms import TextInput
from django.forms.widgets import Textarea, Select, ClearableFileInput
from django.conf import settings
from django import forms
import re
import string

pattern = re.compile(settings.REGEXP)

class TaskForm(ModelForm):
    class Meta:
        model = Task
        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 
                                     'id': 'name',
                                     'placeholder': 'Enter Name'}),
            
            'description': Textarea(attrs={'class': 'form-control',
                                           'id': 'description',
                                           'rows': 3}),
            
            'schedule': TextInput(attrs={'class': 'form-control',
                                         'id': 'schedule',
                                         'data-placement': 'right',
                                         'data-trigger': 'focus',
                                         'data-html': 'true',
                                         'data-container': 'body',
                                         'data-content': 'This field follows the syntax of' 
                                         'cron (with minor differences). Specifically,' 
                                         'each line consists of 5 fields separated by TAB or whitespace:<br/>'
                                         '<strong>MINUTE HOUR DOM MONTH DOW</strong>'
                                         '<ul><li>MINUTE    Minutes within the hour (0-59)</li>'
                                         '<li>HOUR    The hour of the day (0-23)</li>'
                                         '<li>DOM    The day of the month (1-31)</li>'
                                         '<li>MONTH    The month (1-12)</li>'
                                         '<li>DOW    The day of the week (0-7) where 0 and 7 are Sunday.</li></ul>'
                                         'Example<br/># every minute<br/>'
                                         '* * * * *<br/>'
                                         '# every 5 mins past the hour<br/>'
                                         '5 * * * *'}),
            
            'after_trigger': Select(attrs={'class': 'form-control',
                                           'id': 'after_trigger'}),
            
            'cases_set': Select(attrs={'class': 'form-control',
                                       'id': 'cases_set'}), 
        }
    
    def clean_name(self):
        name = self.cleaned_data['name']
        if not name:
            raise forms.ValidationError('This field is required.')
        if not pattern.match(name):
            raise forms.ValidationError('Please enter 2-30 characters,' 
                "\"A-Z, a-z, 0-9, _, -, ., \" are valid." )
        return name 
    
    def clean_schedule(self):
        pattern = re.compile(r'^((\d?\d|\*)\s){4}[\d\*]$')
        schedule = self.cleaned_data['schedule']
        items = schedule.split(' ')
        if not schedule:
            return schedule
        else:
            if not pattern.match(schedule):
                raise forms.ValidationError('Invalid format.')
            else:
                if items[0] != '*' and not (0 <= string.atoi(items[0]) <= 59):
                    raise forms.ValidationError('The first value overs the range: 0-59')
                if items[1] != '*' and not (0 <= string.atoi(items[1]) <= 23):
                    raise forms.ValidationError('The second value overs the range: 0-23')
                if items[2] != '*' and not (1 <= string.atoi(items[2]) <= 31):
                    raise forms.ValidationError('The third value overs the range: 1-31')
                if items[3] != '*' and not (1 <= string.atoi(items[3]) <= 12):
                    raise forms.ValidationError('The forth value overs the range: 1-12')
                if items[4] != '*' and not (0 <= string.atoi(items[4]) <= 7):
                    raise forms.ValidationError('The fifth value overs the range: 0-7')
                    
        return schedule 

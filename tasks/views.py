# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from tasks.models import *
from tasks.forms import TaskForm
import ConfigParser

'''
    Task's Actions
'''
@login_required
def index(request):
    tasks = Task.objects.all()
    config = ConfigParser.ConfigParser()
    config.read( request.user.get_username() + ".profile")
    limit = config.get("system", "rows_per_page")
    paginator = Paginator(tasks, limit)
    
    page = request.GET.get('page')
    try:
        tasks = paginator.page(page)
    except PageNotAnInteger:
        tasks = paginator.page(1)
    except EmptyPage:
        tasks = paginator.page(paginator.num_pages)
    context = {'tasks': tasks}
    return render(request,'tasks/index.html',context)

@login_required
def detail(request, task_id):
    task = get_object_or_404(Task,pk=task_id)
    return render(request, 'tasks/detail.html', {'task': task})

@login_required
def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            new_task = form.save(commit=False)
            new_task.last_success = 'N/A'
            new_task.last_failure = 'N/A'
            new_task.last_duration = 'N/A'
            new_task.operator = 'N/A'
            new_task.status = 'N/A'
            new_task.created_by = request.user
            new_task.updated_by = request.user
            if form.is_valid(): # All validation rules pass
                new_task.save()
                return HttpResponseRedirect('/tasks/') # Redirect after POST
    else:
        form = TaskForm() # An unbound form

    return render(request, 'tasks/create_task_form.html', {
        'form': form
    })
    
@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task,pk=task_id)
    old_value = task.created_by
    name = task.name
    if request.method == 'POST':
        form = TaskForm(request.POST,instance=task)
        if form.is_valid(): # All validation rules pass
            current_task = form.save(commit=False)
            current_task.name = name
            current_task.last_success = 'N/A'
            current_task.last_failure = 'N/A'
            current_task.last_duration = 'N/A'
            current_task.operator = 'N/A'
            current_task.status = 'N/A'
            current_task.created_by = old_value
            current_task.updated_by = request.user
            if form.is_valid():
                current_task.save()
                return HttpResponseRedirect('/tasks/') # Redirect after POST
    else:
        form = TaskForm(instance=task) # An bound form

    return render(request, 'tasks/edit_task_form.html', {
        'form': form, 'task': task,
    })

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    task.delete()
    return HttpResponseRedirect('/tasks/')
    
@login_required
def search_task(request):
    kw = request.GET.get('kw','')
    if kw:
        tasks = Task.objects.filter(name__icontains=kw)
    else:
        tasks = Task.objects.all()
    config = ConfigParser.ConfigParser()
    config.read( request.user.get_username() + ".profile")
    limit = config.get("system", "rows_per_page")
    paginator = Paginator(tasks, limit)
    
    page = request.GET.get('page')
    try:
        tasks = paginator.page(page)
    except PageNotAnInteger:
        tasks = paginator.page(1)
    except EmptyPage:
        tasks = paginator.page(paginator.num_pages)
    
    context = {'tasks': tasks, 'kw': kw}
    return render(request,'tasks/search_result.html',context) 

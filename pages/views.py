# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from pages.models import *
from pages.forms import PageForm, ElementForm
from products.models import Project
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
import ConfigParser

'''
    Page's Actions
'''
@login_required
def index(request, project_id):
    pages = Page.objects.filter(project_id=project_id)
    project = Project.objects.get(id=project_id)
    
    config = ConfigParser.ConfigParser()
    config.read( request.user.get_username() + ".profile")
    limit = config.get("system", "rows_per_page")
    paginator = Paginator(pages, limit)
    
    page = request.GET.get('page')
    try:
        pages = paginator.page(page)
    except PageNotAnInteger:
        pages = paginator.page(1)
    except EmptyPage:
        pages = paginator.page(paginator.num_pages)
        
    context = {'pages': pages, 'project': project}
    return render(request,'pages/index.html',context)

@login_required
def detail(request, project_id, page_id):
    page = get_object_or_404(Page,pk=page_id)
    return render(request, 'pages/detail.html', {'page': page, 'project_id': project_id})

@login_required
def create_page(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid(): # All validation rules pass
            new_page = form.save(commit=False)
            new_page.project = project
            new_page.created_by = request.user
            new_page.updated_by = request.user
            if form.is_valid():
                new_page.save()
                return HttpResponseRedirect('/pages/%s/' % project_id) # Redirect after POST
    else:
        form = PageForm() # An unbound form

    return render(request, 'pages/create_page_form.html', {
        'form': form,
        'project_id': project_id 
    })

@login_required
def delete_page(request, project_id, page_id):
    page = get_object_or_404(Page, pk=page_id)
    page.delete()
    return HttpResponseRedirect('/pages/%s/' % project_id)

@login_required
def search_page(request):
    kw = request.GET.get('kw', '')
    project_id = request.GET.get('project_id', '')
    project = Project.objects.get(id=project_id)
    pages = Page.objects.filter(project_id=project_id)
    if kw:
        pages = pages.filter(name__icontains=kw)
    
    config = ConfigParser.ConfigParser()
    config.read( request.user.get_username() + ".profile")
    limit = config.get("system", "rows_per_page")
    paginator = Paginator(pages, limit)

    page = request.GET.get('page')
    try:
        pages = paginator.page(page)
    except PageNotAnInteger:
        pages = paginator.page(1)
    except EmptyPage:
        pages = paginator.page(paginator.num_pages)
    
    context = {'pages': pages, 'project': project, 'kw': kw}
    return render(request,'pages/search_result.html',context)

'''
    Element's Actions
'''
@login_required
def element_index(request, project_id, page_id):
    elements = Element.objects.filter(page_id=page_id)
    page = Page.objects.get(id=page_id)
    
    config = ConfigParser.ConfigParser()
    config.read( request.user.get_username() + ".profile")
    limit = config.get("system", "rows_per_page")
    
    paginator = Paginator(elements, limit)
    
    total = request.GET.get('page')
    try:
        elements = paginator.page(total)
    except PageNotAnInteger:
        elements = paginator.page(1)
    except EmptyPage:
        elements = paginator.page(paginator.num_pages)
    
    context = {'elements': elements, 'page': page, 'project_id': project_id}
    return render(request, 'elements/index.html', context)

@login_required
def create_element(request, project_id, page_id):
    page = get_object_or_404(Page, pk=page_id)
    if request.method == 'POST':
        form = ElementForm(request.POST)
        if form.is_valid(): # All validation rules pass
            new_element = form.save(commit=False)
            new_element.page = page
            new_element.created_by = request.user
            new_element.updated_by = request.user
            if form.is_valid():
                new_element.save()
                return HttpResponseRedirect("/pages/%s/%s/elements/" % (project_id, page_id))
    else:
        form = ElementForm()
    return render(request, 'elements/create_element_form.html', {
        'form': form,
        'project_id': project_id,
        'page_id': page_id,
    }) 

@login_required
def edit_element(request, project_id, page_id ,element_id):
    page = get_object_or_404(Page,pk=page_id)
    element = get_object_or_404(Element,pk=element_id)
    old_value = element.created_by
    if request.method == 'POST':
        form = ElementForm(request.POST,instance=element)
        if form.is_valid(): # All validation rules pass
            current_element = form.save(commit=False)
            current_element.page = page
            current_element.created_by = old_value
            current_element.updated_by = request.user
            if form.is_valid():
                current_element.save()
                return HttpResponseRedirect('/pages/%s/%s/elements/' % (project_id, page_id)) # Redirect after POST
    else:
        form = ElementForm(instance=element) # An bound form

    return render(request, 'elements/edit_element_form.html', {
        'form': form, 'page': page, 'element': element, 'project_id': project_id,
    })

@login_required
def delete_element(request, project_id, page_id, element_id):
    element = get_object_or_404(Element, pk=element_id)
    element.delete()
    return HttpResponseRedirect("/pages/%s/%s/elements/" % (project_id, page_id))

@login_required
def search_element(request):
    kw = request.GET.get('kw', '')
    project_id = request.GET.get('project_id', '')
    page_id = request.GET.get('page_id', '')
    page = Page.objects.get(id=page_id)
    elements = Element.objects.filter(page_id=page_id)
    if kw:
        elements = elements.filter(name__icontains=kw)
    
    config = ConfigParser.ConfigParser()
    config.read( request.user.get_username() + ".profile")
    limit = config.get("system", "rows_per_page")
        
    paginator = Paginator(elements, limit)
    
    total = request.GET.get('page')
    try:
        elements = paginator.page(total)
    except PageNotAnInteger:
        elements = paginator.page(1)
    except EmptyPage:
        elements = paginator.page(paginator.num_pages)
    
    context = {'elements': elements, 'page': page, 'project_id': project_id, 'kw': kw}
    return render(request, 'elements/search_result.html', context)

'''
    Logout Action
'''
def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/")
    
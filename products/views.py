# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from products.models import *
from products.forms import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
import ConfigParser
import string

'''
    Product's Actions
'''

@login_required
def index(request):
    products = Product.objects.all()
    config = ConfigParser.ConfigParser()
    config.read( request.user.get_username() + ".profile")
    if config.has_section("system"):
        limit = config.get("system", "rows_per_page")
        print config.get("system", "session_timeout")
        request.session.set_expiry( 60 *
            string.atof(config.get("system", "session_timeout")))
    else:
        limit = 3
        request.session.set_expiry(1209600)
    paginator = Paginator(products, limit)

    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    context = {'products': products}
    return render(request,'products/index.html',context)

@login_required
def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            new_product = form.save(commit=False)
            new_product.created_by = request.user
            new_product.updated_by = request.user
            if form.is_valid(): # All validation rules pass
                new_product.save()
                return HttpResponseRedirect('/products/') # Redirect after POST
    else:
        form = ProductForm() # An unbound form

    return render(request, 'products/create_product_form.html', {
        'form': form
    })
    
@login_required
def detail(request, product_id):
    product = get_object_or_404(Product,pk=product_id)
    return render(request, 'products/detail.html', {'product': product})

@login_required
def delete_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    return HttpResponseRedirect('/products/')

@login_required
def edit_product(request,product_id):
    product = get_object_or_404(Product,pk=product_id)
    old_value = product.created_by
    name = product.name
    if request.method == 'POST':
        form = ProductForm(request.POST,instance=product)
        if form.is_valid(): # All validation rules pass
            current_product = form.save(commit=False)
            current_product.name = name
            current_product.created_by = old_value
            current_product.updated_by = request.user
            if form.is_valid():
                current_product.save()
                return HttpResponseRedirect('/products/') # Redirect after POST
    else:
        form = ProductForm(instance=product) # An bound form

    return render(request, 'products/edit_product_form.html', {
        'form': form, 'product': product,
    })
    
@login_required
def search_product(request):
    kw = request.GET.get('kw','')
    if kw:
        products = Product.objects.filter(name__icontains=kw)
    else:
        products = Product.objects.all()
    config = ConfigParser.ConfigParser()
    config.read( request.user.get_username() + ".profile")
    if config.has_section("system"):
        limit = config.get("system", "rows_per_page")
    else:
        limit = 3
    paginator = Paginator(products, limit)

    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    
    context = {'products': products, 'kw': kw}
    return render(request,'products/search_result.html',context)     
    
'''
    Project's Actions
'''
@login_required
def project_index(request, product_id):
    projects = Project.objects.filter(product_id=product_id)
    product = Product.objects.get(id=product_id)
    config = ConfigParser.ConfigParser()
    config.read( request.user.get_username() + ".profile")
    limit = config.get("system", "rows_per_page")
    paginator = Paginator(projects, limit)
    
    page = request.GET.get('page')
    try:
        projects = paginator.page(page)
    except PageNotAnInteger:
        projects = paginator.page(1)
    except EmptyPage:
        projects = paginator.page(paginator.num_pages)
    
    context = {'projects': projects, 'product': product}
    return render(request, 'projects/index.html', context)

@login_required
def detail_project(request, product_id, project_id):
    project = get_object_or_404(Project,pk=project_id)
    return render(request, 'projects/detail.html', {'project': project, 'product_id': product_id })

@login_required
def create_project(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid(): # All validation rules pass
            new_project = form.save(commit=False)
            new_project.product = product
            new_project.created_by = request.user
            new_project.updated_by = request.user
            if form.is_valid():
                new_project.save()
                form.save_m2m()
                return HttpResponseRedirect("/products/%s/projects/" % product_id)
    else:   
        form = ProjectForm()
    return render(request, 'projects/create_project_form.html', {
        'form': form,
        'product': product,
    })
    
@login_required
def delete_project(request, product_id, project_id):
    project = get_object_or_404(Project, pk=project_id)
    project.delete()
    return HttpResponseRedirect("/products/%s/projects/" % product_id)

@login_required
def edit_project(request, product_id , project_id):
    product = get_object_or_404(Product,pk=product_id)
    project = get_object_or_404(Project,pk=project_id)
    old_value = project.created_by
    name = project.name
    if request.method == 'POST':
        form = ProjectForm(request.POST,instance=project)
        if form.is_valid(): # All validation rules pass
            current_project = form.save(commit=False)
            current_project.product = product
            current_project.created_by = old_value
            current_project.updated_by = request.user
            if form.is_valid():
                current_project.save()
                form.save_m2m()
                return HttpResponseRedirect('/products/%s/projects/' % product_id) # Redirect after POST
        else:
            print form.errors
    else:
        form = ProjectForm(instance=project) # An bound form

    return render(request, 'projects/edit_project_form.html', {
        'form': form, 'product': product, 'project': project,
    })
    
@login_required
def search_project(request):
    kw = request.GET.get('kw', '')
    product_id = request.GET.get('product_id', '')
    projects = Project.objects.filter(product_id=product_id)
    if kw:
        projects = projects.filter(name__icontains=kw)
    
    config = ConfigParser.ConfigParser()
    config.read( request.user.get_username() + ".profile")
    limit = config.get("system", "rows_per_page")    
    paginator = Paginator(projects, limit)
    
    page = request.GET.get('page')
    try:
        projects = paginator.page(page)
    except PageNotAnInteger:
        projects = paginator.page(1)
    except EmptyPage:
        projects = paginator.page(paginator.num_pages)
    
    product = Product.objects.get(id=product_id)
    context = {'projects': projects, 'product': product, 'kw': kw}
    return render(request, 'projects/search_result.html', context)

@login_required
def upload_file(request):
    data = request.POST.get('data')
    filename = request.user.get_username() + '.profile'
    f = open(filename, 'wb')
    f.write(data)
    f.close()
    return HttpResponseRedirect('/products/')
    
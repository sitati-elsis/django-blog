from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.contrib.auth.decorators import login_required

from blog.models import Post
from blog.forms import UserForm, PostForm

# Create your views here.
def sign_in(request):
    context = {
        'form': UserForm()
    }
    if request.method == 'GET':
        return render(request, 'sign_in.html', context=context)

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        # user = authenticate(username='elsis', password='password')
        if user is not None:
            login(request, user)
            
            posts = Post.objects.filter(author=request.user)
            return redirect('posts_list')
        else:  
            messages.error(request, 'Incorrect username/password.')
            return render(request, 'sign_in.html', context=context)


@login_required
def logout_view(request):
    logout(request)
    return redirect('sign_in')

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, "Successfully Created")
            # return HttpResponseRedirect(post.get_absolute_url())
            return redirect('posts_list')

    if request.method == "GET":
        context = {
            "form": PostForm()
        }
        return render(request, "post_form.html", context)


@login_required
def list_post(request):
    posts = Post.objects.filter(author=request.user)
    
    query = request.GET.get("q")
    if query:
        posts = posts.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(author__username__icontains=query) 
            ).distinct()
    paginator = Paginator(posts, 5)
    
    page = request.GET.get('page') or 1
    
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset = paginator.page(paginator.num_pages)

    context = {
        "posts": queryset
    }
    return render(request, "posts_list.html", context)


@login_required
def post_detail(request, pk=None):
    post = get_object_or_404(Post, pk=pk)
    context = {
        "post": post
    }
    return render(request, "post_detail.html", context)


@login_required
def update_post(request, pk=None):
    post = get_object_or_404(Post, pk=pk)

    form = PostForm(request.POST or None, instance=post)
    if form.is_valid():
        post = form.save(commit=False)
        post.save()
        messages.success(request, "Successfully Edited")
        return redirect('posts_list')
    else:
        messages.error(request, "Error in Editing Post")
        context = {
            "form": form,
        }
    return render(request, "post_update.html", context)


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.paginator import Paginator
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
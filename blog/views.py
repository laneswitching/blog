from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from .forms import PostForm, CustomUserCreationForm
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm

def post_list(request):
    posts = Post.objects.all()  # Fetch all Post objects
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form, 'is_new': True})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            # Optionally update published_date on edit
            # post.published_date = now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form, 'is_new': False})


#delete view with error handling
@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        try:
            post.delete()
            messages.success(request, "Post deleted successfully.")
            return redirect('post_list')
        except Exception as e:
            messages.error(request, f"Error deleting post: {e}")
            return render(request, 'blog/post_confirm_delete.html', {'post': post})
    return render(request, 'blog/post_confirm_delete.html', {'post': post})

def about(request):
    return render(request, 'blog/about.html')

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('post_list')
    else:
        form = AuthenticationForm()
    return render(request, 'blog/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('post_list')

def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful. You can now log in.")
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'blog/register.html', {'form': form})

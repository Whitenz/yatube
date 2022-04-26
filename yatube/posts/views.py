from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CommentForm, PostForm
from .models import Follow, Group, Post, User


def index(request):
    posts_list = Post.objects.select_related(
        'group', 'author'
    ).all()
    paginator = Paginator(posts_list, settings.OBJECTS_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    template = 'posts/index.html'
    context = {
        'page_obj': page_obj,
        'index': True,
    }
    return render(request, template, context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts_list = group.posts.all()
    paginator = Paginator(posts_list, settings.OBJECTS_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    template = 'posts/group_list.html'
    context = {
        'group': group,
        'page_obj': page_obj,
    }
    return render(request, template, context)


def profile(request, username):
    profile = get_object_or_404(User, username=username)
    posts_list = profile.posts.select_related('group').all()
    paginator = Paginator(posts_list, settings.OBJECTS_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    template = 'posts/profile.html'
    context = {
        'page_obj': page_obj,
        'profile': profile,
        'following': (
            request.user.is_authenticated and profile.following.filter(
                user=request.user
            ).exists()
        )
    }
    return render(request, template, context)


def post_detail(request, post_id):
    query = Post.objects.select_related(
        'group', 'author'
    )
    post = get_object_or_404(query, id=post_id)
    comments = post.comments.all()
    form = CommentForm()
    template = 'posts/post_detail.html'
    context = {
        'post': post,
        'form': form,
        'comments': comments,
    }
    return render(request, template, context)


@login_required
def post_create(request):
    form = PostForm(
        request.POST or None,
        files=request.FILES or None
    )

    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('posts:profile', request.user.username)

    template = 'posts/create_post.html'
    context = {
        'form': form,
    }
    return render(request, template, context)


@login_required
def post_edit(request, post_id):
    query = Post.objects.select_related('author')
    post = get_object_or_404(query, id=post_id)

    if post.author != request.user:
        return redirect('posts:post_detail', post_id)

    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
        instance=post
    )

    if form.is_valid():
        form.save()
        return redirect('posts:post_detail', post_id)

    template = 'posts/create_post.html'
    context = {
        'form': form,
        'is_edit': True,
        'post': post,
    }
    return render(request, template, context)


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('posts:post_detail', post_id=post_id)


@login_required
def follow_index(request):
    user = request.user
    posts_list = Post.objects.select_related(
        'author', 'group'
    ).filter(
        author__following__user=user
    )
    paginator = Paginator(posts_list, settings.OBJECTS_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    template = 'posts/follow.html'
    context = {
        'page_obj': page_obj,
        'follow': True
    }
    return render(request, template, context)


@login_required
def profile_follow(request, username):
    profile = get_object_or_404(User, username=username)
    if request.user != profile:
        Follow.objects.get_or_create(user=request.user, author=profile)
    return redirect('posts:profile', username)


@login_required
def profile_unfollow(request, username):
    get_object_or_404(
        Follow,
        user=request.user,
        author__username=username
    ).delete()
    return redirect('posts:profile', username)


@login_required
def post_delete(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user == post.author:
        post.delete()
        return redirect('posts:profile', request.user.username)
    else:
        return redirect('posts:index')

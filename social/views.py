from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Post, Like, Comentario


def home(request):
    posts = Post.objects.all().order_by('-fecha')

    liked_posts = []

    if request.user.is_authenticated:
        likes = Like.objects.filter(usuario=request.user)
        liked_posts = [like.post.id for like in likes]

    return render(request, 'social/home.html', {
        'posts': posts,
        'liked_posts': liked_posts
    })


@login_required
def crear_post(request):
    if request.method == "POST":
        contenido = request.POST['contenido']

        Post.objects.create(
            usuario=request.user,
            contenido=contenido
        )

    return redirect('home')


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()

    return render(request, 'registration/register.html', {'form': form})


def perfil(request, username):
    usuario = get_object_or_404(User, username=username)
    posts = Post.objects.filter(usuario=usuario).order_by('-fecha')

    return render(request, 'social/perfil.html', {
        'usuario': usuario,
        'posts': posts
    })


@login_required
def mi_perfil(request):
    usuario = request.user
    posts = Post.objects.filter(usuario=usuario).order_by('-fecha')

    return render(request, 'social/perfil.html', {
        'usuario': usuario,
        'posts': posts
    })


@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    like, created = Like.objects.get_or_create(
        usuario=request.user,
        post=post
    )

    if not created:
        like.delete()

    return redirect('home')

@login_required
def crear_comentario(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == "POST":
        contenido = request.POST['contenido']

        Comentario.objects.create(
            usuario=request.user,
            post=post,
            contenido=contenido
        )

    return redirect('home')
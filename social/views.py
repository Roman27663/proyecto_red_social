from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Post, Like, Comentario, Profile, Follow


def home(request):
    liked_posts = []
    filtro = request.GET.get('filtro', 'siguiendo')

    if request.user.is_authenticated:
        likes = Like.objects.filter(usuario=request.user)
        liked_posts = [like.post.id for like in likes]

        if filtro == 'global':
            posts = Post.objects.all().order_by('-fecha')

        else:  # siguiendo
            following_users = Follow.objects.filter(
                follower=request.user
            ).values_list('followed', flat=True)

            posts = Post.objects.filter(
                usuario__in=list(following_users) + [request.user.id]
            ).order_by('-fecha')

    else:
        posts = Post.objects.all().order_by('-fecha')

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

    is_following = False

    if request.user.is_authenticated:
        is_following = Follow.objects.filter(
            follower=request.user,
            followed=usuario
        ).exists()

    followers_count = Follow.objects.filter(followed=usuario).count()
    following_count = Follow.objects.filter(follower=usuario).count()

    return render(request, 'social/perfil.html', {
        'usuario': usuario,
        'posts': posts,
        'is_following': is_following,
        'followers_count': followers_count,
        'following_count': following_count
    })


@login_required
def mi_perfil(request):
    usuario = request.user
    posts = Post.objects.filter(usuario=usuario).order_by('-fecha')

    followers_count = Follow.objects.filter(followed=usuario).count()
    following_count = Follow.objects.filter(follower=usuario).count()

    return render(request, 'social/perfil.html', {
        'usuario': usuario,
        'posts': posts,
        'followers_count': followers_count,
        'following_count': following_count
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


@login_required
def editar_perfil(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        profile.bio = request.POST['bio']
        profile.save()
        return redirect('mi_perfil')

    return render(request, 'social/editar_perfil.html', {
        'profile': profile
    })


@login_required
def follow_toggle(request, username):
    user_to_follow = get_object_or_404(User, username=username)

    if user_to_follow == request.user:
        return redirect('perfil', username=username)

    follow, created = Follow.objects.get_or_create(
        follower=request.user,
        followed=user_to_follow
    )

    if not created:
        follow.delete()

    return redirect('perfil', username=username)
from django.shortcuts import render, redirect
from .models import Post
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


def home(request):
    posts = Post.objects.all().order_by('-fecha')
    return render(request, 'social/home.html', {'posts': posts})


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
    usuario = User.objects.get(username=username)
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
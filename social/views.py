from django.shortcuts import render, redirect
from .models import Post
from django.contrib.auth.decorators import login_required

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
from django.shortcuts import render,  redirect
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

# Create your views here.
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'usuarios/login.html', {'erro': 'Usuário ou senha inválidos'})
    return render(request, 'usuarios/login.html')



def cadastro(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, "As senhas não coincidem.")
            return render(request, 'usuarios/cadastro.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Nome de usuário já está em uso.")
            return render(request, 'usuarios/cadastro.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Já existe uma conta com este e-mail.")
            return render(request, 'usuarioscadastro.html')

        User.objects.create_user(username=username, email=email, password=password1)
        return redirect('/login/')

    return render(request, 'usuarios/cadastro.html')


def logout_view(request):
    logout(request)
    return redirect('home')  

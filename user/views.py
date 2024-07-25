from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render

from user.forms import FormularioRegistro, UpdateFormulario


# Pagina de apresentação
def index(request):
    return render(request, "global/index.html")

# Pagina do sistema apos usuario logar
def sistema(request):
    return render(request, "global/sistema.html")

# Cadastro de novos usuarios
def cadastro(request):
    if request.method == 'POST':
        form = FormularioRegistro(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Usuário criado com sucesso.")
            return redirect('login')
        else:
            messages.error(request, "Erro ao criar o usuário.")
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Erro no campo {field}: {error}")
    else:
        form = FormularioRegistro()

    return render(request, "usuarios/cadastro.html", {'form': form})

# Login de Usuarios cadastrados.
def login_view(request):
    form = AuthenticationForm(request)

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        
        if form.is_valid():
            user = form.get_user()
            auth.login(request, user)
            messages.success(request, 'Logado com sucesso!')
            return redirect('sistema')
        messages.error(request, 'Login inválido')
    
    return render(request, 
                    'usuarios/login.html',
            {
            'form': form
            }
        )

@login_required
def user_update(request):
    if request.method == 'POST':
        form = UpdateFormulario(request.POST, instance=request.user)
        if form.is_valid():
            if form.has_changed():  # Verifica se houve mudanças
                form.save()
                messages.success(request, 'Perfil atualizado com sucesso.')
            else:
                messages.info(request, 'Nenhuma alteração foi feita.')
            return redirect('sistema')
        else:
            messages.error(request, 'Erro ao atualizar o perfil.')
    else:
        form = UpdateFormulario(instance=request.user)

    return render(request, 'usuarios/update.html', {'form': form})

# logout de usuarios
def logout_view(request):
    auth.logout(request)
    return redirect('index')

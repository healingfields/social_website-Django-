from django.shortcuts import render
from django.contrib.auth import login, authenticate
from .forms import LoginForm, RegisterForm
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


def user_login(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                    username = cd['username'],
                                    password = cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('authenticated')
                else:
                    return HttpResponse('disabled account')
            else:
                return HttpResponse('Invalid login')
    return render(request, 'account/login.html', {'form': form})

@login_required()
def dashboard(request):
    return render(request, "account/dashboard.html", {'section': 'dashboard'})

def register(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(
                form.cleaned_data['password']
            )
            user.save()
            return render(request, 'account/register_done.html', {'user': user})
    return render(request, 'account/register.html', {'form': form})

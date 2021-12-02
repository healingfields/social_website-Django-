from django.shortcuts import render
from django.contrib.auth import login, authenticate
from .forms import LoginForm, RegisterForm, UserEditForm, ProfileEditForm
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Profile


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
            Profile.objects.create(user=user)
            return render(request, 'account/register_done.html', {'user': user})
    return render(request, 'account/register.html', {'form': form})

@login_required()
def edit(request):
    user_form = UserEditForm()
    profile_form = ProfileEditForm()
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST,
                                 )
        profile_form = ProfileEditForm(instance=request.user.profile,
                                       data = request.POST,
                                       files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
    return render(request, 'account/edit.html', {
        'user_form':user_form,
        'profile_form':profile_form
    })

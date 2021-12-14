from django.shortcuts import get_object_or_404, render
from django.contrib.auth import login, authenticate

import actions
from .forms import LoginForm, RegisterForm, UserEditForm, ProfileEditForm
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Profile, Contact
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
from common.decorators import ajax_required
from actions.utils import create_action 
from actions.models import Action




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
    actions = Action.objects.exclude(user=request.user)
    following_ids = request.user.following.values_list('id', flat=True)
    print(following_ids)
    if following_ids:
        actions = actions.filter(user_id__in=following_ids)
        actions = actions.select_related('user','user__profile')\
            .prefetch_related('target')[:10]
    
    return render(request, "account/dashboard.html", {'section': 'dashboard', 'actions':actions})

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
            create_action(user, 'has created an account')
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
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Error updating your profile')
    return render(request, 'account/edit.html', {
        'user_form':user_form,
        'profile_form':profile_form
    })

@login_required
def user_list(request):
    users = User.objects.filter(is_active=True)
    return render(request,
                    'account/user/list.html',
                    {'section':'people',
                    'users':users})

@login_required
def user_detail(request, username):
    user = get_object_or_404(User,
                            username=username,
                            is_active=True)
    return render(request,
                'account/user/detail.html',
                {'section':'people',
                'user':user})

@ajax_required
@require_POST
@login_required
def user_follow(request):
    user_id = request.POST.get('id')
    action = request.POST.get('action')
    if user_id and action :
        try:
            user = User.objects.get(id=user_id)
            if action == 'follow':
                Contact.objects.get_or_create(
                    user_from = request.user,
                    user_to = user
                )
                create_action(request.user, 'is following', user)
            else:
                Contact.objects.filter(user_from=request.user,
                                        user_to = user).delete()
            return JsonResponse({'status':'ok'})
        except User.DoesNotExist:
            return JsonResponse({'status':'error'})
    return JsonResponse({'status':'error'})
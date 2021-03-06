from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Profile
from .forms import UserEditFroms, ProfileEditForm


def register(request):

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        
        if form.is_valid():
            if form.cleaned_data['password1'] == form.cleaned_data['password2']:
                new_user = form.save()
                profile = Profile.objects.create(user=new_user)
                username = form.cleaned_data['username']
                password = form.cleaned_data['password1']
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('index')
                else:
                    return redirect('login')
    
    else:
        logout(request)
        form = UserCreationForm
    context = {'form':form}
    return render(request,'registration/register.html',context)





@login_required
def edit(request):
    if request.method == 'POST':
        user_form  = UserEditFroms(instance = request.user,
        data = request.POST)
        profile_form = ProfileEditForm(instance = request.user.profile,
        data = request.POST,
        files = request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('index')
        else:
            messages.error(request, 'Error updating profile')
    else:
        user_form = UserEditFroms(instance=request.user)
        profile_form = ProfileEditForm(instance= request.user.profile)
    context = {'user_form': user_form, 'profile_form':profile_form}
    return render(request, 'account/edit.html',context)


@login_required
def user_list(request):
    users = User.objects.filter(is_activate=True)
    context = { 'section':'people', 'users':users}

    return render(request, 'account/user/list.html',context)


@login_required
def user_detail(request,username):
    user = get_object_or_404(User,username=username, is_active=True)
    context = { 'section':'people', 'users':users}

    return render(request, 'account/user/detail.html',context)
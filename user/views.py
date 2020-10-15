from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404, JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, PasswordResetForm
from django.contrib.auth.forms import SetPasswordForm
from .models import UserProfile, PassReset
from rest_framework import generics
from .serializers import UserProfileSerializer

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created!')
            return redirect('login')
    else:
        form = UserRegisterForm()

    return render(request, 'user/register.html', {'form': form})

'''
Register a user from an existing profile object
Someone already has a qr code given to them from a museum admin
'''
def registerFromProfile(request, qr_token):
    profile = get_object_or_404(UserProfile, qr_token=qr_token)
    if profile.user is None:
      ##Profile hasn't been registeres yet
        if request.method == 'POST':
            form = UserRegisterForm(request.POST)
            if form.is_valid():
                form.instance.userprofile = profile  
        ##checks if there is alrady a profile, and assigns1, instead of crating one
                form.save()
                messages.success(request, f'Account created!')
                return redirect('login')
        else:
            form = UserRegisterForm()
        return render(request, 'user/register.html', {'form': form})
    else:
        if request.user.is_authenticated:
            return redirect('profile')
        else:
            return redirect('login')

@login_required
def profile(request):   
    ##form a form for modifying a user profile
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, instance=request.user.userprofile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Account updated')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.userprofile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'user/profile.html', context)

def password_reset(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'user/password_reset_done.html')
        else:
            messages.warning(request, 'email does not exist')
    
    form = PasswordResetForm()
    context = {'form': form}
    return render(request, 'user/password_reset.html', context)

def new_password(request, token):
    if request.method == 'POST':
        reset = get_object_or_404(PassReset, code=token)
        form = SetPasswordForm(reset.user, request.POST)
        if form.is_valid():
            form.save()
            reset.used = True
            reset.save()
            return redirect('login')
        else:
            return redirect('home')
    else:
        reset = get_object_or_404(PassReset, code=token)
        if reset.is_valid():
            form = SetPasswordForm(reset.user)
            context = {'form': form}
            return render(request, 'user/password_reset_confirm.html', context)

def confirm_account(request, token):
    profile = get_object_or_404(UserProfile, confirm_token=token)
    if profile.is_confirmed:
        messages.success(request, 'account already confirmed')
        return redirect('home')
    else:
        profile.is_confirmed = True
        profile.save()
        messages.success(request, 'account confirmed')
        return redirect('home')

def get_user_info(request, qr_token):
    profile = get_object_or_404(UserProfile, qr_token=qr_token)
    serializer = UserProfileSerializer(profile)
    return JsonResponse(serializer.data, safe=False)


from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect
from simulator import mail

def confirmation_required(func):
    @login_required
    def wrapper(request, *args, **kwargs):
        if request.user.userprofile.is_confirmed:
            return func(request, *args, **kwargs)
        else:
            mail.send_confirm_email(request.user.email, request.user.userprofile.confirm_token)
            messages.warning(request, 'account unconfirmed, confirmation email sent')
            return redirect('home')
    return wrapper
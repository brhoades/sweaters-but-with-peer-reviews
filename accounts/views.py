from django.shortcuts import render
from django.contrib.auth import logout
from django.shortcuts import redirect
from .models import UserProfile
from django.contrib.auth.models import User
from django.utils import timezone
from django.template import loader, RequestContext
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.

def email_sent(request):
    messages.info(request, "You have been sent an activation email. Please click the included link to activate your account.")
    return redirect("home")
def register_confirm(request, activation_key):
    #check if user is already logged in and if he is log him out
    if request.user.is_authenticated():
        logout(request)

    # check if there is UserProfile which matches the activation
    try:
        user_profile = UserProfile.objects.get(activation_key=activation_key)
    except ObjectDoesNotExist:
        messages.info(request, "Invalid activation link.")
        return redirect("home")


    #check if the activation key has expired, if it hase then render confirm_expired.html
	# if the user is active, then the
    user = user_profile.user
    if user_profile.key_expires < timezone.now() and not user.is_active:
        user.delete()
        messages.info(request, "This registration email has expired.")
        return redirect("home")

	#if the key hasn't expired save user, remove the activation key, set him as active, and render the confirm activation tempate
    user.is_active = True
    user.save()
    user_profile.activation_key=None
    user_profile.save()

    messages.info(request, "Successfully confirmed account.")
    return redirect("home")

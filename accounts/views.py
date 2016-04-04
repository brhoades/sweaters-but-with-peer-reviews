from django.shortcuts import render
from django.contrib.auth import logout
from django.shortcuts import render_to_response, get_object_or_404
from .models import UserProfile
from django.contrib.auth.models import User
from django.utils import timezone
from django.template import loader, RequestContext

# Create your views here.

def email_sent(request):
    return render(request, 'accounts/email_sent.html', {})
	
def register_confirm(request, activation_key):
    #check if user is already logged in and if he is log him out
    if request.user.is_authenticated():
        logout(request)

    # check if there is UserProfile which matches the activation key (if not then display 404)
    user_profile = get_object_or_404(UserProfile, activation_key=activation_key)

    #check if the activation key has expired, if it hase then render confirm_expired.html
	# if the user is active, then the 
    user = user_profile.user
    if user_profile.key_expires < timezone.now() and not user.is_active:
        user.delete()
        return render_to_response('accounts/confirm_expired.html')
    
	#if the key hasn't expired save user, remove the activation key, set him as active, and render the confirm activation tempate
    user = user_profile.user
    user.is_active = True
    user.save()
    user_profile.activation_key=None
    user_profile.save()
	
    return render_to_response('accounts/confirm.html')
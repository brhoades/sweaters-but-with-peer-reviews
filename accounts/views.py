from django.contrib.auth import logout
from django.shortcuts import redirect
from accounts.models import UserProfile
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
import json
from new.utils import json_error

from django.core.mail import send_mail
from django.conf import settings
import hashlib
import datetime
import random


# Create your views here.
def email_sent(request):
    messages.info(request, "You have been sent an activation email. Please "
                           "click the included link to activate your account.")
    return redirect("home")


def register_confirm(request, activation_key):
    # check if user is already logged in and if he is log him out
    if request.user.is_authenticated():
        logout(request)

    # check if there is UserProfile which matches the activation
    try:
        user_profile = UserProfile.objects.get(activation_key=activation_key)
    except ObjectDoesNotExist:
        messages.error(request, "Invalid activation link.")
        return redirect("home")

    # check if the activation key has expired, if it hase then render
    # confirm_expired.html
    # if the user is active, then the
    user = user_profile.user
    if user_profile.key_expires < timezone.now() and not user.is_active:
        user.delete()
        messages.error(request, "This registration email has expired.")
        return redirect("home")

    # if the key hasn't expired save user, remove the activation key, set
    # him as active, and render the confirm activation tempate
    user.is_active = True
    user.save()
    user_profile.activation_key = None
    user_profile.save()

    messages.success(request, "Successfully confirmed account.")
    return redirect("home")


def register(request):
    """
        "username": username
        "password": password
        "password2": password2
        "firstname": firstname
        "lastname": lastname
        "email": email
    """

    resp = {"message": ""}

    data = json.loads(request.body.decode('utf-8'))
    if request.method != "POST":
        messages.error(request, "This is an AJAX interface.")
        return redirect("home")

    req = ["first_name", "last_name", "password", "password2", "email"]
    for k in req:
        if k not in data or (k in data and len(data[k]) < 2):
            resp["message"] = "{} is a required field.".format(k)
            return JsonResponse(json.dumps(resp))

    # Username
    if len(data['username']) < 4 or len(data['username']) > 25:
        return json_error("Usernames must be between 4 and 25 characters.")
    if User.objects.filter(username=data['username']).exists():
        return json_error("Username already exists")

    if len(data['password1']) < 5:
        return json_error("A password must be at least 5 characters long.")
    if data['password2'] != data['password']:
        return json_error("Passwords do not match")

    if len(data['email']) < 5:
        return json_error("Email is too short")

    user = User(username=data['username'], email=data['email'],
                first_name=data['first_name'], last_name=data['last_name'])
    user.set_password(data['password'])
    user.is_active = False  # not active until he opens activation link
    user.save()

    random_string = str(random.random()).encode('utf8')
    salt = hashlib.sha1(random_string).hexdigest()[:5]
    salted = (salt + data['email']).encode('utf8')
    activation_key = hashlib.sha1(salted).hexdigest()
    key_expires = datetime.datetime.today() + datetime.timedelta(2)

    # Create and save user profile
    new_profile = UserProfile(user=user, activation_key=activation_key,
                              key_expires=key_expires)
    new_profile.save()

    # Send email with activation key
    email_subject = 'Account confirmation'
    email_body = "Hey %s, thanks for signing up. To activate your account, " \
                 "click this link within 48 hours: %saccounts/confirm/%s/"  \
                 % (user.first_name, settings.BASE_URL, activation_key)
    send_mail(email_subject, email_body, settings.EMAIL_HOST_EMAIL,
              [user.email], fail_silently=False)

    messages.success(request, "You have successfully registered. Please "
                              "check your provided email address.")

    return JsonResponse(json.dumps({"refresh": "", "message": ""}))

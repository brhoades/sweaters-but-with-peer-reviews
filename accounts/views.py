from django.contrib.auth import logout
from django.shortcuts import redirect
from accounts.models import UserProfile
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
import json

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


def register(request, type):
    """
        "username": username
        "password": password
        "password2": password2
        "firstname": firstname
        "lastname": lastname
        "email": email
    """

    resp = {"errors": {}}

    data = json.loads(request.body.decode('utf-8'))
    if request.method != "POST":
        messages.error(request, "This is an AJAX interface.")
        return redirect("home")

    req = {"first_name":"First Name", "last_name":"Last Name", "username":"User Name", "password":"Password", "password2":"Repeat Password", "email":"Email"}
    for k in req:
        if k not in data or len(data[k]) == 0:
            resp["errors"][k] = "{} is a required field.".format(req[k])
    if len(resp["errors"]) != 0:
        return JsonResponse(resp)

    # Username
    if len(data['username']) < 4 or len(data['username']) > 25:
        resp["errors"]['username'] = "Usernames must be between 4 and 25 characters."
    elif User.objects.filter(username=data['username']).exists():
        resp["errors"]['username'] = "Username already exists."
    #     return JsonResponse({"message": "Username already exists"})

    if data['password2'] != data['password']:
        resp["errors"]['password2'] = "Passwords don't match."

    try:
        user = User(username=data['username'], email=data['email'],
                    first_name=data['first_name'], last_name=data['last_name'])
        user.set_password(data['password'])
        user.is_active = False  # not active until he opens activation link
        user.full_clean()  # check validators

        if len(resp["errors"]) != 0:
            return JsonResponse(resp)

        user.save()
    except Exception as e:
        for k,v in e:
            resp["errors"][str(k)] = v[0]
        # return JsonResponse({"errors": json.dumps(e)})
        return JsonResponse(resp)

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

    return JsonResponse({"success": True})

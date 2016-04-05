from django.conf.urls import url
from django.contrib import admin

from django.views.generic.edit import CreateView
from accounts.forms import UserCreateForm
from accounts.views import email_sent, register_confirm

urlpatterns = [
    url(r'^register/', CreateView.as_view(template_name='accounts/register.html', form_class=UserCreateForm, success_url='/accounts/email_sent/'), name="user_registration"),
	url(r'^email_sent/', email_sent, name='email_sent'),
	url(r'^confirm/(?P<activation_key>\w+)/', register_confirm, name='register_confirm'),
]

from django.conf.urls import url
from django.contrib import admin

from django.views.generic.edit import CreateView
from .forms import UserCreateForm
from . import views

urlpatterns = [
    url(r'^register/', CreateView.as_view(template_name='accounts/register.html', form_class=UserCreateForm, success_url='/accounts/email_sent/'), name="user_registration"),
	url(r'^email_sent/', views.email_sent, name='email_sent'),
	url(r'^confirm/(?P<activation_key>\w+)/', views.register_confirm, name='register_confirm'),
]

    
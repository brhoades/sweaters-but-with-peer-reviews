from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User


class School(models.Model):
    name = models.CharField(max_length=100)
    email_pattern = models.CharField(max_length=50)
    location = models.CharField(max_length=100)


class Professor(models.Model):
    owner = models.ForeignKey(User)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    school = models.ForeignKey(School)


class Review(models.Model):
    # source = models.ForeignKey(Users)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    course = models.CharField(max_length=100)
    created_ts = models.DateTimeField(auto_now_add=True)
    updated_ts = models.DateTimeField(auto_now=True)


class Review_Votes(models.Model):
    quality = models.IntegerField(validators=[MaxValueValidator(100),
                                  MinValueValidator(0)])
    review = models.ForeignKey(Review)
    reviewer = models.ForeignKey(User)

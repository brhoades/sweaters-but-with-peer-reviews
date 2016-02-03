from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator, \
    RegexValidator, URLValidator
from django.contrib.auth.models import User
from geoposition.fields import GeopositionField


class School(models.Model):
    name = models.CharField(max_length=100)
    email_pattern = models.CharField(max_length=50,
                                     validators=[RegexValidator])
    url = models.CharField(max_length=100,
                           validators=[URLValidator], blank=True, null=True)
    location = GeopositionField()
    created_ts = models.DateTimeField(auto_now_add=True)
    updated_ts = models.DateTimeField(auto_now=True)


class FieldCategories(models.Model):
    name = models.CharField(max_length=30)

    created_by = models.ForeignKey(User)


class Field(models.Model):
    name = models.CharField(max_length=100)
    categories = models.ManyToManyField(FieldCategories)

    created_by = models.ForeignKey(User)


class Department(models.Model):
    name = models.CharField(max_length=100)
    school = models.ForeignKey(School)
    fields = models.ManyToManyField(Field)
    url = models.CharField(max_length=100,
                           validators=[URLValidator], blank=True, null=True)

    created_ts = models.DateTimeField(auto_now_add=True)
    updated_ts = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User)


class Professor(models.Model):
    owner = models.ForeignKey(User, blank=True, null=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    school = models.ForeignKey(School)

    created_ts = models.DateTimeField(auto_now_add=True)
    updated_ts = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, related_name='created_by')


class Course(models.Model):
    name = models.CharField(max_length=100)
    number = models.IntegerField()
    department = models.ForeignKey(Department)

    created_ts = models.DateTimeField(auto_now_add=True)
    updated_ts = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User)


class Review(models.Model):
    source = models.ForeignKey(User)
    course = models.ForeignKey(Course)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)

    # 100k otta be enough for nebody.
    text = models.TextField(max_length=100000)

    created_ts = models.DateTimeField(auto_now_add=True)
    updated_ts = models.DateTimeField(auto_now=True)


class ReviewVotes(models.Model):
    quality = models.IntegerField(validators=[MaxValueValidator(100),
                                  MinValueValidator(0)])
    review = models.ForeignKey(Review)
    reviewer = models.ForeignKey(User)

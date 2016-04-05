from django.db.models import Model
from django.db import models
from django.core.validators import RegexValidator, URLValidator, \
    MinLengthValidator
from django.contrib.auth.models import User
from geoposition.fields import GeopositionField

import urllib.request as urllib
import json


def to_json(self):
    """
    Tries to recursively serialize this object and its references.
    """
    ret = {}
    for field in self._meta.get_fields():
        # If we don't have the attribute (this happens), skip it
        try:
            ret[field.name] = getattr(self, field.name)
        except:
            continue

        # FIXME: Add a catch for user. Don't return the password.
        try:
            ret[field.name] = json.loads(ret[field.name].to_json())
        except:
            ret[field.name] = str(ret[field.name])
            pass
    return json.dumps(ret)

Model.to_json = to_json


class School(Model):
    name = models.CharField(max_length=100)
    email_pattern = models.CharField(max_length=50,
                                     validators=[RegexValidator])
    url = models.CharField(max_length=100,
                           validators=[URLValidator], blank=True, null=True)
    location = GeopositionField()
    created_ts = models.DateTimeField(auto_now_add=True)
    updated_ts = models.DateTimeField(auto_now=True)

    @property
    def num_professors(self):
        return Professor.objects.filter(school_id=self.id).count

    @property
    def num_reviews(self):
        return Review.objects.filter(target__school_id=self.id).count

    @property
    def human_location(self):
        if not self.location:
            return None

        url = ("http://maps.googleapis.com/maps/api/geocode/json"
               "?latlng={},{}&sensor=false").format(self.location.latitude,
                                                    self.location.longitude)
        data = urllib.urlopen(url).read()
        data = json.loads(data.decode("UTF-8"))

        if len(data["results"]) > 0:
            return data["results"][0]["formatted_address"]
        else:
            return "Unknown"

    @property
    def rating(self):
        rating = (Review.objects.filter(target__school_id=self.id)
                  .aggregate(models.Avg("rating_overall"))
                  ["rating_overall__avg"])

        if rating is None:
            rating = "-"
        else:
            rating = round(rating, 1)

        return rating

    def __str__(self):
        return "%s" % (self.name)


class FieldCategory(Model):
    class Meta:
        verbose_name_plural = "Field Categories"

    name = models.CharField(max_length=30)

    created_by = models.ForeignKey(User)

    def __str__(self):
        return "%s" % (self.name)


class Field(Model):
    name = models.CharField(max_length=100)
    categories = models.ManyToManyField(FieldCategory)

    created_by = models.ForeignKey(User)

    def __str__(self):
        return "%s" % (self.name)


class Department(models.Model):
    name = models.CharField(max_length=100)
    school = models.ForeignKey(School)
    fields = models.ManyToManyField(Field)
    url = models.CharField(max_length=100,
                           validators=[URLValidator], blank=True, null=True)

    created_ts = models.DateTimeField(auto_now_add=True)
    updated_ts = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User)

    def __str__(self):
        return "%s" % (self.name)


class Professor(Model):
    owner = models.ForeignKey(User, blank=True, null=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    school = models.ForeignKey(School)

    created_ts = models.DateTimeField(auto_now_add=True)
    updated_ts = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, related_name='created_by')

    @property
    def num_reviews(self):
        return Review.objects.filter(target_id=self.id).count()

    @property
    def num_courses(self):
        return (Review.objects.filter(target_id=self.id).values("course")
                .distinct().count())

    @property
    def rating(self):
        rating = (Review.objects.filter(target_id=self.id)
                  .aggregate(models.Avg("rating_overall"))
                  ["rating_overall__avg"])

        if rating is None:
            rating = "-"
        else:
            rating = round(rating, 1)
        return rating

    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)


class Course(Model):
    name = models.CharField(max_length=100)
    number = models.IntegerField()
    department = models.ForeignKey(Department)

    created_ts = models.DateTimeField(auto_now_add=True)
    updated_ts = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User)

    def __str__(self):
        return "%s (%i)" % (self.name, self.number)


class Review(Model):
    owner = models.ForeignKey(User)
    course = models.ForeignKey(Course)
    target = models.ForeignKey(Professor, on_delete=models.CASCADE)

    title = models.TextField(max_length=100,
                             validators=[MinLengthValidator(3)])

    # [0,5]
    rating_value = models.FloatField()
    rating_difficulty = models.FloatField()
    rating_overall = models.FloatField()

    # 100k otta be enough for nebody.
    text = models.TextField(max_length=100000,
                            validators=[MinLengthValidator(40)])

    created_ts = models.DateTimeField(auto_now_add=True)
    updated_ts = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} {} for {} {}".format(self.owner.first_name,
                                        self.owner.last_name,
                                        self.target.first_name,
                                        self.target.last_name)


class ReviewVote(Model):
    class Meta:
        verbose_name_plural = "Review Votes"

    quality = models.BooleanField()
    target = models.ForeignKey(Review)
    owner = models.ForeignKey(User)

    def __str__(self):
        return "%s %s" % (self.owner.first_name, self.owner.last_name)

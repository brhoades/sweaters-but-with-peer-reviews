from django.db import models
from django.core.validators import RegexValidator, URLValidator, \
    MinLengthValidator
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

    def __str__(self):
        return "%s" % (self.name)


class FieldCategory(models.Model):
    class Meta:
        verbose_name_plural = "Field Categories"

    name = models.CharField(max_length=30)

    created_by = models.ForeignKey(User)

    def __str__(self):
        return "%s" % (self.name)


class Field(models.Model):
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

    def to_json(self):
        # Forcing school to be expanded
        return {
            "id": self.pk,
            "name": self.name,
            "school": self.school.id,
            "school_name": self.school.name,
            # "fields": serializers.serialize("json", self.fields),
            "url": self.url,
            "created_ts": str(self.created_ts),
            "updated_ts": str(self.updated_ts),
            "created_by": str(self.created_by),
            }


class Professor(models.Model):
    owner = models.ForeignKey(User, blank=True, null=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    school = models.ForeignKey(School)

    created_ts = models.DateTimeField(auto_now_add=True)
    updated_ts = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, related_name='created_by')

    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)


class Course(models.Model):
    name = models.CharField(max_length=100)
    number = models.IntegerField()
    department = models.ForeignKey(Department)

    created_ts = models.DateTimeField(auto_now_add=True)
    updated_ts = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User)

    def __str__(self):
        return "%s (%i)" % (self.name, self.number)


class Review(models.Model):
    owner = models.ForeignKey(User)
    course = models.ForeignKey(Course)
    target = models.ForeignKey(Professor, on_delete=models.CASCADE)

    # 100k otta be enough for nebody.
    text = models.TextField(max_length=100000,
                            validators=[MinLengthValidator(50)])

    created_ts = models.DateTimeField(auto_now_add=True)
    updated_ts = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} {} for {} {}".format(self.owner.first_name,
                                        self.owner.last_name,
                                        self.target.first_name,
                                        self.target.last_name)


class ReviewVote(models.Model):
    class Meta:
        verbose_name_plural = "Review Votes"

    quality = models.BooleanField()
    target = models.ForeignKey(Review)
    owner = models.ForeignKey(User)

    def __str__(self):
        return "%s %s" % (self.owner.first_name, self.owner.last_name)


class ReviewComment(models.Model):
    target = models.ForeignKey(Review)
    owner = models.ForeignKey(User)

    # 100k otta be enough for Billy
    text = models.TextField(max_length=100000,
                            validators=[MinLengthValidator(25)])

    created_ts = models.DateTimeField(auto_now_add=True)
    updated_ts = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} {} on {}".format(self.owner.first_name,
                                    self.owner.last_name,
                                    self.target.id)

from django.db.models import Model
from django.db import models
from django.core.validators import RegexValidator, URLValidator, \
    MinLengthValidator
from django.contrib.auth.models import User
from geoposition.fields import GeopositionField
from django.apps import apps

from django.utils import timezone

import urllib.request as urllib
import json
import datetime


def to_json(self):
    """
    Tries to recursively serialize this object and its references.
    """
    ret = {}
    for field in self._meta.get_fields():
        # Don't send passwords or emails.
        if field.name == "password" or field.name == "email":
            continue

        # If we don't have the attribute (this happens), skip it
        try:
            ret[field.name] = getattr(self, field.name)
        except:
            continue

        try:
            ret[field.name] = json.loads(ret[field.name].to_json())
        except:
            ret[field.name] = str(ret[field.name])
            pass
    return json.dumps(ret)


def updated(self):
    """
    Returns true if this model has been updated by a user.
    """
    if abs(self.created_ts - self.updated_ts) < datetime.timedelta(seconds=1):
        return False
    return True


def is_new(self):
    timediff = timezone.now() - self.date_joined
    return timediff.seconds < 10


def one_week(self):
    timediff = timezone.now() - self.date_joined
    return timediff.minute > 10080


# monkey patch some new functions onto models
Model.to_json = to_json
Model.updated = updated
User.is_new = is_new


class School(Model):
    created_by = models.ForeignKey(User, default=1)
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
        return "%s at %s" % (self.name, self.human_location)


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
        return "%s (%s)" % (self.name, self.school.name)


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
        return "%s %s (at %s)" % (self.first_name, self.last_name,
                                  self.school.name)


class Course(Model):
    name = models.CharField(max_length=100)
    number = models.IntegerField()
    department = models.ForeignKey(Department)

    created_ts = models.DateTimeField(auto_now_add=True)
    updated_ts = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User)

    def __str__(self):
        return "%s (%i) at %s" % (self.name, self.number,
                                  self.department.school.name)


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
                            validators=[MinLengthValidator(50)])

    created_ts = models.DateTimeField(auto_now_add=True)
    updated_ts = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Review by {} {} for {} {}".format(self.owner.first_name,
                                                  self.owner.last_name,
                                                  self.target.first_name,
                                                  self.target.last_name)

    def is_new(self):
        timediff = timezone.now() - self.created_ts
        return timediff.seconds < 10


class ReviewVote(Model):
    class Meta:
        verbose_name_plural = "Review Votes"

    quality = models.BooleanField()
    target = models.ForeignKey(Review)
    owner = models.ForeignKey(User)

    def __str__(self):
        if self.quality:
            type = "positive"
        else:
            type = "negative"
        return ("Review Vote for {} by {} {}"
                .format(type,
                        self.target.title,
                        self.owner.first_name,
                        self.owner.last_name))


class ReviewComment(models.Model):
    class Meta:
        verbose_name_plural = "Review Comments"

    target = models.ForeignKey(Review)
    owner = models.ForeignKey(User)

    # 100k otta be enough for Billy
    text = models.TextField(max_length=100000,
                            validators=[MinLengthValidator(25)])

    created_ts = models.DateTimeField(auto_now_add=True)
    updated_ts = models.DateTimeField(auto_now=True)

    def __str__(self):
        return ("{} {} comment on review for {} {} ({})"
                .format(self.owner.first_name, self.owner.last_name,
                        self.target.target.first_name,
                        self.target.target.last_name, self.target.id))


class Log(models.Model):
    """
    Contains an event. Can be a edits, deletions, etc. Reports can point
    to a log of that report.
    """
    # Contains JSON detailing target model name and pk.
    # 'model_type': 'String',
    # 'model_pk': Number
    target_serialized = models.TextField(max_length=1000, null=True)
    action = models.TextField(max_length=10000, null=True)
    comment = models.TextField(max_length=10000, null=True)
    owner = models.ForeignKey(User, null=True)  # null implies system

    created_ts = models.DateTimeField(auto_now_add=True)
    updated_ts = models.DateTimeField(auto_now=True)

    # Types of logs
    ADD = "add"
    DELETE = "del"
    MODIFY = "mod"
    REPORT = "rep"
    REPORT_RESOLVE = "han"
    OTHER = "oth"

    CATEGORIES = (
        (ADD, "Add"),
        (DELETE, "Delete"),
        (MODIFY, "Modify"),
        (REPORT, "Report"),
        (REPORT_RESOLVE, "Report Resolution"),
        (OTHER, "Other"),
    )

    category = models.CharField(max_length=3, choices=CATEGORIES,
                                default=OTHER)

    @property
    def target(self):
        """
        Get the target of this entry. Note that if it was delete, this will
        raise.
        """
        data = json.loads(self.target_serialized)
        model = apps.get_model(model_name=data["model_type"],
                               app_label="browse")
        return model.objects.get(id=data["model_pk"])

    @staticmethod
    def create(model, id, type, action=None, comment=None,
               owner=""):
        """
        Create a log entry given a model, its id, and a type.
        Message optional.

        Does not save, only returns a new Log.
        """
        log = Log(target_serialized=json.dumps({
            "model_type": model.__class__.__name__,
            "model_pk": id
            }), category=type, action=action, comment=comment,
            owner=owner)

        log.save()

        return log

    @property
    def category_name(self):
        """
        Get a pretty category name for this log entry. Do a lazy linear
        search.
        """
        for short, name in Log.CATEGORIES:
            if short == self.category:
                return name

    def __str__(self):
        if self.owner:
            owner = "{} {}".format(self.owner.first_name,
                                   self.owner.last_name)
        else:
            owner = "System"
        return ("\"{}\" (\"{}\") by {}"
                .format(self.action, self.comment, owner))
        # TODO: Add target information in here if there's a target ^^


class Report(models.Model):
    """
    Reports are simply a pointer to a log entry (that's in turn a report).

    Unsatisfied unless handled_by is a log entry.
    """
    target_log = models.ForeignKey(Log, related_name="target_log")
    handled_by = models.ForeignKey(Log, null=True, related_name="handled_by")

    summary = models.TextField(max_length=50)

    @staticmethod
    def create(model, id, reporter, summary, text):
        """
        Creates a new report given a reporter, a message, a target id,
        and a target model.
        """
        log = Log.create(model, id, Log.REPORT, comment=text,
                         owner=reporter)

        new = Report(target_log=log, summary=summary)
        new.save()

        return new

    def resolve(self, by, comment):
        """
        Resolves a report by creating another log entry.
        """
        self.handled_by = Log.create(self.target,
                                     self.target.id,
                                     Log.REPORT_RESOLVE, comment=comment,
                                     owner=by)
        self.handled_by.save()
        self.save()
        return self

    @property
    def target(self):
        """
        Gives the target of this report.
        """
        return self.target_log.target

    @property
    def created_by(self):
        """
        Gives the person who created this report
        """
        return self.target_log.owner

    @property
    def handled(self):
        """
        Returns if this report was handled.
        """
        return self.handled_by is not None

    @property
    def handler(self):
        """
        Gives the user who handled this report.
        """
        return self.handled_by.owner

    @property
    def created_ts(self):
        """
        Gives the time this report was created.
        """
        return self.target_log.created_ts

    @property
    def updated_ts(self):
        """
        Returns the created_ts unless this report has been handled, in which
        case it returns the handler entry's created_ts.
        """
        if self.handled:
            return self.handled_by.created_ts

        return self.created_by.created_ts

    @property
    def owner(self):
        """
        Gives the owner of this report.
        """
        return self.created_by

    @property
    def title(self):
        """
        Gives a report title for our overview page.
        """
        return "[{}] {}".format(self.target.__class__.__name__, self.target)

    @property
    def target_type(self):
        """
        Returns a string that can be used as a link to get the target's info
        page.

        Usually.
        """
        return self.target.__class__.__name__.lower()

    def __str__(self):
        resolved = "pending"
        if self.handled:
            resolved = "addressed by {} {}".format(self.handler.first_name,
                                                   self.handler.last_name)
        return ("\"{}\" for a {} ({}) by {} {} ({})"
                .format(self.summary, self.target.__class__.__name__,
                        str(self.target),
                        self.created_by.first_name,
                        self.created_by.last_name,
                        resolved))


class PeerReview(Model):
    class Meta:
        verbose_name_plural = "Peer Reviews"

    target = models.ForeignKey(Review)
    owner = models.ForeignKey(User)

    text = models.TextField(max_length=100000, blank=True)
    rating = models.FloatField(blank=True, null=True)

    PR_FLAGS = (("LD", "Lewd."),
                ("UH", "Unhelpful."),
                ("OT", "Off Topic."),
                ("OK", "Okay."),)

    flag = models.CharField(max_length=2, choices=PR_FLAGS, default="OK")

    created_ts = models.DateTimeField(auto_now_add=True)
    updated_ts = models.DateTimeField(auto_now=True)

    is_finished = models.BooleanField(default=False)

    def __str__(self):
        return "{} {} on {}".format(self.owner.first_name,
                                    self.owner.last_name,
                                    self.target.title)

from django.contrib import admin
from browse.models import School, Professor, Review, ReviewVote, Field, \
    FieldCategory, Department, Course


# Register your models here.
admin.site.register(School)
admin.site.register(Professor)
admin.site.register(Review)
admin.site.register(ReviewVote)
admin.site.register(Course)
admin.site.register(Department)
admin.site.register(Field)
admin.site.register(FieldCategory)

from django.contrib import admin
from browse.models import School, Professor, Review, ReviewVotes, Field, \
    FieldCategories, Department, Course


# Register your models here.
admin.site.register(School)
admin.site.register(Professor)
admin.site.register(Review)
admin.site.register(ReviewVotes)
admin.site.register(Course)
admin.site.register(Department)
admin.site.register(Field)
admin.site.register(FieldCategories)

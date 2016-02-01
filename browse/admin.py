from django.contrib import admin
from browse.models import School, Professor, Review, Review_Votes


# Register your models here.
admin.site.register(School)
admin.site.register(Professor)
admin.site.register(Review)
admin.site.register(Review_Votes)


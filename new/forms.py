from browse.models import Review, Course, Professor, School
from django.forms import ModelForm


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['target', 'course', 'text']


class CourseForm(ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'number', 'department']


class ProfessorForm(ModelForm):
    class Meta:
        model = Professor
        fields = ['first_name', 'last_name', 'school']


class SchoolForm(ModelForm):
    class Meta:
        model = School
        fields = ['name', 'location', 'url', 'email_pattern']

"""
This file houses forms which are used to check if submitted JSON blobs have
the appropriate fields required.
"""

from browse.models import Review, Course, Professor, School, Department,\
    Field, FieldCategory, ReviewComment, Report
from django.forms import ModelForm


class ReviewForm(ModelForm):
    needs_owner = True
    needs_created_by = False

    class Meta:
        model = Review
        fields = ['target', 'course', 'text', 'rating_overall', 'rating_value',
                  'rating_difficulty']
        fields_extra = []


class CourseForm(ModelForm):
    needs_owner = False
    needs_created_by = True

    class Meta:
        model = Course
        fields = ['name', 'number', 'department']
        fields_extra = []


class ProfessorForm(ModelForm):
    needs_owner = False
    needs_created_by = True

    class Meta:
        model = Professor
        fields = ['first_name', 'last_name', 'school']
        fields_extra = []


class SchoolForm(ModelForm):
    needs_owner = False
    needs_created_by = True

    class Meta:
        model = School
        fields = ['name', 'location', 'url', 'email_pattern']
        fields_extra = []


class DepartmentForm(ModelForm):
    needs_owner = False
    needs_created_by = True

    class Meta:
        model = Department
        fields = ['name', 'school', 'fields', 'url']
        fields_extra = []


class FieldForm(ModelForm):
    needs_owner = False
    needs_created_by = True

    class Meta:
        model = Field
        fields = ['name', 'categories']
        fields_extra = []


class FieldCategoryForm(ModelForm):
    needs_owner = False
    needs_created_by = True

    class Meta:
        model = FieldCategory
        fields = ['name']
        fields_extra = []


class CommentForm(ModelForm):
    needs_owner = True
    needs_created_by = False

    class Meta:
        model = ReviewComment
        fields = ['text', 'target', 'owner']
        fields_extra = []


class ReportForm(ModelForm):
    needs_owner = False
    needs_created_by = False

    class Meta:
        model = Report
        fields = ['summary']
        # Only used for internal checks.
        fields_extra = ['comment']

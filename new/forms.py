from browse.models import Review, Course, Professor, School, Department,\
    Field, FieldCategory
from django.forms import ModelForm


class ReviewForm(ModelForm):
    needs_owner = True
    needs_created_by = False

    class Meta:
        model = Review
        fields = ['target', 'course', 'text']


class CourseForm(ModelForm):
    needs_owner = False
    needs_created_by = True

    class Meta:
        model = Course
        fields = ['name', 'number', 'department']


class ProfessorForm(ModelForm):
    needs_owner = False
    needs_created_by = True

    class Meta:
        model = Professor
        fields = ['first_name', 'last_name', 'school']


class SchoolForm(ModelForm):
    needs_owner = False
    needs_created_by = True

    class Meta:
        model = School
        fields = ['name', 'location', 'url', 'email_pattern']


class DepartmentForm(ModelForm):
    needs_owner = False
    needs_created_by = True

    class Meta:
        model = Department
        fields = ['name', 'school', 'fields', 'url']


class FieldForm(ModelForm):
    needs_owner = False
    needs_created_by = True

    class Meta:
        model = Field
        fields = ['name', 'categories']


class FieldCategoryForm(ModelForm):
    needs_owner = False
    needs_created_by = True

    class Meta:
        model = FieldCategory
        fields = ['name']

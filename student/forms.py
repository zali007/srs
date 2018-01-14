from django import forms
from .models import Student
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions


class StudentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)

        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)

        # You can dynamically adjust your layout
        # self.helper.layout.append(Submit('save', 'save'))
        self.helper.form_class = 'form-horizontal'
        self.helper.layout.append(Submit('submit_change', 'Submit', css_class="btn-primary"))
        self.helper.layout.append(HTML('<a class="btn btn-primary" href={% url "student_home" %}>Reset</a>'))

    # Verify IC number is in XXXXXXXXXX format
    def clean_icnum(self):
        data = self.cleaned_data['icnum']
        # if Student.objects.filter(icnum=data):
        #     raise forms.ValidationError(data + " is already exist!") 
        # elif len(data) is not 12:
        if len(data) is not 12:
            raise forms.ValidationError("IC must be 12 number characters long!")
        elif not data.isnumeric():
            raise forms.ValidationError("IC must be all number!")

        # Always return a value to use as the new cleaned data, even if
        # this method didn't change it.
        return data

    class Meta:
        model = Student
        fields = ('icnum', 'name', 'course',)
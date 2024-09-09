from django import forms
from django.contrib.auth.models import User
from .models import Session, Semester

from accounts.models import User
from .models import Program, Course, CourseAllocation, Upload, UploadVideo,  YEARS

# User = settings.AUTH_USER_MODEL

class ProgramForm(forms.ModelForm):
    class Meta:
        model = Program
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['summary'].widget.attrs.update({'class': 'form-control'})


class CourseAddForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['code'].widget.attrs.update({'class': 'form-control'})
        # self.fields['courseUnit'].widget.attrs.update({'class': 'form-control'})
        self.fields['credit'].widget.attrs.update({'class': 'form-control'})
        self.fields['summary'].widget.attrs.update({'class': 'form-control'})
        self.fields['program'].widget.attrs.update({'class': 'form-control'})
        self.fields['semester'].widget.attrs.update({'class': 'form-control'})


class CourseAllocationForm(forms.ModelForm):
    courses = forms.ModelMultipleChoiceField(
        queryset=Course.objects.all().order_by('program'),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'browser-default checkbox'}),
        required=True
    )
    lecturer = forms.ModelChoiceField(
        queryset=User.objects.filter(is_staff=True),
        widget=forms.Select(attrs={'class': 'browser-default custom-select'}),
        label="staff",
    )

    class Meta:
        model = CourseAllocation
        fields = ['lecturer', 'courses']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(CourseAllocationForm, self).__init__(*args, **kwargs)
        self.fields['lecturer'].queryset = User.objects.filter(is_staff=True)


class EditCourseAllocationForm(forms.ModelForm):
    courses = forms.ModelMultipleChoiceField(
        queryset=Course.objects.all().order_by('program'),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )
    lecturer = forms.ModelChoiceField(
        queryset=User.objects.filter(is_staff=True),
        widget=forms.Select(attrs={'class': 'browser-default custom-select'}),
        label="lecturer",
    )

    class Meta:
        model = CourseAllocation
        fields = ['lecturer', 'courses']

    def __init__(self, *args, **kwargs):
        #    user = kwargs.pop('user')
        super(EditCourseAllocationForm, self).__init__(*args, **kwargs)
        self.fields['lecturer'].queryset = User.objects.filter(is_staff=True)


# Upload files to specific course
class UploadFormFile(forms.ModelForm):
    class Meta:
        model = Upload
        fields = ('title', 'file', 'course',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['file'].widget.attrs.update({'class': 'form-control'})


# Upload video to specific course
class UploadFormVideo(forms.ModelForm):
    class Meta:
        model = UploadVideo
        fields = ('title', 'video', 'course',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['video'].widget.attrs.update({'class': 'form-control'})

#class CourseFilterForm(forms.Form):
#    level = forms.ChoiceField(choices=LEVEL, label='Level', required=False)
#    session = forms.ChoiceField(choices=YEARS, label='Session', required=False)


##################################################################

class SessionForm(forms.ModelForm):
    next_session_begins = forms.DateTimeField(
        widget=forms.TextInput(
            attrs={
                'type': 'date',
            }
        ),
        required=True)

    class Meta:
        model = Session
        fields = ['session', 'is_current_session', 'next_session_begins']


class SemesterForm(forms.ModelForm):
    semester = forms.CharField(
        widget=forms.Select(
            choices=Course,
            attrs={
                'class': 'browser-default custom-select',
            }
        ),
        label="semester",
    )
    is_current_semester = forms.CharField(
        widget=forms.Select(
            choices=((True, 'Yes'), (False, 'No')),
            attrs={
                'class': 'browser-default custom-select',
            }
        ),
        label="is current semester ?",
    )
    session = forms.ModelChoiceField(
        queryset=Session.objects.all(),
        widget=forms.Select(
            attrs={
                'class': 'browser-default custom-select',
            }
        ),
        required=True
    )

    next_semester_begins = forms.DateTimeField(
        widget=forms.TextInput(
            attrs={
                'type': 'date',
                'class': 'form-control',
            }
        ),
        required=True)

    class Meta:
        model = Semester
        fields = ['semester', 'is_current_semester', 'session', 'next_semester_begins']
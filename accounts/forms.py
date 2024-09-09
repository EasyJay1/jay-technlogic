from django.db import transaction
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm, PasswordResetForm
from academy.models import *
from .models import *
from django import forms
from .models import Student
from django.contrib.auth.forms import UserChangeForm


class RegistartionForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Type password', 'class': 'form-control'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm password'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'password']

    def clean(self):
        cleaned_data     = super(RegistartionForm,self).clean()
        password         = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError(
                "Password does not match!"
            )

class StaffAddForm(UserCreationForm):
    username = forms.CharField(
        max_length=30, widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control', }),
        label="Username", )

    first_name = forms.CharField(
        max_length=30, widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control', }),
        label="First Name", )

    last_name = forms.CharField(
        max_length=30, widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control', }),
        label="Last Name", )

    phone = forms.CharField(
        max_length=30, widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control', }),
        label="Mobile No.", )

    email = forms.CharField(
        max_length=30, widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control', }),
        label="Email", )

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic()
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_staff = True
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.phone = self.cleaned_data.get('phone')
        user.address = self.cleaned_data.get('address')
        user.email = self.cleaned_data.get('email')
        if commit:
            user.save()
        return user


class StudentAddForm(UserCreationForm):
    username = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control',
                'id': 'username_id',
                'placeholder': 'Create Username'
            }
        ),
        label="USERNAME",
    )
    email = forms.EmailField(
        max_length=254,
        widget=forms.EmailInput(
            attrs={
                'type': 'email',
                'class': 'form-control',
                'id': 'email_id',
                'placeholder': 'Email Address'
            }
        ),
        label="Email",
    )
    phone = forms.CharField(
        widget=forms.TextInput(attrs={'type': 'Number', 'class': 'form-control'}),
        label="Phone No.",
    )


    first_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control',
            }
        ),
        label="Child's First name",
    )

    last_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control',
            }
        ),
        label="Child's Last name",
    )
    programs = forms.ModelChoiceField(
        queryset=Program.objects.all(),
        widget=forms.Select(attrs={'class': 'browser-default custom-select form-control'}),
        label="Programs",
    )

    courses = forms.CharField(
        widget=forms.Select(
            choices=Course,
            attrs={
                'class': 'browser-default custom-select form-control',
            }
        ),
    )

    session = forms.CharField(
        widget=forms.Select(
            choices=YEARS,
            attrs={
                'class': 'browser-default custom-select form-control',
            }
        ),
    )


    password1 = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'type': 'password', 'class': 'form-control', }),
        label="Password",
    )

    password2 = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'type': 'password', 'class': 'form-control', }),
        label="Password Confirmation",
    )

    accept_terms = forms.BooleanField(label='I accept the Terms and Conditions', required=True)

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic()
    def save(self):
        user = super().save(commit=False)
        user.is_student = True
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.email = self.cleaned_data.get('email')
        user.phone = self.cleaned_data.get('phone')

        user.save()
        student = Student.objects.create(
            student=user,
            courses=self.cleaned_data.get('courses'),
            programs=self.cleaned_data.get('programs'),
            session=self.cleaned_data.get('session')

        )
        student.save()
        return user


##########################################################a
class ProfileUpdateForm(UserChangeForm):
    picture = forms.ImageField(
        widget=forms.FileInput(attrs={'class': 'form-control-file'}),
        label="Profile Picture",
        required=False,  # Set to True if the picture is required
    )

    address = forms.CharField(
        widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control'}),
        label="Address / city",
    )

    nationality = forms.CharField(
        widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control'}),
        label="Nationality",
    )


    class Meta:
        model = User
        fields = ['address', 'nationality', 'picture']

class StudentFilterForm(forms.Form):
    programs = forms.ChoiceField(choices=Program, label='programs_filter', required=False,)
    courses = forms.ChoiceField(choices=Course, label='courses_filter', required=False,)
    session = forms.ChoiceField(choices=YEARS, label='Session', required=False)

class ChatForm(forms.Form):
    message = forms.CharField(widget=forms.TextInput(attrs={'class': 'user-input'}))


class ClientAddForm(UserCreationForm):
    username = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control',
            }
        ),
        label="Username",
    )
    address = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control',
            }
        ),
        label="Address",
    )

    phone = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control',
            }
        ),
        label="Mobile No.",
    )

    first_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control',
            }
        ),
        label="First name",
    )

    last_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control',
            }
        ),
        label="Last name",
    )

    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={
                'type': 'email',
                'class': 'form-control',
            }
        ),
        label="Email Address",
    )


    password1 = forms.CharField(
        max_length=30, widget=forms.TextInput(attrs={'type': 'password', 'class': 'form-control', }),
        label="Password", )

    password2 = forms.CharField(
        max_length=30, widget=forms.TextInput(attrs={'type': 'password', 'class': 'form-control', }),
        label="Password Confirmation", )

    # def validate_email(self):
    #     email = self.cleaned_data['email']
    #     if User.objects.filter(email__iexact=email, is_active=True).exists():
    #         raise forms.ValidationError("Email has taken, try another email address. ")

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic()
    def save(self):
        user = super().save(commit=False)
        user.is_parent = True
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.address = self.cleaned_data.get('address')
        user.phone = self.cleaned_data.get('phone')
        user.email = self.cleaned_data.get('email')
        user.save()
        parent = Client.objects.create(
            user=user
        )
        parent.save()
        return user


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['students','title', 'content']  # Add other fields as needed


class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label='Email', max_length=254,
                             widget=forms.EmailInput(attrs={'autocomplete': 'email'}))


class EmailValidationOnForgotPassword(PasswordResetForm):
    def clean_email(self):
        email = self.cleaned_data.get('email')  # Use get() method to avoid KeyError
        if email:
            if not User.objects.filter(email__iexact=email, is_active=True).exists():
                msg = "There is no user registered with the specified E-mail address."
                self.add_error('email', msg)
        return email





######################################

class CookiesConsentForm(forms.Form):
    consent_given = forms.BooleanField(label='I consent to the use of cookies', required=False)


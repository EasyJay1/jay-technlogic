from django.test import TestCase

# Create your tests here.
class CustomSignupForm(UserCreationForm):
    phone_number = forms.IntegerField(validators=[MaxValueValidator(99999999999)])
    first_name = forms.CharField(max_length=20)
    last_name = forms.CharField(max_length=20)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'email', 'phone_number', 'first_name', 'last_name', 'password1', 'password2']

    def save(self, commit=True):
        user = super(CustomSignupForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']  # Assign first name
        user.last_name = self.cleaned_data['last_name']    # Assign last name
        phone_number = self.cleaned_data['phone_number']
        if commit:
            user.save()
            phone_obj = PhoneNumber.objects.create(user=user, phone_number=phone_number,)
        return user

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email address is already registered. Please reset your password')
        return email

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if PhoneNumber.objects.filter(phone_number=phone_number).exists():
            raise forms.ValidationError('Phone number is already registered.')
        return phone_number

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            new_usernames = []
            for _ in range(2):
                while True:
                    random_number = str(random.randint(10000, 99999))
                    new_username = self.cleaned_data.get('username') + random_number
                    if not User.objects.filter(username=new_username).exists():
                        new_usernames.append(new_username)
                        break

            error_message = f'Username is already taken. Available options: \n {", ".join(new_usernames)}'
            raise forms.ValidationError(error_message)
        return username



###################################################################################################
class CustomSignupView(SignupView):
    form_class = CustomSignupForm
    template_name = 'account/signup.html'

    def form_valid(self, form):
        user = form.save()
        messages.warning(self.request, 'Successful! Please Login to Verify Your Email')
        return redirect('checker')

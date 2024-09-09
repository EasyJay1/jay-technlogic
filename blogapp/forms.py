from .models import Blogs
from .models import Testimonies
from django import forms
from .models import Appointment


class TestimonyForm(forms.ModelForm):
    class Meta:
        model = Testimonies
        fields = ['content']

class AppointmentForm(forms.ModelForm):
    time_choices = [(f'{hour}:00', f'{hour}:00') for hour in range(24)]
    time = forms.ChoiceField(choices=time_choices, label='Select Time')
    date = forms.DateField(label='Select Date', widget=forms.DateInput(attrs={'type': 'date'}))

  #  countries = [(country.name, country.name) for country in pycountry.countries]
 #   location = forms.ChoiceField(choices=countries, label='Select Country')

    class Meta:
        model = Appointment
        fields = ['date', 'time', 'communication_method']

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get('date')
        time = cleaned_data.get('time')
        if date and time:
            combined_datetime = f"{date} {time}"  # Combine date and time
            cleaned_data['booked_for'] = combined_datetime
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        if 'booked_for' in self.cleaned_data:
            instance.booked_for = self.cleaned_data['booked_for']
        if commit:
            instance.save()
        return instance


# news and events
class BlogsForm(forms.ModelForm):
    class Meta:
        model = Blogs
        fields = ('title', 'summary', 'posted_as', 'image')  # Include the 'image' field

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['summary'].widget.attrs.update({'class': 'form-control'})
        self.fields['posted_as'].widget.attrs.update({'class': 'form-control'})
        self.fields['image'].widget.attrs.update({
            'class': 'form-control',
            'accept': 'image/*',  # Allow only image files
        })


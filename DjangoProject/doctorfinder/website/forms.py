from django import forms
from localflavor.us.forms import USStateSelect, USZipCodeField
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from .models import Doctor, Insurance, User, Review

class SearchForm(forms.Form):
    speciality = forms.ChoiceField(widget=forms.Select, choices=Doctor.SPECIALITY_CHOICES)
    city = forms.CharField(max_length = 100)
    state = forms.CharField(widget = USStateSelect, max_length = 100)
    zip = USZipCodeField()
    insurance = forms.ChoiceField(widget = forms.Select, choices = Insurance.INSURANCE_CHOICES)

class SignUpForm(forms.ModelForm):   
    class Meta:
        model = User
        fields = ['username', 'name', 'password']

    confirm_password = forms.CharField(max_length = 100)

    #custom clean implementation to make sure passwords match
    def clean(self):
        if self.cleaned_data.get('password') != self.cleaned_data.get('confirm_password'):
            raise ValidationError('Passwords must match')
        return self.cleaned_data

class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = ('rating', 'comment')

class LoginForm(forms.Form):
    username = forms.EmailField()
    password = forms.CharField(max_length=256)

    def clean(self):
        try:
            user = User.objects.get(username=self.cleaned_data.get('username'))
        except ObjectDoesNotExist:
            raise ValidationError('Username is invalid')
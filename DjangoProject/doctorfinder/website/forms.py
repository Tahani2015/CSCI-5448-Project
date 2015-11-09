from django import forms
from localflavor.us.forms import USStateSelect, USZipCodeField
from .models import Doctor, Insurance

class SearchForm(forms.Form):
    specialty = forms.ChoiceField(widget=forms.Select, choices=Doctor.SPECIALITY_CHOICES)
    city = forms.CharField(max_length = 100)
    state = forms.CharField(widget = USStateSelect, max_length = 100)
    zip = USZipCodeField()
    insurance = forms.ChoiceField(widget = forms.Select, choices = Insurance.INSURANCE_CHOICES)

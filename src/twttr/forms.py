from django import forms
from RNN.models import *


class ContactForm(forms.Form):
    post = forms.CharField()


class RNNCriticForm(forms.ModelForm):
    
    class Meta:
        model = RNNCriticData
        fields = ['markedsentiment','user','review']
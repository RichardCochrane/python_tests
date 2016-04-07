from django import forms

from contacts.models import Contact
from avatar.models import Avatar


class ContactForm(forms.ModelForm):
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'First Name'}),
        error_messages={'required': 'Required'})
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Last Name'}),
        error_messages={'required': 'Required'})

    class Meta:
        model = Contact
        fields = ('first_name', 'last_name', 'nick_name', 'code_name', 'telephone_number', 'email')

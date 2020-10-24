from .models import AddToDatabase
from django import forms


class BookForm(forms.ModelForm):
    class Meta:
        model = AddToDatabase
        fields = ('email_name','pdf')
from django import forms
from .models import Book


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ["title", "published_date", "authors"]
        widgets = {
            "published_date": forms.DateInput(attrs={"type": "date"}),
            "authors": forms.CheckboxSelectMultiple(),
        }

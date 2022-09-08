from django import forms
from django.core.exceptions import ValidationError
from .models import Post



class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text', 'postAuthor', 'Category', 'categoryChoice']

    def clean(self):
        cleaned_data = super().clean()
        text = cleaned_data.get("description")
        if text is not None and len(text) < 20:
            raise ValidationError({
                "text": "Article cannot be less then 20 symbols."
            })

        return cleaned_data



from django.contrib.auth.models import User
from django.forms import ModelForm


class UpdateProfileForm(ModelForm):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
        ]
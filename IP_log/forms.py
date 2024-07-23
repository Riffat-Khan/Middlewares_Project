from django import forms
from .models import CustomUser, Profile
from django.contrib.auth.forms import UserCreationForm
from .enum import RoleChoice

class LoginForm(forms.Form):
    ROLE = [
    ("Gold" , "gold"),
    ("Silver" , "silver"),
    ("Bronze" , "bronze"),
]
    
    
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    role = forms.ChoiceField(choices=[(role.value, role.name) for role in RoleChoice], required=True)

    class Meta:
        model = CustomUser
        fields = ('email', 'password1', 'password2', 'role')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()

        profile = Profile(user=user, role=self.cleaned_data['role'], count=0)
        if commit:
            profile.save()
        return user
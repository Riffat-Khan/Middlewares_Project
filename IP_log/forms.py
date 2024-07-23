from django import forms

class LoginForm(forms.Form):
    ROLE = [
    ("Gold" , "gold"),
    ("Silver" , "silver"),
    ("Bronze" , "bronze"),
]
    
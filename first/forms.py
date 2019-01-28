from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CalcForm(forms.Form):

    first = forms.IntegerField(
        label='Первое число',
        min_value=0,
        max_value=10000,
    )
    second = forms.IntegerField(
        label='Второе число',
        min_value=0,
        max_value=10000,
    )

class SquadEquation(forms.Form):
    a = forms.IntegerField(
        label='x^2',
        min_value=-10000,
        max_value=10000,
    )
    b = forms.IntegerField(
        label='x',
        min_value=-10000,
        max_value=10000,
    )
    c = forms.IntegerField(
        label='',
        min_value=-10000,
        max_value=10000,
    )

class str2wordsForm(forms.Form):
    stroka = forms.CharField(label='stroka', max_length=255)


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


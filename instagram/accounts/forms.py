from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms


class MyUserCreationForm(UserCreationForm):
    avatar = forms.ImageField()

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ['username',
                  'password1',
                  'password2',
                  'first_name',
                  'description',
                  'gender',
                  'avatar']


class UserChangeForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'email']
        labels = {'first_name': 'Имя', 'last_name': 'Фамилия', 'email': 'Email'}

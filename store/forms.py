from django import forms
from .models import Customer
from django.contrib.auth.forms import UserCreationForm


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = Customer
        fields = ['username', 'email', 'phone',
                  'address', 'password1', 'password2']

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')

        phone_number = ''.join(filter(str.isdigit, phone_number))

        if len(phone_number) < 10 or len(phone_number) > 15:
            raise forms.ValidationError(
                'El número de teléfono debe tener entre 10 y 15 dígitos.')

        return phone_number

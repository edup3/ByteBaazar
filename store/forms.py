from django import forms
from .models import Customer, Review
from django.contrib.auth.forms import UserCreationForm


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = Customer
        fields = ['username', 'email', 'phone',
                  'address', 'password1', 'password2']

    def clean_phone(self):
        phone_number = self.cleaned_data.get('phone')
        if not phone_number.isnumeric():
            raise forms.ValidationError(
                'El número de teléfono debe ser numerico')

        if len(phone_number) < 10 or len(phone_number) > 15:
            raise forms.ValidationError(
                'El número de teléfono debe tener entre 10 y 15 dígitos.')

        return phone_number


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5}),
            'comment': forms.Textarea(attrs={'rows': 3}),
        }

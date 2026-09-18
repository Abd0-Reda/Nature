from django import forms
from .models import Product
from .models import Review
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import ContactMessage

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'category', 'image']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['comment', 'rating']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 3}),
            'rating': forms.RadioSelect(choices=[(i, f'{i} ⭐') for i in range(1, 6)])
        }

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']        

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['first_name', 'last_name', 'email', 'phone', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 4}),
        }
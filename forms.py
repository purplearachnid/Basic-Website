from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import UploadedPDF


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class LoginForm(AuthenticationForm):
    pass

class PDFUploadForm(forms.ModelForm):
    class Meta:
        model = UploadedPDF
        fields = ['pdf_file']
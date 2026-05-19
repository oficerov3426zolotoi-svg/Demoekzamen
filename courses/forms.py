from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Application, Course, Review


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=150, label='Логин')
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль')
    confirm_password = forms.CharField(widget=forms.PasswordInput, label='Подтвердите пароль')
    full_name = forms.CharField(max_length=255, label='ФИО')
    phone = forms.CharField(max_length=20, label='Телефон')
    email = forms.EmailField(label='E-mail')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if len(username) < 6:
            raise ValidationError('Логин должен содержать минимум 6 символов')
        if not username.replace('_', '').replace('-', '').isalnum():
            raise ValidationError('Логин должен содержать только латинские буквы и цифры')
        if User.objects.filter(username=username).exists():
            raise ValidationError('Такой логин уже существует')
        return username

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            raise ValidationError('Пароль должен содержать минимум 8 символов')
        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            raise ValidationError('Пароли не совпадают')


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, label='Логин')
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль')


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['course', 'start_date', 'payment_method']
        labels = {
            'course': 'Курс',
            'start_date': 'Дата начала обучения',
            'payment_method': 'Способ оплаты',
        }
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
        }


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['text']
        labels = {
            'text': 'Отзыв',
        }
        widgets = {
            'text': forms.Textarea(attrs={'rows': 4}),
        }
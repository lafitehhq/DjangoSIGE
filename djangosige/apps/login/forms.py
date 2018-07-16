# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy as _

from .models import Usuario

# Form para login do usuario


class UserLoginForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('username', 'password')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control line-input', 'placeholder': '账号'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control line-input', 'placeholder': '密码'}),
        }
        labels = {
            'username': _(u'person'),
            'password': _(u'lock'),
        }

    # Validar/autenticar campos de login
    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if not user or not user.is_active:
            raise forms.ValidationError(u"Usuário ou senha inválidos.")
        return self.cleaned_data

    def authenticate_user(self, username, password):
        user = authenticate(username=username, password=password)
        if not user or not user.is_active:
            raise forms.ValidationError(u"Usuário ou senha inválidos.")
        return user


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control line-input', 'placeholder': '密码'}), min_length=6, label='lock')
    confirm = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control line-input', 'placeholder': '确认密码'}), min_length=6, label='lock')
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control line-input', 'placeholder': '账号'}), label='person')
    email = forms.CharField(widget=forms.EmailInput(attrs={
                            'class': 'form-control line-input', 'placeholder': '邮箱'}), label='email', required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'password',)


class PasswordResetForm(forms.Form):
    email_or_username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control line-input', 'placeholder': '注册邮箱'}))


class SetPasswordForm(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control line-input', 'placeholder': '新密码'}), min_length=6)
    new_password_confirm = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control line-input', 'placeholder': '确认新密码'}), min_length=6)


class PerfilUsuarioForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control'}), label='使用者名称')
    first_name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control'}), label='名', required=False)
    last_name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control'}), label='姓', required=False)
    email = forms.CharField(widget=forms.EmailInput(
        attrs={'class': 'form-control'}), label='邮箱', required=False)
    user_foto = forms.ImageField(widget=forms.FileInput(
        attrs={'class': 'form-control', 'accept': 'image/*'}), label='头像', required=False)

    def __init__(self, *args, **kwargs):
        super(PerfilUsuarioForm, self).__init__(*args, **kwargs)
        self.fields['username'].initial = self.instance.user.username
        self.fields['first_name'].initial = self.instance.user.first_name
        self.fields['last_name'].initial = self.instance.user.last_name
        self.fields['email'].initial = self.instance.user.email

    class Meta:
        model = Usuario
        fields = ('first_name', 'last_name', 'username', 'email', 'user_foto',)

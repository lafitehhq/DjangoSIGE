# -*- coding: utf-8 -*-

from django import forms
from django.forms import inlineformset_factory
from django.utils.translation import ugettext_lazy as _

from djangosige.apps.cadastro.models import Pessoa, Endereco, Telefone, Email, Site, Banco, Documento


class EnderecoForm(forms.ModelForm):

    class Meta:
        model = Endereco
        fields = ('tipo_endereco', 'logradouro', 'numero', 'bairro',
                  'complemento', 'pais', 'cpais', 'uf', 'cep', 'municipio', 'cmun',)

        labels = {
            'tipo_endereco': _('类型'),
            'logradouro': _("地址"),
            'numero': _("数量"),
            'bairro': _("所在区"),
            'complemento': _("补充"),
            'pais': _("国家"),
            'cpais': _("国家代码"),
            'municipio': _("市"),
            'cmun': _("市政代码"),
            'cep': _("CEP(只有数字)"),
            'uf': _("UF"),
        }
        widgets = {
            'tipo_endereco': forms.Select(attrs={'class': 'form-control'}),
            'logradouro': forms.TextInput(attrs={'class': 'form-control'}),
            'numero': forms.TextInput(attrs={'class': 'form-control'}),
            'bairro': forms.TextInput(attrs={'class': 'form-control'}),
            'complemento': forms.TextInput(attrs={'class': 'form-control'}),
            'pais': forms.TextInput(attrs={'class': 'form-control'}),
            'cpais': forms.TextInput(attrs={'class': 'form-control'}),
            'municipio': forms.Select(attrs={'class': 'form-control'}),
            'cmun': forms.TextInput(attrs={'class': 'form-control'}),
            'cep': forms.TextInput(attrs={'class': 'form-control'}),
            'uf': forms.Select(attrs={'class': 'form-control'}),
        }


class TelefoneForm(forms.ModelForm):

    class Meta:
        model = Telefone
        fields = ('tipo_telefone', 'telefone',)
        labels = {
            'tipo_telefone': _("电话"),
            'telefone': _(''),
        }
        widgets = {
            'tipo_telefone': forms.Select(attrs={'class': 'form-control'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control'}),
        }


class EmailForm(forms.ModelForm):

    class Meta:
        model = Email
        fields = ('email',)
        labels = {
            'email': _('邮箱')
        }
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }


class SiteForm(forms.ModelForm):

    class Meta:
        model = Site
        fields = ('site',)
        labels = {
            'site': _('所在地'),
        }
        widgets = {
            'site': forms.TextInput(attrs={'class': 'form-control'}),
        }


class BancoForm(forms.ModelForm):

    class Meta:
        model = Banco
        fields = ('banco', 'agencia', 'conta', 'digito',)
        labels = {
            'banco': _('总行'),
            'agencia': _('支行'),
            'conta': _('银行账户'),
            'digito': _('银行账号'),
        }
        widgets = {
            'banco': forms.Select(attrs={'class': 'form-control'}),
            'agencia': forms.TextInput(attrs={'class': 'form-control'}),
            'conta': forms.TextInput(attrs={'class': 'form-control'}),
            'digito': forms.TextInput(attrs={'class': 'form-control'}),
        }


class DocumentoForm(forms.ModelForm):

    class Meta:
        model = Documento
        fields = ('tipo', 'documento',)
        labels = {
            'tipo': _('类型'),
            'documento': _('文件'),
        }
        widgets = {
            'tipo': forms.TextInput(attrs={'class': 'form-control'}),
            'documento': forms.TextInput(attrs={'class': 'form-control'}),
        }


EnderecoFormSet = inlineformset_factory(
    Pessoa, Endereco, form=EnderecoForm, extra=1, can_delete=True)
TelefoneFormSet = inlineformset_factory(
    Pessoa, Telefone, form=TelefoneForm, extra=1, can_delete=True)
EmailFormSet = inlineformset_factory(
    Pessoa, Email, form=EmailForm, extra=1, can_delete=True)
SiteFormSet = inlineformset_factory(
    Pessoa, Site, form=SiteForm, extra=1, can_delete=True)
BancoFormSet = inlineformset_factory(
    Pessoa, Banco, form=BancoForm, extra=1, can_delete=True)
DocumentoFormSet = inlineformset_factory(
    Pessoa, Documento, form=DocumentoForm, extra=1, can_delete=True)

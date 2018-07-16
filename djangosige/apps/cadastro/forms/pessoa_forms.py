# -*- coding: utf-8 -*-

from django import forms
from django.utils.translation import ugettext_lazy as _

from djangosige.apps.cadastro.models import PessoaJuridica, PessoaFisica


class PessoaJuridicaForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        if 'instance' in kwargs:
            instance = kwargs.pop('instance')
            instance = PessoaJuridica.objects.get(pk=instance.pk)
            super(PessoaJuridicaForm, self).__init__(
                instance=instance, *args, **kwargs)
        else:
            super(PessoaJuridicaForm, self).__init__(*args, **kwargs)

    class Meta:
        model = PessoaJuridica
        fields = ('nome_fantasia', 'cnpj', 'inscricao_estadual',
                  'responsavel', 'sit_fiscal', 'suframa',)

        widgets = {
            'nome_fantasia': forms.TextInput(attrs={'class': 'form-control'}),
            'cnpj': forms.TextInput(attrs={'class': 'form-control'}),
            'inscricao_estadual': forms.TextInput(attrs={'class': 'form-control'}),
            'responsavel': forms.TextInput(attrs={'class': 'form-control'}),
            'sit_fiscal': forms.Select(attrs={'class': 'form-control'}),
            'suframa': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'nome_fantasia': _('公司名称'),
            'cnpj': _('法人税号'),
            'inscricao_estadual': _('申请状态'),
            'responsavel': _('负责人'),
            'sit_fiscal': _('税金'),
            'suframa': _('注册登记号 '),
        }


class PessoaFisicaForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        if 'instance' in kwargs:
            instance = kwargs.pop('instance')
            instance = PessoaFisica.objects.get(pk=instance.pk)
            super(PessoaFisicaForm, self).__init__(
                instance=instance, *args, **kwargs)
        else:
            super(PessoaFisicaForm, self).__init__(*args, **kwargs)

    class Meta:
        model = PessoaFisica
        fields = ('cpf', 'rg', 'nascimento', )

        widgets = {
            'cpf': forms.TextInput(attrs={'class': 'form-control'}),
            'rg': forms.TextInput(attrs={'class': 'form-control'}),
            'nascimento': forms.DateInput(attrs={'class': 'form-control datepicker'}),
        }
        labels = {
            'cpf': _('CPF'),
            'rg': _('RG'),
            'nascimento': _('创建时间'),
        }

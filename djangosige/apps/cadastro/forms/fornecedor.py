# -*- coding: utf-8 -*-

from django import forms
from django.utils.translation import ugettext_lazy as _

from djangosige.apps.cadastro.models import Fornecedor


class FornecedorForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(FornecedorForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Fornecedor
        fields = ('nome_razao_social', 'tipo_pessoa',
                  'inscricao_municipal', 'ramo', 'informacoes_adicionais', )
        widgets = {
            'nome_razao_social': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_pessoa': forms.RadioSelect(attrs={'class': 'form-control'}),
            'ramo': forms.TextInput(attrs={'class': 'form-control'}),
            'inscricao_municipal': forms.TextInput(attrs={'class': 'form-control'}),
            'informacoes_adicionais': forms.Textarea(attrs={'class': 'form-control'}),
        }
        labels = {
            'nome_razao_social': _('法人名称'),
            'tipo_pessoa': _(''),
            'ramo': _('Ramo'),
            'inscricao_municipal': _('所在的城市'),
            'informacoes_adicionais': _('备注'),
        }

    def save(self, commit=True):
        instance = super(FornecedorForm, self).save(commit=False)
        instance.criado_por = self.request.user
        if commit:
            instance.save()
        return instance

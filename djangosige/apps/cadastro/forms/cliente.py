# -*- coding: utf-8 -*-

from django import forms
from django.utils.translation import ugettext_lazy as _

from djangosige.apps.cadastro.models import Cliente


class ClienteForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(ClienteForm, self).__init__(*args, **kwargs)
        self.fields['limite_de_credito'].localize = True

    class Meta:
        model = Cliente
        fields = ('nome_razao_social', 'tipo_pessoa', 'inscricao_municipal',
                  'limite_de_credito', 'indicador_ie', 'id_estrangeiro', 'informacoes_adicionais', )
        widgets = {
            'nome_razao_social': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_pessoa': forms.RadioSelect(attrs={'class': 'form-control'}),
            'limite_de_credito': forms.TextInput(attrs={'class': 'form-control decimal-mask'}),
            'indicador_ie': forms.Select(attrs={'class': 'form-control'}),
            'inscricao_municipal': forms.TextInput(attrs={'class': 'form-control'}),
            'id_estrangeiro': forms.TextInput(attrs={'class': 'form-control'}),
            'informacoes_adicionais': forms.Textarea(attrs={'class': 'form-control'}),
        }
        labels = {
            'nome_razao_social': _('法人名称'),
            'tipo_pessoa': _(''),
            'limite_de_credito': _('贷款限额'),
            'indicador_ie': _('收货人IE指标'),
            'inscricao_municipal': _('所在的城市'),
            'id_estrangeiro': _('法律文件(外国)'),
            'informacoes_adicionais': _('额外信息'),
        }

    def save(self, commit=True):
        instance = super(ClienteForm, self).save(commit=False)
        instance.criado_por = self.request.user
        if commit:
            instance.save()
        return instance

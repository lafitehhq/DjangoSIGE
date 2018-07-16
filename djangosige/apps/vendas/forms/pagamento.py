# -*- coding: utf-8 -*-

from django import forms
from django.utils.translation import ugettext_lazy as _
from django.forms import inlineformset_factory

from djangosige.apps.vendas.models import Venda, Pagamento, CondicaoPagamento


class PagamentoForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(PagamentoForm, self).__init__(*args, **kwargs)
        self.fields['valor_parcela'].localize = True

    class Meta:
        model = Pagamento
        fields = ('indice_parcela', 'vencimento', 'valor_parcela',)
        widgets = {
            'indice_parcela': forms.TextInput(attrs={'class': 'form-control', 'readonly': True}),
            'vencimento': forms.DateInput(attrs={'class': 'form-control datepicker'}),
            'valor_parcela': forms.TextInput(attrs={'class': 'form-control decimal-mask'}),
        }
        labels = {
            'indice_parcela': _('包裹'),
            'vencimento': _('到期日'),
            'valor_parcela': _('票据'),
        }


class CondicaoPagamentoForm(forms.ModelForm):

    class Meta:
        model = CondicaoPagamento
        fields = ('descricao', 'forma', 'n_parcelas',
                  'dias_recorrencia', 'parcela_inicial',)
        widgets = {
            'descricao': forms.TextInput(attrs={'class': 'form-control', 'title': '对付款条件的简要说明, EX: Entrada + 3x s/ juros'}),
            'forma': forms.Select(attrs={'class': 'form-control'}),
            'n_parcelas': forms.NumberInput(attrs={'class': 'form-control'}),
            'dias_recorrencia': forms.NumberInput(attrs={'class': 'form-control'}),
            'parcela_inicial': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'descricao': _('说明'),
            'forma': _('形式'),
            'n_parcelas': _('包裹数'),
            'dias_recorrencia': _('复发率(天)'),
            'parcela_inicial': _('第一期(天)'),
        }


PagamentoFormSet = inlineformset_factory(
    Venda, Pagamento, form=PagamentoForm, extra=1, can_delete=True)

# -*- coding: utf-8 -*-

from django import forms
from django.utils.translation import ugettext_lazy as _
from django.forms import inlineformset_factory

from djangosige.apps.vendas.models import OrcamentoVenda, PedidoVenda, ItensVenda, Venda


class VendaForm(forms.ModelForm):
    total_sem_imposto = forms.DecimalField(widget=forms.TextInput(
        attrs={'class': 'form-control decimal-mask', 'readonly': True}), label='Total s/ imposto (R$)', required=False)

    def __init__(self, *args, **kwargs):
        super(VendaForm, self).__init__(*args, **kwargs)
        self.fields['status'].initial = '0'

        self.fields['total_sem_imposto'].localize = True
        self.fields['total_sem_imposto'].initial = '0.00'

        self.fields['valor_total'].localize = True
        self.fields['valor_total'].initial = '0.00'

        self.fields['desconto'].localize = True
        self.fields['desconto'].initial = '0.00'

        self.fields['despesas'].localize = True
        self.fields['despesas'].initial = '0.00'

        self.fields['seguro'].localize = True
        self.fields['seguro'].initial = '0.00'

        self.fields['frete'].localize = True
        self.fields['frete'].initial = '0.00'

        self.fields['impostos'].localize = True
        self.fields['impostos'].initial = '0.00'

    class Meta:
        fields = ('data_emissao', 'cliente', 'ind_final', 'transportadora', 'mod_frete', 'veiculo', 'vendedor', 'desconto', 'local_orig',
                  'movimentar_estoque', 'tipo_desconto', 'frete', 'despesas', 'seguro', 'impostos', 'valor_total', 'cond_pagamento', 'observacoes',)

        widgets = {
            'data_emissao': forms.DateInput(attrs={'class': 'form-control datepicker'}),
            'cliente': forms.Select(attrs={'class': 'form-control'}),
            'ind_final': forms. CheckboxInput(attrs={'class': 'form-control'}),
            'transportadora': forms.Select(attrs={'class': 'form-control'}),
            'mod_frete': forms.Select(attrs={'class': 'form-control'}),
            'local_orig': forms.Select(attrs={'class': 'form-control'}),
            'movimentar_estoque': forms.CheckboxInput(attrs={'class': 'form-control'}),
            'veiculo': forms.Select(attrs={'class': 'form-control'}),
            'vendedor': forms.TextInput(attrs={'class': 'form-control'}),
            'valor_total': forms.TextInput(attrs={'class': 'form-control decimal-mask', 'readonly': True}),
            'tipo_desconto': forms.Select(attrs={'class': 'form-control'}),
            'desconto': forms.TextInput(attrs={'class': 'form-control decimal-mask-four'}),
            'frete': forms.TextInput(attrs={'class': 'form-control decimal-mask'}),
            'despesas': forms.TextInput(attrs={'class': 'form-control decimal-mask'}),
            'seguro': forms.TextInput(attrs={'class': 'form-control decimal-mask'}),
            'impostos': forms.TextInput(attrs={'class': 'form-control decimal-mask', 'readonly': True}),
            'cond_pagamento': forms.Select(attrs={'class': 'form-control'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control'}),
        }
        labels = {
            'data_emissao': _('签发日期'),
            'cliente': _('Cliente'),
            'ind_final': _('Consumidor final?'),
            'transportadora': _('Transportadora'),
            'mod_frete': _('Modalidade do frete'),
            'local_orig': _('Localização de estoque de origem dos produtos'),
            'movimentar_estoque': _('Movimentar estoque?'),
            'veiculo': _('运载工具'),
            'vendedor': _('推销员'),
            'valor_total': _('汇总 (R$)'),
            'tipo_desconto': _('折扣类型'),
            'desconto': _('折扣 (% ou R$)'),
            'frete': _('货运费用 (R$)'),
            'despesas': _('支出 (R$)'),
            'seguro': _('保险 (R$)'),
            'impostos': _('关税 (R$)'),
            'cond_pagamento': _('付款条件'),
            'observacoes': _('备注'),
        }


class OrcamentoVendaForm(VendaForm):

    class Meta(VendaForm.Meta):
        model = OrcamentoVenda
        fields = VendaForm.Meta.fields + ('data_vencimento', 'status',)
        widgets = VendaForm.Meta.widgets
        widgets['data_vencimento'] = forms.DateInput(
            attrs={'class': 'form-control datepicker'})
        widgets['status'] = forms.Select(
            attrs={'class': 'form-control', 'disabled': True})
        labels = VendaForm.Meta.labels
        labels['data_vencimento'] = _('到期日期')
        labels['status'] = _('状态')


class PedidoVendaForm(VendaForm):

    class Meta(VendaForm.Meta):
        model = PedidoVenda
        fields = VendaForm.Meta.fields + \
            ('data_entrega', 'status', 'orcamento',)
        widgets = VendaForm.Meta.widgets
        widgets['data_entrega'] = forms.DateInput(
            attrs={'class': 'form-control datepicker'})
        widgets['status'] = forms.Select(
            attrs={'class': 'form-control', 'disabled': True})
        widgets['orcamento'] = forms.Select(
            attrs={'class': 'form-control', 'disabled': True})
        labels = VendaForm.Meta.labels
        labels['data_entrega'] = _('交付日期')
        labels['status'] = _('装填')
        labels['orcamento'] = _('预算')


class ItensVendaForm(forms.ModelForm):
    total_sem_desconto = forms.DecimalField(widget=forms.TextInput(
        attrs={'class': 'form-control decimal-mask', 'readonly': True}), label='Subtotal s/ desconto', required=False)
    total_impostos = forms.DecimalField(widget=forms.TextInput(
        attrs={'class': 'form-control decimal-mask', 'readonly': True}), label='税', required=False)
    total_com_impostos = forms.DecimalField(widget=forms.TextInput(
        attrs={'class': 'form-control decimal-mask', 'readonly': True}), label='总价', required=False)
    calculo_imposto = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'hidden', 'disabled': True}), label='税收计算器', required=False)

    # IMPOSTO
    p_red_bc = forms.DecimalField(widget=forms.TextInput(
        attrs={'class': 'modal-field', 'disabled': True}), required=False)
    p_red_bcst = forms.DecimalField(widget=forms.TextInput(
        attrs={'class': 'modal-field', 'disabled': True}), required=False)
    p_mvast = forms.DecimalField(widget=forms.TextInput(
        attrs={'class': 'modal-field', 'disabled': True}), required=False)
    pfcp = forms.DecimalField(widget=forms.TextInput(
        attrs={'class': 'modal-field', 'disabled': True}), required=False)
    p_icms_dest = forms.DecimalField(widget=forms.TextInput(
        attrs={'class': 'modal-field', 'disabled': True}), required=False)
    p_icms_inter = forms.DecimalField(widget=forms.TextInput(
        attrs={'class': 'modal-field', 'disabled': True}), required=False)
    p_icms_part = forms.DecimalField(widget=forms.TextInput(
        attrs={'class': 'modal-field', 'disabled': True}), required=False)
    tipo_ipi = forms.ChoiceField(widget=forms.Select(
        attrs={'class': 'modal-field', 'disabled': True}), choices=([('1', '1'), ('2', '2'), ('3', '3'), ]), required=False)
    vfixo_ipi = forms.DecimalField(widget=forms.TextInput(
        attrs={'class': 'modal-field', 'disabled': True}), required=False)

    def __init__(self, *args, **kwargs):
        super(ItensVendaForm, self).__init__(*args, **kwargs)
        self.fields['quantidade'].localize = True
        self.fields['valor_unit'].localize = True
        self.fields['desconto'].localize = True
        self.fields['subtotal'].localize = True

        self.fields['total_sem_desconto'].localize = True
        self.fields['total_impostos'].localize = True
        self.fields['total_com_impostos'].localize = True

        self.fields['valor_rateio_frete'].localize = True
        self.fields['valor_rateio_despesas'].localize = True
        self.fields['valor_rateio_seguro'].localize = True

        self.fields['vbc_icms'].localize = True
        self.fields['vbc_icms_st'].localize = True
        self.fields['vbc_ipi'].localize = True
        self.fields['vfcp'].localize = True
        self.fields['vicmsufdest'].localize = True
        self.fields['vicmsufremet'].localize = True

        self.fields['vicms'].localize = True
        self.fields['vicms_st'].localize = True
        self.fields['vipi'].localize = True
        self.fields['p_icmsst'].localize = True
        self.fields['p_icms'].localize = True
        self.fields['p_ipi'].localize = True

    class Meta:
        model = ItensVenda
        fields = ('produto', 'quantidade', 'valor_unit', 'tipo_desconto', 'desconto', 'valor_rateio_frete', 'valor_rateio_despesas', 'valor_rateio_seguro',
                  'vbc_icms', 'vbc_icms_st', 'vbc_ipi',
                  'subtotal', 'vicms', 'vicms_st', 'vipi', 'p_icms', 'p_ipi', 'p_icmsst', 'vfcp', 'vicmsufdest', 'vicmsufremet',
                  'ipi_incluido_preco', 'icms_incluido_preco', 'icmsst_incluido_preco', 'incluir_bc_icms', 'incluir_bc_icmsst', 'auto_calcular_impostos',)

        widgets = {
            'produto': forms.Select(attrs={'class': 'form-control select-produto'}),
            'quantidade': forms.TextInput(attrs={'class': 'form-control decimal-mask'}),
            'valor_unit': forms.TextInput(attrs={'class': 'form-control decimal-mask'}),
            'subtotal': forms.TextInput(attrs={'class': 'form-control decimal-mask', 'readonly': True}),
            'tipo_desconto': forms.Select(attrs={'class': 'form-control'}),
            'desconto': forms.TextInput(attrs={'class': 'form-control decimal-mask'}),

            'valor_rateio_frete': forms.TextInput(attrs={'class': 'form-control decimal-mask'}),
            'valor_rateio_despesas': forms.TextInput(attrs={'class': 'form-control decimal-mask'}),
            'valor_rateio_seguro': forms.TextInput(attrs={'class': 'form-control decimal-mask'}),

            'vbc_icms': forms.TextInput(attrs={'class': 'modal-field'}),
            'vbc_icms_st': forms.TextInput(attrs={'class': 'modal-field'}),
            'vbc_ipi': forms.TextInput(attrs={'class': 'modal-field'}),

            'vicms': forms.TextInput(attrs={'class': 'modal-field'}),
            'vicms_st': forms.TextInput(attrs={'class': 'modal-field'}),
            'vipi': forms.TextInput(attrs={'class': 'modal-field'}),
            'vfcp': forms.TextInput(attrs={'class': 'modal-field'}),
            'vicmsufdest': forms.TextInput(attrs={'class': 'modal-field'}),
            'vicmsufremet': forms.TextInput(attrs={'class': 'modal-field'}),
            'p_icmsst': forms.TextInput(attrs={'class': 'modal-field'}),
            'p_icms': forms.TextInput(attrs={'class': 'modal-field'}),
            'p_ipi': forms.TextInput(attrs={'class': 'modal-field'}),

            'ipi_incluido_preco': forms.CheckboxInput(attrs={'class': 'modal-field'}),
            'icms_incluido_preco': forms.CheckboxInput(attrs={'class': 'modal-field'}),
            'icmsst_incluido_preco': forms.CheckboxInput(attrs={'class': 'modal-field'}),
            'incluir_bc_icms': forms.CheckboxInput(attrs={'class': 'modal-field'}),
            'incluir_bc_icmsst': forms.CheckboxInput(attrs={'class': 'modal-field'}),
            'auto_calcular_impostos': forms.CheckboxInput(attrs={'class': 'modal-field'}),

        }
        labels = {
            'produto': _('产品'),
            'quantidade': _('数量'),
            'valor_unit': _('单位'),
            'subtotal': _('小计'),

            'tipo_desconto': _('折扣类型'),
            'desconto': _('Desconto (% ou R$)'),
            'valor_rateio_frete': _('货运费用(R$)'),
            'valor_rateio_despesas': _('支出(R$)'),
            'valor_rateio_seguro': _('保险(R$)'),

        }

    def is_valid(self):
        valid = super(ItensVendaForm, self).is_valid()
        if self.cleaned_data.get('produto', None) is None:
            self.cleaned_data = {}
        return valid


ItensVendaFormSet = inlineformset_factory(
    Venda, ItensVenda, form=ItensVendaForm, extra=1, can_delete=True)

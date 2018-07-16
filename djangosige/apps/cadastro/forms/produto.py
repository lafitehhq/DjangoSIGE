# -*- coding: utf-8 -*-

from django import forms
from django.utils.translation import ugettext_lazy as _

from djangosige.apps.cadastro.models import Produto, Unidade, Marca, Categoria, Fornecedor
from djangosige.apps.estoque.models import LocalEstoque

from decimal import Decimal


class ProdutoForm(forms.ModelForm):
    custo = forms.DecimalField(max_digits=16, decimal_places=2, localize=True, widget=forms.TextInput(
        attrs={'class': 'form-control decimal-mask', 'placeholder': 'R$ 0,00'}), initial=Decimal('0.00'), label='成本', required=False)
    venda = forms.DecimalField(max_digits=16, decimal_places=2, localize=True, widget=forms.TextInput(
        attrs={'class': 'form-control decimal-mask', 'placeholder': 'R$ 0,00'}), initial=Decimal('0.00'), label='售价', required=False)

    # Estoque
    estoque_inicial = forms.DecimalField(max_digits=16, decimal_places=2, localize=True, widget=forms.TextInput(
        attrs={'class': 'form-control decimal-mask'}), label='Qtd初始存货量', initial=Decimal('0.00'), required=False)
    fornecedor = forms.ChoiceField(choices=[(None, '----------')], widget=forms.Select(
        attrs={'class': 'form-control'}), label='Fornecedor', required=False)
    local_dest = forms.ModelChoiceField(queryset=LocalEstoque.objects.all(), widget=forms.Select(
        attrs={'class': 'form-control'}), empty_label=None, label='Localização do estoque de destino', required=False)

    def __init__(self, *args, **kwargs):
        super(ProdutoForm, self).__init__(*args, **kwargs)
        self.fields['estoque_minimo'].localize = True
        self.fields['fornecedor'].choices = list(self.fields['fornecedor'].choices) + [(
            fornecedor.id, fornecedor) for fornecedor in Fornecedor.objects.all()]

    class Meta:
        model = Produto
        fields = ('codigo', 'codigo_barras', 'descricao', 'categoria', 'marca', 'unidade', 'ncm', 'venda', 'custo', 'inf_adicionais',
                  'origem', 'cest', 'cfop_padrao', 'grupo_fiscal', 'estoque_minimo', 'controlar_estoque',)
        widgets = {
            'codigo': forms.TextInput(attrs={'class': 'form-control'}),
            'codigo_barras': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.TextInput(attrs={'class': 'form-control'}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            'marca': forms.Select(attrs={'class': 'form-control'}),
            'unidade': forms.Select(attrs={'class': 'form-control'}),
            'ncm': forms.TextInput(attrs={'class': 'form-control'}),
            'inf_adicionais': forms.Textarea(attrs={'class': 'form-control'}),
            'origem': forms.Select(attrs={'class': 'form-control'}),
            'cest': forms.TextInput(attrs={'class': 'form-control'}),
            'cfop_padrao': forms.Select(attrs={'class': 'form-control'}),
            'grupo_fiscal': forms.Select(attrs={'class': 'form-control'}),
            'estoque_minimo': forms.TextInput(attrs={'class': 'form-control decimal-mask'}),
            'controlar_estoque': forms.CheckboxInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'codigo': _('代码'),
            'codigo_barras': _('条码(GTIN/EAN)'),
            'descricao': _('说明'),
            'categoria': _('分类'),
            'marca': _('品牌'),
            'unidade': _('单位'),
            'ncm': _('NCM'),
            'inf_adicionais': _('备注'),
            'origem': _('产地'),
            'cest': _('CEST'),
            'cfop_padrao': _('CFOP(标准)'),
            'grupo_fiscal': _('税务组(模式)'),
            'estoque_minimo': _('Qtd最低限度'),
            'controlar_estoque': _('是否控制这个产品的库存?'),
        }


class CategoriaForm(forms.ModelForm):

    class Meta:
        model = Categoria
        fields = ('categoria_desc',)
        widgets = {
            'categoria_desc': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'categoria_desc': _('Categoria'),
        }


class MarcaForm(forms.ModelForm):

    class Meta:
        model = Marca
        fields = ('marca_desc',)
        widgets = {
            'marca_desc': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'marca_desc': _('Marca'),
        }


class UnidadeForm(forms.ModelForm):

    class Meta:
        model = Unidade
        fields = ('sigla_unidade', 'unidade_desc',)
        widgets = {
            'unidade_desc': forms.TextInput(attrs={'class': 'form-control'}),
            'sigla_unidade': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'unidade_desc': _('描述性名称'),
            'sigla_unidade': _('字符缩写'),
        }

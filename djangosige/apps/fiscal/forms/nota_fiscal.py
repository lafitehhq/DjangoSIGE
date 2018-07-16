# -*- coding: utf-8 -*-

from django import forms
from django.forms import inlineformset_factory
from django.utils.translation import ugettext_lazy as _

from djangosige.apps.fiscal.models import NotaFiscalSaida, NotaFiscalEntrada, AutXML, ConfiguracaoNotaFiscal, TP_AMB_ESCOLHAS, MOD_NFE_ESCOLHAS
from djangosige.apps.cadastro.models import Empresa

try:
    from pysignfe.nfe.manifestacao_destinatario import MD_CONFIRMACAO_OPERACAO, MD_DESCONHECIMENTO_OPERACAO, MD_OPERACAO_NAO_REALIZADA, MD_CIENCIA_OPERACAO
except ImportError:
    MD_CONFIRMACAO_OPERACAO = u'210200'
    MD_DESCONHECIMENTO_OPERACAO = u'210220'
    MD_OPERACAO_NAO_REALIZADA = u'210240'
    MD_CIENCIA_OPERACAO = u'210210'

TP_MANIFESTO_OPCOES = (
    (MD_CONFIRMACAO_OPERACAO, u'Confirmação da Operação'),
    (MD_DESCONHECIMENTO_OPERACAO, u'Desconhecimento da Operação'),
    (MD_OPERACAO_NAO_REALIZADA, u'Operação Não Realizada'),
    (MD_CIENCIA_OPERACAO, u'Ciência da Emissão (ou Ciência da Operação)'),
)


class NotaFiscalForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(NotaFiscalForm, self).__init__(*args, **kwargs)
        self.fields['dhemi'].input_formats = ('%d/%m/%Y %H:%M',)

    class Meta:
        fields = ('versao', 'status_nfe', 'natop', 'indpag', 'mod', 'serie', 'dhemi', 'dhsaient', 'iddest',
                  'tp_imp', 'tp_emis', 'tp_amb', 'fin_nfe', 'ind_final', 'ind_pres', 'inf_ad_fisco', 'inf_cpl',)

        widgets = {
            'versao': forms.Select(attrs={'class': 'form-control'}),
            'status_nfe': forms.Select(attrs={'class': 'form-control', 'disabled': True}),
            'natop': forms.TextInput(attrs={'class': 'form-control'}),
            'indpag': forms.Select(attrs={'class': 'form-control'}),
            'mod': forms.Select(attrs={'class': 'form-control'}),
            'serie': forms.TextInput(attrs={'class': 'form-control'}),
            'dhemi': forms.DateTimeInput(attrs={'class': 'form-control datetimepicker'}, format='%d/%m/%Y %H:%M'),
            'dhsaient': forms.DateTimeInput(attrs={'class': 'form-control datetimepicker'}, format='%d/%m/%Y %H:%M'),
            'iddest': forms.Select(attrs={'class': 'form-control'}),
            'tp_imp': forms.Select(attrs={'class': 'form-control'}),
            'tp_emis': forms.Select(attrs={'class': 'form-control'}),
            'tp_amb': forms.Select(attrs={'class': 'form-control'}),
            'fin_nfe': forms.Select(attrs={'class': 'form-control'}),
            'ind_final': forms.Select(attrs={'class': 'form-control'}),
            'ind_pres': forms.Select(attrs={'class': 'form-control'}),
            'inf_ad_fisco': forms.Textarea(attrs={'class': 'form-control'}),
            'inf_cpl': forms.Textarea(attrs={'class': 'form-control'}),
        }
        labels = {
            'versao': _('版本'),
            'status_nfe': _('状态'),
            'natop': _('操作性质'),
            'indpag': _('付款方式'),
            'mod': _('Modelo'),
            'serie': _('级数'),
            'dhemi': _('发行日期及时间'),
            'dhsaient': _('输出日期/时间'),
            'iddest': _('操作的目的'),
            'tp_imp': _('对DANFE的印象'),
            'tp_emis': _('发行形式'),
            'tp_amb': _('Ambiente'),
            'fin_nfe': _('发行目的'),
            'ind_final': _('最终消费者'),
            'ind_pres': _('Tipo de atendimento'),
            'inf_ad_fisco': _('税收利益的附加信息'),
            'inf_cpl': _('对纳税人利益的补充信息'),
        }

        error_messages = {
            'n_nf': {
                'unique': _("Nota fiscal com este número já existe"),
            },
        }


class NotaFiscalSaidaForm(NotaFiscalForm):

    def __init__(self, *args, **kwargs):
        super(NotaFiscalSaidaForm, self).__init__(*args, **kwargs)
        self.fields['v_orig'].localize = True
        self.fields['v_desc'].localize = True
        self.fields['v_liq'].localize = True

    class Meta(NotaFiscalForm.Meta):
        model = NotaFiscalSaida
        fields = NotaFiscalForm.Meta.fields + ('n_nf_saida', 'tpnf', 'venda', 'emit_saida',
                                               'dest_saida', 'n_fat', 'v_orig', 'v_desc', 'v_liq', 'grupo_cobr', 'arquivo_proc',)
        widgets = NotaFiscalForm.Meta.widgets
        widgets['n_nf_saida'] = forms.TextInput(
            attrs={'class': 'form-control'})
        widgets['venda'] = forms.Select(attrs={'class': 'form-control'})
        widgets['emit_saida'] = forms.Select(attrs={'class': 'form-control'})
        widgets['dest_saida'] = forms.Select(attrs={'class': 'form-control'})
        widgets['n_fat'] = forms.TextInput(attrs={'class': 'form-control'})
        widgets['tpnf'] = forms.Select(attrs={'class': 'form-control'})
        widgets['v_orig'] = forms.TextInput(
            attrs={'class': 'form-control decimal-mask'})
        widgets['v_desc'] = forms.TextInput(
            attrs={'class': 'form-control decimal-mask'})
        widgets['v_liq'] = forms.TextInput(
            attrs={'class': 'form-control decimal-mask'})
        widgets['grupo_cobr'] = forms.CheckboxInput(
            attrs={'class': 'form-control'})
        widgets['arquivo_proc'] = forms.FileInput(
            attrs={'class': 'form-control'})
        labels = NotaFiscalForm.Meta.labels
        labels['n_nf_saida'] = _('数目')
        labels['venda'] = _('Venda')
        labels['emit_saida'] = _('发行人(公司)')
        labels['dest_saida'] = _('收货人(客户)')
        labels['n_fat'] = _('发票号码')
        labels['tpnf'] = _('操作类型')
        labels['v_orig'] = _('发票的原始价值')
        labels['v_desc'] = _('贴现率')
        labels['v_liq'] = _('发票净额')
        labels['grupo_cobr'] = _(
            '在NF-e中插入恢复数据(发票/复制)?')
        labels['arquivo_proc'] = _('处理文件(*_procNFe.xml)')


class NotaFiscalEntradaForm(NotaFiscalForm):

    class Meta(NotaFiscalForm.Meta):
        model = NotaFiscalEntrada
        fields = NotaFiscalForm.Meta.fields + \
            ('n_nf_entrada', 'compra', 'emit_entrada', 'dest_entrada',)
        widgets = NotaFiscalForm.Meta.widgets
        widgets['n_nf_entrada'] = forms.TextInput(
            attrs={'class': 'form-control'})
        widgets['compra'] = forms.Select(attrs={'class': 'form-control'})
        widgets['emit_entrada'] = forms.Select(attrs={'class': 'form-control'})
        widgets['dest_entrada'] = forms.Select(attrs={'class': 'form-control'})
        labels = NotaFiscalForm.Meta.labels
        labels['n_nf_entrada'] = _('Número')
        labels['compra'] = _('Compra')
        labels['emit_entrada'] = _('Emitente (Fornecedor)')
        labels['dest_entrada'] = _('Destinatário (Empresa)')


class EmissaoNotaFiscalForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(EmissaoNotaFiscalForm, self).__init__(*args, **kwargs)
        self.fields['dhemi'].input_formats = ('%d/%m/%Y %H:%M',)

    class Meta:
        model = NotaFiscalSaida
        fields = ('versao', 'dhemi', 'dhsaient',
                  'tp_imp', 'tp_emis', 'tp_amb',)

        widgets = {
            'versao': forms.Select(attrs={'class': 'form-control', 'required': True}),
            'dhemi': forms.DateTimeInput(attrs={'class': 'form-control datetimepicker', 'required': True}, format='%d/%m/%Y %H:%M'),
            'dhsaient': forms.DateTimeInput(attrs={'class': 'form-control datetimepicker'}, format='%d/%m/%Y %H:%M'),
            'tp_imp': forms.Select(attrs={'class': 'form-control', 'required': True}),
            'tp_emis': forms.Select(attrs={'class': 'form-control', 'required': True}),
            'tp_amb': forms.Select(attrs={'class': 'form-control', 'required': True}),
        }
        labels = {
            'versao': _('Versão'),
            'dhemi': _('Data e hora de emissão'),
            'dhsaient': _('Data e hora de Saída/Entrada'),
            'tp_imp': _('Tipo impressão da DANFE'),
            'tp_emis': _('Forma de emissão'),
            'tp_amb': _('Ambiente'),
        }


class CancelamentoNotaFiscalForm(forms.ModelForm):

    class Meta:
        model = NotaFiscalSaida
        fields = ('just_canc', 'chave',
                  'numero_protocolo', 'tp_emis', 'tp_amb',)

        widgets = {
            'just_canc': forms.Textarea(attrs={'class': 'form-control', 'required': True}),
            'chave': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'numero_protocolo': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'tp_emis': forms.Select(attrs={'class': 'form-control', 'required': True}),
            'tp_amb': forms.Select(attrs={'class': 'form-control', 'required': True}),
        }
        labels = {
            'just_canc': _('Justificativa do cancelamento'),
            'chave': _('Chave'),
            'numero_protocolo': _('Número do protocolo'),
            'tp_emis': _('Forma de emissão'),
            'tp_amb': _('Ambiente'),
        }


class ConsultarCadastroForm(forms.Form):
    empresa = forms.ModelChoiceField(queryset=Empresa.objects.all(), widget=forms.Select(
        attrs={'class': 'form-control', }), label='选择公司', required=True)
    salvar_arquivos = forms.BooleanField(widget=forms.CheckboxInput(
        attrs={'class': 'form-control', }), label='是否保存生成的XML文件?', required=False)


class InutilizarNotasForm(forms.Form):
    ambiente = forms.ChoiceField(choices=TP_AMB_ESCOLHAS, widget=forms.Select(
        attrs={'class': 'form-control', }), label='Ambiente', initial='2', required=True)
    empresa = forms.ModelChoiceField(queryset=Empresa.objects.all(), widget=forms.Select(
        attrs={'class': 'form-control', }), label='选择发行公司', required=True)
    modelo = forms.ChoiceField(choices=MOD_NFE_ESCOLHAS, widget=forms.Select(
        attrs={'class': 'form-control', }), label='Modelo', required=True)
    serie = forms.CharField(max_length=3, widget=forms.TextInput(
        attrs={'class': 'form-control', }), label='级别', required=True)
    numero_inicial = forms.CharField(max_length=9, widget=forms.TextInput(
        attrs={'class': 'form-control', }), label='初始数字', required=True)
    numero_final = forms.CharField(max_length=9, widget=forms.TextInput(
        attrs={'class': 'form-control', }), label='最终数字', required=False)
    justificativa = forms.CharField(max_length=255, widget=forms.Textarea(
        attrs={'class': 'form-control', }), label='禁止原因', required=False)
    salvar_arquivos = forms.BooleanField(widget=forms.CheckboxInput(
        attrs={'class': 'form-control', }), label='是否保存生成的XML文件??', required=False)


class ConsultarNotaForm(forms.Form):
    ambiente = forms.ChoiceField(choices=TP_AMB_ESCOLHAS, widget=forms.Select(
        attrs={'class': 'form-control', }), label='Ambiente', initial='2', required=True)
    nota = forms.ModelChoiceField(queryset=NotaFiscalSaida.objects.all(), widget=forms.Select(
        attrs={'class': 'form-control', }), label='Selecionar nota da base de dados', required=False)
    chave = forms.CharField(max_length=44, widget=forms.TextInput(
        attrs={'class': 'form-control', }), label='Chave da nota', required=False)
    salvar_arquivos = forms.BooleanField(widget=forms.CheckboxInput(
        attrs={'class': 'form-control', }), label='是否保存生成的XML文件??', required=False)


class BaixarNotaForm(forms.Form):
    ambiente = forms.ChoiceField(choices=TP_AMB_ESCOLHAS, widget=forms.Select(
        attrs={'class': 'form-control', }), label='Ambiente', initial='2', required=True)
    nota = forms.ModelChoiceField(queryset=NotaFiscalSaida.objects.all(), widget=forms.Select(
        attrs={'class': 'form-control', }), label='Selecionar nota da base de dados', required=False)
    chave = forms.CharField(max_length=44, widget=forms.TextInput(
        attrs={'class': 'form-control', }), label='Chave da nota', required=False)
    ambiente_nacional = forms.BooleanField(widget=forms.CheckboxInput(
        attrs={'class': 'form-control', }), label='Utilizar ambiente nacional?(Recomendado)', initial=True, required=False)
    salvar_arquivos = forms.BooleanField(widget=forms.CheckboxInput(
        attrs={'class': 'form-control', }), label='是否保存生成的XML文件??', required=False)


class ManifestacaoDestinatarioForm(forms.Form):
    cnpj = forms.CharField(max_length=16, widget=forms.TextInput(attrs={
                           'class': 'form-control', }), label='CNPJ do autor do Evento(apenas digitos)', required=True)
    tipo_manifesto = forms.ChoiceField(choices=TP_MANIFESTO_OPCOES, widget=forms.Select(
        attrs={'class': 'form-control', }), label='Tipo de manifesto', required=True)
    ambiente = forms.ChoiceField(choices=TP_AMB_ESCOLHAS, widget=forms.Select(
        attrs={'class': 'form-control', }), label='Ambiente', initial='2', required=True)
    nota = forms.ModelChoiceField(queryset=NotaFiscalSaida.objects.all(), widget=forms.Select(
        attrs={'class': 'form-control', }), label='Selecionar nota da base de dados', required=False)
    chave = forms.CharField(max_length=44, widget=forms.TextInput(
        attrs={'class': 'form-control', }), label='Chave da nota', required=False)
    ambiente_nacional = forms.BooleanField(widget=forms.CheckboxInput(
        attrs={'class': 'form-control', }), label='Utilizar ambiente nacional?(Recomendado)', initial=True, required=False)
    justificativa = forms.CharField(max_length=255, widget=forms.Textarea(
        attrs={'class': 'form-control', }), label='Justificativa', required=False)
    salvar_arquivos = forms.BooleanField(widget=forms.CheckboxInput(
        attrs={'class': 'form-control', }), label='是否保存生成的XML文件??', required=False)


class AutXMLForm(forms.ModelForm):

    class Meta:
        model = AutXML
        fields = ('cpf_cnpj',)
        labels = {
            'cpf_cnpj': _('法人名称/法人税号 (Apenas digitos)'),
        }
        widgets = {
            'cpf_cnpj': forms.TextInput(attrs={'class': 'form-control'}),
        }


class ConfiguracaoNotaFiscalForm(forms.ModelForm):

    class Meta:
        model = ConfiguracaoNotaFiscal
        fields = ('serie_atual', 'ambiente', 'imp_danfe', 'arquivo_certificado_a1',
                  'senha_certificado', 'inserir_logo_danfe', 'orientacao_logo_danfe', 'csc', 'cidtoken',)
        labels = {
            'arquivo_certificado_a1': _('A1证书'),
            'serie_atual': _('系列'),
            'ambiente': _('Ambiente'),
            'imp_danfe': _('印刷类型'),
            'senha_certificado': _('证书密码'),
            'inserir_logo_danfe': _('是否在DANFE上插入公司标志?'),
            'orientacao_logo_danfe': _('标志指引'),
            'csc': _('纳税人的安全代码'),
            'cidtoken': _('CSC标识符'),
        }
        widgets = {
            'arquivo_certificado_a1': forms.FileInput(attrs={'class': 'form-control'}),
            'serie_atual': forms.TextInput(attrs={'class': 'form-control'}),
            'ambiente': forms.Select(attrs={'class': 'form-control'}),
            'imp_danfe': forms.Select(attrs={'class': 'form-control'}),
            'senha_certificado': forms.PasswordInput(attrs={'class': 'form-control'}, render_value=True),
            'inserir_logo_danfe': forms.CheckboxInput(attrs={'class': 'form-control'}),
            'orientacao_logo_danfe': forms.Select(attrs={'class': 'form-control'}),
            'csc': forms.TextInput(attrs={'class': 'form-control'}),
            'cidtoken': forms.TextInput(attrs={'class': 'form-control'}),
        }


AutXMLFormSet = inlineformset_factory(
    NotaFiscalSaida, AutXML, form=AutXMLForm, extra=1, can_delete=True)

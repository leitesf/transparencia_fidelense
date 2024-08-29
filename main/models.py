from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Sum


class Usuario(AbstractUser):
    contato = models.CharField("Contato", max_length=100)
    data_nascimento = models.DateField("Data de Nascimento", null=True, blank=True)

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'

    def __str__(self):
        return self.get_full_name()

    def get_edit_url(self):
        return '/admin/main/usuario/{}/change/'.format(self.id)
    

class Folha(models.Model):
    ano = models.IntegerField("Ano")
    mes = models.IntegerField("Mês")
    ordenacao = models.IntegerField("Formato Ordenado")

    class Meta:
        verbose_name = 'Folha'
        verbose_name_plural = 'Folhas'
        ordering = ['ordenacao']

    def __str__(self):
        return '{}/{}'.format(self.mes, self.ano)

    def get_edit_url(self):
        return '/admin/main/folha/{}/change/'.format(self.id)

    def get_absolute_url(self):
        return '/folha/{}/'.format(self.id)
    
    def get_quantidade_e_valor_por_categoria_pra_csv(self):
        retorno = []
        retorno.append(self)
        for categoria in CategoriaFuncional.objects.all():
            retorno.append(self.pagamento_set.filter(categoria=categoria).count())
            retorno.append(self.pagamento_set.filter(categoria=categoria).aggregate(Sum("remuneracao"))['remuneracao__sum'])
        return retorno
    

class Pessoa(models.Model):
    nome = models.CharField("Nome", max_length=100)
    cpf_formatado = models.CharField("CPF Formatado", max_length=15)

    class Meta:
        verbose_name = 'Pessoa'
        verbose_name_plural = 'Pessoas'
        ordering = ['nome']

    def __str__(self):
        return self.nome

    def get_edit_url(self):
        return '/admin/main/pessoa/{}/change/'.format(self.id)

    def get_absolute_url(self):
        return '/pessoa/{}/'.format(self.id)
    

class Divisao(models.Model):
    nome = models.CharField("Nome", max_length=100)

    class Meta:
        verbose_name = 'Divisão'
        verbose_name_plural = 'Divisões'
        ordering = ['nome']

    def __str__(self):
        return self.nome

    def get_edit_url(self):
        return '/admin/main/divisao/{}/change/'.format(self.id)

    def get_absolute_url(self):
        return '/divisao/{}/'.format(self.id)
    

class Subdivisao(models.Model):
    nome = models.CharField("Nome", max_length=100)

    class Meta:
        verbose_name = 'Subdivisão'
        verbose_name_plural = 'Subdivisões'
        ordering = ['nome']

    def __str__(self):
        return self.nome

    def get_edit_url(self):
        return '/admin/main/subdivisao/{}/change/'.format(self.id)

    def get_absolute_url(self):
        return '/subdivisao/{}/'.format(self.id)
    

class Unidade(models.Model):
    nome = models.CharField("Nome", max_length=100)

    class Meta:
        verbose_name = 'Unidade'
        verbose_name_plural = 'Unidades'
        ordering = ['nome']

    def __str__(self):
        return self.nome

    def get_edit_url(self):
        return '/admin/main/unidade/{}/change/'.format(self.id)

    def get_absolute_url(self):
        return '/unidade/{}/'.format(self.id)
    

class Cargo(models.Model):
    nome = models.CharField("Nome", max_length=100)

    class Meta:
        verbose_name = 'Cargo'
        verbose_name_plural = 'Cargos'
        ordering = ['nome']

    def __str__(self):
        return self.nome

    def get_edit_url(self):
        return '/admin/main/cargo/{}/change/'.format(self.id)

    def get_absolute_url(self):
        return '/cargo/{}/'.format(self.id)
    

class CategoriaFuncional(models.Model):
    nome = models.CharField("Nome", max_length=100)

    class Meta:
        verbose_name = 'Categoria Funcional'
        verbose_name_plural = 'Categorias Funcionais'
        ordering = ['nome']

    def __str__(self):
        return self.nome

    def get_edit_url(self):
        return '/admin/main/categoriafuncional/{}/change/'.format(self.id)

    def get_absolute_url(self):
        return '/categoriafuncional/{}/'.format(self.id)
        return '/cargo/{}/'.format(self.id)
    

class TipoVinculo(models.Model):
    nome = models.CharField("Nome", max_length=100)

    class Meta:
        verbose_name = 'Tipo de Vínculo'
        verbose_name_plural = 'Tipos de Vínculo'
        ordering = ['nome']

    def __str__(self):
        return self.nome

    def get_edit_url(self):
        return '/admin/main/tipovinculo/{}/change/'.format(self.id)

    def get_absolute_url(self):
        return '/tipovinculo/{}/'.format(self.id)
    

class LocalTrabalho(models.Model):
    nome = models.CharField("Nome", max_length=100)

    class Meta:
        verbose_name = 'Local de Trabalho'
        verbose_name_plural = 'Locais de Trabalho'
        ordering = ['nome']

    def __str__(self):
        return self.nome

    def get_edit_url(self):
        return '/admin/main/localtrabalho/{}/change/'.format(self.id)

    def get_absolute_url(self):
        return '/localtrabalho/{}/'.format(self.id)
    

class Contrato(models.Model):
    id_prefeitura = models.IntegerField("ID Prefeitura", unique=True)
    pessoa = models.ForeignKey(Pessoa, on_delete=models.CASCADE)
    cargo_atual = models.ForeignKey(Cargo, related_name='contratos_como_atual', on_delete=models.CASCADE)
    cargo_inicio = models.ForeignKey(Cargo, related_name='contratos_como_inicio', on_delete=models.CASCADE)
    categoria = models.ForeignKey(CategoriaFuncional, on_delete=models.CASCADE)
    tipo_vinculo_atual = models.ForeignKey(TipoVinculo, on_delete=models.CASCADE)
    divisao_atual = models.ForeignKey(Divisao, on_delete=models.CASCADE)
    subdivisao_atual = models.ForeignKey(Subdivisao, on_delete=models.CASCADE)
    local_trabalho_atual = models.ForeignKey(LocalTrabalho, on_delete=models.CASCADE)
    data_admissao_atual = models.DateField("Data de Admissão Atual", null=False, blank=False)
    folha_mais_recente = models.ForeignKey(Folha, on_delete=models.CASCADE)
    data_atualizacao = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Contrato'
        verbose_name_plural = 'Contratos'
        ordering = ['pessoa__nome']

    def __str__(self):
        return '%s - %s'.format(self.pessoa.nome, self.cargo_atual)

    def get_edit_url(self):
        return '/admin/main/contrato/{}/change/'.format(self.id)

    def get_absolute_url(self):
        return '/contrato/{}/'.format(self.id)
    

class Pagamento(models.Model):
    contrato = models.ForeignKey(Contrato, on_delete=models.CASCADE)
    folha = models.ForeignKey(Folha, on_delete=models.CASCADE)
    cargo = models.ForeignKey(Cargo, on_delete=models.CASCADE)
    categoria = models.ForeignKey(CategoriaFuncional, on_delete=models.CASCADE)
    tipo_vinculo = models.ForeignKey(TipoVinculo, on_delete=models.CASCADE)
    divisao = models.ForeignKey(Divisao, on_delete=models.CASCADE)
    subdivisao = models.ForeignKey(Subdivisao, on_delete=models.CASCADE)
    local_trabalho = models.ForeignKey(LocalTrabalho, on_delete=models.CASCADE)
    carga_horaria = models.SmallIntegerField("Carga Horária", null=True, blank=True)
    remuneracao = models.DecimalField("Remuneração", decimal_places=2, max_digits=8)
    data_admissao = models.DateField("Data de Admissão", null=False, blank=False)

    class Meta:
        verbose_name = 'Pagamento'
        verbose_name_plural = 'Pagamentos'
        ordering = ['-folha__ordenacao', 'contrato__pessoa__nome']

    def __str__(self):
        return '{} ({})'.format(self.contrato.pessoa, self.folha)

    def get_edit_url(self):
        return '/admin/main/pagamento/{}/change/'.format(self.id)

    def get_absolute_url(self):
        return '/pagamento/{}/'.format(self.id)
    
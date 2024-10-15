from datetime import date, datetime, timedelta
from decimal import Decimal

from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
import requests
from django.core.management.base import BaseCommand
from django.db import transaction
from tqdm import tqdm
from django.conf import settings
from datetime import datetime

from main.models import *


class Command(BaseCommand):
    help = "Baixa dados da prefeitura"

    def handle(self, *args, **options):
        with transaction.atomic():
            hoje = date.today()
            dia = date(2020,1,1)
            delta = timedelta(days=1)
            while dia <= hoje:
                if dia.day == 1 and not Folha.objects.filter(ano=dia.year, mes=dia.month).exists():
                    mes = dia.month
                    ano = dia.year
                    dados = requests.get(
                        "{}/Transparencia/VersaoJson/Pessoal/?Listagem=Servidores&Empresa=1&Exercicio={}&MesFinalPeriodo={}".format(
                            settings.IP_PREFEITURA,
                            str(ano).zfill(4),
                            str(mes).zfill(2)
                        )
                    ).json()

                    folha = Folha.objects.get_or_create(
                        mes=mes,
                        ano=ano,
                        ordenacao = int('{}{}'.format(ano, mes))
                    )[0]
                    folha_mais_nova = True if date(hoje.year, hoje.month, 2) > date(folha.ano, folha.mes, 1) else False

                    print("Importando dados referencia {}/{}".format(mes,ano))
                    for item in tqdm(dados):
                        pessoa = Pessoa.objects.get_or_create(
                            nome = item['NOME'],
                            cpf_formatado = item['CPFFORMATADO']
                        )[0]
                        divisao = Divisao.objects.get_or_create(
                            nome = item['DIVISAO']
                        )[0]
                        subdivisao = Subdivisao.objects.get_or_create(
                            nome = item['SUBDIVISAO']
                        )[0]
                        unidade = Unidade.objects.get_or_create(
                            nome = item['UNIDADE']
                        )[0]
                        cargo = Cargo.objects.get_or_create(
                            nome = item['CARGO']
                        )[0]
                        categoria_funcional = CategoriaFuncional.objects.get_or_create(
                            nome = item['CATEGORIAFUNCIONAL']
                        )[0]
                        tipo_vinculo = TipoVinculo.objects.get_or_create(
                            nome = item['VINCULO']
                        )[0]
                        local_trabalho = LocalTrabalho.objects.get_or_create(
                            nome=item['LOCALDETRABALHO']                
                        )[0]
                        data_admissao = datetime.strptime(item["DATAADMISSAO"], '%d/%m/%Y %H:%M:%S').date()
                        data_desligamento = datetime.strptime(item["DATADESLIGAMENTO"], '%d/%m/%Y %H:%M:%S').date() if item['DATADESLIGAMENTO'] else None

                        if Contrato.objects.filter(id_prefeitura = item['ID']):
                            contrato = Contrato.objects.get(id_prefeitura = item['ID'])
                            if folha_mais_nova:
                                contrato.cargo_atual = cargo
                                contrato.tipo_vinculo_atual = tipo_vinculo
                                contrato.divisao_atual = divisao
                                contrato.subdivisao_atual = subdivisao
                                contrato.local_trabalho_atual = local_trabalho
                                contrato.data_admissao_atual = data_admissao
                                contrato.data_desligamento = data_desligamento
                                contrato.folha_mais_recente = folha
                                contrato.save()
                        else:
                            contrato = Contrato.objects.get_or_create(
                                id_prefeitura = item['ID'],
                                pessoa = pessoa,
                                cargo_atual = cargo,
                                cargo_inicio = cargo,
                                categoria = categoria_funcional,
                                tipo_vinculo_atual = tipo_vinculo,
                                divisao_atual = divisao,
                                subdivisao_atual = subdivisao,
                                local_trabalho_atual = local_trabalho,
                                folha_mais_recente = folha, 
                                data_admissao_atual = data_admissao
                            )[0]
                        if not Pagamento.objects.filter(contrato=contrato, folha=folha).exists():
                            valor_convertido = item['PROVENTOS'].replace(',','.')
                            try: 
                                Pagamento.objects.create(
                                    contrato = contrato,
                                    folha=folha,
                                    cargo = cargo,
                                    categoria = categoria_funcional,
                                    tipo_vinculo = tipo_vinculo,
                                    divisao = divisao,
                                    subdivisao = subdivisao,
                                    local_trabalho = local_trabalho,
                                    carga_horaria = int(item['HORASEMANAL']),
                                    remuneracao = Decimal(valor_convertido or 0),
                                    data_admissao = data_admissao,
                                )
                            except:
                                import ipdb; ipdb.set_trace()
                dia += delta
                

                

from datetime import date
from django.contrib import messages
from django.shortcuts import render, redirect

from main.forms import RelatorioGastosForm
from main.models import CategoriaFuncional, Folha
from main.utils import gerar_menu
from django.http import HttpResponse
from django.template import loader, Context
from dateutil.relativedelta import relativedelta
import csv



def relatorio_evolucao_gastos(request):
    side_menu_list = gerar_menu(request.user, ativo='relatorio_evolucao_gastos')
    titulo = "Relatório de Evolução de Gastos"

    if request.method == "POST":
        form = RelatorioGastosForm(request.POST)
        if form.is_valid():


            response = HttpResponse(
                content_type="text/csv",
                headers={"Content-Disposition": 'attachment; filename="relatorio_gastos.csv"'},
            )

            writer = csv.writer(response)

            folha_inicial = form.cleaned_data['folha_inicial']
            folha_inicial = date(folha_inicial.ano, folha_inicial.mes, 1)
            folha_final = form.cleaned_data['folha_final']
            folha_final = date(folha_final.ano, folha_final.mes, 1)

            cabecalho = ['Folha']
            for categoria in CategoriaFuncional.objects.all():
                cabecalho.append("{} - QTD".format(categoria.nome or "Vazio"))
                cabecalho.append("{} - Total".format(categoria.nome or "Vazio"))
            writer.writerow(cabecalho)
            while folha_inicial <= folha_final:
                folha_atual = Folha.objects.get(ano=folha_inicial.year, mes=folha_inicial.month)
                writer.writerow(folha_atual.get_quantidade_e_valor_por_categoria_pra_csv())
                folha_inicial = folha_inicial + relativedelta(months=1)
            return response
    else:
        form = RelatorioGastosForm()
    return render(request, 'form.html', locals())

# Create your views here.

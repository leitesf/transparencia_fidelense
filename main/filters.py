from datetime import date
from django.contrib.admin import SimpleListFilter
from django_middleware_global_request import get_request



class GovernoFilter(SimpleListFilter):
    title = "Quem Contratou?"  # a label for our filter
    parameter_name = "quem_contratou"

    def lookups(self, request, model_admin):
        return [
            ("amarildo", "Amarildo"),
            ("zewilliam", "Zé William")
        ]

    def queryset(self, request, queryset):
        user = get_request().user
        data_referencia = date(2024,3,13)
        if self.value() == "amarildo":
            return queryset.filter(data_admissao_atual__lte=data_referencia)
        elif self.value() == "zewilliam":
            return queryset.filter(data_admissao_atual__gt=data_referencia)
        else:
            return queryset
        
class DemitidosEsseAnoFilter(SimpleListFilter):
    title = "Foi demitido esse ano?"  # a label for our filter
    parameter_name = "demitido"

    def lookups(self, request, model_admin):
        return [
            ("foi_demitido", "Sim"),
            ("nao_foi_demitido", "Não"),
        ]

    def queryset(self, request, queryset):
        print(self.value())
        if self.value() == "foi_demitido":
            return queryset.filter(folha_mais_recente__ano=2024, folha_mais_recente__mes__lt=8, folha_mais_recente__mes__gte=3)
        else:
            return queryset

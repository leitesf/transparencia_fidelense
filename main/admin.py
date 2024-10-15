import csv
from decimal import Decimal
from django.contrib import admin
from django.http import HttpResponse
from django.utils.safestring import mark_safe
from django_bootstrap_icons.templatetags.bootstrap_icons import bs_icon

from main.filters import DemitidosEsseAnoFilter, GovernoFilter
from main.forms import UsuarioForm
from main.models import Contrato, Pagamento, Usuario
from django.templatetags.static import static


class AdminBasico(admin.ModelAdmin):
    def get_links(self, obj):
        info = static('svg/info-square.svg')
        pencil = static('svg/pencil-square.svg')
        return mark_safe(
            "<a href='{}' title='Visualizar'><img src='{}'></a>&nbsp;<a href='{}' title='Editar'><img src='{}'></a>".format(obj.get_absolute_url(), info, obj.get_edit_url(), pencil)
        )

    get_links.short_description = '#'
    get_links.allow_tags = True
    list_per_page = 50

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
    
    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response


class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('get_links', 'get_nome', 'username', 'email', 'contato', 'get_grupos', 'is_superuser')
    search_fields = ('first_name', 'last_name', 'email')
    list_display_links = None
    form = UsuarioForm

    def get_nome(self, obj):
        return obj.get_full_name()

    get_nome.short_description = 'Nome'
    get_nome.admin_order_field = ["first_name"]

    def get_grupos(self, obj):
        return ', '.join(obj.groups.values_list('name', flat=True))

    get_grupos.short_description = 'Grupos'

    def get_links(self, obj):
        links = ""
        links += "<a class='text-reset text-decoration-none' href='{}' title='Editar'>{}</a>".format(obj.get_edit_url(), bs_icon('pencil-square'))
        links += "<a class='text-reset text-decoration-none' href='{}' title='Alterar Senha'>{}</a>".format('/usuario/{}/alterar_senha/'.format(obj.id), bs_icon('key'))
        return mark_safe(links)

    get_links.short_description = '#'
    get_links.allow_tags = True

    # def get_actions(self, request):
    #     actions = super().get_actions(request)
    #     if 'delete_selected' in actions:
    #         del actions['delete_selected']
    #     return actions
    

class PagamentoAdmin(AdminBasico):
    list_display = (
        'get_pessoa', 'folha', 'cargo', 'categoria', 'tipo_vinculo', 
        'divisao', 'subdivisao', 'local_trabalho', 'carga_horaria', 'remuneracao',
        'data_admissao'
    )
    search_fields = ('contrato__pessoa__nome', 'cargo__nome')
    list_filter = (
        ('folha', admin.RelatedOnlyFieldListFilter),
        ('categoria', admin.RelatedOnlyFieldListFilter),
        ('tipo_vinculo', admin.RelatedOnlyFieldListFilter),
        ('subdivisao', admin.RelatedOnlyFieldListFilter),
        ('local_trabalho', admin.RelatedOnlyFieldListFilter),
        ('data_admissao', admin.DateFieldListFilter),
    )
    list_display_links = None
    actions = ["export_as_csv"]

    def get_pessoa(self, obj):
        return obj.contrato.pessoa
    get_pessoa.short_description='Pessoa'
    get_pessoa.admin_order_field='contrato__pessoa'
    
    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)
        valor_total = Decimal(0)

        writer.writerow(
            [
                'Funcionário', 
                'Folha', 
                'Cargo', 
                'Categoria', 
                'Tipo de Vínculo', 
                'Divisão',
                'Subdivisão',
                'Local de Trabalho',
                'Carga Horária',
                'Remuneração',
                'Data de Admissão'
            ]
        )
        for obj in queryset:
            valor_total += obj.remuneracao
            writer.writerow(
                [
                    obj.contrato.pessoa,
                    obj.folha,
                    obj.cargo,
                    obj.categoria,
                    obj.tipo_vinculo,
                    obj.divisao,
                    obj.subdivisao,
                    obj.local_trabalho,
                    obj.carga_horaria,
                    obj.remuneracao,
                    obj.data_admissao
                ]
            )
        writer.writerow(
                [
                    '',
                    '',
                    '',
                    '',
                    '',
                    '',
                    '',
                    '',
                    '',
                    valor_total,
                    ''
                ]
            )

        return response


class ContratoAdmin(AdminBasico):
    list_display = (
        'pessoa', 'cargo_atual', 'categoria', 'tipo_vinculo_atual', 'data_admissao_atual', 'data_desligamento', 
        'folha_mais_recente', 'divisao_atual', 'local_trabalho_atual'
    )
    search_fields = ('pessoa__nome', 'cargo_atual__nome')
    list_filter = (
        ('folha_mais_recente', admin.RelatedOnlyFieldListFilter),
        ('categoria', admin.RelatedOnlyFieldListFilter),
        ('tipo_vinculo_atual', admin.RelatedOnlyFieldListFilter),
        ('local_trabalho_atual', admin.RelatedOnlyFieldListFilter),
        ('data_admissao_atual', admin.DateFieldListFilter),
        ("data_desligamento", admin.EmptyFieldListFilter),
        GovernoFilter,
        DemitidosEsseAnoFilter
    )
    list_display_links = None
    actions = ["export_as_csv"]
    
    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(
            [
                'Funcionário', 
                'Folha Mais Recente', 
                'Cargo Atual', 
                'Categoria', 
                'Tipo de Vínculo Atual',    
                'Divisão Atual',
                'Local de Trabalho Atual',
                'Data de Admissão Atual',
                'Data de Desligamento'
            ]
        )
        for obj in queryset:
            writer.writerow(
                [
                    obj.pessoa,
                    obj.folha_mais_recente,
                    obj.cargo_atual,
                    obj.categoria,
                    obj.tipo_vinculo_atual,
                    obj.divisao_atual,
                    obj.local_trabalho_atual,
                    obj.data_admissao_atual,
                    obj.data_desligamento
                ]
            )

        return response

admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Pagamento, PagamentoAdmin)
admin.site.register(Contrato, ContratoAdmin)
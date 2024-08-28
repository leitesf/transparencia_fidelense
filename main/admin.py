from django.contrib import admin
from django.utils.safestring import mark_safe
from django_bootstrap_icons.templatetags.bootstrap_icons import bs_icon

from main.forms import UsuarioForm
from main.models import Pagamento, Usuario
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
    search_fields = ('contrato__pessoa', )
    list_filter = (
        ('folha', admin.RelatedOnlyFieldListFilter),
        ('categoria', admin.RelatedOnlyFieldListFilter),
        ('tipo_vinculo', admin.RelatedOnlyFieldListFilter),
        ('subdivisao', admin.RelatedOnlyFieldListFilter),
        ('local_trabalho', admin.RelatedOnlyFieldListFilter),
    )
    list_display_links = None

    def get_pessoa(self, obj):
        return obj.contrato.pessoa
    get_pessoa.short_description='Pessoa'
    get_pessoa.order_field='contrato__pessoa'


admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Pagamento, PagamentoAdmin)
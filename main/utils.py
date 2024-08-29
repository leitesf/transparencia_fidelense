from django.utils.safestring import mark_safe
from django_bootstrap_icons.templatetags.bootstrap_icons import bs_icon

#
def gerar_menu(usuario, ativo=None):
    side_menu_list = [
        {
            'name': 'Transparência Fidelense',
            'app_label': 'main',
            'app_url': '/admin/main/',
            'has_module_perms': True,
            'models': []
        }
    ]
    is_active = True if ativo == 'relatorio_evolucao_gastos' else False
    side_menu_list[0]['models'].append(
        {'name': 'Relatório de Evolução de Gastos', 'object_name': 'Relatório de Evolução de Gastos', 'perms': {'add': True, 'change': True, 'delete': True, 'view': True}, 'view_only': False, 'url': '/relatorio_evolucao_gastos/', 'model_str': 'main.pagamento', 'icon': 'fas fa-object-group', 'is_active': is_active}
    )
    if usuario.is_superuser:
        is_active = True if ativo == 'usuario' else False
        side_menu_list.append({
            'name': 'Autenticação e Autorização',
            'app_label': 'auth',
            'app_url': '/admin/auth/',
            'has_module_perms': True,
            'models':
                [
                    {
                        'name': 'Grupos',
                        'object_name': 'Group',
                        'perms':
                            {
                                'add': True, 'change': True, 'delete': True, 'view': True
                            },
                        'admin_url': '/admin/auth/group/',
                        'add_url': '/admin/auth/group/add/',
                        'view_only': False,
                        'url': '/admin/auth/group/',
                        'model_str': 'auth.group',
                        'icon': 'fas fa-users'
                    },
                    {
                        'name': 'Usuários',
                        'url': '/admin/main/usuario/',
                        'children': None,
                        'new_window': False,
                        'icon': 'fas fa-user',
                        'is_active': is_active
                    },
                    {
                        'name': 'Configuração do Sistema',
                        'url': '/admin/main/configuracaosistema/',
                        'children': None,
                        'new_window': False,
                        'icon': 'fas fa-wrench'
                    },
                ], 'icon': 'fas fa-users-cog'
        }
        )
    return side_menu_list


def links_no_admin(objeto, pode_visualizar, pode_editar):
    links=""
    if pode_visualizar:
        links = links + "<a class='text-reset text-decoration-none' href='{}' title='Visualizar'>{}</a>".format(objeto.get_absolute_url(), bs_icon('info-square'))
    if pode_editar:
        links = links + "<a class='text-reset text-decoration-none' href='{}' title='Editar'>{}</a>".format(objeto.get_edit_url(), bs_icon('pencil-square'))
    return mark_safe(links)
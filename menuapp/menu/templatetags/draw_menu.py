from django import template
from menu import models

QUERY_MENU_NAME = 'm'

register = template.Library()

@register.inclusion_tag(
  'templatetags/menu/draw_menu.jinja',
  name='draw_menu'
)
def draw_menu(name, with_root=True):
    fc: dict[str,str] = {
        'with_root':with_root
    }
    root = None
    parents = {}
    for it in models.MenuModel.get_menu(name):
        setattr(it,'children', [])
        if root is None:
            root = it
        if it.id not in parents:
            parents[it.id] = it.children
        if it.parent is not None:
            if it.parent.id not in parents:
                parents[it.parent.id] = []
            parents[it.parent.id].append(it)
    fc['root'] = root
    return fc
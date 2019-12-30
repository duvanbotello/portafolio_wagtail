from django import template

from home.models import FormField

register = template.Library()


def search_parent_page(parent, page):
    if page._meta.model_name != 'homepage':
        try:
            parent.insert(0, page.get_parent().homepage)
        except:
            pass
        search_parent_page(parent, parent[0])

    return


@register.inclusion_tag('blocks/main/header_block.html', takes_context=True, )
def render_header(context, page):
    parent = [page]
    search_parent_page(parent, page)

    if parent:
        context['page_parent'] = parent[0]
    return context


@register.simple_tag
def is_menu_item_dropdown(value):
    return \
        len(value.get('sub_links', [])) > 0 or \
        (
                value.get('show_child_links', False) and len(value.get('page', []).get_children().live()) > 0
        )


@register.simple_tag
def get_parent_page(page):
    return page.get_parent()


@register.simple_tag
def get_input_icon(page, ord):
    try:
        field = FormField.objects.get(page_id=page, sort_order=ord)
        return field.icon
    except:
        return ""


@register.simple_tag
def search_parent(page):
    parent = [get_parent_page(page)]
    if page._meta.model_name in ['entrypage']:
        parent = [get_parent_page(parent[0]), parent[0]]
    return parent

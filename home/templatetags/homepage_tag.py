from django import template

register = template.Library()

@register.inclusion_tag('blocks/main/header_block.html', takes_context=True, )
def render_header(context, page):
     parent = [page]
     get_parent_page(parent, page)

     if parent:
        context['page_parent'] = parent[0]
     return context

def get_parent_page(parent, page):
    if page._meta.model_name != 'homepage':
        try:
            parent.insert(0, page.get_parent().homepage)
        except:
            pass
        get_parent_page(parent, parent[0])

    return

@register.simple_tag
def is_menu_item_dropdown(value):
    return \
        len(value.get('sub_links', [])) > 0 or \
        (
                value.get('show_child_links', False) and len(value.get('page', []).get_children().live()) > 0
        )


def get_parent_page(parent, page):
    if page._meta.model_name != 'homepage':
        try:
            parent.insert(0, page.get_parent().homepage)
        except:
            pass
        get_parent_page(parent, parent[0])

    return


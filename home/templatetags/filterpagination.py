from django import template


register = template.Library()

@register.filter(name='curpage')
def get_current_page(page, current_page) -> str:
    return 'active' if page == current_page else '' 
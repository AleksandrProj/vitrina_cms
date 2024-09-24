from django.urls import path, reverse

from wagtail.admin.menu import MenuItem
from wagtail import hooks

from seo.views import SEOAdminView


# Hooks SEO module


@hooks.register('register_admin_urls')
def register_seo_url():
    """Регистранция SEO URL"""

    return [
        path('seo/', SEOAdminView.as_view(), name='seo'),
    ]


@hooks.register('register_admin_menu_item')
def register_seo_menu_item():
    """Регистранция SEO меню в админке"""

    return MenuItem('SEO', reverse('seo'), icon_name='edit')

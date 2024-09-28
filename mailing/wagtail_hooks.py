from django.urls import path, reverse

from wagtail.admin.menu import MenuItem
from wagtail import hooks

from mailing.views import SubscribersAdminView


@hooks.register('register_admin_urls')
def register_seo_url():
    """Регистрация ПОДПИСЧИКИ URL"""

    return [
        path('subscribers/', SubscribersAdminView.as_view(), name='subscribers'),
    ]


@hooks.register('register_admin_menu_item')
def register_seo_menu_item():
    """Регистрация ПОДПИСЧИКИ меню в админке"""

    return MenuItem('Подписчики', reverse('subscribers'), icon_name='user')
import copy
import re
import httpx

from django.conf import settings
from django.urls import path, reverse
from django.contrib.auth import get_user_model

from wagtail import hooks
from wagtail.admin.menu import MenuItem

from mailing.views import SubscribersAdminView
from mailing.utils.hooks import (
    get_template_hooks_page, 
    get_body_text_hooks_page,
    get_body_button_hooks_page,
)

from home.models import ArticlesPage, VacanciesPage
from home.handlers import NewWindowExternalLinkHandler


@hooks.register('register_rich_text_features', order=10)
def register_externallink_handler(features):
    features.register_link_type(NewWindowExternalLinkHandler)


@hooks.register('after_publish_page')
def after_publish_page(request, page):
    """
        Hooks для публикации страниц
    """
    if  isinstance(page, ArticlesPage|VacanciesPage) and not page.is_send_email:
        payload = {
            'format': 'json',
            'api_key': settings.SUBSCRIBE_API_KEY,
        }

        title_material, title_button = '', ''

        if isinstance(page, VacanciesPage):
            title_material = 'Вакансия'
            title_button = 'Подробнее о вакансии'
        elif isinstance(page, ArticlesPage):
            title_material = 'Статья'
            title_button = 'Читать статью'
        
        user_data = get_user_model().objects.get(is_superuser=True)
        body_html = get_template_hooks_page()
        body_text = get_body_text_hooks_page(title_material, page)   
        body_button = get_body_button_hooks_page(title_button, page)   

        body_text = re.sub('insert_body_text_code', body_text, body_html)
        body_text = re.sub('insert_body_button_code', body_button, body_text)
    
        create_message_payload = copy.copy(payload)
        create_message_payload.update({
            'sender_name': page.get_site().site_name,
            'sender_email': user_data.email,
            'subject': page.title,
            'body': body_text,
            'generate_text': 1,
            'list_id': 3,
        })

        # Создание нового сообщения
        create_message_res = httpx.post(f'{settings.UNISENDER_URL}/createEmailMessage', data=create_message_payload)

        # TODO: Настроить логгирование 
        print('create message', create_message_res.json())

        # Удалить как включим отправку
        page.is_send_email = True
        page.save()
        
        # # Отправка нового сообщения (ВКЛЮЧИТЬ КАК ПРОГРЕЕМ ДОМЕН)
        # if create_message_res.status_code == 200:
        #     send_message_payload = copy.copy(payload)

        #     message = create_message_res.json()
        #     send_message_payload.update({
        #         "message_id": message['result']['message_id'],
        #         "track_read": 1,
        #     })

        #     send_message_res = httpx.post(f'{settings.UNISENDER_URL}/createCampaign', data=send_message_payload)
            
        #     print('send message', send_message_res.json())

        #     # Отмечаем что рассылка на данный материал была создана
        #     page.is_send_email = True
        #     page.save()


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
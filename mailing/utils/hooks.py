import re

from django.conf import settings

from wagtail.rich_text import expand_db_html

from home.models import ArticlesPage, VacanciesPage


def get_template_hooks_page():
    """
        Получение общего шаблона письма для вакансий и статей
    """
    body_html = ''
    with open(f'{settings.BASE_DIR}/mailing/templates/mailing/mail_template.html', 'r') as file:
        body_html = file.read()
    
    return body_html


def get_body_text_hooks_page(title_mail: str, page: ArticlesPage|VacanciesPage):    
    """
        Получение общего текста письма для вакансий и статей
    """    
    body_text = f"<div><h1 class='heading_mail'>{title_mail} {str.lower(page.title)}</h1></div>{expand_db_html(page.description)}"
    return re.sub('src="', f'src="{page.get_site().root_url}', body_text)


def get_body_button_hooks_page(text_button, page: ArticlesPage|VacanciesPage):    
    """
        Получение кнопки письма для вакансий и статей
    """
    return f"<div class='main-button'><a href='{page.full_url}'>{text_button}</a></div>"
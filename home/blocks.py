from wagtail import blocks
from wagtail.documents.blocks import DocumentChooserBlock


# Блоки для страницы вакансий
class VacancyBlock(blocks.StructBlock):
    """
        Блок с вакансией
    """
    vacancies = blocks.PageChooserBlock(target_model="home.VacanciesPage", label="Вакансия")


class VacanciesBlock(blocks.StreamBlock):
    """
        Блок лучших вакансий
    """
    title = blocks.CharBlock(
        max_length=100,
        required=True,
        label="Заголовок блока"
    )
    vacancies = VacancyBlock(label="Добавить вакансию")

    class Meta:
        block_counts = {
            "title": {
                "max_num": 1
            },
            "vacancies": {
                "max_num": 10
            }
        }


# Блоки для шапки и подвала
class MenuElementBlock(blocks.StructBlock):
    """
        Блок для элементов меню
    """
    name = blocks.CharBlock(
        max_length=100,
        required=True,
        label="Название пункта меню"
    )
    link = blocks.PageChooserBlock(label="Страница сайта")


class MenuBlock(blocks.StreamBlock):
    """
        Блок для меню
    """
    block = MenuElementBlock(label="Выбрать меню")


class DataPolicyBlock(blocks.StructBlock):
    """
        Блок с основными элементами для юридических документов
    """
    name_block = blocks.CharBlock(
        max_length=100,
        required=True,
        label="Заголовок блока"
    )
    document_block = DocumentChooserBlock(required=True, label="Добавить политику или соглашение")

class PolicyBlock(blocks.StreamBlock):
    """
        Блок для юридических документов
    """
    privacy_policy_block = DataPolicyBlock(label="Добавить блок с юридическими документами")

    class Meta:
        required = True
        block_counts = {
            "privacy_policy_block": {
                "max_num": 2
            },
        }


class HeaderBlock(blocks.StructBlock):
    """
        Блок шапки сайта
    """
    title_site = blocks.CharBlock(
        max_length=100,
        required=True,
        label="Название сайта"
    )
    menu = MenuBlock(required=False, label="Меню сайта")

    class Meta:
        label = "Блок шапки сайта"


class FooterBlock(blocks.StructBlock):
    """
        Блок подвала сайта
    """
    copyright = blocks.CharBlock(required=True, max_length=250, label="Копирайт для сайта")
    sitemap = blocks.URLBlock(required=False, label="Ссылка на карту сайта")
    policy_block = PolicyBlock(label="Блок юридических документов")  
    menu = MenuBlock(required=False, label="Меню сайта")

    class Meta:
        label = "Блок подвала сайта"


class FormBlock(blocks.StructBlock):
    """
        Блок для форм сайта
    """
    name_input = blocks.CharBlock(required=True, max_length=100, label="Текст для инпута для имени")
    email_input = blocks.CharBlock(required=True, max_length=100, label="Текст для инпута E-mail")
    button = blocks.CharBlock(required=True, max_length=100, label="Текст для кнопки формы")

    class Meta:
        label = "Форма подписки"
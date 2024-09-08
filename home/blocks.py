from wagtail import blocks
from wagtail.fields import StreamField
from wagtail.images.blocks import ImageChooserBlock


# Блоки для страницы вакансий
class VacancyBlock(blocks.StructBlock):
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
    copyright = blocks.RichTextBlock(required=True, label="Копирайт для сайта")
    sitemap = blocks.URLBlock(required=False, label="Ссылка на карту сайта")
    privacy_policy = blocks.RichTextBlock(required=True, label="Политика конфидициальности")
    user_agreement = blocks.RichTextBlock(required=False, label="Пользовательское соглашение")   
    menu = MenuBlock(required=False, label="Меню сайта")

    class Meta:
        label = "Блок подвала сайта"
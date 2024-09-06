from django.db import models

from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField
from wagtail.snippets.models import register_snippet
from wagtail.admin.panels import (
    FieldPanel,
    InlinePanel,
    MultiFieldPanel,
)

from wagtailmetadata.models import MetadataPageMixin

from modelcluster.fields import ParentalKey


class HomePage(Page):
    subpage_types = [
        "home.RubricArticlesPage",
        "home.RubricVacanciesPage",
    ]


class SeoPageMixin(MetadataPageMixin, Page):
    """
        Класс миксин для добавление моделям seo параметров
    """
    seo_keyword = models.CharField(
        "Ключевые слова", help_text="Ключевые слова для поисковых систем", default="", max_length=255, blank=True, null=False)
    seo_site = models.CharField(
        "SEO сайт", max_length=255, blank=True, null=False)
    seo_title_footer = models.CharField(
        "Заголовок нижнего SEO блока", max_length=200, blank=True, null=False)
    seo_description_footer = models.TextField(
        "Заголовок нижнего SEO блока", blank=True, null=False)

    promote_panels = MetadataPageMixin.promote_panels + [
        FieldPanel("seo_keyword"),
        FieldPanel("seo_site"),
        FieldPanel("seo_title_footer"),
        FieldPanel("seo_description_footer"),
    ]

    class Meta(MetadataPageMixin.Meta, Page.Meta):
        pass


class RubricArticlesPage(SeoPageMixin):
    """
        Рубрика для статей
    """
    description = models.CharField(
        "Описание рубрики статей", max_length=255, null=False, blank=True)

    parent_page_type = ["home.HomePage"]
    subpage_types = ["home.ArticlesPage"]

    content_panels = SeoPageMixin.content_panels + [
        FieldPanel("description")
    ]

    class Meta(SeoPageMixin.Meta):
        verbose_name = "Рубрика для статей"
        verbose_name_plural = "Рубрики для статей"


class RubricVacanciesPage(SeoPageMixin):
    """
        Рубрика для вакансий
    """
    description = models.CharField(
        "Описание рубрики вакансий", max_length=255, null=False, blank=True)

    parent_page_type = ["home.HomePage"]
    subpage_types = ["home.VacanciesPage"]

    content_panels = SeoPageMixin.content_panels + [
        FieldPanel("description")
    ]

    class Meta(SeoPageMixin.Meta):
        verbose_name = "Рубрика для вакансий"
        verbose_name_plural = "Рубрики для вакансий"


class BaseMaterialPage(SeoPageMixin):
    """
        Базовая модель для материалов сайта
    """
    description = RichTextField("Описание материала")
    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name="Изображение для материала",
        help_text="Выберите подходящее изображение материала из галереи и добавьте сюда",
        related_name="+",
    )
    caption_image = models.CharField(
        "Подпись для изображения", max_length=150, blank=False, null=True)
    
    content_panels = SeoPageMixin.content_panels + [
        FieldPanel('description'),
        MultiFieldPanel([
            FieldPanel("image"),
            FieldPanel("caption_image"),
        ]),
    ]
    
    class Meta(SeoPageMixin.Meta):
        abstract=True

class ArticlesPage(BaseMaterialPage):
    """
        Модель для статей сайта
    """  
    parent_page_type = ["home.RubricArticlesPage"]

    class Meta(BaseMaterialPage.Meta):
        verbose_name = "Статья для сайта"
        verbose_name_plural = "Статьи для сайта"


class ElementsVacancyModel(Orderable):
    """
        Модель для добавление элементов вакансии
    """
    page = ParentalKey('home.VacanciesPage',
                       on_delete=models.CASCADE, related_name="elements_vacancy")
    element = models.ForeignKey(
        'home.ElementsVacanciesSnippet', on_delete=models.CASCADE, related_name="+", verbose_name="Элемент вакансии")
    content = models.CharField("Описание элемента вакансии", max_length=150)

    panels = [
        FieldPanel("element"),
        FieldPanel("content"),
    ]


class VacanciesPage(BaseMaterialPage):
    """
        Модель для вакансий сайта
    """
    url = models.URLField("Партнерская ссылка на вакансию")

    parent_page_type = ["home.RubricVacanciesPage"]

    content_panels = BaseMaterialPage.content_panels + [
        FieldPanel('url'),
        InlinePanel('elements_vacancy', heading="Выберите элемент вакансии"),
    ]

    class Meta(BaseMaterialPage.Meta):
        verbose_name = "Вакансия"
        verbose_name_plural = "Вакансии"


@register_snippet
class ElementsVacanciesSnippet(models.Model):
    """
        Справочник для элементов вакансий
    """
    name = models.CharField("Название элемента вакансии",
                            max_length=150, null=False, blank=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Элемент для вакансии"
        verbose_name_plural = "Элементы для вакансии"

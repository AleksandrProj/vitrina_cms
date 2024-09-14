from django.db import models

from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField, StreamField
from wagtail.snippets.models import register_snippet
from wagtail.admin.panels import (
    FieldPanel,
    InlinePanel,
    MultiFieldPanel,
)

from wagtailmetadata.models import MetadataPageMixin

from modelcluster.fields import ParentalKey

from home.blocks import (
    VacanciesBlock,
    HeaderBlock,
    FooterBlock,
    FormBlock,
)


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
        MultiFieldPanel([
            FieldPanel("seo_title_footer"),
            FieldPanel("seo_description_footer"),
        ], "Нижний SEO блок для страниц"),
    ]

    class Meta:
        abstract = True


class HomePage(SeoPageMixin):
    """
        Модель главной страницы
    """
    body = StreamField([
        ("vacancies", VacanciesBlock(label="Блок лучших вакансий")),
    ],
    use_json_field=True,
    blank=True,
    verbose_name="Блоки для главной страницы",
    block_counts={
        "vacancies": {
            "max_num": 1,
        }
    }
    )

    name_button = models.CharField("Название для кнопки", max_length=100, null=True, blank=False)
    url_button = models.ForeignKey(
        "home.RubricVacanciesPage",
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Страница для ссылки",
    )

    content_panels = SeoPageMixin.content_panels + [
        FieldPanel("body"),
        MultiFieldPanel([
            FieldPanel("name_button"),
            FieldPanel("url_button"),
        ], heading="Кнопка просмотра всех вакансий")
    ]

    subpage_types = [
        "home.RubricArticlesPage",
        "home.RubricVacanciesPage",
    ]

    class Meta:
        verbose_name = "Главная страница"
        verbose_name_plural = "Главная страницы"


class RubricArticlesPage(SeoPageMixin):
    """
        Рубрика для статей
    """
    template = "home/articles-list.html"
    description = models.CharField(
        "Описание рубрики статей", max_length=255, null=False, blank=True)

    parent_page_type = ["home.HomePage"]
    subpage_types = ["home.ArticlesPage"]

    max_count = 1

    content_panels = SeoPageMixin.content_panels + [
        FieldPanel("description")
    ]

    class Meta:
        verbose_name = "Рубрика для статей"
        verbose_name_plural = "Рубрики для статей"


class RubricVacanciesPage(SeoPageMixin):
    """
        Рубрика для вакансий
    """
    template = "home/vacancies-list.html"
    description = models.CharField(
        "Описание рубрики вакансий", max_length=255, null=False, blank=True)

    parent_page_type = ["home.HomePage"]
    subpage_types = ["home.VacanciesPage"]

    max_count = 1

    content_panels = SeoPageMixin.content_panels + [
        FieldPanel("description")
    ]

    class Meta:
        verbose_name = "Рубрика для вакансий"
        verbose_name_plural = "Рубрики для вакансий"


class BaseMaterialPage(SeoPageMixin):
    """
        Базовая модель для материалов сайта
    """
    title_description_block = models.CharField("Название блока для описания", max_length=150, null=True, blank=False)
    description = RichTextField("Описание материала")
    short_description = models.CharField("Краткое описание материала", max_length=200, null=True, blank=False)
    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        verbose_name="Изображение для материала",
        help_text="Выберите подходящее изображение материала из галереи и добавьте сюда",
        related_name="+",
    )
    caption_image = models.CharField(
        "Подпись для изображения", max_length=150, blank=False, null=True)
    
    content_panels = SeoPageMixin.content_panels + [
        MultiFieldPanel([
            FieldPanel("title_description_block"),
            FieldPanel("short_description"),
            FieldPanel("description"),
        ], heading="Блок описания"),

        MultiFieldPanel([
            FieldPanel("image"),
            FieldPanel("caption_image"),
        ], heading="Блок изображения"),
    ]
    
    class Meta:
        abstract=True

class ArticlesPage(BaseMaterialPage):
    """
        Модель для статей сайта
    """  
    template = "home/article-detail.html"

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
    pp_name_button = models.CharField("Название для кнопки вакансии", max_length=100, null=True, blank=False)
    pp_url_button = models.URLField("Ссылка для кнопки вакансии", null=True, blank=False)

    parent_page_type = ["home.RubricVacanciesPage"]

    content_panels = BaseMaterialPage.content_panels + [
        MultiFieldPanel([
            FieldPanel('pp_name_button'),
            FieldPanel('pp_url_button'),
        ], "Кнопка партнерской ссылки"),
        InlinePanel('elements_vacancy', heading="Выберите элемент вакансии"),
    ]

    class Meta(BaseMaterialPage.Meta):
        verbose_name = "Вакансия"
        verbose_name_plural = "Вакансии"


# Snippets
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


@register_snippet
class HeaderAndFooterSnippet(models.Model):
    """
        Snippet меню
    """
    logo = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        verbose_name="Логотип сайта",
        related_name="+",
    )
    caption_logo = models.CharField("Подпись для логотипа", max_length=100, null=False, blank=False)
    header = StreamField([
        ('header_block', HeaderBlock())
    ],
    use_json_field=True,
    blank=True,
    verbose_name = "Блок шапки сайта",
    block_counts = {
        "header_block": {
            "max_num": 1
        }
    }) 
    footer = StreamField([
        ('footer_block', FooterBlock())
    ],
    use_json_field=True,
    blank=True,
    verbose_name = "Блок подвала сайта",
    block_counts = {
        "footer_block": {
            "max_num": 1
        }
    })

    panels = [
        MultiFieldPanel([
            FieldPanel('logo'),
            FieldPanel('caption_logo'),
        ]),
        FieldPanel('header'),
        FieldPanel('footer'),
    ]

    def __str__(self) -> str:
        return f"Блок шапки и подвала ({self.pk})"

    class Meta:
        verbose_name = "Блок шапки и подвала"
        verbose_name_plural = "Блоки шапки и подвала"


@register_snippet
class MainBannerSnippet(models.Model):
    """
        Модель для первого экрана для всего сайта
    """
    header = RichTextField(features=['h1'], verbose_name="Заголовок")
    form = StreamField([
        ("form_block", FormBlock())
    ],
    use_json_field=True,
    blank=True,
    verbose_name = "Блок формы подписки",
    block_counts = {
        "form_block": {
            "max_num": 1
        }
    }) 
    cover = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        verbose_name="Изображение для главного экрана",
        related_name="+",
    )

    def __str__(self) -> str:
        return f"Форма подписки для сайта ({self.pk})"

    class Meta:
        verbose_name = "Блок первого экрана сайта"
        verbose_name_plural = "Блоки первого экрана сайта"
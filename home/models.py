import re

from datetime import datetime

from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField, StreamField
from wagtail.snippets.models import register_snippet
from wagtail.documents import get_document_model
from wagtail.admin.panels import (
    FieldPanel,
    InlinePanel,
    MultiFieldPanel,
)

from wagtailmetadata.models import MetadataPageMixin

from modelcluster.fields import ParentalKey

from transliterate import slugify

from home.blocks import (
    VacanciesBlock,
    ArticlesBlock,
    HeaderBlock,
    FooterBlock,
)

from backend.utils import get_paginator


def get_image_model_string():
    try:
        image_model = settings.WAGTAILIMAGES_IMAGE_MODEL
    except AttributeError:
        image_model = 'wagtailimages.Image'
    return image_model

class SeoPageMixin(MetadataPageMixin, Page):
    """
        Класс миксин для добавление моделям seo параметров
    """
    seo_keyword = models.CharField(
        "Ключевые слова", help_text="Ключевые слова для поисковых систем", default="", max_length=255, blank=True, null=False)
    seo_site = models.CharField(
        "SEO сайт", max_length=255, blank=True, null=False)
    seo_title_footer = models.CharField(
        "Заголовок нижнего SEO блока", max_length=200, blank=False, null=False)
    seo_description_footer = models.TextField(
        "Описание нижнего SEO блока", blank=False, null=False)
    search_image = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=False,
        related_name='+',
        on_delete=models.SET_NULL,
        verbose_name=_('SEO Изображение страницы'),
        help_text=_("Добавьте изображение страницы для поисковых систем")
    )

    promote_panels = MetadataPageMixin.promote_panels + [
        FieldPanel("seo_keyword"),
        FieldPanel("seo_site"),
        MultiFieldPanel([
            FieldPanel("seo_title_footer"),
            FieldPanel("seo_description_footer"),
        ], "Нижний SEO блок для страниц"),
    ]

    def get_meta_title(self):
        return self.seo_title or self.title
    
    def get_meta_description(self):
        return self.search_description
    
    def get_meta_image(self):
        return self.search_image
    
    def get_context(self, request, *args, **kwargs):
        """
            Главный кастомный контекст
        """
        context = super().get_context(request, *args, **kwargs)
        context['main_banner'] = MainBannerSnippet.objects.first()
        context['kolontituls'] = HeaderAndFooterSnippet.objects.first()
        context['year_page'] = datetime.now().year
        return context
    

    def save(self, *args, **kwargs):
        name_current_class = self.__class__.__name__ 
        
        if not self.seo_title:
            self.seo_title = self.title

        if name_current_class == 'RubricArticlesPage':
            self.slug = 'articles'
        elif name_current_class == 'RubricVacanciesPage':
            self.slug = 'vacancies'
        elif name_current_class == 'HomePage':
            self.slug = 'home'
        else:
            if self.slug:
                self.slug = self.slug if not re.search('[а-яА-Я]', self.slug) else slugify(self.title)
            elif not self.slug:
                self.slug = slugify(self.title)

        return super().save(*args, **kwargs)

    class Meta:
        abstract = True


class HomePage(SeoPageMixin):
    """
        Модель главной страницы
    """
    body = StreamField([
        ("vacancies", VacanciesBlock(label="Блок вакансий на главной")),
        ("articles", ArticlesBlock(label="Блок статей на главной")),
    ],
    use_json_field=True,
    blank=True,
    verbose_name="Блоки для главной страницы",
    block_counts={
        "vacancies": {
            "max_num": 1,
        },
        "articles": {
            "max_num": 1,
        }
    })

    content_panels = SeoPageMixin.content_panels + [
        FieldPanel("body"),
    ]

    subpage_types = [
        "home.RubricArticlesPage",
        "home.RubricVacanciesPage",
    ]

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('home')
    
    def get_preview_template(self, request, mode_name):
        return f"home/home_page.html"

    def get_context(self, request, *args, **kwargs):
        """
            Кастомный контекст для главной страницы
        """
        # Определение основного контекста
        context = super().get_context(request, *args, **kwargs)

        # Написание пользовательского контекста
        context['page'] = self

        return context

    class Meta:
        verbose_name = "Главная страница"
        verbose_name_plural = "Главная страницы"


class RubricArticlesPage(SeoPageMixin):
    """
        Рубрика для статей
    """
    description = models.CharField(
        "Описание рубрики статей", max_length=300, null=False, blank=True)

    parent_page_type = ["home.HomePage"]
    subpage_types = ["home.ArticlesPage"]

    max_count = 1

    content_panels = SeoPageMixin.content_panels + [
        FieldPanel("description")
    ]

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('articles')
    
    def get_preview_template(self, request, mode_name):
        return f"home/articles-list.html"
    
    def get_context(self, request, *args, **kwargs):
        """
            Кастомный контекст для рубрики статей
        """
        # Определение основного контекста
        context = super().get_context(request, *args, **kwargs)

        # Написание пользовательского контекста
        articles_list = ArticlesPage.objects.filter(live=True)
        context['rubric'] = self
        context['pages'] = get_paginator(request, articles_list, per_page=10)

        return context

    class Meta:
        verbose_name = "Рубрика для статей"
        verbose_name_plural = "Рубрики для статей"


class RubricVacanciesPage(SeoPageMixin):
    """
        Рубрика для вакансий
    """
    template = "home/vacancies-list.html"
    description = models.CharField(
        "Описание рубрики вакансий", max_length=300, null=False, blank=True)

    parent_page_type = ["home.HomePage"]
    subpage_types = ["home.VacanciesPage"]

    max_count = 1

    content_panels = SeoPageMixin.content_panels + [
        FieldPanel("description")
    ]

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('vacancies')
    
    def get_preview_template(self, request, mode_name):
        return f"home/vacancies-list.html"

    def get_context(self, request, *args, **kwargs):
        """
            Кастомный контекст для рубрики вакансий
        """
        # Определение основного контекста
        context = super().get_context(request, *args, **kwargs)

        # Написание пользовательского контекста
        vacancies_list = VacanciesPage.objects.filter(live=True)
        context['rubric'] = self
        context['pages'] = get_paginator(request, vacancies_list, per_page=10)

        return context

    class Meta:
        verbose_name = "Рубрика для вакансий"
        verbose_name_plural = "Рубрики для вакансий"


class BaseMaterialPage(SeoPageMixin):
    """
        Базовая модель для материалов сайта
    """
    title_description_block = models.CharField("Название блока для описания", max_length=150, null=True, blank=True, default="Описание", editable=False)
    description = RichTextField("Описание материала")
    short_description = models.CharField("Краткое описание материала", max_length=300, null=True, blank=False)
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
    is_send_email = models.BooleanField("Флаг отправки email", default=False)

    content_panels = SeoPageMixin.content_panels + [
        MultiFieldPanel([
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

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('article_detail', kwargs={'slug': self.slug})
    
    def get_preview_template(self, request, mode_name):
        return f"home/article-detail.html"

    def get_context(self, request, *args, **kwargs):
        """
            Кастомный контекст для детальной страницы статьи
        """
        # Определение основного контекста
        context = super().get_context(request, *args, **kwargs)

        # Написание пользовательского контекста
        context['article'] = self

        return context

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
    template_name = ""
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

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('vacancy_detail', kwargs={'slug': self.slug})
    
    def get_preview_template(self, request, mode_name):
        return f"home/vacancy-detail.html"

    def get_context(self, request, *args, **kwargs):
        """
            Кастомный контекст для детальной страницы вакансии
        """
        # Определение основного контекста
        context = super().get_context(request, *args, **kwargs)

        # Написание пользовательского контекста
        context['vacancy'] = self

        return context

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
    privacy_policy_document = models.ForeignKey(
        get_document_model(),
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        verbose_name="Документ политики конфидициальности",
        related_name="+"
    )
    policy_personal_document = models.ForeignKey(
        get_document_model(),
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        verbose_name="Документ обработки персональных данных",
        related_name="+"
    )
    agreement_document = models.ForeignKey(
        get_document_model(),
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        verbose_name="Документ согласия на обработку данных",
        related_name="+"
    )
    cookie_document = models.ForeignKey(
        get_document_model(),
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        verbose_name="Документ обработки cookie",
        related_name="+"
    )

    panels = [
        MultiFieldPanel([
            FieldPanel('logo'),
            FieldPanel('caption_logo'),
        ]),
        FieldPanel('header'),
        FieldPanel('footer'),
        MultiFieldPanel([
            FieldPanel('privacy_policy_document'),
            FieldPanel('policy_personal_document'),
            FieldPanel('agreement_document'),
            FieldPanel('cookie_document'),
        ])
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
    cover = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        verbose_name="Изображение для главного экрана",
        related_name="+",
    )

    def __str__(self) -> str:
        return f"Первый экран для сайта ({self.pk})"

    class Meta:
        verbose_name = "Блок первого экрана сайта"
        verbose_name_plural = "Блоки первого экрана сайта"
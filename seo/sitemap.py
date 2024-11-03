from django.conf import settings
from django.contrib.sitemaps import Sitemap

from home.models import (
    HomePage,
    ArticlesPage,
    VacanciesPage,
    RubricArticlesPage,
    RubricVacanciesPage,
)


class MainSitemap(Sitemap):
    """
        Главный класс для всех Sitemaps с определенными параметрами
    """
    protocol = "https" if not settings.DEBUG else "http"
    changefreq = "weekly"
    priority = 0.9


class HomeSitemap(MainSitemap):
    """
        Sitemap для главной страницы
    """
    def items(self):
        return HomePage.objects.filter(live=True)
    
    def lastmod(self, obj):
        return obj.latest_revision_created_at


class RubricArticlesSitemap(MainSitemap):
    """
        Sitemap для страницы рубрики статей
    """
    def items(self):
        return RubricArticlesPage.objects.filter(live=True)
    
    def lastmod(self, obj):
        return obj.latest_revision_created_at
    

class RubricVacanciesSitemap(MainSitemap):
    """
        Sitemap для страницы рубрики вакансий
    """
    def items(self):
        return RubricVacanciesPage.objects.filter(live=True)
    
    def lastmod(self, obj):
        return obj.latest_revision_created_at


class ArticlesSitemap(MainSitemap):
    """
        Sitemap для страниц статей
    """
    def items(self):
        return ArticlesPage.objects.filter(live=True)
    
    def lastmod(self, obj):
        return obj.latest_revision_created_at
    
    
class VacanciesSitemap(MainSitemap):
    """
        Sitemap для страниц вакансий
    """
    def items(self):
        return VacanciesPage.objects.filter(live=True)
    
    def lastmod(self, obj):
        return obj.latest_revision_created_at
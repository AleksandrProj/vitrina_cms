from django.contrib.sitemaps import Sitemap
from home.models import (
    HomePage,
    ArticlesPage,
    VacanciesPage,
    RubricArticlesPage,
    RubricVacanciesPage,
)


class HomeSitemap(Sitemap):
    """
        Sitemap для главной страницы
    """
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return HomePage.objects.filter(live=True)
    
    def lastmod(self, obj):
        return obj.latest_revision_created_at


class RubricArticlesSitemap(Sitemap):
    """
        Sitemap для страницы рубрики статей
    """
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return RubricArticlesPage.objects.filter(live=True)
    
    def lastmod(self, obj):
        return obj.latest_revision_created_at
    

class RubricVacanciesSitemap(Sitemap):
    """
        Sitemap для страницы рубрики вакансий
    """
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return RubricVacanciesPage.objects.filter(live=True)
    
    def lastmod(self, obj):
        return obj.latest_revision_created_at


class ArticlesSitemap(Sitemap):
    """
        Sitemap для страниц статей
    """
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return ArticlesPage.objects.filter(live=True)
    
    def lastmod(self, obj):
        return obj.latest_revision_created_at
    
    
class VacanciesSitemap(Sitemap):
    """
        Sitemap для страниц вакансий
    """
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return VacanciesPage.objects.filter(live=True)
    
    def lastmod(self, obj):
        return obj.latest_revision_created_at
from datetime import datetime
from typing import Any

from django.shortcuts import render
from django.views.generic.base import View, ContextMixin

from home.models import (
    HomePage,
    VacanciesPage,
    RubricVacanciesPage,
    ArticlesPage,
    RubricArticlesPage,
    HeaderAndFooterSnippet,
    MainBannerSnippet,
)

from seo.views import SEOViewSet

from backend.utils import get_paginator


class MainViewsetMixin(SEOViewSet, ContextMixin):
    """
        Главный Viewset для всех представлений
    """
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        from mailing.views import SubscribersViewSet
        
        subscriber_form = SubscribersViewSet.get_context_data(SubscribersViewSet(), **kwargs)
        seo = SEOViewSet.get_context_data(SEOViewSet(), **kwargs)
        main_banner_queryset = MainBannerSnippet.objects.first()
        kolontituls_queryset = HeaderAndFooterSnippet.objects.first()
        year_page_queryset = datetime.now().year

        context = {
            'main_banner': main_banner_queryset,
            'kolontituls': kolontituls_queryset,
            'year_page': year_page_queryset,
            'seo': seo,
            'form': subscriber_form['form']
        }
        return context

    
class HomePageViewset(View, MainViewsetMixin):
    """
        Viewset для главной страницы
    """
    def get(self, request, **kwargs):
        context = super().get_context_data(**kwargs)
        page_queryset = HomePage.objects.first()

        context['page'] = page_queryset

        return render(request, "home/home_page.html", context)


class ArticlesListViewset(View, MainViewsetMixin):
    """
        Viewset для вывода списка статьей
    """
    def get(self, request, **kwargs):
        context = super().get_context_data(**kwargs)
        rubric_articles = RubricArticlesPage.objects.first()
        article_list = ArticlesPage.objects.filter(live=True)   
        
        context['rubric'] = rubric_articles
        context['pages'] = get_paginator(request, article_list, per_page=10)

        return render(request, "home/articles-list.html", context)


class ArticlesDetailViewset(View, MainViewsetMixin):
    """
        Viewset для вывода детальной информации по статье
    """
    def get(self, request, slug, **kwargs):
        context = super().get_context_data(**kwargs)
        
        try:
            article_queryset = ArticlesPage.objects.get(slug=slug)
        except ArticlesPage.DoesNotExist:
            return render(request, "404.html", context)
        
        context['article'] = article_queryset

        return render(request, "home/article-detail.html", context)


class VacanciesListViewset(View, MainViewsetMixin):
    """
        Viewset для вывода списка вакансий
    """
    def get(self, request, **kwargs):
        context = super().get_context_data(**kwargs)
        rubric_vacancies = RubricVacanciesPage.objects.first()
        vacancies_list = VacanciesPage.objects.filter(live=True)   
        
        context['rubric'] = rubric_vacancies
        context['pages'] = get_paginator(request, vacancies_list, per_page=10)

        return render(request, "home/vacancies-list.html", context)


class VacanciesDetailViewset(View, MainViewsetMixin):
    """
        Viewset для вывода детальной информации по вакансии
    """
    def get(self, request, slug, **kwargs):
        context = super().get_context_data(**kwargs)
        
        try:
            vacancy_queryset = VacanciesPage.objects.get(slug=slug)
        except VacanciesPage.DoesNotExist:
            return render(request, "404.html", context)
        
        context['vacancy'] = vacancy_queryset

        return render(request, "home/vacancy-detail.html", context)
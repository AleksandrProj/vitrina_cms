from datetime import datetime
from typing import Any

from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.base import View, ContextMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from home.models import (
    HomePage,
    VacanciesPage,
    RubricVacanciesPage,
    ArticlesPage,
    RubricArticlesPage,
    HeaderAndFooterSnippet,
    MainBannerSnippet,
)


class MainViewsetMixin(ContextMixin):
    """
        Главный Viewset для всех представлений
    """
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        main_banner_queryset = MainBannerSnippet.objects.first()
        kolontituls_queryset = HeaderAndFooterSnippet.objects.first()
        year_page_queryset = datetime.now().year

        context = {
            'main_banner': main_banner_queryset,
            'kolontituls': kolontituls_queryset,
            'year_page': year_page_queryset,
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
        article_list = ArticlesPage.objects.all()    
        
        # Пагинатор 
        paginator = Paginator(article_list, 3)   
        page_number = request.GET.get('page', 1)
        try:
            articles = paginator.page(page_number)
        except PageNotAnInteger:
            articles = paginator.page(1)
        except EmptyPage:
            articles = paginator.page(paginator.num_pages)
        
        context['rubric'] = rubric_articles
        context['articles'] = articles

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


class VacanciesListViewset(ListView):
    """
        Viewset для вывода списка вакансий
    """
    model=VacanciesPage
    template_name="home/vacancies-list.html"

    # def get_queryset(self):
    #     queryset = super(CLASS_NAME, self).get_queryset()
    #     queryset = queryset # TODO
    #     return queryset


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
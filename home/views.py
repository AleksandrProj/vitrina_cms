from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.base import View

from home.models import (
    HomePage,
    VacanciesPage,
    ArticlesPage,
    HeaderAndFooterSnippet,
)


class HomePageViewset(View):
    """
        Viewset для главной страницы
    """
    def get(self, request, *args, **kwargs):
        page_queryset = HomePage.objects.first()
        kolontituls_queryset = HeaderAndFooterSnippet.objects.first()
        return render(request, "home/home_page.html", {
            'kolontituls': kolontituls_queryset,
            'page': page_queryset,
        })


class ArticlesListViewset(ListView):
    """
        Viewset для вывода списка статьей
    """
    model=ArticlesPage
    template_name="home/articles-list.html"

    # def get_queryset(self):
    #     queryset = super(CLASS_NAME, self).get_queryset()
    #     queryset = queryset # TODO
    #     return queryset


class ArticlesDetailViewset(DetailView):
    """
        Viewset для вывода детальной информации по статье
    """
    model=ArticlesPage
    template_name="home/article-detail.html"

    # def get_queryset(self):
    #     queryset = super(CLASS_NAME, self).get_queryset()
    #     queryset = queryset # TODO
    #     return queryset


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


class VacanciesDetailViewset(DetailView):
    """
        Viewset для вывода детальной информации по вакансии
    """
    model=VacanciesPage
    template_name="home/vacancy-detail.html"

    # def get_queryset(self):
    #     queryset = super(CLASS_NAME, self).get_queryset()
    #     queryset = queryset # TODO
    #     return queryset
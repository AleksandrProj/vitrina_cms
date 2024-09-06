from django.views.generic.list import ListView

from home.models import HomePage


class ArticlesViewset(ListView):
    model=HomePage
    template_name="home/articles.html"

    # def get_queryset(self):
    #     queryset = super(CLASS_NAME, self).get_queryset()
    #     queryset = queryset # TODO
    #     return queryset


class VacanciesViewset(ListView):
    model=HomePage
    template_name="home/vacancies.html"

    # def get_queryset(self):
    #     queryset = super(CLASS_NAME, self).get_queryset()
    #     queryset = queryset # TODO
    #     return queryset
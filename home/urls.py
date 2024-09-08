from django.urls import path

from home.views import (
    HomePageViewset,
    ArticlesListViewset, 
    ArticlesDetailViewset,
    VacanciesListViewset,
    VacanciesDetailViewset,
)


urlpatterns = [
    path("articles/", ArticlesListViewset.as_view(), name="articles"),
    path("articles/<slug:slug>", ArticlesDetailViewset.as_view(), name="article_detail"),
    path("vacancies/", VacanciesListViewset.as_view(), name="vacancies"),
    path("vacancies/<slug:slug>", VacanciesDetailViewset.as_view(), name="vacancy_detail"),
    path("", HomePageViewset.as_view(), name="home"),
]
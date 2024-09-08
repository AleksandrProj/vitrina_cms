from django.urls import path

from home.views import (
    HomePageViewset,
    ArticlesListViewset, 
    ArticlesDetailViewset,
    VacanciesListViewset,
    VacanciesDetailViewset,
)


urlpatterns = [
    path("articles/", ArticlesListViewset.as_view(), name="list-articles"),
    path("articles/<slug:slug>", ArticlesDetailViewset.as_view(), name="detail_article"),
    path("vacancies/", VacanciesListViewset.as_view(), name="list-vacancies"),
    path("vacancies/<slug:slug>", VacanciesDetailViewset.as_view(), name="detail_vacancy"),
    path("", HomePageViewset.as_view(), name="main-page"),
]
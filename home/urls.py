from django.urls import include, path

from home.views import ArticlesViewset, VacanciesViewset

urlpatterns = [
    path("articles/", ArticlesViewset.as_view(), name="articles"),
    path("vacancies/", VacanciesViewset.as_view(), name="vacancies"),
]
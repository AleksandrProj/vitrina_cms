from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def str_to_bool(value):
    """Преобразование строчных значений True/False в булевый тип

    Args:
        value (str): значения True/False в строковом формате

    Returns:
        bool: состояние флага в булевом типе
    """
    if value == "True":
        return True
    elif value == "False":
        return False
    

def show_toolbar(request):
    """
        Функция обработки django toolbar
    """
    return settings.IS_SHOW_TOOLBAR


def get_paginator(request, list_data, per_page=10):
    """Функция для пагинации

    Args:
        request (_type_): параметр request
        list_data (_type_): Набор queryset
        per_page (int, optional): Кол-во карточек на странице

    Returns:
        paginator: Возращает модель пагинатора
    """
    paginator = Paginator(list_data, per_page)   
    page_number = request.GET.get('page', 1)
    try:
        articles = paginator.page(page_number)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)

    return articles
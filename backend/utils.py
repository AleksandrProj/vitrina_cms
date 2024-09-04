from django.conf import settings


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
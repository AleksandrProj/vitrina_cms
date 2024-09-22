from wagtail import hooks


@hooks.register('before_copy_page')
def before_copy_page(request, page):
    """
        Hooks для копирования страниц
    """
    if request.method == "POST":
        page.seo_title = request.POST['new_title']
        page.save()
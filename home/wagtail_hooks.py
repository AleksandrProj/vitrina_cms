from wagtail import hooks
from wagtail.models import ReferenceIndex

from home.models import (
    Page,
)

from backend.exceptions import UsageException


# Hooks
@hooks.register('before_copy_page')
def before_copy_page(request, page):
    """
        Hooks для копирования страниц
    """
    if request.method == "POST":
        page.seo_title = request.POST['new_title']
        page.save()


@hooks.register('before_delete_page')
def before_delete_page(request, page):
    """Block awesome page deletion and show a message."""

    if request.method == 'POST':
        if ReferenceIndex.get_grouped_references_to(page).count():
            raise UsageException(f"{page.title} используется и не может быть удален!")
        

@hooks.register("before_bulk_action")
def hook_func(request, action_type, objects, action_class_instance):
    if action_type == 'delete':
        instances_error = []
        for instance in objects:
            if isinstance(instance, Page):
                instance = instance.specific
            if ReferenceIndex.get_grouped_references_to(instance).count(): instances_error.append(instance.__str__())
        if instances_error:
            raise UsageException(f"{', '.join(instances_error)} используется(-ются) и не может быть удален!")
from typing import Any

from django.views.generic import TemplateView
from django.views.generic.base import View, ContextMixin
from django.shortcuts import render

from wagtail.models import Site

from seo.forms import SEOAdminForm
from seo.models import SEO


# Views SEO module
class SEOAdminView(View):
    def get(self, request):
        if not SEO.objects.count():
            seo = SEO()
            seo.save()
        else:
            seo = SEO.objects.first()

        seo_form = SEOAdminForm(instance=seo)
        context = {'form': seo_form}
        return render(request, 'seo/index.html', context=context)

    def post(self, request):
        seo_form = SEOAdminForm(data=request.POST, instance=SEO.objects.first())
        if seo_form.is_valid():
            seo_form.save()

        return render(request, 'seo/index.html', context={'form': seo_form})


class SEOViewSet(ContextMixin):
     def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        seo = SEO.objects.first()
        seo_dict = {
            "yandex_metric": seo.metric_yandex if seo is not None else None,
            "yandex_webmaster": seo.yandex_webmaster if seo is not None else None,
            "google_metric": seo.google_analytics if seo is not None else None,
            "google_webmaster": seo.google_webmaster if seo is not None else None,
        }

        return seo_dict


class RobotsView(TemplateView):

    content_type = 'text/plain'

    def get_template_names(self):
        return 'robots.txt'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        request = context['view'].request
        context['wagtail_site'] = Site.find_for_request(request)
        return context
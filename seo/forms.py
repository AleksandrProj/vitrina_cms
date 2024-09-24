from wagtail.admin.forms.models import WagtailAdminModelForm

from seo.models import SEO


# Forms SEO module

class SEOAdminForm(WagtailAdminModelForm):
    class Meta:
        model = SEO
        fields = ['metric_yandex', 'yandex_webmaster', 'google_analytics', 'google_webmaster']

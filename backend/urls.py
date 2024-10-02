from django.conf import settings
from django.urls import include, path

from wagtail import urls as wagtail_urls
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls

from search import views as search_views

from mailing.views import HandleSubscribersView

urlpatterns = [
    path("admin/", include(wagtailadmin_urls)),
    path("media/documents/", include(wagtaildocs_urls)),
    path("search/", search_views.search, name="search"),

    path("subscribe/", HandleSubscribersView.as_view(), name="subscribe"),
    path("subscribe/success/<int:subscribe_id>", HandleSubscribersView.as_view(), name="subscribe_success"),
    path("subscribe/fail", HandleSubscribersView.as_view(), name="subscribe_fail"),
    path("", include("home.urls"))
]


if settings.DEBUG:
    import debug_toolbar
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    from django.views import defaults as default_views

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls)),]
    urlpatterns = [
        path('404/', default_views.page_not_found, kwargs={'exception': Exception("Page not Found")}),
        path('500/', default_views.server_error),
    ] + urlpatterns

urlpatterns = urlpatterns + [
    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's page serving mechanism. This should be the last pattern in
    # the list:
    path("", include(wagtail_urls)),
    # Alternatively, if you want Wagtail pages to be served from a subpath
    # of your site, rather than the site root:
    #    path("pages/", include(wagtail_urls)),
]

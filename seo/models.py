from django.db import models


class SEO(models.Model):
    """
        SEO модель
    """
    metric_yandex = models.IntegerField(verbose_name='Яндекс.Метрика - Идентификатор счётчика аналитики', blank=True, null=True)
    google_analytics = models.CharField(verbose_name='Google Analytics - Идентификатор счётчика аналитики', max_length=255, blank=True, null=True)
    yandex_webmaster = models.CharField(verbose_name="Yandex webmaster - Индентификатор счетчика кабинета вебмастер", max_length=255, blank=True, null=True)
    google_webmaster = models.CharField(verbose_name="Google webmaster - Индентификатор счетчика кабинета вебмастер", max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = 'SEO'

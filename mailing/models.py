from django.db import models


class Subscribers(models.Model):
    """
        Модель подписчиков
    """
    name = models.CharField("Имя подписчика", max_length=200, blank=False, null=True)
    email = models.EmailField("E-mail подписчика", blank=False, null=True)

    class Meta:
        unique_together = ['email']
        verbose_name = "Подписчик"
        verbose_name_plural = "Подписчики"

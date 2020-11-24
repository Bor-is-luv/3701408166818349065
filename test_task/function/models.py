from django.db import models
from django.utils.html import format_html
from django.core.exceptions import ValidationError

from django.utils.safestring import mark_safe


class Function(models.Model):
    equation = models.CharField('Формула функции', max_length=30)
    graph = models.ImageField('График функции', blank=True, null=True)
    datetime = models.DateTimeField('Дата обработки', blank=True, null=True)
    interval = models.IntegerField('Глубина периода моделирования в днях')
    dt = models.IntegerField('Шаг в часах')
    exception = models.CharField('Ошибка', max_length=100, blank=True, null=True)

    def graph_or_error(self):
        if self.exception:
            return format_html(
                "<div>"
                f"{self.exception}"
                "</div>"
            )
        elif self.graph:
            return format_html(
                '<img src="{}">', mark_safe(self.graph.url)
            )
        else:
            return "---"

    def clean(self):
        if self.dt is not None and self.interval is not None:
            if self.dt <= 0 or self.interval <= 0:
                raise ValidationError("dt and interval must be positive")
        else:
            raise ValidationError("dt or interval is empty")

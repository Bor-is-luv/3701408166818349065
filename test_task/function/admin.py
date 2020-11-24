from django.contrib import admin

from .models import Function
from .tasks import task_to_gen_graph_and_save

from django.db import transaction

from django.contrib.auth.models import User

try:
    User.objects.create_superuser(username='admin', email='mail@mail.ru', password='qwerty1234')
except:
    pass


@admin.register(Function)
class AdminFunction(admin.ModelAdmin):
    exclude = ('datetime', 'graph', 'exception', 'graph_or_error')
    list_display = 'equation', 'graph_or_error', 'interval', 'dt', 'datetime'

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        transaction.on_commit(lambda: task_to_gen_graph_and_save.apply_async((obj.id,)).get())

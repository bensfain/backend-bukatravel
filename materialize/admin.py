from django.contrib import admin
from solo.admin import SingletonModelAdmin

from materialize.models import TemplateConfig

admin.site.register(TemplateConfig, SingletonModelAdmin)

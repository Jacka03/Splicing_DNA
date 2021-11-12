from django.contrib import admin

# Register your models here.
from . import models

admin.site.register(models.User)


class GeneInfoAdmin(admin.ModelAdmin):

    list_display = ('id', 'email', 'date')
    list_per_page = 25


admin.site.register(models.GeneInfo, GeneInfoAdmin)

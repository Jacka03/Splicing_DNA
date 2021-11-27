from django.contrib import admin

# Register your models here.
from . import models

admin.site.register(models.User)


class GeneInfoAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'date', 'min_len', 'max_len', 'gene_len', 'pools', 'get_avg_pool')

    @admin.display(ordering='get_avg_pool')
    def get_avg_pool(self, obj):
        return obj.gene_len / obj.pools

    list_per_page = 25


admin.site.register(models.GeneInfo, GeneInfoAdmin)

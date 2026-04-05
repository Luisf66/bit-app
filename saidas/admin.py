from django.contrib import admin
from saidas.models import Saidas, Categorias_Saidas
# Register your models here.

class SaidasAdmin(admin.ModelAdmin):
    list_display = ('data', 'valor', 'descricao', 'categoria')

class Categorias_SaidasAdmin(admin.ModelAdmin):
    list_display = ('nome',)

admin.site.register(Saidas, SaidasAdmin)
admin.site.register(Categorias_Saidas, Categorias_SaidasAdmin)
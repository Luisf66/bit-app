from django.contrib import admin
from entradas.models import Entradas, Categorias_Entradas
# Register your models here.

class EntradasAdmin(admin.ModelAdmin):
    list_display = ('data', 'valor', 'descricao', 'categoria')

class Categorias_EntradasAdmin(admin.ModelAdmin):
    list_display = ('nome',)

admin.site.register(Entradas, EntradasAdmin)
admin.site.register(Categorias_Entradas, Categorias_EntradasAdmin)
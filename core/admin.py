from django.contrib import admin
from .models import Productos, Restaurantes, Usuarios, Pedidos

admin.site.register(Productos)
admin.site.register(Restaurantes)
admin.site.register(Pedidos)  # ← agregá esta línea

@admin.register(Usuarios)
class UsuariosAdmin(admin.ModelAdmin):
   list_display = ('id_usuario', 'nombre', 'email', 'rol')
   search_fields = ('nombre', 'email')
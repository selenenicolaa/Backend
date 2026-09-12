from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('apps.core.urls')),  
    # cambio debido a que en core.urls.py ya no tenemos 
    #el prefijo 'api/' en las rutas
]
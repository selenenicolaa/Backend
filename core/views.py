from django.http import HttpResponse, JsonResponse
from .models import Productos

def inicio(request):
    return HttpResponse("API funcionando")
def productos(request):
    productos = Productos.objects.all()

    data = []

    for p in productos:
        data.append({
            "id": p.id_producto,
            "name": p.nombre,
            "price": p.precio,
            "description": p.descripcion,
            "stock": p.stock,
            "image": p.imagen_url,
            "available": p.disponible,
            "restaurante": p.id_restaurante_id
        })

    return JsonResponse(data, safe=False)

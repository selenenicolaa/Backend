from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from .models import Productos, Usuarios, Pedidos, Categoria

#este DEF lo que hace es leer el token JWT del header de la peticion
#y devuelve el id_restaurante que esta guardado dentro del token. 
# Si el token es invalido o no existe, devuelve None.
def get_restaurante_from_token(request):
    
    auth_header = request.headers.get('Authorization', '')
    # lee el token del header Authorization, que tiene el formato "Bearer <token>" para
    # evitar problemas de seguridad. 
    if not auth_header.startswith('Bearer '): #bearer: formato estandar para enviar tokens en el header
        return None                           # para evitar problemas de seguridad.
    
    token_str = auth_header.split(' ')[1] #extrae el token del header, que viene después de "Bearer "
    try:
        from rest_framework_simplejwt.tokens import AccessToken 
        #importamos AccessToken para decodificar el token y obtener el id_restaurante
        token = AccessToken(token_str)
        return token.get('id_restaurante')
    except (InvalidToken, TokenError):
        return None


class LoginView(APIView):

    def post(self, request):
        nombre = request.data.get('nombre')
        contrasena = request.data.get('contrasena')

        if not nombre or not contrasena:
            return Response(
                {'error': 'Usuario y contraseña son requeridos'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            usuario = Usuarios.objects.get(nombre=nombre, contrasena=contrasena)
        except Usuarios.DoesNotExist:
            return Response(
                {'error': 'Credenciales inválidas'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        if not usuario.id_restaurante:
            return Response(
                {'error': 'Este usuario no tiene un restaurante asignado'},
                status=status.HTTP_403_FORBIDDEN
            )

        # Generamos el token y metemos el id_restaurante adentro.
        token = RefreshToken()
        token['id_usuario'] = usuario.id_usuario
        token['nombre'] = usuario.nombre
        token['id_restaurante'] = usuario.id_restaurante.id_restaurante

        return Response({
            'access': str(token.access_token),
            'refresh': str(token),
            'id_usuario': usuario.id_usuario,
            'nombre': usuario.nombre,
            'email': usuario.email,
            'rol': usuario.rol,
            'id_restaurante': usuario.id_restaurante.id_restaurante,
            'nombre_restaurante': usuario.id_restaurante.nombre,
        })


# PRODUCTOS: solo se puede acceder a este panel si el token válido, para que muestre
# los productos del restaurante que corresponde al token. 
# No se puede acceder a productos de otros restaurantes.
class ProductosView(APIView):

    def get(self, request):
        #se lee el token y se obtiene el id_restaurante para filtrar los productos de ese restaurante
        id_restaurante = get_restaurante_from_token(request)

        if not id_restaurante:
            return Response(
                {'error': 'Token inválido o no enviado'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        productos = Productos.objects.filter(id_restaurante=id_restaurante)

        data = [
            {
                "id_producto": p.id_producto,
                "nombre": p.nombre,
                "descripcion": p.descripcion,
                "precio": float(p.precio) if p.precio else 0,
                "stock": p.stock,
                "imagen_url": p.imagen_url,
                "disponible": p.disponible,
            }
            for p in productos
        ]
        return Response(data)

    def post(self, request):
        # El restaurante viene del token, no del body — así no puede falsificarlo
        id_restaurante = get_restaurante_from_token(request)

        if not id_restaurante:
            return Response(
                {'error': 'Token inválido o no enviado'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        nombre = request.data.get('nombre')
        precio = request.data.get('precio')

        if not all([nombre, precio]):
            return Response(
                {'error': 'nombre y precio son requeridos'},
                status=status.HTTP_400_BAD_REQUEST
            )

        producto = Productos.objects.create(
            nombre=nombre,
            precio=precio,
            descripcion=request.data.get('descripcion', ''),
            stock=request.data.get('stock', 0),
            imagen_url=request.data.get('imagen_url', ''),
            disponible=request.data.get('disponible', True),
            id_restaurante_id=id_restaurante,  # Viene del token, no del usuario
        )

        return Response({
            'id_producto': producto.id_producto,
            'nombre': producto.nombre,
            'precio': float(producto.precio),
        }, status=status.HTTP_201_CREATED)

# PEDIDOS... Lo mismoq que productos
class PedidosView(APIView):

    def get(self, request):
        id_restaurante = get_restaurante_from_token(request)

        if not id_restaurante:
            return Response(
                {'error': 'Token inválido o no enviado'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        pedidos = Pedidos.objects.filter(id_restaurante=id_restaurante)

        data = [
            {
                "id_pedido": p.id_pedido,
                "fecha": p.fecha,
                "estado": p.estado if p.estado is not None else 0,
                "total": float(p.total) if p.total else 0,
                "direccion_entega": p.direccion_entega,
                "id_usuario": p.id_usuario_id,
            }
            for p in pedidos
        ]
        return Response(data)

    def put(self, request, pedido_id):
        id_restaurante = get_restaurante_from_token(request)

        if not id_restaurante:
            return Response(
                {'error': 'Token inválido o no enviado'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        try:
            # Buscamos el pedido Y verificamos que pertenezca al restaurante del token
            pedido = Pedidos.objects.get(pk=pedido_id, id_restaurante=id_restaurante)
        except Pedidos.DoesNotExist:
            return Response(
                {'error': 'Pedido no encontrado o no pertenece a tu restaurante'},
                status=status.HTTP_404_NOT_FOUND
            )

        pedido.estado = request.data.get('estado', pedido.estado)
        pedido.save()
        return Response({'id_pedido': pedido.id_pedido, 'estado': pedido.estado})
   
   
    #lista de categorias
class CategoriasView(APIView):

    def get(self, request):

        id_restaurante = get_restaurante_from_token(request)

        categorias = Categoria.objects.filter(
            id_restaurante=id_restaurante
        )

        data = [
            {
                "id_categoria": c.id_categoria,
                "nombre": c.nombre
            }
            for c in categorias
        ]

        return Response(data)
#crear categorias
def post(self, request):

    id_restaurante = get_restaurante_from_token(request)

    nombre = request.data.get("nombre")

    categoria = Categoria.objects.create(
        nombre=nombre,
        id_restaurante_id=id_restaurante
    )

    return Response(
        {
            "id_categoria": categoria.id_categoria,
            "nombre": categoria.nombre
        },
        status=status.HTTP_201_CREATED
    )

#edicion de la categoria
def put(self, request, categoria_id):

    id_restaurante = get_restaurante_from_token(request)

    try:
        categoria = Categoria.objects.get(
            pk=categoria_id,
            id_restaurante=id_restaurante
        )

    except Categoria.DoesNotExist:

        return Response(
            {"error": "Categoria no encontrada"},
            status=status.HTTP_404_NOT_FOUND
        )

    categoria.nombre = request.data.get(
        "nombre",
        categoria.nombre
    )

    categoria.save()

    return Response({
        "id_categoria": categoria.id_categoria,
        "nombre": categoria.nombre
    })

#esta parte es de categoria pero de agregar y eliminar
class CategoriaDetailView(APIView):

    def put(self, request, categoria_id):
        try:
            categoria = Categoria.objects.get(pk=categoria_id)
        except Categoria.DoesNotExist:
            return Response(
                {"error": "Categoría no encontrada"},
                status=status.HTTP_404_NOT_FOUND
            )

        categoria.nombre = request.data.get(
            "nombre",
            categoria.nombre
        )

        categoria.save()

        return Response({
            "id_categoria": categoria.id_categoria,
            "nombre": categoria.nombre
        })

    def delete(self, request, categoria_id):
        try:
            categoria = Categoria.objects.get(pk=categoria_id)
        except Categoria.DoesNotExist:
            return Response(
                {"error": "Categoría no encontrada"},
                status=status.HTTP_404_NOT_FOUND
            )

        categoria.delete()

        return Response(
            {"mensaje": "Categoría eliminada"},
            status=status.HTTP_204_NO_CONTENT
        )
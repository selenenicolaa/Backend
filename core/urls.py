from django.urls import path
from .views import ProductosView, LoginView, PedidosView, CategoriasView, CategoriaDetailView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login_api'),
    path('products/', ProductosView.as_view(), name='productos_api'),
    path('orders/', PedidosView.as_view(), name='pedidos_api'),
    path('orders/<int:pedido_id>/', PedidosView.as_view(), name='pedido_update'),
    path("categorias/", CategoriasView.as_view()),
    path( 'categorias/<int:categoria_id>/',  CategoriaDetailView.as_view(), name='categoria_detail' ),
]
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Categoria(models.Model):
    id_categoria = models.BigAutoField(db_column='id_Categoria', primary_key=True)  # Field name made lowercase.
    nombre = models.CharField()
    id_restaurante = models.ForeignKey('Restaurantes', models.DO_NOTHING, db_column='id_restaurante',blank=True, null=True, 
        #se agrega esto para que no choque con el atributo de categoria de restaurante
        related_name='categorias')
  
    class Meta:
        managed = False
        db_table = 'categoria'


class DetallePedido(models.Model):
    id_detalle = models.BigAutoField(primary_key=True)
    cantidad = models.FloatField()
    subtotal = models.FloatField(blank=True, null=True)
    id_pedido = models.ForeignKey('Pedidos', models.DO_NOTHING, db_column='id_pedido', blank=True, null=True)
    id_producto = models.ForeignKey('Productos', models.DO_NOTHING, db_column='id_producto', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'detalle_pedido'
        db_table_comment = 'productos dentro del pedido'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Entrega(models.Model):
    id_entrega = models.BigAutoField(primary_key=True)
    estado = models.BooleanField()
    hora_salida = models.TimeField(blank=True, null=True)
    hora_entrega = models.TimeField(blank=True, null=True)
    id_pedido = models.ForeignKey('Pedidos', models.DO_NOTHING, db_column='id_pedido', blank=True, null=True)
    id_repartidor = models.ForeignKey('Repartidor', models.DO_NOTHING, db_column='id_repartidor', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'entrega'


class Pagos(models.Model):
    id_pago = models.BigAutoField(primary_key=True)
    metodo_pago = models.TextField()
    monto = models.FloatField(blank=True, null=True)
    estado_pago = models.BooleanField(blank=True, null=True)
    fecha_pago = models.FloatField(blank=True, null=True)
    id_pedido = models.ForeignKey('Pedidos', models.DO_NOTHING, db_column='id_pedido', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pagos'


class Pedidos(models.Model):
    id_pedido = models.BigAutoField(primary_key=True)
    fecha = models.DateTimeField()
    estado = models.DateField(blank=True, null=True)
    total = models.FloatField(blank=True, null=True)
    direccion_entega = models.CharField(blank=True, null=True)
    id_usuario = models.ForeignKey('Usuarios', models.DO_NOTHING, db_column='id_usuario', blank=True, null=True)
    id_restaurante = models.ForeignKey('Restaurantes', models.DO_NOTHING, db_column='id_restaurante', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pedidos'


class Productos(models.Model):
    id_producto = models.BigAutoField(primary_key=True)
    nombre = models.CharField()
    descripcion = models.CharField(blank=True, null=True)
    precio = models.FloatField(blank=True, null=True)
    stock = models.SmallIntegerField(blank=True, null=True)
    imagen_url = models.CharField(blank=True, null=True)
    disponible = models.BooleanField(blank=True, null=True)
    id_restaurante = models.ForeignKey('Restaurantes', models.DO_NOTHING, db_column='id_restaurante', blank=True, null=True)
    id_categoria = models.ForeignKey(Categoria, models.DO_NOTHING, db_column='id_Categoria', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'productos'
        db_table_comment = 'menu restaurantes/locales'


class Repartidor(models.Model):
    id_repartidor = models.BigAutoField(primary_key=True)
    nombre = models.CharField()
    telefono = models.SmallIntegerField(blank=True, null=True)
    vehiculo = models.CharField(blank=True, null=True)
    disponible = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'repartidor'


class Restaurantes(models.Model):
    id_restaurante = models.BigAutoField(primary_key=True)
    nombre = models.CharField()
    direccion = models.CharField(blank=True, null=True)
    telefono = models.SmallIntegerField(blank=True, null=True)
    categoria = models.TextField(blank=True, null=True)
    estado = models.CharField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'restaurantes'
        db_table_comment = 'infromacion de los comercios'


class Usuarios(models.Model):
    id_usuario = models.BigAutoField(primary_key=True)
    nombre = models.CharField()
    email = models.CharField(blank=True, null=True)
    telefono = models.SmallIntegerField(blank=True, null=True)
    contrasena = models.CharField(blank=True, null=True)
    direccion = models.CharField(blank=True, null=True)
    rol = models.BooleanField(blank=True, null=True)
    id_restaurante = models.ForeignKey(Restaurantes, models.DO_NOTHING, db_column='id_restaurante', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'usuarios'
        db_table_comment = 'guarda clientes y admins'

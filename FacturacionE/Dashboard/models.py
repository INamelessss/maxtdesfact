from django.db import models

# Create your models here.
class Cliente(models.Model):
    tipo_documento = models.CharField(max_length=10, default='DNI')
    numero_documento = models.CharField(max_length=20)
    razon_social = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    celular = models.CharField(max_length=20, blank=True, null=True)  # Suponiendo que puede ser opcional
    direccion = models.TextField()
    departamento = models.CharField(max_length=50, blank=True, null=True)
    provincia = models.CharField(max_length=50, blank=True, null=True)
    distrito = models.CharField(max_length=50, blank=True, null=True)
    cuenta_detraccion = models.CharField(max_length=50, blank=True, null=True)  # Suponiendo que puede ser opcional
    detalles_adicionales = models.TextField(blank=True, null=True)  # Suponiendo que puede ser opcional

class Categoria(models.Model):
    nombre = models.CharField(max_length=255, unique=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True)  # Esta línea añade la fecha de creación

class Unidad(models.Model):
    unidad = models.CharField(max_length=5)
    nombre = models.CharField(max_length=50)

class Producto(models.Model):
    codigo = models.CharField(max_length=50, unique=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    descripcion = models.TextField()
    unidad = models.ForeignKey(Unidad, on_delete=models.SET_NULL, null=True)
    moneda = models.CharField(max_length=10) # Puedes agregar más monedas si es necesario
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2)
    observaciones = models.TextField(blank=True, null=True)
    incluye_igv = models.BooleanField(default=False)
    afecto_icbper = models.BooleanField(default=False)

class Sucursal(models.Model):
    codigo_sunat = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=255)
    direccion = models.TextField()
    departamento = models.CharField(max_length=50)
    provincia = models.CharField(max_length=50)
    distrito = models.CharField(max_length=50)
    telefono = models.CharField(max_length=20,blank=True, null=True )
    correo_electronico = models.EmailField(blank=True, null=True)
    pagina_web = models.URLField(blank=True, null=True)

class Stock(models.Model):
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=0)

class Ingreso(models.Model):
    motivo = models.CharField(max_length=50, default='ingreso_productos')
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE)
    requisicion = models.CharField(max_length=100, blank=True, null=True)
    orden_compra = models.CharField(max_length=100, blank=True, null=True)
    fecha = models.DateTimeField(auto_now_add=True)

class DetalleIngreso(models.Model):
    ingreso = models.ForeignKey(Ingreso, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()

class Salida(models.Model):
    motivo = models.CharField(max_length=50, default='salida_productos')
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE)
    requisicion = models.CharField(max_length=100, blank=True, null=True)
    orden_compra = models.CharField(max_length=100, blank=True, null=True)
    fecha = models.DateTimeField(auto_now_add=True)

class DetalleSalida(models.Model):
    salida = models.ForeignKey(Salida, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()

class NotaDeCredito(models.Model):
    codigo = models.CharField(max_length=50, unique=True)
    razon = models.CharField(max_length=255)
    tipo_documento = models.CharField(max_length=10, default='DNI')
    numero_documento = models.CharField(max_length=20)
    direccion = models.TextField()
    fecha_emision = models.DateField()
    tipo_documento_afectado = models.CharField(max_length=50)  # Puedes agregar más opciones si es necesario
    anulacion_operacion = models.BooleanField(default=False)
    documento_que_modifica_serie = models.CharField(max_length=10)  # Asumiendo un tamaño arbitrario
    documento_que_modifica_correlativo = models.IntegerField()
    igv = models.DecimalField(max_digits=10, decimal_places=2)
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2)

class Factura(models.Model):
    codigo = models.CharField(max_length=50, unique=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)  # El modelo Cliente ya fue definido anteriormente
    fecha_emision = models.DateField()
    fecha_vencimiento = models.DateField(null=True, blank=True)  # Es opcional según el formulario
    moneda = models.CharField(max_length=20)  # Puedes añadir más monedas si es necesario
    tipo_venta = models.CharField(max_length=50)  # Puedes añadir más opciones si es necesario
    importe_en_letras = models.TextField()
    modo_envio = models.CharField(max_length=50)

class Boleta(models.Model):
    codigo = models.CharField(max_length=50, unique=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)  # El modelo Cliente ya fue definido anteriormente
    fecha_emision = models.DateField()
    fecha_vencimiento = models.DateField(null=True, blank=True)  # Es opcional según el formulario
    moneda = models.CharField(max_length=20)  # Puedes añadir más monedas si es necesario
    tipo_venta = models.CharField(max_length=50)  # Puedes añadir más opciones si es necesario
    importe_en_letras = models.TextField()
    modo_envio = models.CharField(max_length=50)

class DetalleFactura(models.Model):
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

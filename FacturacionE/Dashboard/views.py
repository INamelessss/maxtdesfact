from django.contrib.auth import views as auth_views
from django.shortcuts import get_object_or_404, render, redirect
from django.http import JsonResponse
from .models import *
from .forms import CategoriaForm, SucursalForm
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView
from django.contrib import messages
from django.shortcuts import redirect
from django.views import View
from django.http import JsonResponse
from django.db import transaction
from django.contrib.auth.models import User
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from django.template.loader import render_to_string
from django.http import HttpResponse
from xhtml2pdf import pisa
from .forms import UserRegisterForm
from django.contrib.auth.forms import UserChangeForm

def custom_login(request, *args, **kwargs):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        return auth_views.login(request, *args, **kwargs)

def custom_logout(request, *args, **kwargs):
    return auth_views.logout_then_login(request, *args, **kwargs)

def dashboard(request):
    return render(request, 'base.html')

def clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'clientes/clientes.html', {'clientes': clientes})

def nuevocliente(request):
        if request.method == 'POST':
            tipo_documento = request.POST.get('tipoDocumento', 'Sin documento')
            numero_documento = request.POST.get('numDocumento', '')
            razon_social = request.POST.get('nombreCompleto', '')
            email = request.POST.get('inputEmail', '')
            telefono = request.POST.get('inputTelefono', '')
            celular = request.POST.get('inputCelular', '')
            direccion = request.POST.get('inputDireccion', '')
            departamento = request.POST.get('ubigeo_dep', '')
            provincia = request.POST.get('ubigeo_pro', '')
            distrito = request.POST.get('ubigeo_dis', '')
            cuenta_detraccion = request.POST.get('cuentaDetraccion', '')
            detalles_adicionales = request.POST.get('detallesAdicionales', '')

            # Creando el objeto cliente
            cliente = Cliente(
                tipo_documento=tipo_documento,
                numero_documento=numero_documento,
                razon_social=razon_social,
                email=email if email else None,
                telefono=telefono if telefono else None,
                celular=celular if celular else None,
                direccion=direccion,
                departamento=departamento,
                provincia=provincia,
                distrito=distrito,
                cuenta_detraccion=cuenta_detraccion if cuenta_detraccion else None,
                detalles_adicionales=detalles_adicionales if detalles_adicionales else None
            )
            cliente.save()

            # Redireccionar a la página de lista de clientes o donde prefieras después de guardar.
            return redirect('clientes')  # Asegúrate de reemplazar 'nombre_url_lista_clientes' con el nombre de URL adecuado.
        else:
            return render(request, 'clientes/nuevo.html')  # Asegúrate de reemplazar 'ruta_a_tu_template.html' con la ruta a tu template.

def editarcliente(request, id):
    cliente = get_object_or_404(Cliente, id=id) # Obtener el objeto cliente o devolver un error 404

    if request.method == 'POST':
        # Actualizar los campos del objeto cliente con la información del formulario
        cliente.tipo_documento = request.POST.get('tipoDocumento', 'Sin documento')
        cliente.numero_documento = request.POST.get('numDocumento', '')
        cliente.razon_social = request.POST.get('nombreCompleto', '')
        cliente.email = request.POST.get('inputEmail', '')
        cliente.telefono = request.POST.get('inputTelefono', '')
        cliente.celular = request.POST.get('inputCelular', '')
        cliente.direccion = request.POST.get('inputDireccion', '')
        cliente.departamento = request.POST.get('ubigeo_dep', '')
        cliente.provincia = request.POST.get('ubigeo_pro', '')
        cliente.distrito = request.POST.get('ubigeo_dis', '')
        cliente.cuenta_detraccion = request.POST.get('cuentaDetraccion', '')
        cliente.detalles_adicionales = request.POST.get('detallesAdicionales', '')

        cliente.save()

        return redirect('clientes')
    else:
        return render(request, 'clientes/editar.html', {'cliente': cliente})

class CrearFacturaView(View):
    template_name = "comprobantes/factura.html"

    def get(self, request):
        sucursal_id = "1"  # Asumo que el ID de la sucursal es 1. Cambia esto si es dinámico.
        cantidad_facturas = Factura.objects.all().count() + 1

        codigo_sucursal = sucursal_id.zfill(4)
        codigo_factura = str(cantidad_facturas).zfill(8)

        codigo_final = f"F{codigo_sucursal} - {codigo_factura}"
        productos = Producto.objects.all()
        clientes = Cliente.objects.all()
        context = {
            'clientes': clientes,
            'productos': productos,
            'codigo_final':codigo_final,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        # Recogemos los datos del formulario
        cliente_id = request.POST.get('cliente')
        fecha_emision = request.POST.get('fecha_emision')
        fecha_vencimiento = request.POST.get('fecha_vencimiento')
        moneda = request.POST.get('moneda')
        tipo_venta = request.POST.get('tipo_venta')
        importe_en_letras = request.POST.get('importe_en_letras')
        modo_envio = request.POST.get('modoEnvio')

        sucursal_id = "1"  # Asumo que el ID de la sucursal es 1. Cambia esto si es dinámico.
        cantidad_facturas = Factura.objects.all().count() + 1

        codigo_sucursal = sucursal_id.zfill(4)
        codigo_factura = str(cantidad_facturas).zfill(8)
        codigo_final = f"F{codigo_sucursal} - {codigo_factura}"

        cliente_registrado = 'clienteRegistrado' in request.POST
        if not cliente_registrado:
            # Crea un nuevo cliente
            cliente = Cliente.objects.create(
                razon_social=request.POST.get('nombre_cliente'),
                direccion=request.POST.get('direccion'),
                tipo_documento='RUC',
                numero_documento=request.POST.get('ruc')
            )
            cliente_id = cliente.id
        else:
            cliente_id = request.POST.get('cliente')

        factura = Factura.objects.create(
            codigo=codigo_final,
            cliente_id=cliente_id,
            fecha_emision=fecha_emision,
            fecha_vencimiento=fecha_vencimiento if fecha_vencimiento else None,
            moneda=moneda,
            tipo_venta=tipo_venta,
            importe_en_letras=importe_en_letras,
            modo_envio=modo_envio
        )

        productos = request.POST.getlist('producto')
        cantidades = request.POST.getlist('cantidad')

        for prod, qty in zip(productos, cantidades):
            producto = Producto.objects.get(id=prod)
            detalle = DetalleFactura.objects.create(
                factura=factura,
                producto=producto,
                cantidad=int(qty),
                precio_unitario=producto.precio_venta
            )

        return redirect('factura')

def get_datos_por_ruc(request):
    ruc = request.GET.get('ruc', None)
    data = obtener_datos_por_ruc(ruc)
    if not data:
        data = {
            'error': 'RUC especificado no encontrada'
        }
    return JsonResponse(data)

def obtener_datos_por_ruc(ruc):
    # Iniciar el navegador
    driver = webdriver.Chrome()

    # Ir a la página
    driver.get("https://e-consultaruc.sunat.gob.pe/cl-ti-itmrconsruc/FrameCriterioBusquedaWeb.jsp")

    # Encontrar el input de RUC y llenarlo
    input_ruc = driver.find_element(By.ID, "txtRuc")
    input_ruc.send_keys(ruc)

    # Hacer clic en el botón Buscar
    btn_aceptar = driver.find_element(By.ID, "btnAceptar")
    btn_aceptar.click()

    # Esperar a que los datos se carguen (ajusta el tiempo si es necesario)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "list-group-item-text"))
    )

    # Extraer los datos (ajusta estos selectores según tus necesidades)
    nombre = driver.find_elements(By.CLASS_NAME, "list-group-item-text")[1].text
    domicilio_fiscal = driver.find_elements(By.CLASS_NAME, "list-group-item-text")[6].text

    # Cerrar el navegador
    driver.quit()

    return {
        'nombre': nombre,
        'domicilio_fiscal': domicilio_fiscal
    }

def boleta(request):
    return render(request, 'comprobantes/boleta.html')

def notadebito(request):
    return render(request, 'comprobantes/notadebito.html')

def notacredito(request):
    return render(request, 'comprobantes/notacredito.html')

def categorias(request):
    categorias = Categoria.objects.all()
    return render(request, 'categorias/categorias.html', {'categorias':categorias})

def nuevacategoria(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('categorias')
    else:
        form = CategoriaForm()

    context = {
        'form': form,
    }

    return render(request, 'categorias/nuevo.html', context)

class CategoriaUpdateView(UpdateView):
    model = Categoria
    fields = ['nombre']  # Asegúrate de que el nombre del campo coincida con tu modelo
    template_name = 'categorias/editar.html'  # Cambia esto al nombre real de tu archivo template
    context_object_name = 'categoria'
    success_url = reverse_lazy('categorias')  # Cambia 'lista_categorias' al nombre de la URL donde deseas redirigir después de una edición exitosa

def nuevoproducto(request):
    if request.method == "POST":
        # Handle the form submission
        codigo = request.POST.get('codigo')
        categoria_id = request.POST.get('categoria')
        unidad_id = request.POST.get('unidad')
        descripcion = request.POST.get('descripcion')
        moneda = request.POST.get('moneda')
        precio_venta = request.POST.get('precio_venta')
        observaciones = request.POST.get('observaciones')
        incluye_igv = request.POST.get('incluye_igv') == 'on'
        afecto_icbper = request.POST.get('afecto_icbper') == 'on'

        categoria = Categoria.objects.get(pk=categoria_id)
        unidad = Unidad.objects.get(pk=unidad_id)

        Producto.objects.create(
            codigo=codigo,
            categoria=categoria,
            descripcion=descripcion,
            unidad=unidad,
            moneda=moneda,
            precio_venta=precio_venta,
            observaciones=observaciones,
            incluye_igv=incluye_igv,
            afecto_icbper=afecto_icbper
        )
        messages.success(request, 'Producto creado exitosamente!')
        return redirect('productos')

    categorias = Categoria.objects.all()
    unidades = Unidad.objects.all()

    context = {
        'categorias': categorias,
        'unidades': unidades,
    }

    return render(request, 'productos/nuevo.html', context)

def productos(request):
    productos = Producto.objects.all()  # Consulta para obtener todos los productos

    context = {
        'productos': productos,
    }

    return render(request, 'productos/productos.html', context)

def editarproducto(request, id):
    producto = get_object_or_404(Producto, pk=id)  # Use get_object_or_404 for better error handling

    if request.method == "POST":
        # Handle the form submission
        codigo = request.POST.get('codigo')
        categoria_id = request.POST.get('categoria')
        unidad_id = request.POST.get('unidad')
        descripcion = request.POST.get('descripcion')
        moneda = request.POST.get('moneda')
        precio_venta = request.POST.get('precio_venta')
        observaciones = request.POST.get('observaciones')
        incluye_igv = request.POST.get('incluye_igv') == 'on'
        afecto_icbper = request.POST.get('afecto_icbper') == 'on'

        categoria = get_object_or_404(Categoria, pk=categoria_id)
        unidad = get_object_or_404(Unidad, pk=unidad_id)

        # Update the attributes of the producto object
        producto.codigo = codigo
        producto.categoria = categoria
        producto.descripcion = descripcion
        producto.unidad = unidad
        producto.moneda = moneda
        producto.precio_venta = precio_venta
        producto.observaciones = observaciones
        producto.incluye_igv = incluye_igv
        producto.afecto_icbper = afecto_icbper
        producto.save()  # Save the updated product

        messages.success(request, 'Producto actualizado exitosamente!')
        return redirect('productos')

    else:
        categorias = Categoria.objects.all()
        unidades = Unidad.objects.all()

    context = {
        'producto': producto,
        'categorias': categorias,
        'unidades': unidades
    }
    return render(request, 'productos/editar.html', context)

class CrearSalidaView(View):
    template_name = 'movimientos/nuevasalida.html'

    def get(self, request):
        sucursales = Sucursal.objects.all()
        productos = Producto.objects.all()
        context = {
            'sucursales': sucursales,
            'productos': productos,
        }
        return render(request, self.template_name, context)

    @transaction.atomic
    def post(self, request):
        motivo = request.POST.get('motivo')
        sucursal_id = request.POST.get('sucursal')
        sucursal = Sucursal.objects.get(id=sucursal_id)
        requisicion = request.POST.get('requisicion')
        orden_compra = request.POST.get('orden_compra')

        salida = Salida.objects.create(
            motivo=motivo,
            sucursal=sucursal,
            requisicion=requisicion,
            orden_compra=orden_compra
        )

        productos = request.POST.getlist('producto')
        cantidades = request.POST.getlist('cantidad')

        for prod, qty in zip(productos, cantidades):
            producto = Producto.objects.get(id=prod)
            detalle = DetalleSalida.objects.create(
                salida=salida,
                producto=producto,
                cantidad=int(qty)
            )

            # Actualizar o crear el stock en la sucursal
            stock, created = Stock.objects.get_or_create(
                sucursal=sucursal,
                producto=producto,
                defaults={'cantidad': int(qty)}
            )

            if not created:
                stock.cantidad -= int(qty)
                stock.save()

        return redirect('salidas')

def salidas(request):
    salidas = Salida.objects.all()
    return render(request, 'movimientos/salida.html', {'salidas':salidas})

def ingresos(request):
    ingresos = Ingreso.objects.all()
    return render(request, 'movimientos/ingreso.html', {'ingresos':ingresos})

class CrearIngresoView(View):
    template_name = 'movimientos/nuevoingreso.html'

    def get(self, request):
        sucursales = Sucursal.objects.all()
        productos = Producto.objects.all()
        context = {
            'sucursales': sucursales,
            'productos': productos,
        }
        return render(request, self.template_name, context)

    @transaction.atomic
    def post(self, request):
        motivo = request.POST.get('motivo')
        sucursal_id = request.POST.get('sucursal')
        sucursal = Sucursal.objects.get(id=sucursal_id)
        requisicion = request.POST.get('requisicion')
        orden_compra = request.POST.get('orden_compra')

        # Creamos el Ingreso
        ingreso = Ingreso.objects.create(
            motivo=motivo,
            sucursal=sucursal,
            requisicion=requisicion,
            orden_compra=orden_compra
        )

        productos = request.POST.getlist('producto')
        cantidades = request.POST.getlist('cantidad')

        for prod, qty in zip(productos, cantidades):
            producto = Producto.objects.get(id=prod)
            detalle = DetalleIngreso.objects.create(
                ingreso=ingreso,
                producto=producto,
                cantidad=int(qty)
            )

            # Actualizar o crear el stock en la sucursal
            stock, created = Stock.objects.get_or_create(
                sucursal=sucursal,
                producto=producto,
                defaults={'cantidad': int(qty)}
            )

            if not created:
                stock.cantidad += int(qty)
                stock.save()

        return redirect('ingresos')

def stock(request):
    stocks = Stock.objects.select_related('sucursal', 'producto').all()
    return render(request, 'stock/stock.html', {'stocks': stocks})

def sucursales(request):
    sucursales = Sucursal.objects.all()  # Consulta para obtener todos los productos

    context = {
        'sucursales': sucursales,
    }
    return render(request, 'sucursales/sucursales.html',context)

def nuevasucursal(request):
    if request.method == "POST":
        # Handle the form submission
        codigo_sunat = request.POST.get('codigo')
        nombre = request.POST.get('nombre')
        direccion = request.POST.get('direccion')
        departamento = request.POST.get('ubigeo_dep')
        provincia = request.POST.get('ubigeo_pro')
        distrito = request.POST.get('ubigeo_dis')
        telefono = request.POST.get('telefono')
        correo_electronico = request.POST.get('correo')
        pagina_web = request.POST.get('web')

        Sucursal.objects.create(
            codigo_sunat=codigo_sunat,
            nombre=nombre,
            direccion=direccion,
            departamento=departamento,
            provincia=provincia,
            distrito=distrito,
            telefono=telefono,
            correo_electronico=correo_electronico,
            pagina_web=pagina_web
        )

        messages.success(request, 'Sucursal creada exitosamente!')
        return redirect('sucursales')

    return render(request, 'sucursales/nuevo.html')

def editarsucursal(request, id):
    sucursal = get_object_or_404(Sucursal, pk=id)  # Use get_object_or_404 for better error handling

    if request.method == "POST":
        # Handle the form submission
        codigo_sunat = request.POST.get('codigo')
        nombre = request.POST.get('nombre')
        direccion = request.POST.get('direccion')
        departamento = request.POST.get('ubigeo_dep')
        provincia = request.POST.get('ubigeo_pro')
        distrito = request.POST.get('ubigeo_dis')
        telefono = request.POST.get('telefono')
        correo_electronico = request.POST.get('correo')
        pagina_web = request.POST.get('web')

        sucursal.codigo_sunat = codigo_sunat
        sucursal.nombre = nombre
        sucursal.direccion = direccion
        sucursal.departamento = departamento
        sucursal.provincia = provincia
        sucursal.distrito = distrito
        sucursal.telefono = telefono
        sucursal.correo_electronico = correo_electronico
        sucursal.pagina_web = pagina_web
        sucursal.save()  # Save the updated product

        messages.success(request, 'Sucursal creada exitosamente!')
        return redirect('sucursales')

    return render(request, 'sucursales/editar.html',{'sucursal': sucursal})

def get_precio_producto(request):
    producto_id = request.GET.get('producto_id')
    try:
        producto = Producto.objects.get(id=producto_id)
        precio = str(producto.precio_venta)  # Convertir a string para ser serializable en JSON
    except Producto.DoesNotExist:
        precio = "0.00"

    return JsonResponse({'precio': precio})

def lista_documentos(request):
    # Obtener todos los documentos
    boletas = Boleta.objects.all()
    facturas = Factura.objects.all()
    notas_credito = NotaDeCredito.objects.all()

    # Crear una lista unificada
    documentos = []

    for boleta in boletas:
        documentos.append({
            'fecha': boleta.fecha_emision,
            'comprobante': boleta.codigo,
            'cliente': f"{boleta.cliente.numero_documento} - {boleta.cliente.razon_social}"
        })

    for factura in facturas:
        documentos.append({
            'fecha': factura.fecha_emision,
            'comprobante': factura.codigo,
            'cliente': f"{factura.cliente.numero_documento} - {factura.cliente.razon_social}"
        })

    for nota_credito in notas_credito:
        documentos.append({
            'fecha': nota_credito.fecha_emision,
            'comprobante': nota_credito.codigo,
            'cliente': f"{nota_credito.numero_documento} - {nota_credito.razon}"
        })

    # Ordenar documentos por fecha (opcional)
    documentos.sort(key=lambda x: x['fecha'])

    return render(request, 'comprobantes/comprobantes.html', {'documentos': documentos})

def descargar_pdf(request, codigo):
    # Obtener la factura por su código
    factura = Factura.objects.get(codigo=codigo)

    # Obtener los detalles de la factura
    detalles = DetalleFactura.objects.filter(factura=factura)

    # Renderizar la plantilla HTML con los datos de la factura
    html_string = render_to_string('pdf.html', {
        'factura': factura,
        'detalles': detalles,
        'cliente': factura.cliente
    })

    # Crear una respuesta HTTP de tipo PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Factura_{factura.codigo}.pdf"'

    # Convertir el HTML en un PDF y escribirlo en la respuesta
    pisa_status = pisa.CreatePDF(
        html_string, dest=response
    )

    # Manejar posibles errores en la creación del PDF
    if pisa_status.err:
        return HttpResponse('Tuvimos algunos errores <pre>' + html_string + '</pre>')
    return response

def descargar_xml(request, codigo):
    # Obtener la factura por su código
    factura = Factura.objects.get(codigo=codigo)

    # Obtener los detalles de la factura
    detalles = DetalleFactura.objects.filter(factura=factura)

    # Renderizar la plantilla XML con los datos de la factura
    xml_string = render_to_string('xml.xml', {
        'factura': factura,
        'detalles': detalles,
        'cliente': factura.cliente
    })

    # Crear una respuesta HTTP con el contenido XML
    response = HttpResponse(xml_string, content_type='application/xml')
    response['Content-Disposition'] = f'attachment; filename="Factura_{factura.codigo}.xml"'

    return response

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')  # Redirecciona a la página de login
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

def list_users(request):
    users = User.objects.all()
    return render(request, 'user_list.html', {'users': users})

def edit_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'User updated successfully')
            return redirect('list_users')
    else:
        form = UserChangeForm(instance=user)
    return render(request, 'edit_user.html', {'form': form})

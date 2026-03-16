# logica.py
import re
# Lógica de negocio para la aplicación de gestión de productos, países, precios e impuestos, y generación de reportes. Incluye funciones para validar datos, manejar archivos de almacenamiento, realizar cálculos y generar reportes en diferentes formatos, así como enviar reportes por correo electrónico.
import smtplib
# Para el envío de correos electrónicos, se utilizan las clases MIMEText y MIMEMultipart para construir el mensaje con formato adecuado, incluyendo el cuerpo del correo con los detalles del reporte generado.
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
# La función obtener_datos_usuario se encarga de cargar los datos de configuración del usuario desde un archivo, y si el archivo no existe, devuelve valores vacíos para nombre y correo, lo que permite manejar la situación de manera adecuada en la interfaz.
from datetime import datetime
# Se define una expresión regular para validar el formato de correo electrónico, asegurando que los datos ingresados por el usuario sean correctos antes de guardarlos o utilizarlos para enviar reportes.
EMAIL_REGEX = r"^[\w\.-]+@[\w\.-]+\.\w+$"
# Se definen listas globales para almacenar los productos, países y registros de precios e impuestos, junto con contadores para asignar IDs únicos a cada nuevo registro agregado.
MONEDAS = ["CRC", "USD", "EUR", "BRL"]
productos = []
contador_productos = 1
paises = []
contador_paises = 1
precios_impuestos = []
contador_registros = 1


# --------------------------------------------------------------
# CONFIGURACIÓN DE USUARIO
# --------------------------------------------------------------

# Función para validar el formato de correo electrónico utilizando una expresión regular, asegurando que los datos ingresados por el usuario sean correctos antes de guardarlos o utilizarlos para enviar reportes.
def validar_correo(correo):
    return re.match(EMAIL_REGEX, correo) is not None

# Función para guardar la configuración del usuario (nombre y correo) en un archivo de texto, validando que los datos no estén vacíos y que el correo tenga un formato válido antes de guardarlos.
def guardar_config_usuario(nombre, correo, ruta="config_usuario.txt"):
    if not nombre.strip() or not correo.strip():
        raise ValueError("Todos los datos son requeridos.")

    if not validar_correo(correo):
        raise ValueError("Formato de correo electrónico inválido.")

    with open(ruta, "w", encoding="utf-8") as f:
        f.write(f"nombre={nombre.strip()}\n")
        f.write(f"correo={correo.strip()}\n")

# Función para cargar la configuración del usuario desde un archivo de texto, leyendo el contenido del archivo y extrayendo los valores de nombre y correo, validando que el archivo contenga los datos esperados antes de devolverlos.
def cargar_config_usuario_desde_archivo(ruta_archivo):
    with open(ruta_archivo, "r", encoding="utf-8") as archivo:
        lineas = archivo.readlines()

    nombre = ""
    correo = ""

    for linea in lineas:
        if linea.startswith("nombre="):
            nombre = linea.replace("nombre=", "").strip()
        elif linea.startswith("correo="):
            correo = linea.replace("correo=", "").strip()

    if not nombre or not correo:
        raise ValueError("El archivo no contiene los datos esperados de nombre y correo.")

    return nombre, correo

# Función para obtener los datos de usuario, intentando cargar la configuración desde el archivo y devolviendo los valores de nombre y correo, o valores vacíos si el archivo no existe o no contiene los datos esperados.
def obtener_datos_usuario(ruta="config_usuario.txt"):
    try:
        with open(ruta, "r", encoding="utf-8") as f:
            lineas = f.readlines()

        nombre = ""
        correo = ""

        for linea in lineas:
            if linea.startswith("nombre="):
                nombre = linea.replace("nombre=", "").strip()
            elif linea.startswith("correo="):
                correo = linea.replace("correo=", "").strip()

        if nombre and correo:
            return nombre, correo

        return None, None

    except FileNotFoundError:
        return None, None


# --------------------------------------------------------------
# PRODUCTOS
# --------------------------------------------------------------

# Función para guardar la lista de productos en un archivo de texto, escribiendo el contador de productos y los detalles de cada producto en un formato específico, asegurando que los datos se conserven para la próxima vez que se abra la aplicación.
def guardar_productos(ruta="productos.txt"):
    global productos, contador_productos

    with open(ruta, "w", encoding="utf-8") as archivo:
        archivo.write(str(contador_productos) + "\n")
        for producto in productos:
            linea = f"{producto['id']}|{producto['nombre']}|{producto['precio']}\n"
            archivo.write(linea)

# Función para cargar la lista de productos desde un archivo de texto, leyendo el contenido del archivo y extrayendo los detalles de cada producto, validando que el archivo contenga los datos esperados antes de cargarlos en la lista de productos.
def cargar_productos(ruta="productos.txt"):
    global productos, contador_productos

    try:
        with open(ruta, "r", encoding="utf-8") as archivo:
            lineas = archivo.readlines()

        if len(lineas) > 0:
            contador_productos = int(lineas[0].strip())

        productos.clear()
        for linea in lineas[1:]:
            datos = linea.strip().split("|")
            if len(datos) == 3:
                producto = {
                    "id": int(datos[0]),
                    "nombre": datos[1],
                    "precio": float(datos[2])
                }
                productos.append(producto)

    except FileNotFoundError:
        productos.clear()
        contador_productos = 1

# Función para agregar un nuevo producto, validando que el nombre y el precio sean proporcionados y que el precio sea un número positivo antes de agregarlo a la lista de productos y guardarlo en el archivo.
def agregar_producto(nombre, precio_texto):
    global contador_productos

    nombre = nombre.strip()
    precio_texto = precio_texto.strip()

    if not nombre or not precio_texto:
        raise ValueError("Nombre y precio son obligatorios.")

    try:
        precio = float(precio_texto)
        if precio < 0:
            raise ValueError()
    except ValueError:
        raise ValueError("El precio debe ser un número positivo.")

    nuevo = {
        "id": contador_productos,
        "nombre": nombre,
        "precio": precio
    }

    productos.append(nuevo)
    contador_productos += 1
    guardar_productos()
    return nuevo

# Función para actualizar un producto existente, validando que el nombre y el precio sean proporcionados y que el precio sea un número positivo antes de actualizar los detalles del producto en la lista de productos y guardarlo en el archivo, o lanzando un error si el producto no se encuentra.
def actualizar_producto(prod_id, nombre, precio_texto):
    nombre = nombre.strip()
    precio_texto = precio_texto.strip()

    if not nombre or not precio_texto:
        raise ValueError("Nombre y precio son obligatorios.")

    try:
        precio = float(precio_texto)
        if precio < 0:
            raise ValueError()
    except ValueError:
        raise ValueError("El precio debe ser un número positivo.")

    for prod in productos:
        if prod["id"] == prod_id:
            prod["nombre"] = nombre
            prod["precio"] = precio
            guardar_productos()
            return prod

    raise ValueError("Producto no encontrado.")

# Función para eliminar un producto por su ID, buscando el producto en la lista de productos y eliminándolo si se encuentra, luego guardando la lista actualizada en el archivo, o lanzando un error si el producto no se encuentra.
def eliminar_producto_por_id(prod_id):
    global productos
    productos[:] = [p for p in productos if p["id"] != prod_id]
    guardar_productos()

# Función para obtener un producto por su ID, buscando el producto en la lista de productos y devolviéndolo si se encuentra, o devolviendo None si no se encuentra.
def obtener_producto_por_id(prod_id):
    for prod in productos:
        if prod["id"] == prod_id:
            return prod
    return None

# Función para obtener un producto por su nombre, buscando el producto en la lista de productos y devolviéndolo si se encuentra, o devolviendo None si no se encuentra.
def obtener_producto_por_nombre(nombre):
    for prod in productos:
        if prod["nombre"] == nombre:
            return prod
    return None


# --------------------------------------------------------------
# PAÍSES
# --------------------------------------------------------------

# Función para guardar la lista de países en un archivo de texto, escribiendo el contador de países y los detalles de cada país en un formato específico, asegurando que los datos se conserven para la próxima vez que se abra la aplicación.
def guardar_paises(ruta="paises.txt"):
    global paises, contador_paises

    with open(ruta, "w", encoding="utf-8") as archivo:
        archivo.write(str(contador_paises) + "\n")
        for pais in paises:
            archivo.write(f"{pais['id']}|{pais['nombre']}\n")

# Función para cargar la lista de países desde un archivo de texto, leyendo el contenido del archivo y extrayendo los detalles de cada país, validando que el archivo contenga los datos esperados antes de cargarlos en la lista de países.
def cargar_paises(ruta="paises.txt"):
    global paises, contador_paises

    try:
        with open(ruta, "r", encoding="utf-8") as archivo:
            lineas = archivo.readlines()

        if len(lineas) > 0:
            contador_paises = int(lineas[0].strip())

        paises.clear()
        for linea in lineas[1:]:
            datos = linea.strip().split("|")
            if len(datos) == 2:
                paises.append({
                    "id": int(datos[0]),
                    "nombre": datos[1]
                })

    except FileNotFoundError:
        paises.clear()
        contador_paises = 1

# Función para agregar un nuevo país, validando que el nombre sea proporcionado antes de agregarlo a la lista de países y guardarlo en el archivo, o lanzando un error si el nombre está vacío.
def agregar_pais(nombre):
    global contador_paises

    nombre = nombre.strip()
    if not nombre:
        raise ValueError("El nombre del país es obligatorio.")

    nuevo = {
        "id": contador_paises,
        "nombre": nombre
    }

    paises.append(nuevo)
    contador_paises += 1
    guardar_paises()
    return nuevo

# Función para actualizar un país existente, validando que el nombre sea proporcionado antes de actualizar los detalles del país en la lista de países y guardarlo en el archivo, o lanzando un error si el país no se encuentra o si el nombre está vacío.
def actualizar_pais(pais_id, nombre):
    nombre = nombre.strip()
    if not nombre:
        raise ValueError("El nombre del país es obligatorio.")

    for pais in paises:
        if pais["id"] == pais_id:
            pais["nombre"] = nombre
            guardar_paises()
            return pais

    raise ValueError("País no encontrado.")

# Función para eliminar un país por su ID, buscando el país en la lista de países y eliminándolo si se encuentra, luego guardando la lista actualizada en el archivo, o lanzando un error si el país no se encuentra.
def eliminar_pais_por_id(pais_id):
    global paises
    paises[:] = [p for p in paises if p["id"] != pais_id]
    guardar_paises()

# Función para obtener un país por su ID, buscando el país en la lista de países y devolviéndolo si se encuentra, o devolviendo None si no se encuentra.
def obtener_pais_por_id(pais_id):
    for pais in paises:
        if pais["id"] == pais_id:
            return pais
    return None

# Función para obtener un país por su nombre, buscando el país en la lista de países y devolviéndolo si se encuentra, o devolviendo None si no se encuentra.
def obtener_pais_por_nombre(nombre):
    for pais in paises:
        if pais["nombre"] == nombre:
            return pais
    return None


# --------------------------------------------------------------
# PRECIOS E IMPUESTOS
# --------------------------------------------------------------

# Función para guardar la lista de precios e impuestos en un archivo de texto, escribiendo el contador de registros y los detalles de cada registro en un formato específico, asegurando que los datos se conserven para la próxima vez que se abra la aplicación.
def guardar_precios_impuestos(ruta="precios_impuestos.txt"):
    global precios_impuestos, contador_registros

    with open(ruta, "w", encoding="utf-8") as archivo:
        archivo.write(str(contador_registros) + "\n")
        for registro in precios_impuestos:
            linea = (
                f"{registro['id']}|{registro['producto_id']}|"
                f"{registro['pais_id']}|{registro['precio']}|"
                f"{registro['impuesto']}|{registro['moneda']}\n"
            )
            archivo.write(linea)

# Función para cargar la lista de precios e impuestos desde un archivo de texto, leyendo el contenido del archivo y extrayendo los detalles de cada registro, validando que el archivo contenga los datos esperados antes de cargarlos en la lista de precios e impuestos.
def cargar_precios_impuestos(ruta="precios_impuestos.txt"):
    global precios_impuestos, contador_registros

    try:
        with open(ruta, "r", encoding="utf-8") as archivo:
            lineas = archivo.readlines()

        if len(lineas) > 0:
            contador_registros = int(lineas[0].strip())

        precios_impuestos.clear()
        for linea in lineas[1:]:
            datos = linea.strip().split("|")
            if len(datos) == 6:
                registro = {
                    "id": int(datos[0]),
                    "producto_id": int(datos[1]),
                    "pais_id": int(datos[2]),
                    "precio": float(datos[3]),
                    "impuesto": float(datos[4]),
                    "moneda": datos[5]
                }
                precios_impuestos.append(registro)

    except FileNotFoundError:
        precios_impuestos.clear()
        contador_registros = 1

# Función para calcular el costo total de un producto en un país específico, sumando el precio base y el impuesto aplicado, y devolviendo el resultado.
def calcular_costo_total(precio, impuesto):
    return precio + (precio * (impuesto / 100))

# Función para agregar un nuevo registro de precio e impuesto, validando que el producto, país, precio, impuesto y moneda sean proporcionados y que el precio e impuesto sean números positivos antes de agregarlo a la lista de precios e impuestos y guardarlo en el archivo, o lanzando un error si los datos son inválidos o si no se han registrado productos o países.
def agregar_registro_precio_impuesto(producto_nombre, pais_nombre, precio_texto, impuesto_texto, moneda):
    global contador_registros

    if len(productos) == 0:
        raise ValueError("Primero debe registrar al menos un producto.")

    if len(paises) == 0:
        raise ValueError("Primero debe registrar al menos un país.")

    producto_nombre = producto_nombre.strip()
    pais_nombre = pais_nombre.strip()
    precio_texto = precio_texto.strip()
    impuesto_texto = impuesto_texto.strip()
    moneda = moneda.strip()

    if not producto_nombre or not pais_nombre or not precio_texto or not impuesto_texto or not moneda:
        raise ValueError("Todos los datos son obligatorios.")

    try:
        precio = float(precio_texto)
        impuesto = float(impuesto_texto)
        if precio < 0 or impuesto < 0:
            raise ValueError()
    except ValueError:
        raise ValueError("Precio e impuesto (%) deben ser números positivos.")

    producto = obtener_producto_por_nombre(producto_nombre)
    pais = obtener_pais_por_nombre(pais_nombre)

    if producto is None or pais is None:
        raise ValueError("Producto o país inválido.")

    nuevo = {
        "id": contador_registros,
        "producto_id": producto["id"],
        "pais_id": pais["id"],
        "precio": precio,
        "impuesto": impuesto,
        "moneda": moneda
    }

    precios_impuestos.append(nuevo)
    contador_registros += 1
    guardar_precios_impuestos()
    return nuevo

# Función para actualizar un registro de precio e impuesto existente, validando que el producto, país, precio, impuesto y moneda sean proporcionados y que el precio e impuesto sean números positivos antes de actualizar los detalles del registro en la lista de precios e impuestos y guardarlo en el archivo, o lanzando un error si los datos son inválidos o si no se han registrado productos o países, o si el registro no se encuentra.
def actualizar_registro_precio_impuesto(registro_id, producto_nombre, pais_nombre, precio_texto, impuesto_texto, moneda):
    producto_nombre = producto_nombre.strip()
    pais_nombre = pais_nombre.strip()
    precio_texto = precio_texto.strip()
    impuesto_texto = impuesto_texto.strip()
    moneda = moneda.strip()

    if not producto_nombre or not pais_nombre or not precio_texto or not impuesto_texto or not moneda:
        raise ValueError("Todos los datos son obligatorios.")

    try:
        precio = float(precio_texto)
        impuesto = float(impuesto_texto)
        if precio < 0 or impuesto < 0:
            raise ValueError()
    except ValueError:
        raise ValueError("Precio e impuesto (%) deben ser números positivos.")

    producto = obtener_producto_por_nombre(producto_nombre)
    pais = obtener_pais_por_nombre(pais_nombre)

    if producto is None or pais is None:
        raise ValueError("Producto o país inválido.")

    for registro in precios_impuestos:
        if registro["id"] == registro_id:
            registro["producto_id"] = producto["id"]
            registro["pais_id"] = pais["id"]
            registro["precio"] = precio
            registro["impuesto"] = impuesto
            registro["moneda"] = moneda
            guardar_precios_impuestos()
            return registro

    raise ValueError("Registro no encontrado.")

# Función para eliminar un registro de precio e impuesto por su ID, buscando el registro en la lista de precios e impuestos y eliminándolo si se encuentra, luego guardando la lista actualizada en el archivo, o lanzando un error si el registro no se encuentra.
def eliminar_registro_precio_impuesto(registro_id):
    global precios_impuestos
    precios_impuestos[:] = [r for r in precios_impuestos if r["id"] != registro_id]
    guardar_precios_impuestos()

# Función para obtener el nombre de un producto por su ID, buscando el producto en la lista de productos y devolviendo su nombre si se encuentra, o devolviendo "Desconocido" si no se encuentra.
def obtener_nombre_producto(producto_id):
    producto = obtener_producto_por_id(producto_id)
    return producto["nombre"] if producto else "Desconocido"

# Función para obtener el nombre de un país por su ID, buscando el país en la lista de países y devolviendo su nombre si se encuentra, o devolviendo "Desconocido" si no se encuentra.
def obtener_nombre_pais(pais_id):
    pais = obtener_pais_por_id(pais_id)
    return pais["nombre"] if pais else "Desconocido"

# Función para obtener los registros de precios e impuestos asociados a un producto específico filtrados por moneda, validando que se hayan registrado productos, países y precios, y que el nombre del producto y la moneda sean proporcionados antes de realizar la consulta, o lanzando un error si los datos son inválidos o si el producto no se encuentra.
def obtener_registros_consulta_producto(nombre_producto, moneda_seleccionada):
    if len(productos) == 0:
        raise ValueError("Primero debe registrar productos.")

    if len(paises) == 0:
        raise ValueError("Primero debe registrar países.")

    if len(precios_impuestos) == 0:
        raise ValueError("No hay precios e impuestos registrados.")

    if not nombre_producto.strip():
        raise ValueError("Debe seleccionar un producto.")

    if not moneda_seleccionada.strip():
        raise ValueError("Debe seleccionar una moneda.")

    producto = obtener_producto_por_nombre(nombre_producto.strip())
    if producto is None:
        raise ValueError("Producto no válido.")

    registros_filtrados = [
        r for r in precios_impuestos
        if r["producto_id"] == producto["id"] and r["moneda"] == moneda_seleccionada
    ]

    resultado = []
    for reg in registros_filtrados:
        total = calcular_costo_total(reg["precio"], reg["impuesto"])
        resultado.append({
            "pais": obtener_nombre_pais(reg["pais_id"]),
            "precio": reg["precio"],
            "impuesto": reg["impuesto"],
            "moneda": reg["moneda"],
            "total": total
        })

    return resultado


# --------------------------------------------------------------
# REPORTES
# --------------------------------------------------------------

# Función para generar un reporte de productos por país y moneda, mostrando el resultado en una tabla ordenada por costo total descendente, validando que se hayan registrado productos, países y precios, y que el nombre del país y la moneda sean proporcionados antes de generar el reporte, o lanzando un error si los datos son inválidos o si el país no se encuentra.
def generar_reporte_por_pais(nombre_pais, moneda_seleccionada):
    if len(productos) == 0 or len(paises) == 0 or len(precios_impuestos) == 0:
        raise ValueError("Debe tener productos, países y precios registrados.")

    nombre_pais = nombre_pais.strip()
    moneda_seleccionada = moneda_seleccionada.strip()

    if not nombre_pais:
        raise ValueError("Debe seleccionar un país.")

    if not moneda_seleccionada:
        raise ValueError("Debe seleccionar una moneda.")

    pais = obtener_pais_por_nombre(nombre_pais)
    if pais is None:
        raise ValueError("País no válido.")

    registros_pais = []
    for registro in precios_impuestos:
        if registro["pais_id"] == pais["id"] and registro["moneda"] == moneda_seleccionada:
            total = calcular_costo_total(registro["precio"], registro["impuesto"])
            producto_nombre = obtener_nombre_producto(registro["producto_id"])

            registros_pais.append({
                "producto": producto_nombre,
                "precio": registro["precio"],
                "impuesto": registro["impuesto"],
                "moneda": registro["moneda"],
                "total": total
            })

    registros_pais.sort(key=lambda x: x["total"], reverse=True)
    return registros_pais

# Función para guardar el reporte generado en formato TXT, escribiendo los detalles del reporte y los registros de productos en un formato legible, validando que se haya generado un reporte antes de intentar guardarlo, o lanzando un error si no se ha generado un reporte.
def guardar_reporte_txt(reporte_generado, nombre_pais, moneda, ruta_archivo):
    if not reporte_generado:
        raise ValueError("Primero debe generar un reporte.")

    with open(ruta_archivo, "w", encoding="utf-8") as f:
        f.write("REPORTE ATI Logística Aduanera\n")
        f.write(f"País: {nombre_pais}\n")
        f.write(f"Moneda: {moneda}\n")
        f.write(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 80 + "\n\n")

        f.write(
            "Producto".ljust(30) +
            "Precio".rjust(12) +
            "Impuesto%".rjust(10) +
            "Moneda".rjust(8) +
            "Total".rjust(15) + "\n"
        )
        f.write("-" * 80 + "\n")

        for reg in reporte_generado:
            f.write(
                f"{reg['producto'][:29]:<30}"
                f"{reg['precio']:>12.2f}"
                f"{reg['impuesto']:>10.2f}"
                f"{reg['moneda']:<8}"
                f"{reg['total']:>15.2f}\n"
            )

# Función para exportar el reporte generado en formato PDF, utilizando la librería reportlab para crear un documento PDF con el título del reporte, los detalles del país y moneda, y una tabla con los registros de productos ordenados por costo total, validando que se haya generado un reporte antes de intentar exportarlo, o lanzando un error si no se ha generado un reporte o si la librería reportlab no está instalada.
def exportar_reporte_pdf(reporte_generado, nombre_pais, moneda, ruta_archivo):
    if not reporte_generado:
        raise ValueError("Primero debe generar un reporte.")

    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
        from reportlab.lib.styles import getSampleStyleSheet
        from reportlab.lib import colors
    except ImportError:
        raise ImportError("La librería reportlab no está instalada. Instale con: pip install reportlab")

    doc = SimpleDocTemplate(ruta_archivo, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    titulo = Paragraph(
        (
            f"<b>REPORTE ATI Logística Aduanera</b><br/>"
            f"<b>País:</b> {nombre_pais}<br/>"
            f"<b>Moneda:</b> {moneda}<br/>"
            f"<b>Fecha:</b> {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"
        ),
        styles["Heading1"]
    )
    story.append(titulo)
    story.append(Spacer(1, 12))

    data = [["Producto", "Precio", "Impuesto %", "Moneda", "Costo total"]]
    for reg in reporte_generado:
        data.append([
            reg["producto"],
            f"{reg['precio']:.2f}",
            f"{reg['impuesto']:.2f}",
            reg["moneda"],
            f"{reg['total']:.2f}"
        ])

    tabla = Table(data)
    tabla.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 12),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
        ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
        ("GRID", (0, 0), (-1, -1), 1, colors.black)
    ]))
    story.append(tabla)

    doc.build(story)

# Función para enviar el reporte generado por correo electrónico, construyendo un mensaje con formato adecuado que incluye el cuerpo del correo con los detalles del reporte generado, y utilizando el servidor SMTP de Gmail para enviar el correo al usuario configurado, validando que se haya generado un reporte y que los datos de usuario estén configurados antes de intentar enviar el correo, o lanzando un error si no se ha generado un reporte o si los datos de usuario no están configurados.
def enviar_reporte_por_correo(reporte_generado, nombre_pais, moneda):
    if not reporte_generado:
        raise ValueError("Primero debe generar un reporte.")

    nombre_usuario, correo_usuario = obtener_datos_usuario()
    if not nombre_usuario or not correo_usuario:
        raise ValueError("Primero debe configurar sus datos de usuario.")

    smtp_servidor = "smtp.gmail.com"
    smtp_puerto = 587
    email_remitente = "ProyectoCalidad2026@gmail.com"
    password_app = "ylua mgdr jcrw eqhi"

    mensaje = MIMEMultipart()
    mensaje["From"] = email_remitente
    mensaje["To"] = correo_usuario
    mensaje["Subject"] = f"Reporte ATI Logística - {nombre_pais} - {datetime.now().strftime('%d/%m/%Y')}"

    detalle = ""
    for reg in reporte_generado:
        detalle += (
            f"- {reg['producto']} | Precio: {reg['precio']:.2f} | "
            f"Impuesto: {reg['impuesto']:.2f}% | "
            f"Moneda: {reg['moneda']} | Total: {reg['total']:.2f}\n"
        )

    cuerpo = f"""Hola {nombre_usuario},

Se generó el reporte de productos ordenados por costo total para el país {nombre_pais}.

Datos del reporte:
- País: {nombre_pais}
- Moneda: {moneda}
- Productos: {len(reporte_generado)}
- Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}

Detalle:
{detalle}

Saludos,
ATI Logística Aduanera
"""

    mensaje.attach(MIMEText(cuerpo, "plain"))

    server = smtplib.SMTP(smtp_servidor, smtp_puerto)
    server.starttls()
    server.login(email_remitente, password_app)
    server.sendmail(email_remitente, correo_usuario, mensaje.as_string())
    server.quit()

    return correo_usuario

import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

EMAIL_REGEX = r"^[\w\.-]+@[\w\.-]+\.\w+$"

# Variables globales
productos = []
contador_productos = 1

paises = []
contador_paises = 1

precios_impuestos = []
contador_registros = 1

MONEDAS = ["CRC", "USD", "EUR", "BRL"]


# -------------------------------------------------------------- FUNCIONES ARCHIVOS --------------------------------------------------------------

def guardar_productos():
    global productos, contador_productos
    try:
        with open("productos.txt", "w", encoding="utf-8") as archivo:
            archivo.write(str(contador_productos) + "\n")
            for producto in productos:
                linea = f"{producto['id']}|{producto['nombre']}|{producto['precio']}\n"
                archivo.write(linea)
    except Exception as e:
        messagebox.showerror("Error", f"No se pudieron guardar los productos.\n{e}")


def cargar_productos():
    global productos, contador_productos
    try:
        with open("productos.txt", "r", encoding="utf-8") as archivo:
            lineas = archivo.readlines()

            if len(lineas) > 0:
                contador_productos = int(lineas[0].strip())

            productos = []
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
        productos = []
        contador_productos = 1
    except Exception as e:
        messagebox.showerror("Error", f"No se pudieron cargar los productos.\n{e}")


def guardar_paises():
    global paises, contador_paises
    try:
        with open("paises.txt", "w", encoding="utf-8") as archivo:
            archivo.write(str(contador_paises) + "\n")
            for pais in paises:
                archivo.write(f"{pais['id']}|{pais['nombre']}\n")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudieron guardar los países.\n{e}")


def cargar_paises():
    global paises, contador_paises
    try:
        with open("paises.txt", "r", encoding="utf-8") as archivo:
            lineas = archivo.readlines()

            if len(lineas) > 0:
                contador_paises = int(lineas[0].strip())

            paises = []
            for linea in lineas[1:]:
                datos = linea.strip().split("|")
                if len(datos) == 2:
                    paises.append({
                        "id": int(datos[0]),
                        "nombre": datos[1]
                    })
    except FileNotFoundError:
        paises = []
        contador_paises = 1
    except Exception as e:
        messagebox.showerror("Error", f"No se pudieron cargar los países.\n{e}")


def guardar_precios_impuestos():
    global precios_impuestos, contador_registros
    try:
        with open("precios_impuestos.txt", "w", encoding="utf-8") as archivo:
            archivo.write(str(contador_registros) + "\n")
            for registro in precios_impuestos:
                linea = f"{registro['id']}|{registro['producto_id']}|{registro['pais_id']}|{registro['precio']}|{registro['impuesto']}|{registro['moneda']}\n"
                archivo.write(linea)
    except Exception as e:
        messagebox.showerror("Error", f"No se pudieron guardar los precios e impuestos.\n{e}")


def cargar_precios_impuestos():
    global precios_impuestos, contador_registros
    try:
        with open("precios_impuestos.txt", "r", encoding="utf-8") as archivo:
            lineas = archivo.readlines()

            if len(lineas) > 0:
                contador_registros = int(lineas[0].strip())

            precios_impuestos = []
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
        precios_impuestos = []
        contador_registros = 1
    except Exception as e:
        messagebox.showerror("Error", f"No se pudieron cargar los precios e impuestos.\n{e}")


def obtener_datos_usuario():
    try:
        with open("config_usuario.txt", "r", encoding="utf-8") as f:
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


# -------------------------------------------------------------- VENTANA CONFIGURACIÓN USUARIO --------------------------------------------------------------

class ConfigUsuarioWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Configuración de usuario")
        self.geometry("400x220")
        self.resizable(False, False)

        self.nombre_var = tk.StringVar()
        self.correo_var = tk.StringVar()

        lbl_titulo = tk.Label(
            self,
            text="Configuración básica del usuario",
            font=("Arial", 12, "bold")
        )
        lbl_titulo.pack(pady=10)

        frame_form = tk.Frame(self)
        frame_form.pack(pady=5, padx=10, fill="x")

        lbl_nombre = tk.Label(frame_form, text="Nombre:")
        lbl_nombre.grid(row=0, column=0, sticky="e", padx=5, pady=5)
        entry_nombre = tk.Entry(frame_form, textvariable=self.nombre_var, width=30)
        entry_nombre.grid(row=0, column=1, padx=5, pady=5)

        lbl_correo = tk.Label(frame_form, text="Correo electrónico:")
        lbl_correo.grid(row=1, column=0, sticky="e", padx=5, pady=5)
        entry_correo = tk.Entry(frame_form, textvariable=self.correo_var, width=30)
        entry_correo.grid(row=1, column=1, padx=5, pady=5)

        frame_botones = tk.Frame(self)
        frame_botones.pack(pady=10)

        btn_guardar = ttk.Button(frame_botones, text="Guardar", command=self.guardar_config)
        btn_guardar.grid(row=0, column=0, padx=10)

        btn_cargar = ttk.Button(frame_botones, text="Cargar datos", command=self.cargar_config)
        btn_cargar.grid(row=0, column=1, padx=10)

        btn_cerrar = ttk.Button(frame_botones, text="Cerrar", command=self.destroy)
        btn_cerrar.grid(row=0, column=2, padx=10)

    def cargar_config(self):
        ruta_archivo = filedialog.askopenfilename(
            title="Seleccionar archivo de configuración",
            filetypes=[("Archivos de texto", "*.txt")]
        )

        if not ruta_archivo:
            return

        try:
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
                messagebox.showerror("Error", "El archivo no contiene los datos esperados de nombre y correo.")
                return

            self.nombre_var.set(nombre)
            self.correo_var.set(correo)

            messagebox.showinfo("Éxito", "Datos cargados correctamente.")

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar el archivo.\n{e}")

    def guardar_config(self):
        nombre = self.nombre_var.get().strip()
        correo = self.correo_var.get().strip()

        if not nombre or not correo:
            messagebox.showerror("Error", "Todos los datos son requeridos.")
            return

        if not re.match(EMAIL_REGEX, correo):
            messagebox.showerror("Error", "Formato de correo electrónico inválido.")
            return

        try:
            with open("config_usuario.txt", "w", encoding="utf-8") as f:
                f.write(f"nombre={nombre}\n")
                f.write(f"correo={correo}\n")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar la configuración.\n{e}")
            return

        messagebox.showinfo("Éxito", "Registro de usuario completado correctamente.")
        self.destroy()


# -------------------------------------------------------------- VENTANA GESTIÓN PRODUCTOS --------------------------------------------------------------

class ProductosWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Gestión de productos")
        self.geometry("600x350")
        self.resizable(False, False)

        self.nombre_var = tk.StringVar()
        self.precio_var = tk.StringVar()

        frame_lista = tk.Frame(self)
        frame_lista.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        lbl_lista = tk.Label(frame_lista, text="Productos registrados")
        lbl_lista.pack()

        self.tree = ttk.Treeview(
            frame_lista,
            columns=("id", "nombre", "precio"),
            show="headings",
            height=12
        )
        self.tree.heading("id", text="ID")
        self.tree.heading("nombre", text="Nombre")
        self.tree.heading("precio", text="Precio")
        self.tree.column("id", width=50, anchor="center")
        self.tree.column("nombre", width=220)
        self.tree.column("precio", width=100, anchor="e")
        self.tree.pack(side="left", fill="y")

        scrollbar = ttk.Scrollbar(frame_lista, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

        frame_form = tk.Frame(self)
        frame_form.pack(side="right", fill="y", padx=10, pady=10)

        lbl_titulo = tk.Label(frame_form, text="Datos del producto", font=("Arial", 11, "bold"))
        lbl_titulo.grid(row=0, column=0, columnspan=2, pady=5)

        lbl_nombre = tk.Label(frame_form, text="Nombre:")
        lbl_nombre.grid(row=1, column=0, sticky="e", padx=5, pady=5)
        entry_nombre = tk.Entry(frame_form, textvariable=self.nombre_var, width=25)
        entry_nombre.grid(row=1, column=1, padx=5, pady=5)

        lbl_precio = tk.Label(frame_form, text="Precio base:")
        lbl_precio.grid(row=2, column=0, sticky="e", padx=5, pady=5)
        entry_precio = tk.Entry(frame_form, textvariable=self.precio_var, width=25)
        entry_precio.grid(row=2, column=1, padx=5, pady=5)

        btn_agregar = ttk.Button(frame_form, text="Agregar / Guardar", command=self.guardar_producto)
        btn_agregar.grid(row=3, column=0, columnspan=2, pady=5)

        btn_nuevo = ttk.Button(frame_form, text="Nuevo", command=self.limpiar_formulario)
        btn_nuevo.grid(row=4, column=0, columnspan=2, pady=5)

        btn_consultar = ttk.Button(frame_form, text="Consultar", command=self.consultar_producto)
        btn_consultar.grid(row=5, column=0, columnspan=2, pady=5)

        btn_eliminar = ttk.Button(frame_form, text="Eliminar", command=self.eliminar_producto)
        btn_eliminar.grid(row=6, column=0, columnspan=2, pady=5)

        btn_cerrar = ttk.Button(frame_form, text="Cerrar", command=self.destroy)
        btn_cerrar.grid(row=7, column=0, columnspan=2, pady=10)

        self.cargar_productos_en_tabla()

    def cargar_productos_en_tabla(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for prod in productos:
            self.tree.insert("", "end", values=(
                prod["id"], prod["nombre"], f"{prod['precio']:.2f}"
            ))

    def limpiar_formulario(self):
        self.nombre_var.set("")
        self.precio_var.set("")
        self.tree.selection_remove(*self.tree.selection())

    def on_tree_select(self, event):
        selected = self.tree.selection()
        if not selected:
            return

        item = self.tree.item(selected[0])
        _id, nombre, precio = item["values"]
        self.nombre_var.set(nombre)
        self.precio_var.set(str(precio))

    def guardar_producto(self):
        global contador_productos

        nombre = self.nombre_var.get().strip()
        precio_texto = self.precio_var.get().strip()

        if not nombre or not precio_texto:
            messagebox.showerror("Error", "Nombre y precio son obligatorios.")
            return

        try:
            precio = float(precio_texto)
            if precio < 0:
                raise ValueError()
        except ValueError:
            messagebox.showerror("Error", "El precio debe ser un número positivo.")
            return

        selected = self.tree.selection()
        if selected:
            item = self.tree.item(selected[0])
            prod_id = item["values"][0]

            for prod in productos:
                if prod["id"] == prod_id:
                    prod["nombre"] = nombre
                    prod["precio"] = precio
                    break
        else:
            nuevo = {
                "id": contador_productos,
                "nombre": nombre,
                "precio": precio
            }
            productos.append(nuevo)
            contador_productos += 1

        guardar_productos()
        self.cargar_productos_en_tabla()
        self.limpiar_formulario()

    def consultar_producto(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Atención", "Seleccione un producto para consultar.")
            return

        item = self.tree.item(selected[0])
        prod_id, nombre, precio = item["values"]

        mensaje = (
            f"Información del producto\n\n"
            f"ID: {prod_id}\n"
            f"Nombre: {nombre}\n"
            f"Precio base: {precio}"
        )

        messagebox.showinfo("Consulta de producto", mensaje)

    def eliminar_producto(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Atención", "Seleccione un producto para eliminar.")
            return

        item = self.tree.item(selected[0])
        prod_id = item["values"][0]

        confirmar = messagebox.askyesno(
            "Confirmar", "¿Está seguro de eliminar el producto seleccionado?"
        )
        if not confirmar:
            return

        global productos
        productos = [p for p in productos if p["id"] != prod_id]

        guardar_productos()
        self.cargar_productos_en_tabla()
        self.limpiar_formulario()


# -------------------------------------------------------------- VENTANA GESTIÓN PAÍSES --------------------------------------------------------------

class PaisesWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Gestión de países")
        self.geometry("550x320")
        self.resizable(False, False)

        self.nombre_var = tk.StringVar()

        frame_lista = tk.Frame(self)
        frame_lista.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        lbl_lista = tk.Label(frame_lista, text="Países registrados")
        lbl_lista.pack()

        self.tree = ttk.Treeview(
            frame_lista,
            columns=("id", "nombre"),
            show="headings",
            height=12
        )
        self.tree.heading("id", text="ID")
        self.tree.heading("nombre", text="País")
        self.tree.column("id", width=60, anchor="center")
        self.tree.column("nombre", width=220)
        self.tree.pack(side="left", fill="y")

        scrollbar = ttk.Scrollbar(frame_lista, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

        frame_form = tk.Frame(self)
        frame_form.pack(side="right", fill="y", padx=10, pady=10)

        lbl_titulo = tk.Label(frame_form, text="Datos del país", font=("Arial", 11, "bold"))
        lbl_titulo.grid(row=0, column=0, columnspan=2, pady=5)

        lbl_nombre = tk.Label(frame_form, text="Nombre:")
        lbl_nombre.grid(row=1, column=0, sticky="e", padx=5, pady=5)

        entry_nombre = tk.Entry(frame_form, textvariable=self.nombre_var, width=25)
        entry_nombre.grid(row=1, column=1, padx=5, pady=5)

        btn_guardar = ttk.Button(frame_form, text="Agregar / Guardar", command=self.guardar_pais)
        btn_guardar.grid(row=2, column=0, columnspan=2, pady=5)

        btn_nuevo = ttk.Button(frame_form, text="Nuevo", command=self.limpiar_formulario)
        btn_nuevo.grid(row=3, column=0, columnspan=2, pady=5)

        btn_eliminar = ttk.Button(frame_form, text="Eliminar", command=self.eliminar_pais)
        btn_eliminar.grid(row=4, column=0, columnspan=2, pady=5)

        btn_cerrar = ttk.Button(frame_form, text="Cerrar", command=self.destroy)
        btn_cerrar.grid(row=5, column=0, columnspan=2, pady=10)

        self.cargar_paises_en_tabla()

    def cargar_paises_en_tabla(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for pais in paises:
            self.tree.insert("", "end", values=(pais["id"], pais["nombre"]))

    def limpiar_formulario(self):
        self.nombre_var.set("")
        self.tree.selection_remove(*self.tree.selection())

    def on_tree_select(self, event):
        selected = self.tree.selection()
        if not selected:
            return

        item = self.tree.item(selected[0])
        _id, nombre = item["values"]
        self.nombre_var.set(nombre)

    def guardar_pais(self):
        global contador_paises

        nombre = self.nombre_var.get().strip()

        if not nombre:
            messagebox.showerror("Error", "El nombre del país es obligatorio.")
            return

        selected = self.tree.selection()
        if selected:
            item = self.tree.item(selected[0])
            pais_id = item["values"][0]

            for pais in paises:
                if pais["id"] == pais_id:
                    pais["nombre"] = nombre
                    break
        else:
            nuevo = {
                "id": contador_paises,
                "nombre": nombre
            }
            paises.append(nuevo)
            contador_paises += 1

        guardar_paises()
        self.cargar_paises_en_tabla()
        self.limpiar_formulario()

    def eliminar_pais(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Atención", "Seleccione un país para eliminar.")
            return

        item = self.tree.item(selected[0])
        pais_id = item["values"][0]

        confirmar = messagebox.askyesno(
            "Confirmar", "¿Está seguro de eliminar el país seleccionado?"
        )
        if not confirmar:
            return

        global paises
        paises = [p for p in paises if p["id"] != pais_id]

        guardar_paises()
        self.cargar_paises_en_tabla()
        self.limpiar_formulario()


# -------------------------------------------------------------- VENTANA PRECIOS E IMPUESTOS --------------------------------------------------------------

class PreciosImpuestosWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Precios e impuestos")
        self.geometry("850x420")
        self.resizable(False, False)

        self.producto_var = tk.StringVar()
        self.pais_var = tk.StringVar()
        self.precio_var = tk.StringVar()
        self.impuesto_var = tk.StringVar()
        self.moneda_var = tk.StringVar(value=MONEDAS[0])

        frame_lista = tk.Frame(self)
        frame_lista.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        lbl_lista = tk.Label(frame_lista, text="Registros de precios e impuestos")
        lbl_lista.pack()

        self.tree = ttk.Treeview(
            frame_lista,
            columns=("id", "producto", "pais", "precio", "impuesto", "moneda", "total"),
            show="headings",
            height=14
        )
        self.tree.heading("id", text="ID")
        self.tree.heading("producto", text="Producto")
        self.tree.heading("pais", text="País")
        self.tree.heading("precio", text="Precio")
        self.tree.heading("impuesto", text="Impuesto (%)")
        self.tree.heading("moneda", text="Moneda")
        self.tree.heading("total", text="Costo total")

        self.tree.column("id", width=40, anchor="center")
        self.tree.column("producto", width=120)
        self.tree.column("pais", width=120)
        self.tree.column("precio", width=80, anchor="e")
        self.tree.column("impuesto", width=80, anchor="e")
        self.tree.column("moneda", width=70, anchor="center")
        self.tree.column("total", width=100, anchor="e")

        self.tree.pack(side="left", fill="y")

        scrollbar = ttk.Scrollbar(frame_lista, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

        frame_form = tk.Frame(self)
        frame_form.pack(side="right", fill="y", padx=10, pady=10)

        lbl_titulo = tk.Label(frame_form, text="Datos del registro", font=("Arial", 11, "bold"))
        lbl_titulo.grid(row=0, column=0, columnspan=2, pady=5)

        lbl_producto = tk.Label(frame_form, text="Producto:")
        lbl_producto.grid(row=1, column=0, sticky="e", padx=5, pady=5)

        self.combo_producto = ttk.Combobox(
            frame_form,
            textvariable=self.producto_var,
            state="readonly",
            width=25
        )
        self.combo_producto.grid(row=1, column=1, padx=5, pady=5)

        lbl_pais = tk.Label(frame_form, text="País:")
        lbl_pais.grid(row=2, column=0, sticky="e", padx=5, pady=5)

        self.combo_pais = ttk.Combobox(
            frame_form,
            textvariable=self.pais_var,
            state="readonly",
            width=25
        )
        self.combo_pais.grid(row=2, column=1, padx=5, pady=5)

        lbl_precio = tk.Label(frame_form, text="Precio:")
        lbl_precio.grid(row=3, column=0, sticky="e", padx=5, pady=5)
        entry_precio = tk.Entry(frame_form, textvariable=self.precio_var, width=28)
        entry_precio.grid(row=3, column=1, padx=5, pady=5)

        lbl_impuesto = tk.Label(frame_form, text="Impuesto (%):")
        lbl_impuesto.grid(row=4, column=0, sticky="e", padx=5, pady=5)
        entry_impuesto = tk.Entry(frame_form, textvariable=self.impuesto_var, width=28)
        entry_impuesto.grid(row=4, column=1, padx=5, pady=5)

        lbl_moneda = tk.Label(frame_form, text="Moneda:")
        lbl_moneda.grid(row=5, column=0, sticky="e", padx=5, pady=5)

        combo_moneda = ttk.Combobox(
            frame_form,
            textvariable=self.moneda_var,
            values=MONEDAS,
            state="readonly",
            width=25
        )
        combo_moneda.grid(row=5, column=1, padx=5, pady=5)

        btn_guardar = ttk.Button(frame_form, text="Agregar / Guardar", command=self.guardar_registro)
        btn_guardar.grid(row=6, column=0, columnspan=2, pady=5)

        btn_nuevo = ttk.Button(frame_form, text="Nuevo", command=self.limpiar_formulario)
        btn_nuevo.grid(row=7, column=0, columnspan=2, pady=5)

        btn_eliminar = ttk.Button(frame_form, text="Eliminar", command=self.eliminar_registro)
        btn_eliminar.grid(row=8, column=0, columnspan=2, pady=5)

        btn_cerrar = ttk.Button(frame_form, text="Cerrar", command=self.destroy)
        btn_cerrar.grid(row=9, column=0, columnspan=2, pady=10)

        self.cargar_comboboxes()
        self.cargar_registros_en_tabla()

    def cargar_comboboxes(self):
        nombres_productos = [producto["nombre"] for producto in productos]
        nombres_paises = [pais["nombre"] for pais in paises]
        self.combo_producto["values"] = nombres_productos
        self.combo_pais["values"] = nombres_paises

    def obtener_nombre_producto(self, producto_id):
        for producto in productos:
            if producto["id"] == producto_id:
                return producto["nombre"]
        return "Desconocido"

    def obtener_nombre_pais(self, pais_id):
        for pais in paises:
            if pais["id"] == pais_id:
                return pais["nombre"]
        return "Desconocido"

    def obtener_id_producto_por_nombre(self, nombre):
        for producto in productos:
            if producto["nombre"] == nombre:
                return producto["id"]
        return None

    def obtener_id_pais_por_nombre(self, nombre):
        for pais in paises:
            if pais["nombre"] == nombre:
                return pais["id"]
        return None

    def calcular_costo_total(self, precio, impuesto):
        return precio + (precio * (impuesto / 100))

    def cargar_registros_en_tabla(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for registro in precios_impuestos:
            producto_nombre = self.obtener_nombre_producto(registro["producto_id"])
            pais_nombre = self.obtener_nombre_pais(registro["pais_id"])
            total = self.calcular_costo_total(registro["precio"], registro["impuesto"])

            self.tree.insert("", "end", values=(
                registro["id"],
                producto_nombre,
                pais_nombre,
                f"{registro['precio']:.2f}",
                f"{registro['impuesto']:.2f}",
                registro["moneda"],
                f"{total:.2f}"
            ))

    def limpiar_formulario(self):
        self.producto_var.set("")
        self.pais_var.set("")
        self.precio_var.set("")
        self.impuesto_var.set("")
        self.moneda_var.set(MONEDAS[0])
        self.tree.selection_remove(*self.tree.selection())

    def on_tree_select(self, event):
        selected = self.tree.selection()
        if not selected:
            return

        item = self.tree.item(selected[0])
        valores = item["values"]

        self.producto_var.set(valores[1])
        self.pais_var.set(valores[2])
        self.precio_var.set(str(valores[3]))
        self.impuesto_var.set(str(valores[4]))
        self.moneda_var.set(valores[5])

    def guardar_registro(self):
        global contador_registros

        if len(productos) == 0:
            messagebox.showwarning("Atención", "Primero debe registrar al menos un producto.")
            return

        if len(paises) == 0:
            messagebox.showwarning("Atención", "Primero debe registrar al menos un país.")
            return

        producto_nombre = self.producto_var.get().strip()
        pais_nombre = self.pais_var.get().strip()
        precio_texto = self.precio_var.get().strip()
        impuesto_texto = self.impuesto_var.get().strip()
        moneda = self.moneda_var.get().strip()

        if not producto_nombre or not pais_nombre or not precio_texto or not impuesto_texto or not moneda:
            messagebox.showerror("Error", "Todos los datos son obligatorios.")
            return

        try:
            precio = float(precio_texto)
            impuesto = float(impuesto_texto)
            if precio < 0 or impuesto < 0:
                raise ValueError()
        except ValueError:
            messagebox.showerror("Error", "Precio e impuesto (%) deben ser números positivos.")
            return

        producto_id = self.obtener_id_producto_por_nombre(producto_nombre)
        pais_id = self.obtener_id_pais_por_nombre(pais_nombre)

        if producto_id is None or pais_id is None:
            messagebox.showerror("Error", "Producto o país inválido.")
            return

        selected = self.tree.selection()
        if selected:
            item = self.tree.item(selected[0])
            registro_id = item["values"][0]

            for registro in precios_impuestos:
                if registro["id"] == registro_id:
                    registro["producto_id"] = producto_id
                    registro["pais_id"] = pais_id
                    registro["precio"] = precio
                    registro["impuesto"] = impuesto
                    registro["moneda"] = moneda
                    break
        else:
            nuevo = {
                "id": contador_registros,
                "producto_id": producto_id,
                "pais_id": pais_id,
                "precio": precio,
                "impuesto": impuesto,
                "moneda": moneda
            }
            precios_impuestos.append(nuevo)
            contador_registros += 1

        guardar_precios_impuestos()
        self.cargar_registros_en_tabla()
        self.limpiar_formulario()

    def eliminar_registro(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Atención", "Seleccione un registro para eliminar.")
            return

        item = self.tree.item(selected[0])
        registro_id = item["values"][0]

        confirmar = messagebox.askyesno("Confirmar", "¿Está seguro de eliminar el registro seleccionado?")
        if not confirmar:
            return

        global precios_impuestos
        precios_impuestos = [r for r in precios_impuestos if r["id"] != registro_id]

        guardar_precios_impuestos()
        self.cargar_registros_en_tabla()
        self.limpiar_formulario()


# -------------------------------------------------------------- VENTANA CONSULTA POR PRODUCTO --------------------------------------------------------------

class ConsultaProductoWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Consulta de precios e impuestos por producto")
        self.geometry("800x420")
        self.resizable(False, False)

        self.producto_var = tk.StringVar()
        self.moneda_var = tk.StringVar(value=MONEDAS[0])

        frame_filtros = tk.Frame(self)
        frame_filtros.pack(fill="x", padx=10, pady=10)

        lbl_producto = tk.Label(frame_filtros, text="Producto:")
        lbl_producto.grid(row=0, column=0, sticky="e", padx=5, pady=5)

        self.combo_producto = ttk.Combobox(
            frame_filtros,
            textvariable=self.producto_var,
            state="readonly",
            width=30
        )
        self.combo_producto.grid(row=0, column=1, padx=5, pady=5)

        lbl_moneda = tk.Label(frame_filtros, text="Moneda:")
        lbl_moneda.grid(row=0, column=2, sticky="e", padx=5, pady=5)

        self.combo_moneda = ttk.Combobox(
            frame_filtros,
            textvariable=self.moneda_var,
            values=MONEDAS,
            state="readonly",
            width=10
        )
        self.combo_moneda.grid(row=0, column=3, padx=5, pady=5)

        btn_consultar = ttk.Button(frame_filtros, text="Consultar", command=self.consultar)
        btn_consultar.grid(row=0, column=4, padx=10, pady=5)

        frame_tabla = tk.Frame(self)
        frame_tabla.pack(fill="both", expand=True, padx=10, pady=10)

        self.tree = ttk.Treeview(
            frame_tabla,
            columns=("pais", "precio", "impuesto", "moneda", "total"),
            show="headings",
            height=14
        )
        self.tree.heading("pais", text="País")
        self.tree.heading("precio", text="Precio")
        self.tree.heading("impuesto", text="Impuesto %")
        self.tree.heading("moneda", text="Moneda")
        self.tree.heading("total", text="Costo total")

        self.tree.column("pais", width=160)
        self.tree.column("precio", width=100, anchor="e")
        self.tree.column("impuesto", width=100, anchor="e")
        self.tree.column("moneda", width=80, anchor="center")
        self.tree.column("total", width=120, anchor="e")

        self.tree.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        btn_cerrar = ttk.Button(self, text="Cerrar", command=self.destroy)
        btn_cerrar.pack(pady=5)

        self.cargar_productos_en_combobox()

    def cargar_productos_en_combobox(self):
        nombres_productos = [producto["nombre"] for producto in productos]
        self.combo_producto["values"] = nombres_productos

    def obtener_id_producto_por_nombre(self, nombre):
        for producto in productos:
            if producto["nombre"] == nombre:
                return producto["id"]
        return None

    def obtener_nombre_pais(self, pais_id):
        for pais in paises:
            if pais["id"] == pais_id:
                return pais["nombre"]
        return "Desconocido"

    def calcular_costo_total(self, precio, impuesto):
        return precio + (precio * (impuesto / 100))

    def consultar(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        if len(productos) == 0:
            messagebox.showwarning("Atención", "Primero debe registrar productos.")
            return

        if len(paises) == 0:
            messagebox.showwarning("Atención", "Primero debe registrar países.")
            return

        if len(precios_impuestos) == 0:
            messagebox.showwarning("Atención", "No hay precios e impuestos registrados.")
            return

        nombre_producto = self.producto_var.get().strip()
        moneda_seleccionada = self.moneda_var.get().strip()

        if not nombre_producto:
            messagebox.showerror("Error", "Debe seleccionar un producto.")
            return

        if not moneda_seleccionada:
            messagebox.showerror("Error", "Debe seleccionar una moneda.")
            return

        producto_id = self.obtener_id_producto_por_nombre(nombre_producto)
        if producto_id is None:
            messagebox.showerror("Error", "Producto no válido.")
            return

        registros_filtrados = [
            r for r in precios_impuestos
            if r["producto_id"] == producto_id and r["moneda"] == moneda_seleccionada
        ]

        if not registros_filtrados:
            messagebox.showinfo("Sin datos", "No hay precios registrados para ese producto en la moneda seleccionada.")
            return

        for reg in registros_filtrados:
            pais_nombre = self.obtener_nombre_pais(reg["pais_id"])
            total = self.calcular_costo_total(reg["precio"], reg["impuesto"])

            self.tree.insert(
                "",
                "end",
                values=(
                    pais_nombre,
                    f"{reg['precio']:.2f}",
                    f"{reg['impuesto']:.2f}",
                    reg["moneda"],
                    f"{total:.2f}"
                )
            )


# -------------------------------------------------------------- VENTANA REPORTES --------------------------------------------------------------

class ReporteWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Reporte de productos por país")
        self.geometry("900x500")
        self.resizable(False, False)

        self.pais_var = tk.StringVar()
        self.moneda_var = tk.StringVar(value=MONEDAS[0])
        self.reporte_generado = []

        frame_filtros = tk.Frame(self)
        frame_filtros.pack(fill="x", padx=10, pady=10)

        lbl_pais = tk.Label(frame_filtros, text="País:")
        lbl_pais.grid(row=0, column=0, sticky="e", padx=5, pady=5)

        self.combo_pais = ttk.Combobox(
            frame_filtros,
            textvariable=self.pais_var,
            state="readonly",
            width=30
        )
        self.combo_pais.grid(row=0, column=1, padx=5, pady=5)

        lbl_moneda = tk.Label(frame_filtros, text="Moneda:")
        lbl_moneda.grid(row=0, column=2, sticky="e", padx=5, pady=5)

        self.combo_moneda = ttk.Combobox(
            frame_filtros,
            textvariable=self.moneda_var,
            values=MONEDAS,
            state="readonly",
            width=10
        )
        self.combo_moneda.grid(row=0, column=3, padx=5, pady=5)

        btn_generar = ttk.Button(frame_filtros, text="Generar reporte", command=self.generar_reporte)
        btn_generar.grid(row=0, column=4, padx=10, pady=5)

        frame_tabla = tk.Frame(self)
        frame_tabla.pack(fill="both", expand=True, padx=10, pady=10)

        lbl_reporte = tk.Label(
            frame_tabla,
            text="Productos ordenados por costo total descendente",
            font=("Arial", 12, "bold")
        )
        lbl_reporte.pack(pady=(0, 10))

        self.tree = ttk.Treeview(
            frame_tabla,
            columns=("producto", "precio", "impuesto", "moneda", "total"),
            show="headings",
            height=16
        )
        self.tree.heading("producto", text="Producto")
        self.tree.heading("precio", text="Precio")
        self.tree.heading("impuesto", text="Impuesto %")
        self.tree.heading("moneda", text="Moneda")
        self.tree.heading("total", text="Costo total")

        self.tree.column("producto", width=200)
        self.tree.column("precio", width=100, anchor="e")
        self.tree.column("impuesto", width=100, anchor="e")
        self.tree.column("moneda", width=80, anchor="center")
        self.tree.column("total", width=120, anchor="e")

        self.tree.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        frame_botones = tk.Frame(self)
        frame_botones.pack(fill="x", padx=10, pady=10)

        self.btn_txt = ttk.Button(frame_botones, text="Guardar como TXT", command=self.guardar_txt, state="disabled")
        self.btn_txt.pack(side="right", padx=5)

        self.btn_pdf = ttk.Button(frame_botones, text="Exportar PDF", command=self.exportar_pdf, state="disabled")
        self.btn_pdf.pack(side="right", padx=5)

        self.btn_correo = ttk.Button(frame_botones, text="Enviar por correo", command=self.enviar_correo, state="disabled")
        self.btn_correo.pack(side="right", padx=5)

        btn_cerrar = ttk.Button(frame_botones, text="Cerrar", command=self.destroy)
        btn_cerrar.pack(side="right")

        self.cargar_paises_en_combobox()

    def cargar_paises_en_combobox(self):
        nombres_paises = [pais["nombre"] for pais in paises]
        self.combo_pais["values"] = nombres_paises

    def obtener_nombre_producto(self, producto_id):
        for producto in productos:
            if producto["id"] == producto_id:
                return producto["nombre"]
        return "Desconocido"

    def calcular_costo_total(self, precio, impuesto):
        return precio + (precio * (impuesto / 100))

    def habilitar_botones(self):
        self.btn_txt.config(state="normal")
        self.btn_pdf.config(state="normal")
        self.btn_correo.config(state="normal")

    def generar_reporte(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        self.reporte_generado = []

        if len(productos) == 0 or len(paises) == 0 or len(precios_impuestos) == 0:
            messagebox.showwarning("Atención", "Debe tener productos, países y precios registrados.")
            return

        nombre_pais = self.pais_var.get().strip()
        moneda_seleccionada = self.moneda_var.get().strip()

        if not nombre_pais:
            messagebox.showerror("Error", "Debe seleccionar un país.")
            return

        if not moneda_seleccionada:
            messagebox.showerror("Error", "Debe seleccionar una moneda.")
            return

        pais_id = None
        for pais in paises:
            if pais["nombre"] == nombre_pais:
                pais_id = pais["id"]
                break

        if pais_id is None:
            messagebox.showerror("Error", "País no válido.")
            return

        registros_pais = []
        for registro in precios_impuestos:
            if registro["pais_id"] == pais_id and registro["moneda"] == moneda_seleccionada:
                total = self.calcular_costo_total(registro["precio"], registro["impuesto"])
                producto_nombre = self.obtener_nombre_producto(registro["producto_id"])

                registros_pais.append({
                    "producto": producto_nombre,
                    "precio": registro["precio"],
                    "impuesto": registro["impuesto"],
                    "moneda": registro["moneda"],
                    "total": total
                })

        if not registros_pais:
            messagebox.showinfo("Sin datos", f"No hay precios registrados para {nombre_pais} en {moneda_seleccionada}.")
            return

        registros_pais.sort(key=lambda x: x["total"], reverse=True)
        self.reporte_generado = registros_pais

        for reg in registros_pais:
            self.tree.insert(
                "",
                "end",
                values=(
                    reg["producto"],
                    f"{reg['precio']:.2f}",
                    f"{reg['impuesto']:.2f}",
                    reg["moneda"],
                    f"{reg['total']:.2f}"
                )
            )

        self.habilitar_botones()

        messagebox.showinfo(
            "Reporte generado",
            f"Reporte generado exitosamente.\n"
            f"{len(registros_pais)} productos encontrados para {nombre_pais}."
        )

    def guardar_txt(self):
        if not self.reporte_generado:
            messagebox.showwarning("Atención", "Primero debe generar un reporte.")
            return

        ruta_archivo = filedialog.asksaveasfilename(
            title="Guardar reporte como TXT",
            defaultextension=".txt",
            filetypes=[("Archivos de texto", "*.txt")]
        )

        if not ruta_archivo:
            return

        try:
            with open(ruta_archivo, "w", encoding="utf-8") as f:
                f.write("REPORTE ATI Logística Aduanera\n")
                f.write(f"País: {self.pais_var.get()}\n")
                f.write(f"Moneda: {self.moneda_var.get()}\n")
                f.write(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("=" * 80 + "\n\n")

                f.write("Producto".ljust(30) + "Precio".rjust(12) + "Impuesto%".rjust(10) + "Moneda".rjust(8) + "Total".rjust(15) + "\n")
                f.write("-" * 80 + "\n")

                for reg in self.reporte_generado:
                    f.write(
                        f"{reg['producto'][:29]:<30}"
                        f"{reg['precio']:>12.2f}"
                        f"{reg['impuesto']:>10.2f}"
                        f"{reg['moneda']:<8}"
                        f"{reg['total']:>15.2f}\n"
                    )

            messagebox.showinfo("Éxito", f"Reporte guardado en:\n{ruta_archivo}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el archivo.\n{e}")

    def exportar_pdf(self):
        if not self.reporte_generado:
            messagebox.showwarning("Atención", "Primero debe generar un reporte.")
            return

        try:
            from reportlab.lib.pagesizes import letter
            from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
            from reportlab.lib.styles import getSampleStyleSheet
            from reportlab.lib import colors
        except ImportError:
            messagebox.showerror(
                "Error",
                "La librería reportlab no está instalada.\nInstale con: pip install reportlab"
            )
            return

        ruta_archivo = filedialog.asksaveasfilename(
            title="Guardar reporte como PDF",
            defaultextension=".pdf",
            filetypes=[("Archivos PDF", "*.pdf")]
        )

        if not ruta_archivo:
            return

        try:
            doc = SimpleDocTemplate(ruta_archivo, pagesize=letter)
            styles = getSampleStyleSheet()
            story = []

            titulo = Paragraph(
                f"<b>REPORTE ATI Logística Aduanera</b><br/>"
                f"<b>País:</b> {self.pais_var.get()}<br/>"
                f"<b>Moneda:</b> {self.moneda_var.get()}<br/>"
                f"<b>Fecha:</b> {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}",
                styles["Heading1"]
            )
            story.append(titulo)

            data = [["Producto", "Precio", "Impuesto %", "Moneda", "Costo total"]]
            for reg in self.reporte_generado:
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
            messagebox.showinfo("Éxito", f"Reporte PDF guardado en:\n{ruta_archivo}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo generar el PDF.\n{e}")

    def enviar_correo(self):
        if not self.reporte_generado:
            messagebox.showwarning("Atención", "Primero debe generar un reporte.")
            return

        nombre_usuario, correo_usuario = obtener_datos_usuario()
        if not nombre_usuario or not correo_usuario:
            messagebox.showerror("Error", "Primero debe configurar sus datos de usuario.")
            return

        try:
            smtp_servidor = "smtp.gmail.com"
            smtp_puerto = 587
            email_remitente = "ProyectoCalidad2026@gmail.com"
            password_app = "ylua mgdr jcrw eqhi"

            mensaje = MIMEMultipart()
            mensaje["From"] = email_remitente
            mensaje["To"] = correo_usuario
            mensaje["Subject"] = f"Reporte ATI Logística - {self.pais_var.get()} - {datetime.now().strftime('%d/%m/%Y')}"

            cuerpo = f"""
Hola {nombre_usuario},

Adjunto el reporte de productos ordenados por costo total para el país {self.pais_var.get()}.

Datos del reporte:
- País: {self.pais_var.get()}
- Moneda: {self.moneda_var.get()}
- Productos: {len(self.reporte_generado)}
- Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}

Saludos,
ATI Logística Aduanera
            """

            mensaje.attach(MIMEText(cuerpo, "plain"))

            server = smtplib.SMTP(smtp_servidor, smtp_puerto)
            server.starttls()
            server.login(email_remitente, password_app)
            server.sendmail(email_remitente, correo_usuario, mensaje.as_string())
            server.quit()

            messagebox.showinfo("Éxito", f"Reporte enviado correctamente a {correo_usuario}")

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo enviar el correo.\n{e}\n\nNota: Verifique configuración SMTP.")


# -------------------------------------------------------------- VENTANA PRINCIPAL --------------------------------------------------------------

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("ATI Logística Aduanera")
        self.geometry("500x400")

        cargar_productos()
        cargar_paises()
        cargar_precios_impuestos()

        self.protocol("WM_DELETE_WINDOW", self.cerrar_app)

        titulo = tk.Label(self, text="ATI Logística Aduanera", font=("Arial", 16, "bold"))
        titulo.pack(pady=10)

        btn_config = tk.Button(
            self,
            text="Configuración de usuario",
            width=30,
            command=self.abrir_config_usuario
        )
        btn_config.pack(pady=5)

        btn_productos = tk.Button(
            self,
            text="Gestión de productos",
            width=30,
            command=self.abrir_productos
        )
        btn_productos.pack(pady=5)

        btn_consulta = tk.Button(
            self,
            text="Consulta por producto",
            width=30,
            command=self.abrir_consulta_producto
        )
        btn_consulta.pack(pady=5)

        btn_paises = tk.Button(
            self,
            text="Gestión de países",
            width=30,
            command=self.abrir_paises
        )
        btn_paises.pack(pady=5)

        btn_precios = tk.Button(
            self,
            text="Precios e impuestos",
            width=30,
            command=self.abrir_precios
        )
        btn_precios.pack(pady=5)

        btn_reportes = tk.Button(
            self,
            text="Reportes",
            width=30,
            command=self.abrir_reportes
        )
        btn_reportes.pack(pady=5)

        btn_salir = tk.Button(self, text="Salir", width=30, command=self.cerrar_app)
        btn_salir.pack(pady=20)

    def cerrar_app(self):
        guardar_productos()
        guardar_paises()
        guardar_precios_impuestos()
        self.destroy()

    def abrir_config_usuario(self):
        ConfigUsuarioWindow(self)

    def abrir_productos(self):
        ProductosWindow(self)

    def abrir_consulta_producto(self):
        ConsultaProductoWindow(self)

    def abrir_paises(self):
        PaisesWindow(self)

    def abrir_precios(self):
        PreciosImpuestosWindow(self)

    def abrir_reportes(self):
        ReporteWindow(self)


if __name__ == "__main__":
    app = App()
    app.mainloop()

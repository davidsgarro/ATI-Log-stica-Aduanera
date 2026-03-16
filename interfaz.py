# Interfaz gráfica para la aplicación de logística aduanera
import tkinter as tk
from tkinter import messagebox, ttk, filedialog

# Importamos la lógica de negocio y las funciones necesarias para la interfaz
import logica
from logica import (
    MONEDAS,
    cargar_productos,
    cargar_paises,
    cargar_precios_impuestos,
    guardar_productos,
    guardar_paises,
    guardar_precios_impuestos,
    guardar_config_usuario,
    cargar_config_usuario_desde_archivo,
    agregar_producto,
    actualizar_producto,
    eliminar_producto_por_id,
    agregar_pais,
    actualizar_pais,
    eliminar_pais_por_id,
    agregar_registro_precio_impuesto,
    actualizar_registro_precio_impuesto,
    eliminar_registro_precio_impuesto,
    obtener_nombre_producto,
    obtener_nombre_pais,
    calcular_costo_total,
    obtener_registros_consulta_producto,
    generar_reporte_por_pais,
    guardar_reporte_txt,
    exportar_reporte_pdf,
    enviar_reporte_por_correo
)

# Ventanas y componentes de la interfaz gráfica
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

        tk.Label(frame_form, text="Nombre:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        tk.Entry(frame_form, textvariable=self.nombre_var, width=30).grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame_form, text="Correo electrónico:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        tk.Entry(frame_form, textvariable=self.correo_var, width=30).grid(row=1, column=1, padx=5, pady=5)

        frame_botones = tk.Frame(self)
        frame_botones.pack(pady=10)

        ttk.Button(frame_botones, text="Guardar", command=self.guardar_config).grid(row=0, column=0, padx=10)
        ttk.Button(frame_botones, text="Cargar datos", command=self.cargar_config).grid(row=0, column=1, padx=10)
        ttk.Button(frame_botones, text="Cerrar", command=self.destroy).grid(row=0, column=2, padx=10)
    # Funciones para cargar y guardar la configuración del usuario
    def cargar_config(self):
        ruta_archivo = filedialog.askopenfilename(
            title="Seleccionar archivo de configuración",
            filetypes=[("Archivos de texto", "*.txt")]
        )

        if not ruta_archivo:
            return

        try:
            nombre, correo = cargar_config_usuario_desde_archivo(ruta_archivo)
            self.nombre_var.set(nombre)
            self.correo_var.set(correo)
            messagebox.showinfo("Éxito", "Datos cargados correctamente.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    # Función para guardar la configuración del usuario en un archivo
    def guardar_config(self):
        nombre = self.nombre_var.get().strip()
        correo = self.correo_var.get().strip()

        try:
            guardar_config_usuario(nombre, correo)
            messagebox.showinfo("Éxito", "Registro de usuario completado correctamente.")
            self.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))

# Ventana para gestionar productos: agregar, editar, eliminar y consultar productos registrados en el sistema
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

        tk.Label(frame_lista, text="Productos registrados").pack()

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

        tk.Label(frame_form, text="Datos del producto", font=("Arial", 11, "bold")).grid(row=0, column=0, columnspan=2, pady=5)
        tk.Label(frame_form, text="Nombre:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        tk.Entry(frame_form, textvariable=self.nombre_var, width=25).grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frame_form, text="Precio base:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        tk.Entry(frame_form, textvariable=self.precio_var, width=25).grid(row=2, column=1, padx=5, pady=5)

        ttk.Button(frame_form, text="Agregar / Guardar", command=self.guardar_producto).grid(row=3, column=0, columnspan=2, pady=5)
        ttk.Button(frame_form, text="Nuevo", command=self.limpiar_formulario).grid(row=4, column=0, columnspan=2, pady=5)
        ttk.Button(frame_form, text="Consultar", command=self.consultar_producto).grid(row=5, column=0, columnspan=2, pady=5)
        ttk.Button(frame_form, text="Eliminar", command=self.eliminar_producto).grid(row=6, column=0, columnspan=2, pady=5)
        ttk.Button(frame_form, text="Cerrar", command=self.destroy).grid(row=7, column=0, columnspan=2, pady=10)

        self.cargar_productos_en_tabla()
    # Función para cargar los productos registrados en la tabla de la interfaz
    def cargar_productos_en_tabla(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for prod in logica.productos:
            self.tree.insert("", "end", values=(
                prod["id"],
                prod["nombre"],
                f"{prod['precio']:.2f}"
            ))
    # Función para limpiar el formulario de entrada de datos y deseleccionar cualquier producto seleccionado en la tabla
    def limpiar_formulario(self):
        self.nombre_var.set("")
        self.precio_var.set("")
        self.tree.selection_remove(*self.tree.selection())
    # Función que se ejecuta al seleccionar un producto en la tabla, cargando sus datos en el formulario para su edición o consulta
    def on_tree_select(self, event):
        selected = self.tree.selection()
        if not selected:
            return

        item = self.tree.item(selected[0])
        _, nombre, precio = item["values"]
        self.nombre_var.set(nombre)
        self.precio_var.set(str(precio))
    # Función para guardar un nuevo producto o actualizar uno existente según si hay un producto seleccionado en la tabla. Luego recarga la tabla y limpia el formulario.
    
    def guardar_producto(self):
        nombre = self.nombre_var.get().strip()
        precio = self.precio_var.get().strip()

        try:
            selected = self.tree.selection()
            if selected:
                item = self.tree.item(selected[0])
                prod_id = item["values"][0]
                actualizar_producto(prod_id, nombre, precio)
            else:
                agregar_producto(nombre, precio)

            self.cargar_productos_en_tabla()
            self.limpiar_formulario()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    # Función para mostrar una ventana emergente con la información detallada del producto seleccionado en la tabla
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
    # Función para eliminar el producto seleccionado en la tabla, mostrando una confirmación antes de realizar la acción. Luego recarga la tabla y limpia el formulario.
    def eliminar_producto(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Atención", "Seleccione un producto para eliminar.")
            return

        item = self.tree.item(selected[0])
        prod_id = item["values"][0]

        confirmar = messagebox.askyesno("Confirmar", "¿Está seguro de eliminar el producto seleccionado?")
        if not confirmar:
            return

        try:
            eliminar_producto_por_id(prod_id)
            self.cargar_productos_en_tabla()
            self.limpiar_formulario()
        except Exception as e:
            messagebox.showerror("Error", str(e))

# Ventana para gestionar países: agregar, editar, eliminar y consultar países registrados en el sistema
class PaisesWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Gestión de países")
        self.geometry("550x320")
        self.resizable(False, False)

        self.nombre_var = tk.StringVar()

        frame_lista = tk.Frame(self)
        frame_lista.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        tk.Label(frame_lista, text="Países registrados").pack()

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

        tk.Label(frame_form, text="Datos del país", font=("Arial", 11, "bold")).grid(row=0, column=0, columnspan=2, pady=5)
        tk.Label(frame_form, text="Nombre:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        tk.Entry(frame_form, textvariable=self.nombre_var, width=25).grid(row=1, column=1, padx=5, pady=5)

        ttk.Button(frame_form, text="Agregar / Guardar", command=self.guardar_pais).grid(row=2, column=0, columnspan=2, pady=5)
        ttk.Button(frame_form, text="Nuevo", command=self.limpiar_formulario).grid(row=3, column=0, columnspan=2, pady=5)
        ttk.Button(frame_form, text="Eliminar", command=self.eliminar_pais).grid(row=4, column=0, columnspan=2, pady=5)
        ttk.Button(frame_form, text="Cerrar", command=self.destroy).grid(row=5, column=0, columnspan=2, pady=10)

        self.cargar_paises_en_tabla()

    # Función para cargar los países registrados en la tabla de la interfaz
    def cargar_paises_en_tabla(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for pais in logica.paises:
            self.tree.insert("", "end", values=(pais["id"], pais["nombre"]))

    # Función para limpiar el formulario de entrada de datos y deseleccionar cualquier país seleccionado en la tabla
    def limpiar_formulario(self):
        self.nombre_var.set("")
        self.tree.selection_remove(*self.tree.selection())

    # Función que se ejecuta al seleccionar un país en la tabla, cargando su nombre en el formulario para su edición o consulta
    def on_tree_select(self, event):
        selected = self.tree.selection()
        if not selected:
            return

        item = self.tree.item(selected[0])
        _, nombre = item["values"]
        self.nombre_var.set(nombre)

    # Función para guardar un nuevo país o actualizar uno existente según si hay un país seleccionado en la tabla. Luego recarga la tabla y limpia el formulario.
    def guardar_pais(self):
        nombre = self.nombre_var.get().strip()

        try:
            selected = self.tree.selection()
            if selected:
                item = self.tree.item(selected[0])
                pais_id = item["values"][0]
                actualizar_pais(pais_id, nombre)
            else:
                agregar_pais(nombre)

            self.cargar_paises_en_tabla()
            self.limpiar_formulario()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    # Función para eliminar el país seleccionado en la tabla, mostrando una confirmación antes de realizar la acción. Luego recarga la tabla y limpia el formulario.
    def eliminar_pais(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Atención", "Seleccione un país para eliminar.")
            return

        item = self.tree.item(selected[0])
        pais_id = item["values"][0]

        confirmar = messagebox.askyesno("Confirmar", "¿Está seguro de eliminar el país seleccionado?")
        if not confirmar:
            return

        try:
            eliminar_pais_por_id(pais_id)
            self.cargar_paises_en_tabla()
            self.limpiar_formulario()
        except Exception as e:
            messagebox.showerror("Error", str(e))

# Ventana para gestionar precios e impuestos: agregar, editar, eliminar y consultar registros de precios e impuestos asociados a productos y países
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

        tk.Label(frame_lista, text="Registros de precios e impuestos").pack()

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

        tk.Label(frame_form, text="Datos del registro", font=("Arial", 11, "bold")).grid(row=0, column=0, columnspan=2, pady=5)

        tk.Label(frame_form, text="Producto:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.combo_producto = ttk.Combobox(frame_form, textvariable=self.producto_var, state="readonly", width=25)
        self.combo_producto.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frame_form, text="País:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.combo_pais = ttk.Combobox(frame_form, textvariable=self.pais_var, state="readonly", width=25)
        self.combo_pais.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(frame_form, text="Precio:").grid(row=3, column=0, sticky="e", padx=5, pady=5)
        tk.Entry(frame_form, textvariable=self.precio_var, width=28).grid(row=3, column=1, padx=5, pady=5)

        tk.Label(frame_form, text="Impuesto (%):").grid(row=4, column=0, sticky="e", padx=5, pady=5)
        tk.Entry(frame_form, textvariable=self.impuesto_var, width=28).grid(row=4, column=1, padx=5, pady=5)

        tk.Label(frame_form, text="Moneda:").grid(row=5, column=0, sticky="e", padx=5, pady=5)
        ttk.Combobox(frame_form, textvariable=self.moneda_var, values=MONEDAS, state="readonly", width=25).grid(row=5, column=1, padx=5, pady=5)

        ttk.Button(frame_form, text="Agregar / Guardar", command=self.guardar_registro).grid(row=6, column=0, columnspan=2, pady=5)
        ttk.Button(frame_form, text="Nuevo", command=self.limpiar_formulario).grid(row=7, column=0, columnspan=2, pady=5)
        ttk.Button(frame_form, text="Eliminar", command=self.eliminar_registro).grid(row=8, column=0, columnspan=2, pady=5)
        ttk.Button(frame_form, text="Cerrar", command=self.destroy).grid(row=9, column=0, columnspan=2, pady=10)

        self.cargar_comboboxes()
        self.cargar_registros_en_tabla()

    # Función para cargar los productos y países registrados en los comboboxes del formulario
    def cargar_comboboxes(self):
        self.combo_producto["values"] = [producto["nombre"] for producto in logica.productos]
        self.combo_pais["values"] = [pais["nombre"] for pais in logica.paises]


    # Función para cargar los registros de precios e impuestos registrados en la tabla de la interfaz, mostrando el nombre del producto y país en lugar de sus IDs, y calculando el costo total con impuestos incluido.
    def cargar_registros_en_tabla(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for registro in logica.precios_impuestos:
            producto_nombre = obtener_nombre_producto(registro["producto_id"])
            pais_nombre = obtener_nombre_pais(registro["pais_id"])
            total = calcular_costo_total(registro["precio"], registro["impuesto"])

            self.tree.insert("", "end", values=(
                registro["id"],
                producto_nombre,
                pais_nombre,
                f"{registro['precio']:.2f}",
                f"{registro['impuesto']:.2f}",
                registro["moneda"],
                f"{total:.2f}"
            ))

    # Función para limpiar el formulario de entrada de datos y deseleccionar cualquier registro seleccionado en la tabla
    def limpiar_formulario(self):
        self.producto_var.set("")
        self.pais_var.set("")
        self.precio_var.set("")
        self.impuesto_var.set("")
        self.moneda_var.set(MONEDAS[0])
        self.tree.selection_remove(*self.tree.selection())


    # Función que se ejecuta al seleccionar un registro en la tabla, cargando sus datos en el formulario para su edición o consulta
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

    # Función para guardar un nuevo registro de precio e impuesto o actualizar uno existente según si hay un registro seleccionado en la tabla. Luego recarga la tabla y limpia el formulario.
    def guardar_registro(self):
        try:
            selected = self.tree.selection()
            if selected:
                item = self.tree.item(selected[0])
                registro_id = item["values"][0]
                actualizar_registro_precio_impuesto(
                    registro_id,
                    self.producto_var.get(),
                    self.pais_var.get(),
                    self.precio_var.get(),
                    self.impuesto_var.get(),
                    self.moneda_var.get()
                )
            else:
                agregar_registro_precio_impuesto(
                    self.producto_var.get(),
                    self.pais_var.get(),
                    self.precio_var.get(),
                    self.impuesto_var.get(),
                    self.moneda_var.get()
                )

            self.cargar_comboboxes()
            self.cargar_registros_en_tabla()
            self.limpiar_formulario()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    # Función para eliminar el registro seleccionado en la tabla, mostrando una confirmación antes de realizar la acción. Luego recarga la tabla y limpia el formulario.
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

        try:
            eliminar_registro_precio_impuesto(registro_id)
            self.cargar_registros_en_tabla()
            self.limpiar_formulario()
        except Exception as e:
            messagebox.showerror("Error", str(e))

# Ventana para consultar precios e impuestos por producto, mostrando una tabla con los registros filtrados por producto y moneda, y el costo total calculado con impuestos incluido.
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

        tk.Label(frame_filtros, text="Producto:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.combo_producto = ttk.Combobox(frame_filtros, textvariable=self.producto_var, state="readonly", width=30)
        self.combo_producto.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame_filtros, text="Moneda:").grid(row=0, column=2, sticky="e", padx=5, pady=5)
        self.combo_moneda = ttk.Combobox(frame_filtros, textvariable=self.moneda_var, values=MONEDAS, state="readonly", width=10)
        self.combo_moneda.grid(row=0, column=3, padx=5, pady=5)

        ttk.Button(frame_filtros, text="Consultar", command=self.consultar).grid(row=0, column=4, padx=10, pady=5)

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

        ttk.Button(self, text="Cerrar", command=self.destroy).pack(pady=5)

        self.cargar_productos_en_combobox()

    # Función para cargar los productos registrados en el combobox del formulario de consulta
    def cargar_productos_en_combobox(self):
        self.combo_producto["values"] = [producto["nombre"] for producto in logica.productos]

    # Función para consultar los registros de precios e impuestos filtrados por producto y moneda, mostrando el resultado en la tabla de la interfaz. Si no hay registros para el producto y moneda seleccionados, muestra un mensaje informativo.
    def consultar(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        try:
            registros = obtener_registros_consulta_producto(
                self.producto_var.get(),
                self.moneda_var.get()
            )

            if not registros:
                messagebox.showinfo(
                    "Sin datos",
                    "No hay precios registrados para ese producto en la moneda seleccionada."
                )
                return

            for reg in registros:
                self.tree.insert(
                    "",
                    "end",
                    values=(
                        reg["pais"],
                        f"{reg['precio']:.2f}",
                        f"{reg['impuesto']:.2f}",
                        reg["moneda"],
                        f"{reg['total']:.2f}"
                    )
                )

        except Exception as e:
            messagebox.showerror("Error", str(e))

# Ventana para generar un reporte de productos por país, mostrando una tabla con los registros filtrados por país y moneda, ordenados por costo total descendente, y con opciones para guardar el reporte en formato TXT, exportarlo a PDF o enviarlo por correo electrónico.
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

        tk.Label(frame_filtros, text="País:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.combo_pais = ttk.Combobox(frame_filtros, textvariable=self.pais_var, state="readonly", width=30)
        self.combo_pais.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame_filtros, text="Moneda:").grid(row=0, column=2, sticky="e", padx=5, pady=5)
        self.combo_moneda = ttk.Combobox(frame_filtros, textvariable=self.moneda_var, values=MONEDAS, state="readonly", width=10)
        self.combo_moneda.grid(row=0, column=3, padx=5, pady=5)

        ttk.Button(frame_filtros, text="Generar reporte", command=self.generar_reporte).grid(row=0, column=4, padx=10, pady=5)

        frame_tabla = tk.Frame(self)
        frame_tabla.pack(fill="both", expand=True, padx=10, pady=10)

        tk.Label(
            frame_tabla,
            text="Productos ordenados por costo total descendente",
            font=("Arial", 12, "bold")
        ).pack(pady=(0, 10))

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

        ttk.Button(frame_botones, text="Cerrar", command=self.destroy).pack(side="right")

        self.cargar_paises_en_combobox()

    # Función para cargar los países registrados en el combobox del formulario de generación de reporte
    def cargar_paises_en_combobox(self):
        self.combo_pais["values"] = [pais["nombre"] for pais in logica.paises]

    # Función para habilitar los botones de guardar, exportar y enviar por correo después de generar un reporte exitosamente
    def habilitar_botones(self):
        self.btn_txt.config(state="normal")
        self.btn_pdf.config(state="normal")
        self.btn_correo.config(state="normal")

    # Función para generar el reporte de productos por país y moneda, mostrando el resultado en la tabla de la interfaz. Si no hay registros para el país y moneda seleccionados, muestra un mensaje informativo.
    def generar_reporte(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        self.reporte_generado = []

        try:
            registros = generar_reporte_por_pais(
                self.pais_var.get(),
                self.moneda_var.get()
            )

            if not registros:
                messagebox.showinfo(
                    "Sin datos",
                    f"No hay precios registrados para {self.pais_var.get()} en {self.moneda_var.get()}."
                )
                return

            self.reporte_generado = registros

            for reg in registros:
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
                f"Reporte generado exitosamente.\n{len(registros)} productos encontrados para {self.pais_var.get()}."
            )

        except Exception as e:
            messagebox.showerror("Error", str(e))

    # Función para guardar el reporte generado en un archivo de texto, mostrando un diálogo para seleccionar la ubicación y nombre del archivo. Si no se ha generado un reporte, muestra una advertencia.
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
            guardar_reporte_txt(
                self.reporte_generado,
                self.pais_var.get(),
                self.moneda_var.get(),
                ruta_archivo
            )
            messagebox.showinfo("Éxito", f"Reporte guardado en:\n{ruta_archivo}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # Función para exportar el reporte generado a un archivo PDF, mostrando un diálogo para seleccionar la ubicación y nombre del archivo. Si no se ha generado un reporte, muestra una advertencia.
    def exportar_pdf(self):
        if not self.reporte_generado:
            messagebox.showwarning("Atención", "Primero debe generar un reporte.")
            return

        ruta_archivo = filedialog.asksaveasfilename(
            title="Guardar reporte como PDF",
            defaultextension=".pdf",
            filetypes=[("Archivos PDF", "*.pdf")]
        )

        if not ruta_archivo:
            return

        try:
            exportar_reporte_pdf(
                self.reporte_generado,
                self.pais_var.get(),
                self.moneda_var.get(),
                ruta_archivo
            )
            messagebox.showinfo("Éxito", f"Reporte PDF guardado en:\n{ruta_archivo}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # Función para enviar el reporte generado por correo electrónico, mostrando un diálogo para ingresar el correo destino. Si no se ha generado un reporte, muestra una advertencia.
    def enviar_correo(self):
        if not self.reporte_generado:
            messagebox.showwarning("Atención", "Primero debe generar un reporte.")
            return

        try:
            correo_destino = enviar_reporte_por_correo(
                self.reporte_generado,
                self.pais_var.get(),
                self.moneda_var.get()
            )
            messagebox.showinfo("Éxito", f"Reporte enviado correctamente a {correo_destino}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

# Ventana principal de la aplicación, con botones para acceder a las diferentes funcionalidades del sistema y un protocolo para guardar los datos antes de cerrar la aplicación
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("ATI Logística Aduanera")
        self.geometry("500x400")

        cargar_productos()
        cargar_paises()
        cargar_precios_impuestos()

        self.protocol("WM_DELETE_WINDOW", self.cerrar_app)

        tk.Label(self, text="ATI Logística Aduanera", font=("Arial", 16, "bold")).pack(pady=10)

        tk.Button(self, text="Configuración de usuario", width=30, command=self.abrir_config_usuario).pack(pady=5)
        tk.Button(self, text="Gestión de productos", width=30, command=self.abrir_productos).pack(pady=5)
        tk.Button(self, text="Consulta por producto", width=30, command=self.abrir_consulta_producto).pack(pady=5)
        tk.Button(self, text="Gestión de países", width=30, command=self.abrir_paises).pack(pady=5)
        tk.Button(self, text="Precios e impuestos", width=30, command=self.abrir_precios).pack(pady=5)
        tk.Button(self, text="Reportes", width=30, command=self.abrir_reportes).pack(pady=5)
        tk.Button(self, text="Salir", width=30, command=self.cerrar_app).pack(pady=20)

    # Función para guardar los datos de productos, países y precios e impuestos antes de cerrar la aplicación, asegurando que los cambios realizados durante la sesión se conserven para la próxima vez que se abra la aplicación.
    def cerrar_app(self):
        guardar_productos()
        guardar_paises()
        guardar_precios_impuestos()
        self.destroy()

    # Funciones para abrir las diferentes ventanas de gestión y consulta, cada una con su propia lógica y funcionalidades específicas para manejar los datos relacionados con productos, países, precios e impuestos, y generación de reportes.
    def abrir_config_usuario(self):
        ConfigUsuarioWindow(self)

    # Función para abrir la ventana de gestión de productos, donde se pueden agregar, editar, eliminar y consultar los productos registrados en el sistema.
    def abrir_productos(self):
        ProductosWindow(self)

    # Función para abrir la ventana de consulta por producto, donde se pueden consultar los precios e impuestos asociados a un producto específico filtrados por moneda, mostrando el resultado en una tabla.
    def abrir_consulta_producto(self):
        ConsultaProductoWindow(self)

    # Función para abrir la ventana de gestión de países, donde se pueden agregar, editar, eliminar y consultar los países registrados en el sistema.
    def abrir_paises(self):
        PaisesWindow(self)

    # Función para abrir la ventana de gestión de precios e impuestos, donde se pueden agregar, editar, eliminar y consultar los registros de precios e impuestos asociados a productos y países, mostrando el resultado en una tabla.
    def abrir_precios(self):
        PreciosImpuestosWindow(self)

    # Función para abrir la ventana de generación de reportes, donde se pueden generar reportes de productos por país y moneda, mostrando el resultado en una tabla ordenada por costo total descendente, y con opciones para guardar el reporte en formato TXT, exportarlo a PDF o enviarlo por correo electrónico.
    def abrir_reportes(self):
        ReporteWindow(self)

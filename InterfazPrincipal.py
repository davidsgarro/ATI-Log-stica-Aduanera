import tkinter as tk
from tkinter import messagebox, ttk
import re

#variables globales
productos = []
contador_productos = 1
paises = []
contador_paises = 1
precios_impuestos = []
contador_registros = 1
MONEDAS = ["CRC", "USD", "EUR", "BRL"]

#---------------------------------------------------------------------------------------- FUNCIONES ----------------------------------------------------------------------------------------

#-------------------------------------------------------------- FUNCIONES PRECIOS E IMPUESTOS --------------------------------------------------------------

#funcion para guardar precios e impuestos en el archivo precios_impuestos.txt, guarda el contador de registros en la primera linea
#luego cada registro en una linea con su id, producto_id, pais_id, precio, impuesto y moneda separados por |
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

#funcion para cargar precios e impuestos desde el archivo de precios_impuestos.txt
#si ese archivo no existe, lo crea con un contador de registros en 1 y una lista vacia de precios e impuestos
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


#-------------------------------------------------------------- FUNCIONES GESTION PAISES --------------------------------------------------------------

#funcion para guardar paises en el archivo paises.txt, guarda el contador de paises en la primera linea y luego cada pais en una linea con su id y nombre separados por |
def guardar_paises():
    global paises, contador_paises
    try:
        with open("paises.txt", "w", encoding="utf-8") as archivo:
            archivo.write(str(contador_paises) + "\n")
            for pais in paises:
                archivo.write(f"{pais['id']}|{pais['nombre']}\n")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudieron guardar los países.\n{e}")

#funcion para cargar paises desde el archivo de paises.txt, si ese archivo no existe, lo crea con un contador de paises en 1 y una lista vacia de paises
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

#-------------------------------------------------------------- FUNCIONES GESTION PRODUCTOS --------------------------------------------------------------

#funcion para guardar productos en el archivo productos.txt
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

#funcion para cargar productos desde el archivo de productos.txtsi ese archivo no existe, lo crea con un contador de productos en 1 y una lista vacia de productos 
#si el archivo existe, lee el contador y los productos guardados para guardarlos en la variable global productos y contador_productos 
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

EMAIL_REGEX = r"^[\w\.-]+@[\w\.-]+\.\w+$"

#--------------------------------------------------------------------------- VENTANAS ---------------------------------------------------------------------------

#-------------------------------------------------------------- VENTANA PRECIOS E IMPUESTOS --------------------------------------------------------------

#ventana para gestionar precios e impuestos, con una tabla para mostrar los registros y un formulario para agregar o editar registros
#valida que se hayan registrado al menos un producto y un país antes de permitir agregar un registro
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

        lbl_impuesto = tk.Label(frame_form, text="Impuesto: (%)")
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
    #funcion para cargar los nombres de los productos y paises en los comboboxes, obtiene los nombres de las variables globales productos y paises y los asigna a los comboboxes correspondientes
    def cargar_comboboxes(self):
        nombres_productos = [producto["nombre"] for producto in productos]
        nombres_paises = [pais["nombre"] for pais in paises]

        self.combo_producto["values"] = nombres_productos
        self.combo_pais["values"] = nombres_paises

    #funcion para obtener el nombre de un producto a partir de su id, busca en la variable global productos el producto con el id dado y devuelve su nombre
    #si no lo encuentra devuelve "Desconocido"
    def obtener_nombre_producto(self, producto_id):
        for producto in productos:
            if producto["id"] == producto_id:
                return producto["nombre"]
        return "Desconocido"

    #funcion para obtener el nombre de un pais a partir de su id, busca en la variable global paises el pais con el id dado y devuelve su nombre
    def obtener_nombre_pais(self, pais_id):
        for pais in paises:
            if pais["id"] == pais_id:
                return pais["nombre"]
        return "Desconocido"

    #funcion para obtener el id de un producto a partir de su nombre, busca en la variable global productos el producto con el nombre dado y devuelve su id
    def obtener_id_producto_por_nombre(self, nombre):
        for producto in productos:
            if producto["nombre"] == nombre:
                return producto["id"]
        return None

    #funcion para obtener el id de un pais a partir de su nombre, busca en la variable global paises el pais con el nombre dado y devuelve su id
    def obtener_id_pais_por_nombre(self, nombre):
        for pais in paises:
            if pais["nombre"] == nombre:
                return pais["id"]
        return None

    #funcion para calcular el costo total a partir del precio y el impuesto, devuelve el resultado de sumar el precio con el impuesto calculado como un porcentaje del precio
    def calcular_costo_total(self, precio, impuesto):
        return precio + (precio * (impuesto / 100))

    #funcion para cargar los registros de precios e impuestos en la tabla, primero borra los registros que ya estan en la tabla para evitar duplicados
    #luego carga los registros desde la variable global precios_impuestos
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

    #funcion para limpiar el formulario de datos del registro y deseleccionar cualquier registro seleccionado en la tabla
    def limpiar_formulario(self):
        self.producto_var.set("")
        self.pais_var.set("")
        self.precio_var.set("")
        self.impuesto_var.set("")
        self.moneda_var.set(MONEDAS[0])
        self.tree.selection_remove(*self.tree.selection())

    #funcion que se ejecuta al seleccionar un registro en la tabla, carga los datos del registro seleccionado en el formulario para poder editarlos o eliminarlos
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

    #funcion para guardar un nuevo registro o actualizar uno existente, valida que se hayan registrado al menos un producto y un país antes de permitir agregar un registro
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

    #funcion para eliminar un registro seleccionado en la tabla, muestra un mensaje de confirmacion antes de eliminar el registro
    #si se confirma, elimina el registro de la variable global precios_impuestos y actualiza la tabla y el formulario
    def eliminar_registro(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Atención", "Seleccione un registro para eliminar.")
            return

        item = self.tree.item(selected[0])
        registro_id = item["values"][0]

        confirmar = messagebox.askyesno(
            "Confirmar", "¿Está seguro de eliminar el registro seleccionado?"
        )
        if not confirmar:
            return

        global precios_impuestos
        precios_impuestos = [r for r in precios_impuestos if r["id"] != registro_id]

        guardar_precios_impuestos()
        self.cargar_registros_en_tabla()
        self.limpiar_formulario()


#-------------------------------------------------------------- VENTANA GESTION PAISES --------------------------------------------------------------
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


#-------------------------------------------------------------- VENTANA GESTION USUARIOS --------------------------------------------------------------

#ventana para configurar datos del usuario, ya está validado el formato del correo y que no quede vacio y se guarda en txt
class ConfigUsuarioWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Configuración de usuario")
        self.geometry("400x220")
        self.resizable(False, False)

        self.parent = parent

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

        btn_cancelar = ttk.Button(frame_botones, text="Cerrar", command=self.destroy)
        btn_cancelar.grid(row=0, column=1, padx=10)
    #funcion para guardar la configuracion del usuario en el archivo config_usuario.txt
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

#-------------------------------------------------------------- VENTANA GESTION PRODUCTOS --------------------------------------------------------------

#Ventana para gestionar productos con su respectiva tabla
class ProductosWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Gestión de productos")
        self.geometry("600x350")
        self.resizable(False, False)

        self.parent = parent

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

        btn_eliminar = ttk.Button(frame_form, text="Eliminar", command=self.eliminar_producto)
        btn_eliminar.grid(row=5, column=0, columnspan=2, pady=5)

        btn_cerrar = ttk.Button(frame_form, text="Cerrar", command=self.destroy)
        btn_cerrar.grid(row=6, column=0, columnspan=2, pady=10)

        self.cargar_productos_en_tabla()

    #funcion para cargar los productos en la tabla, primero borra los productos que ya estan en la tabla y luego los vuelve a cargar desde la variable global productos
    def cargar_productos_en_tabla(self):
        #borra los productos que ya estan en la tabla para evitar duplicados
        for item in self.tree.get_children():
            self.tree.delete(item)
        #circulo para cargar los productos en la tabla, formatea el precio a 2 decimales y muestra
        for prod in productos:
            self.tree.insert("", "end", values=(
                prod["id"], prod["nombre"], f"{prod['precio']:.2f}"
            ))
    #funcion para limpiar el formulario de datos del producto y deseleccionar cualquier producto seleccionado en la tabla
    def limpiar_formulario(self):
        self.nombre_var.set("")
        self.precio_var.set("")
        self.tree.selection_remove(*self.tree.selection())

    #funcion que se ejecuta al seleccionar un producto en la tabla, carga los datos del producto seleccionado en el formulario para poder editarlos o eliminarlos
    def on_tree_select(self, event):
        selected = self.tree.selection()
        if not selected:
            return
        item = self.tree.item(selected[0])
        _id, nombre, precio = item["values"]
        self.nombre_var.set(nombre)
        self.precio_var.set(str(precio))

    #funcion para guardar un nuevo producto o actualizar uno existente, valida que el nombre y el precio no esten vacios y que el precio sea un numero positivo
    #si se selecciono un producto en la tabla actualiza ese producto, si no se selecciono ninguno agrega uno nuevo a la lista de productos, luego guarda los productos en el archivo y recarga la tabla
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

    #funcion para eliminar un producto seleccionado en la tabla, primero pregunta por confirmación y luego elimina el producto de la lista de productos
    #por último guarda los productos en el archivo y recarga la tabla
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

#-------------------------------------------------------------- VENTANA GESTION CENTRAL --------------------------------------------------------------

#ventana principal de la aplicación con botones para acceder a las diferentes funcionalidades
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

        #boton para abrir ventana configuracion de usuario
        btn_config = tk.Button(
            self,
            text="Configuración de usuario",
            width=30,
            command=self.abrir_config_usuario
        )
        btn_config.pack(pady=5)

        #boton para abrir ventana gestion de productos
        btn_productos = tk.Button(
            self,
            text="Gestión de productos",
            width=30,
            command=self.abrir_productos
        )
        btn_productos.pack(pady=5)

        #boton para abrir ventana gestion de paises
        btn_paises = tk.Button(
            self,
            text="Gestión de países",
            width=30,
            command=self.abrir_paises
        )
        btn_paises.pack(pady=5)

        #boton para abrir ventana gestion de precios e impuestos
        btn_precios = tk.Button(
            self,
            text="Precios e impuestos",
            width=30,
            command=self.abrir_precios
        )
        btn_precios.pack(pady=5)

        #boton para abrir ventana generacion de reportes
        btn_reportes = tk.Button(
            self,
            text="Reportes",
            width=30,
            command=self.abrir_reportes
        )
        btn_reportes.pack(pady=5)

        #boton para salir de la aplicación
        btn_salir = tk.Button(self, text="Salir", width=30, command=self.cerrar_app)
        btn_salir.pack(pady=20)

    #funcion para cerrar la aplicación, primero guarda los productos en el archivo y luego cierra la ventana principal
    def cerrar_app(self):
        guardar_productos()
        guardar_paises()
        guardar_precios_impuestos()
        self.destroy()

    #funcion para abrir la ventana de configuración de usuario
    def abrir_config_usuario(self):
        ConfigUsuarioWindow(self)

    #funcion para abrir la ventana de gestión de productos
    def abrir_productos(self):
        ProductosWindow(self)

    #funcion para abrir la ventana de gestión de países
    def abrir_paises(self):
        PaisesWindow(self)

    #funcion para abrir la ventana de gestión de precios e impuestos
    def abrir_precios(self):
        PreciosImpuestosWindow(self)

    #funcion para abrir la ventana de generación de reportes
    def abrir_reportes(self):
        messagebox.showinfo("Reportes", "Aquí irá la generación de reportes")

#funcion principal para iniciar la aplicación
if __name__ == "__main__":
    app = App()
    app.mainloop()

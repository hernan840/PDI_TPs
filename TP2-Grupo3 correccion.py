"""
Interfaz Gráfica - TP2 Grupo 3 (Tkinter + NumPy + Pillow)
Geupo 3
integrantes:
   FLORES, HERNAN
   GUZMAN, ARMIN
   MERCADO, ALEJANDRO
"""

import tkinter as tk
from tkinter import filedialog, messagebox
import numpy as np
from PIL import Image, ImageTk

# ---------Funciones de Conversión de Espacio de Color----------------


def rgbAyiq(rgb):
    """Convierte una imagen de formato RGB a YIQ."""
    yiq = np.zeros(rgb.shape)
    yiq[:, :, 0] = 0.229*rgb[:, :, 0] + 0.587*rgb[:, :, 1] + 0.114*rgb[:, :, 2]
    yiq[:, :, 1] = 0.595716*rgb[:, :, 0] - \
        0.274453*rgb[:, :, 1] - 0.321263*rgb[:, :, 2]
    yiq[:, :, 2] = 0.211456*rgb[:, :, 0] - \
        0.522591*rgb[:, :, 1] + 0.311135*rgb[:, :, 2]
    return yiq


def yiqArgb(yiq):
    """Convierte una imagen de formato YIQ a RGB asegurando valores entre 0 y 1."""
    rgb = np.zeros(yiq.shape)
    rgb[:, :, 0] = yiq[:, :, 0] + 0.9663 * yiq[:, :, 1] + 0.6210 * yiq[:, :, 2]
    rgb[:, :, 1] = yiq[:, :, 0] - 0.2721 * yiq[:, :, 1] - 0.6474 * yiq[:, :, 2]
    rgb[:, :, 2] = yiq[:, :, 0] - 1.1070 * yiq[:, :, 1] + 1.7046 * yiq[:, :, 2]
    return rgb

# ---------Funciones de Operaciones----------------


def sumaClipeada(img1, img2, formato):
    """Suma dos imágenes (procesa canales YIQ si corresponde)."""
    if formato == "YIQ":
        yiq1 = rgbAyiq(img1)
        yiq2 = rgbAyiq(img2)
        # Separar canales
        y1, i1, q1 = yiq1[:, :, 0], yiq1[:, :, 1], yiq1[:, :, 2]
        y2, i2, q2 = yiq2[:, :, 0], yiq2[:, :, 1], yiq2[:, :, 2]

        yC = np.clip(y1 + y2, 0.0, 1.0)

        denominador = np.maximum(y1 + y2, 1e-6)
        iC = (y1 * i1 + y2 * i2) / denominador
        qC = (y1 * q1 + y2 * q2) / denominador

        i_C = np.clip(iC, -0.5957, 0.5957)
        q_C = np.clip(qC, -0.5226, 0.5226)

        # Reconstruir la imagen
        yiqC = np.stack([yC, i_C, q_C], axis=-1)

        rgb = yiqArgb(yiqC)
        return np.clip(rgb, 0.0, 1.0)

    # Si no es YIQ
    return np.clip(img1 + img2, 0.0, 1.0)


def sumaPromedio(img1, img2, formato):
    """Suma dos imágenes calculando el promedio aritmético entre ambas."""
    if formato == "YIQ":

        yiq1 = rgbAyiq(img1)
        yiq2 = rgbAyiq(img2)
        # Separar canales
        y1, i1, q1 = yiq1[:, :, 0], yiq1[:, :, 1], yiq1[:, :, 2]
        y2, i2, q2 = yiq2[:, :, 0], yiq2[:, :, 1], yiq2[:, :, 2]

        yC = (y1 + y2)/2

        denominador = np.maximum(y1 + y2, 1e-6)
        iC = (y1 * i1 + y2 * i2) / denominador
        qC = (y1 * q1 + y2 * q2) / denominador

        y_C = np.clip(yC, 0, 1)
        i_C = np.clip(iC, -0.5957, 0.5957)
        q_C = np.clip(qC, -0.5226, 0.5226)

        # Reconstruir la imagen
        yiqC = np.stack([y_C, i_C, q_C], axis=-1)
        return yiqArgb(yiqC)

    # Si es RGB
    r1, g1, b1 = img1[:, :, 0], img1[:, :, 1], img1[:, :, 2]
    r2, g2, b2 = img2[:, :, 0], img2[:, :, 1], img2[:, :, 2]

    rC = (r1 + r2)/2
    gC = (g1 + g2)/2
    bC = (b1 + b2)/2

    # Reconstruir la imagen
    rgbC = np.stack([rC, gC, bC], axis=-1)
    return rgbC


def restaClipeada(img1, img2, formato):
    """Resta dos imágenes (procesa canales YIQ si corresponde)."""
    if formato == "YIQ":
        yiq1 = rgbAyiq(img1)
        yiq2 = rgbAyiq(img2)
        # Separar canales
        y1, i1, q1 = yiq1[:, :, 0], yiq1[:, :, 1], yiq1[:, :, 2]
        y2, i2, q2 = yiq2[:, :, 0], yiq2[:, :, 1], yiq2[:, :, 2]

        yC = np.clip(y1 - y2, 0.0, 1.0)

        denominador = np.maximum(y1 + y2, 1e-6)
        iC = (y1 * i1 + y2 * i2) / denominador
        qC = (y1 * q1 + y2 * q2) / denominador

        i_C = np.clip(iC, -0.5957, 0.5957)
        q_C = np.clip(qC, -0.5226, 0.5226)

        # Reconstruir la imagen
        yiqC = np.stack([yC, i_C, q_C], axis=-1)
        rgb = yiqArgb(yiqC)
        return np.clip(rgb, 0.0, 1.0)

    # Si es RGB
    r1, g1, b1 = img1[:, :, 0], img1[:, :, 1], img1[:, :, 2]
    r2, g2, b2 = img2[:, :, 0], img2[:, :, 1], img2[:, :, 2]

    rC = np.clip(r1 - r2, 0.0, 1.0)
    gC = np.clip(g1 - g2, 0.0, 1.0)
    bC = np.clip(b1 - b2, 0.0, 1.0)

    # Reconstruir la imagen
    rgbC = np.stack([rC, gC, bC], axis=-1)

    return rgbC


def restaPromedio(img1, img2, formato):
    """Resta la imagen 2 de la imagen 1 y calcula el promedio o escala de la diferencia."""
    if formato == "YIQ":
        yiq1 = rgbAyiq(img1)
        yiq2 = rgbAyiq(img2)
        # Separar canales
        y1, i1, q1 = yiq1[:, :, 0], yiq1[:, :, 1], yiq1[:, :, 2]
        y2, i2, q2 = yiq2[:, :, 0], yiq2[:, :, 1], yiq2[:, :, 2]

        yC = (y1 - y2)/2

        denominador = np.maximum(y1 + y2, 1e-6)
        iC = (y1 * i1 + y2 * i2) / denominador
        qC = (y1 * q1 + y2 * q2) / denominador

        # Reconstruir la imagen
        yiqC = np.stack([yC, iC, qC], axis=-1)
        return yiqArgb(yiqC)

    # Si es RGB
    return (img1 - img2) / 2.0


def restaValorAbsoluto(img1, img2, formato):
    """Calcula el valor absoluto de la diferencia entre dos imágenes."""
    if formato == "YIQ":
        yiq1 = rgbAyiq(img1)
        yiq2 = rgbAyiq(img2)
        # Separar canales
        y1, i1, q1 = yiq1[:, :, 0], yiq1[:, :, 1], yiq1[:, :, 2]
        y2, i2, q2 = yiq2[:, :, 0], yiq2[:, :, 1], yiq2[:, :, 2]

        yC = np.abs(y1 - y2)

        denominador = np.maximum(y1 + y2, 1e-6)
        iC = (y1 * i1 + y2 * i2) / denominador
        qC = (y1 * q1 + y2 * q2) / denominador

        # Reconstruir la imagen
        yiqC = np.stack([yC, iC, qC], axis=-1)
        return yiqArgb(yiqC)

    # Si es RGB
    return np.abs(img1 - img2)


def producto(img1, img2, formato):
    """Multiplica dos imágenes píxel a píxel y recorta los valores entre 0 y 1."""
    if formato == "YIQ":
        yiq1 = rgbAyiq(img1)
        yiq2 = rgbAyiq(img2)
        # Separar canales
        y1, i1, q1 = yiq1[:, :, 0], yiq1[:, :, 1], yiq1[:, :, 2]
        y2, i2, q2 = yiq2[:, :, 0], yiq2[:, :, 1], yiq2[:, :, 2]

        yC = y1 * y2

        denominador = np.maximum(y1 + y2, 1e-6)
        iC = (y1 * i1 + y2 * i2) / denominador
        qC = (y1 * q1 + y2 * q2) / denominador

        # Reconstruir la imagen
        yiqC = np.stack([yC, iC, qC], axis=-1)
        return yiqArgb(yiqC)

    # Si es RGB
    return img1 * img2


def cociente(img1, img2, formato):
    """Divide la imagen 1 por la imagen 2 de forma segura evitando divisiones por cero."""
    epsilon = 1e-6

    if formato == "YIQ":
        yiq1 = rgbAyiq(img1)
        yiq2 = rgbAyiq(img2)
        # Separar canales
        y1, i1, q1 = yiq1[:, :, 0], yiq1[:, :, 1], yiq1[:, :, 2]
        y2, i2, q2 = yiq2[:, :, 0], yiq2[:, :, 1], yiq2[:, :, 2]

        denominador = np.maximum(y2, epsilon)
        yC = y1 / (y2 + epsilon)

        denominador = np.maximum(y1 + y2, epsilon)
        iC = (y1 * i1 + y2 * i2) / denominador
        qC = (y1 * q1 + y2 * q2) / denominador

        # Reconstruir la imagen
        yiqC = np.stack([yC, iC, qC], axis=-1)
        return yiqArgb(yiqC)

    # Si es RGB
    return img1 / (img2 + epsilon)


def interpolar_imagenes(img1, img2):
    """
    Realiza la interpolación combinando canales YIQ de dos imágenes.
    Convierte ambas a YIQ, separa canales, combina y retorna la imagen en RGB.
    """
    # Convertir imágenes de RGB a YIQ
    im_yiqA = rgbAyiq(img1)
    im_yiqB = rgbAyiq(img2)

    # Separar canales im_yiqA
    yA, iA, qA = im_yiqA[:, :, 0], im_yiqA[:, :, 1], im_yiqA[:, :, 2]
    # Separar canales im_yiqB
    yB, iB, qB = im_yiqB[:, :, 0], im_yiqB[:, :, 1], im_yiqB[:, :, 2]

    # Por lo general, se usa la mayor luminancia
    # yC = np.maximum(yA, yB)
    yC = yA + yB       # Correccion
    # Aplicar la fórmula exacta de interpolación para I y Q
    # Añadimos un pequeño epsilon para evitar división por cero si YA + YB = 0
    epsilon = 1e-7
    suma_Y = yA + yB + epsilon

    iC = (yA * iA + yB * iB) / suma_Y
    qC = (yA * qA + yB * qB) / suma_Y

    # Unir canales YIQ interpolados
    im_yiq_interp = np.stack([yC, iC, qC], axis=-1)

    # Convertir de YIQ a RGB y retornar
    im_rgb_interp = yiqArgb(im_yiq_interp)
    return np.clip(im_rgb_interp, 0.0, 1.0)


def if_darker(im_1, im_2):
    yiq_1 = rgbAyiq(im_1)
    yiq_2 = rgbAyiq(im_2)

    yA = yiq_1[:, :, 0]
    yB = yiq_2[:, :, 0]

    # compara liminancia
    mask = yA < yB
    # Utiliza np.where para seleccionar los píxeles según la máscara
    result_rgb = np.where(mask[:, :, np.newaxis], im_1, im_2)
    return np.clip(result_rgb, 0, 1)


def if_lighter(im_1, im_2):
    yiq_1 = rgbAyiq(im_1)
    yiq_2 = rgbAyiq(im_2)

    yA = yiq_1[:, :, 0]
    yB = yiq_2[:, :, 0]

    # compara liminancia
    mask = yA > yB
    # Utiliza np.where para seleccionar los píxeles según la máscara
    result_rgb = np.where(mask[:, :, np.newaxis], im_1, im_2)
    return np.clip(result_rgb, 0, 1)

# ---------------------------------------------------


class AppTP2:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Procesamiento Digital de Imágenes - TP2 Grupo N°3")
        self.ventana.geometry("1250x620")
        self.ventana.config(bg="#f0f4f8")

        # Variables para almacenar las imágenes
        self.imagen1_data = None
        self.imagen2_data = None
        self.imagen_procesada_data = None

        # Construir la interfaz gráfica
        self.crear_interfaz()

    def crear_interfaz(self):
        # ----------------------------------------------------
        # TÍTULO SUPERIOR
        # ----------------------------------------------------
        frame_titulo = tk.Frame(self.ventana, bg="#1e3d59", pady=10)
        frame_titulo.pack(side="top", fill="x")

        lbl_titulo = tk.Label(
            frame_titulo,
            text="Procesamiento Digital de Imágenes - TP2 grupo 3",
            font=("Arial", 16, "bold"),
            fg="white",
            bg="#1e3d59"
        )
        lbl_titulo.pack()

        # ----------------------------------------------------
        # PANEL CENTRAL (CONTENEDOR DE IMÁGENES FIJOS)
        # ----------------------------------------------------
        frame_imagenes = tk.Frame(self.ventana, bg="#f0f4f8")
        frame_imagenes.pack(fill="both", expand=True, padx=15, pady=15)

        # Centrar los contenedores en el panel principal
        frame_imagenes.columnconfigure(0, weight=1)
        frame_imagenes.columnconfigure(1, weight=1)
        frame_imagenes.columnconfigure(2, weight=1)
        frame_imagenes.rowconfigure(0, weight=1)

        # Contenedor intermedio centrado para evitar deformaciones
        sub_frame = tk.Frame(frame_imagenes, bg="#f0f4f8")
        sub_frame.grid(row=0, column=0, columnspan=3)

        # Dimensiones fijas exactas para que los 3 contenedores sean idénticos y estables
        ANCHO_CAJA = 380
        ALTO_CAJA = 380

        estilo_marco = {
            "bg": "white",
            "bd": 2,
            "relief": "groove",
            "width": ANCHO_CAJA,
            "height": ALTO_CAJA
        }

        # --- Imagen 1 ---
        marco_img1 = tk.Frame(sub_frame, **estilo_marco)
        marco_img1.pack(side="left", padx=12)
        marco_img1.pack_propagate(False)  # Bloquea cambios de tamaño

        # Texto fijo inferior
        tk.Label(marco_img1, text="Imagen 1", bg="white", font=(
            "Arial", 10, "bold"), fg="#333333").pack(side="bottom", fill="x", pady=4)

        self.label_img1 = tk.Label(
            marco_img1, text="imagen 1", bg="#e8edf2", fg="#555555", font=("Arial", 11))
        self.label_img1.pack(fill="both", expand=True, padx=4, pady=4)

        # --- Imagen 2 ---
        marco_img2 = tk.Frame(sub_frame, **estilo_marco)
        marco_img2.pack(side="left", padx=12)
        marco_img2.pack_propagate(False)  # Bloquea cambios de tamaño

        # Texto fijo inferior
        tk.Label(marco_img2, text="Imagen 2", bg="white", font=(
            "Arial", 10, "bold"), fg="#333333").pack(side="bottom", fill="x", pady=4)

        self.label_img2 = tk.Label(
            marco_img2, text="imagen 2", bg="#e8edf2", fg="#555555", font=("Arial", 11))
        self.label_img2.pack(fill="both", expand=True, padx=4, pady=4)

        # --- Imagen Procesada ---
        marco_proc = tk.Frame(sub_frame, **estilo_marco)
        marco_proc.pack(side="left", padx=12)
        marco_proc.pack_propagate(False)  # Bloquea cambios de tamaño

        # Texto fijo inferior
        tk.Label(marco_proc, text="Procesada", bg="white", font=(
            "Arial", 10, "bold"), fg="#333333").pack(side="bottom", fill="x", pady=4)

        self.label_procesada = tk.Label(
            marco_proc, text="procesada", bg="#e8edf2", fg="#555555", font=("Arial", 11))
        self.label_procesada.pack(fill="both", expand=True, padx=4, pady=4)

        # ----------------------------------------------------
        # PANEL INFERIOR (CONTROLES Y ACCIONES)
        # ----------------------------------------------------
        frame_controles = tk.Frame(
            self.ventana, bg="#d8e2dc", pady=15, padx=15)
        frame_controles.pack(side="bottom", fill="x")

        # Columna Izquierda: Botones de Carga
        frame_botones_carga = tk.Frame(frame_controles, bg="#d8e2dc")
        frame_botones_carga.pack(side="left", padx=5)

        btn_cargar1 = tk.Button(
            frame_botones_carga,
            text="cargar imagen1",
            command=lambda: self.cargar_imagen(1),
            bg="#438a5e",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=10,
            pady=5,
            relief="raised"
        )
        btn_cargar1.pack(fill="x", pady=3)

        btn_cargar2 = tk.Button(
            frame_botones_carga,
            text="cargar imagen2",
            command=lambda: self.cargar_imagen(2),
            bg="#438a5e",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=10,
            pady=5,
            relief="raised"
        )
        btn_cargar2.pack(fill="x", pady=3)

        # Columna Central: Menús desplegables y botón Procesar
        frame_menus = tk.Frame(frame_controles, bg="#d8e2dc")
        frame_menus.pack(side="left", padx=25)

        # Etiqueta para Operaciones
        lbl_operaciones = tk.Label(frame_menus, text="Operaciones", bg="#d8e2dc", font=(
            "Arial", 10, "bold"), fg="#333333")
        lbl_operaciones.grid(row=0, column=0, padx=5, pady=4, sticky="w")

        # Opcion 1
        self.opcion1_var = tk.StringVar(value="Suma(clip)")
        operaciones1 = [
            "Suma(clip)",
            "Suma (prom)",
            "Resta(clip)",
            "Resta(prom)",
            "Resta(abs)",
            "Producto",
            "Cociente",
            "Interpolar",
            "if-darker",
            "if-lighter"
        ]
        menu_opcion1 = tk.OptionMenu(
            frame_menus, self.opcion1_var, *operaciones1)
        menu_opcion1.config(bg="white", width=12, font=("Arial", 10))
        menu_opcion1.grid(row=0, column=1, padx=5, pady=4, sticky="w")

        # Etiqueta para Formato
        lbl_formato = tk.Label(frame_menus, text="Formato", bg="#d8e2dc", font=(
            "Arial", 10, "bold"), fg="#333333")
        lbl_formato.grid(row=1, column=0, padx=5, pady=4, sticky="w")

        # Opcion 2
        self.opcion2_var = tk.StringVar(value="RGB")
        self.opcion2_var.trace_add(
            "write", lambda *args: self.actualizar_visualizacion_formatos())

        operaciones2 = [
            "RGB",
            "YIQ"
        ]
        menu_opcion2 = tk.OptionMenu(
            frame_menus, self.opcion2_var, *operaciones2)
        menu_opcion2.config(bg="white", width=12, font=("Arial", 10))
        menu_opcion2.grid(row=1, column=1, padx=5, pady=4, sticky="w")

        btn_procesar = tk.Button(
            frame_menus,
            text="procesar",
            command=self.procesar_imagenes,
            bg="#1e3d59",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=15,
            pady=8
        )
        btn_procesar.grid(row=0, column=2, rowspan=2, padx=15)

        # Columna Derecha: Guardar y Salir
        frame_acciones = tk.Frame(frame_controles, bg="#d8e2dc")
        frame_acciones.pack(side="right", padx=5)

        btn_guardar = tk.Button(
            frame_acciones,
            text="guardar",
            command=self.guardar_imagen,
            bg="#17b978",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=12,
            pady=6
        )
        btn_guardar.pack(side="left", padx=8)

        btn_salir = tk.Button(
            frame_acciones,
            text="salir",
            command=self.ventana.quit,
            bg="#ff6e40",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=12,
            pady=6
        )
        btn_salir.pack(side="left", padx=8)

        # ----------------------------------------------------
        # BARRA DE ESTADO
        # ----------------------------------------------------
        self.estado = tk.Label(
            self.ventana,
            text="Listo. Cargue las imágenes para comenzar.",
            bd=1,
            relief="sunken",
            anchor="w",
            bg="#e2e8f0",
            font=("Arial", 11)
        )
        self.estado.pack(side="bottom", fill="x")

    # ========================================================
    # MÉTODOS DE LA APLICACIÓN
    # ========================================================

    def cargar_imagen(self, numero):
        ruta = filedialog.askopenfilename(
            title=f"Seleccionar imagen {numero}",
            filetypes=[("Imágenes", "*.jpg *.jpeg *.png *.bmp *.tif *.tiff")]
        )
        if not ruta:
            return
        imagen_pil = Image.open(ruta).convert("RGB")

        # Si se carga la imagen 1 y ya existe la imagen 2, ajustamos la imagen 1
        # para que tenga exactamente las mismas dimensiones que la imagen 2.
        if numero == 1:
            if self.imagen2_data is not None:
                # obtener las dimensiones exactas (alto y ancho) de imagen2 para usarlas como referencia
                h, w, _ = self.imagen2_data.shape
                imagen_pil = imagen_pil.resize(
                    (w, h), Image.Resampling.LANCZOS)

            imagen_array = np.array(imagen_pil) / 255.0
            self.imagen1_data = imagen_array
            self.mostrar_imagen_en_label(self.imagen1_data, self.label_img1)
            self.estado.config(text="Imagen 1 cargada correctamente.")

        # Si se carga la imagen 2 y ya existe la imagen 1, ajustamos la imagen 2
        # para que tenga exactamente las mismas dimensiones que la imagen 1.
        elif numero == 2:
            if self.imagen1_data is not None:
                h, w, _ = self.imagen1_data.shape
                imagen_pil = imagen_pil.resize(
                    (w, h), Image.Resampling.LANCZOS)

            imagen_array = np.array(imagen_pil) / 255.0
            self.imagen2_data = imagen_array
            self.mostrar_imagen_en_label(self.imagen2_data, self.label_img2)
            self.estado.config(text="Imagen 2 cargada correctamente.")

    def mostrar_imagen_en_label(self, array_imagen, label_destino):
        """Muestra la imagen rellenando el contenedor fijo de manera uniforme."""
        if array_imagen is None:
            return

        # Convertimos 0-1 nuevamente a 0-255. uint8
        imagen_uint8 = (np.clip(array_imagen, 0, 1) * 255).astype(np.uint8)

        # Pillow -> Tkinter
        imagen_pil = Image.fromarray(imagen_uint8)

        # Forzar el tamaño al espacio completo del contenedor fijo (350x380 menos márgenes)
        ancho_util = 350
        alto_util = 368

        # Redimensionar ocupando toda el área disponible con alta calidad
        imagen_redimensionada = imagen_pil.resize(
            (ancho_util, alto_util), Image.Resampling.LANCZOS)

        foto = ImageTk.PhotoImage(imagen_redimensionada)

        # Guardamos la referencia.
        label_destino.foto = foto

        # Mostramos la imagen.
        label_destino.config(image=foto, text="")

    def procesar_imagenes(self):
        if self.imagen1_data is None:
            messagebox.showwarning(
                "Atención", "Debe cargar la 'imagen 1' para procesar.")
            return
        if self.imagen2_data is None:
            messagebox.showwarning(
                "Atención", "Debe cargar la 'imagen 2' para procesar.")
            return

        operacion = self.opcion1_var.get().strip()
        formato = self.opcion2_var.get().strip()

        # Validar restricción para Interpolar, if-darker y if-lighter en formato YIQ
        if (operacion == "Interpolar" or operacion == "if-darker" or operacion == "if-lighter") and formato != "RGB":
            self.estado.config(
                text=f"No esta permitida la operacion entre: (Operacion : {operacion}, Formato: {formato})")

            messagebox.showwarning(
                "Atención", f"La operación '{operacion}' solo está permitida seleccionando Formato: RGB.")
            # Limpiar la imagen procesada y su contenedor visual
            self.imagen_procesada_data = None
            self.label_procesada.config(image="", text="procesada")

            return
        resultado = self.imagen1_data.copy()

        # Conversión y procesamiento según formato seleccionado
        if formato == "YIQ":
            # img1_yiq = rgbAyiq(self.imagen1_data)
            # img2_yiq = rgbAyiq(self.imagen2_data)

            if operacion == "Suma(clip)":
                resultado_yiq = sumaClipeada(
                    self.imagen1_data, self.imagen2_data, formato)
            elif operacion == "Suma (prom)":
                resultado_yiq = sumaPromedio(
                    self.imagen1_data, self.imagen2_data, formato)
            elif operacion == "Resta(clip)":
                resultado_yiq = restaClipeada(
                    self.imagen1_data, self.imagen2_data, formato)
            elif operacion == "Resta(prom)":
                resultado_yiq = restaPromedio(
                    self.imagen1_data, self.imagen2_data, formato)
            elif operacion == "Resta(abs)":
                resultado_yiq = restaValorAbsoluto(
                    self.imagen1_data, self.imagen2_data, formato)
            elif operacion == "Producto":
                resultado_yiq = producto(
                    self.imagen1_data, self.imagen2_data, formato)
            elif operacion == "Cociente":
                resultado_yiq = cociente(
                    self.imagen1_data, self.imagen2_data, formato)

            # Asignamos resultado_yiq a resultado
            resultado = resultado_yiq

        elif formato == "RGB":
            if operacion == "Suma(clip)":
                resultado = sumaClipeada(
                    self.imagen1_data, self.imagen2_data, formato)
            elif operacion == "Suma (prom)":
                resultado = sumaPromedio(
                    self.imagen1_data, self.imagen2_data, formato)
            elif operacion == "Resta(clip)":
                resultado = restaClipeada(
                    self.imagen1_data, self.imagen2_data, formato)
            elif operacion == "Resta(prom)":
                resultado = restaPromedio(
                    self.imagen1_data, self.imagen2_data, formato)
            elif operacion == "Resta(abs)":
                resultado = restaValorAbsoluto(
                    self.imagen1_data, self.imagen2_data, formato)
            elif operacion == "Producto":
                resultado = producto(
                    self.imagen1_data, self.imagen2_data, formato)
            elif operacion == "Cociente":
                resultado = cociente(
                    self.imagen1_data, self.imagen2_data, formato)
            elif operacion == "Interpolar":
                resultado = interpolar_imagenes(
                    self.imagen1_data, self.imagen2_data)
            elif operacion == "if-darker":
                resultado = if_darker(self.imagen1_data, self.imagen2_data)
            elif operacion == "if-lighter":
                resultado = if_lighter(self.imagen1_data, self.imagen2_data)

        self.imagen_procesada_data = resultado
        self.mostrar_imagen_en_label(
            self.imagen_procesada_data, self.label_procesada)

        self.estado.config(
            text=f"Procesamiento completado (Operacion : {operacion}, Formato: {formato})")

    def guardar_imagen(self):
        if self.imagen_procesada_data is None:
            messagebox.showwarning(
                "Atención", "No hay ninguna imagen procesada para guardar.")
            return

        ruta = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG Image", "*.png"),
                       ("JPEG Image", "*.jpg"), ("All Files", "*.*")]
        )

        if not ruta:
            return

        imagen_uint8 = (np.clip(self.imagen_procesada_data,
                        0, 1) * 255).astype(np.uint8)
        imagen_pil = Image.fromarray(imagen_uint8)
        imagen_pil.save(ruta)

        messagebox.showinfo("Éxito", f"Imagen guardada con éxito en:\n{ruta}")
        self.estado.config(text=f"Imagen guardada en: {ruta}")


if __name__ == "__main__":
    ventana = tk.Tk()
    app = AppTP2(ventana)
    ventana.mainloop()

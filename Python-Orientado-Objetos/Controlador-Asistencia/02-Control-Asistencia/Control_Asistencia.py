import pandas as pd
from datetime import datetime
import numpy as np
import os
import face_recognition as fr
import cv2

# Congfiguración de rutas y listas
ruta_script = os.path.dirname(os.path.abspath(__file__))
ruta = os.path.join(ruta_script, 'Empleados')
mis_imagenes = []
nombres_empleados = []

# Filtro de seguridad para cargar solo imágenes válidas
extensiones_validas = ('.png', '.jpg', '.jpeg')
lista_empleados = [f for f in os.listdir(
    ruta) if f.lower().endswith(extensiones_validas)]

for nombre in lista_empleados:
    imagen_actual = cv2.imread(os.path.join(ruta, nombre))
    if imagen_actual is not None:
        mis_imagenes.append(imagen_actual)
        nombres_empleados.append(os.path.splitext(nombre)[0])

# Codificación de imágenes


def codificar(imagenes):
    lista_codificada = []
    for imagen in imagenes:
        imagen = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)
        codificado = fr.face_encodings(imagen)[0]
        lista_codificada.append(codificado)
    return lista_codificada


# Registro diario y acumulativo
ruta_csv = os.path.join(ruta_script, 'registro.csv')


def registrar_ingresos(persona):
    ahora = datetime.now()
    fecha_hoy = ahora.strftime('%Y-%m-%d')
    hora_actual = ahora.strftime('%H:%M:%S')

    # Si el archivo no existe, lo creamos con cabeceras
    if not os.path.exists(ruta_csv):
        with open(ruta_csv, 'w', encoding='utf-8') as f:
            f.write("Nombre,Fecha,Hora\n")

    with open(ruta_csv, 'r+', encoding='utf-8') as f:
        lineas = f.readlines()
        ya_fichado_hoy = False

        # Comprobamos si el nombre ya aparece con la fecha de hoy
        for linea in lineas:
            registro = linea.strip().split(',')
            if len(registro) >= 2:
                if registro[0] == persona and registro[1] == fecha_hoy:
                    ya_fichado_hoy = True
                    break

        # Solo registramos si es la primera vez que aparece hoy
        if not ya_fichado_hoy:
            f.write(f"{persona},{fecha_hoy},{hora_actual}\n")
            f.flush()  # Forzamos la escritura en el disco
            print(
                f"✅ REGISTRO DIARIO: {persona} ha fichado a las {hora_actual}")


# Iniciamos el sistema
lista_empleados_codificada = codificar(mis_imagenes)
captura = cv2.VideoCapture(0, cv2.CAP_DSHOW)

print("🚀 Sistema de Control de Asistencia iniciado...")

# Bucle principal de reconocimiento facial
while True:
    exito, imagen = captura.read()
    if not exito:
        break

    # Optimización: procesar a 0.25 del tamaño original
    img_pequena = cv2.resize(imagen, (0, 0), None, 0.25, 0.25)
    img_pequena = cv2.cvtColor(img_pequena, cv2.COLOR_BGR2RGB)

    caras_frame = fr.face_locations(img_pequena)
    codif_frame = fr.face_encodings(img_pequena, caras_frame)

    for caracodif, caraubic in zip(codif_frame, caras_frame):
        distancias = fr.face_distance(lista_empleados_codificada, caracodif)
        indice_coincidencia = np.argmin(distancias)
        distancia_valor = distancias[indice_coincidencia]

        # Umbral de reconocimiento: 0.6
        if distancia_valor < 0.6:
            nombre = nombres_empleados[indice_coincidencia].upper()
            color_cuadro = (0, 255, 0)  # Verde
            registrar_ingresos(nombre)
        else:
            nombre = "DESCONOCIDO"
            color_cuadro = (0, 0, 255)  # Rojo

        # Dibujar resultados (escalando x4 para volver al tamaño original)
        y1, x2, y2, x1 = [v * 4 for v in caraubic]
        cv2.rectangle(imagen, (x1, y1), (x2, y2), color_cuadro, 2)
        cv2.rectangle(imagen, (x1, y2 - 35), (x2, y2),
                      color_cuadro, cv2.FILLED)

        info_pantalla = f"{nombre} ({distancia_valor:.2f})"
        cv2.putText(imagen, info_pantalla, (x1 + 6, y2 - 10),
                    cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)

    cv2.imshow('Control de Asistencia Biometrico', imagen)

    if cv2.waitKey(1) == 27:  # Salir con ESC
        break

# Finalización y exportación de datos
captura.release()
cv2.destroyAllWindows()

try:
    # Ajustamos las columnas para el nuevo formato con Fecha
    df = pd.read_csv(ruta_csv)
    df.to_excel('Asistencia_Final.xlsx', index=False)
    print("📊 Reporte Excel 'Asistencia_Final.xlsx' generado con éxito.")
except Exception as e:
    print(f"⚠️ Error al exportar: {e}")

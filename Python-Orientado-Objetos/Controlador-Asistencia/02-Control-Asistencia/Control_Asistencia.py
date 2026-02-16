import pandas as pd
from datetime import datetime
import numpy as np
import os
import sys
import face_recognition as fr
import cv2


# crear base de datos de empleados
ruta_script = os.path.dirname(os.path.abspath(__file__))
ruta = os.path.join(ruta_script, 'Empleados')
mis_imagenes = []
nombres_empleados = []
lista_empleados = os.listdir(ruta)

for nombre in lista_empleados:
    imagen_actual = cv2.imread(os.path.join(ruta, nombre))
    mis_imagenes.append(imagen_actual)
    nombres_empleados.append(os.path.splitext(nombre)[0])

# codificar imagenes


def codificar(imagenes):

    # crear una lista nueva
    lista_codificada = []

    # pasar todas las imagenes a RGB
    for imagen in imagenes:
        imagen = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)
        # codificar
        codificado = fr.face_encodings(imagen)[0]
        # agregar a la lista
        lista_codificada.append(codificado)
    # devolver lista codificada
    return lista_codificada

# registrar los ingresos


def registrar_ingresos(persona):
    with open('registro.csv', 'a+') as f:
        f.seek(0)
        lineas = f.readlines()
        nombres_registro = [linea.split(',')[0] for linea in lineas]

        if persona not in nombres_registro:
            ahora = datetime.now()
            f.write(f"{persona},{ahora.strftime('%H:%M:%S')}\n")


lista_empleados_codificada = codificar(mis_imagenes)

# Iniciar webcam
captura = cv2.VideoCapture(0, cv2.CAP_DSHOW)

while True:
    exito, imagen = captura.read()

    # Reducir imagen para mejorar rendimiento
    img_pequena = cv2.resize(imagen, (0, 0), None, 0.25, 0.25)
    img_pequena = cv2.cvtColor(img_pequena, cv2.COLOR_BGR2RGB)

    # Localizar y codificar caras en el frame actual
    caras_frame = fr.face_locations(img_pequena)
    codif_frame = fr.face_encodings(img_pequena, caras_frame)

    for caracodif, caraubic in zip(codif_frame, caras_frame):
        distancias = fr.face_distance(lista_empleados_codificada, caracodif)
        indice_coincidencia = np.argmin(distancias)

        if distancias[indice_coincidencia] < 0.6:
            nombre = nombres_empleados[indice_coincidencia]

            # Dibujar rectángulo y nombre en la imagen
            y1, x2, y2, x1 = [v * 4 for v in caraubic]
            cv2.rectangle(imagen, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(imagen, nombre, (x1, y1 - 10),
                        cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

            registrar_ingresos(nombre)

    cv2.imshow('Control de Asistencia', imagen)

    # Cerrar con la tecla 'ESC'
    if cv2.waitKey(1) == 27:
        break

captura.release()
cv2.destroyAllWindows()

# Exportar a Excel
df = pd.read_csv('registro.csv', names=['Nombre', 'Hora_Ingreso'])
df.to_excel('Asistencia_Final.xlsx', index=False)

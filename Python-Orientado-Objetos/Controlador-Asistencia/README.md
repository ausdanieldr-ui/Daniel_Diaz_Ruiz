## 👤 Sistema de Asistencia por Biometría Facial

Un sistema avanzado de **Visión Artificial** capaz de identificar personas en tiempo real a través de una webcam y registrar su asistencia de forma automática en una base de datos local (CSV).

### 🛠️ Tecnologías y Herramientas
<p align="left">
  <img src="https://skillicons.dev/icons?i=py,vscode,r,mssql,opencv" />
</p>

### 🌟 Funcionalidades Principales
* **Procesamiento de Imágenes:** Conversión de imágenes a espacio de color RGB y codificación de 128 puntos faciales únicos.
* **Reconocimiento en Tiempo Real:** Captura de video mediante webcam para detectar y comparar rostros con una base de datos de empleados existente.
* **Cálculo de Distancia Facial:** Utiliza algoritmos de comparación para determinar el nivel de coincidencia y evitar falsos positivos.
* **Registro Automatizado:** Si el rostro es reconocido, el sistema verifica si ya ha fichado y registra el nombre junto con la hora exacta en un archivo `registro.csv`.

### 📂 Lógica del Proyecto
1.  **Carga de Base de Datos:** El script escanea la carpeta `/empleados` y genera los encodings de cada fotografía de forma masiva.
2.  **Detección:** Se localizan los rostros en el video en vivo.
3.  **Validación:** Se comparan los encodings de la cámara con los de la base de datos.
4.  **Logging:** Escritura de datos en el archivo de asistencia.

---

### 🚀 Cómo ejecutarlo
1.  Añade las fotos de las personas en la carpeta `03-biometria-facial/empleados/` (nombre_apellido.jpg).
2.  Instala las dependencias: `pip install -r requirements.txt`.
3.  Ejecuta el programa: `python 03-biometria-facial/asistencia.py`.# Controlador Aistencia con Biometría facial

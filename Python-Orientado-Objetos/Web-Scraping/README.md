# 🕸️ Web Scraping & Data Extraction

Este repositorio contiene herramientas desarrolladas en **Python** para la extracción automatizada de datos desde páginas web (Web Scraping), utilizando técnicas de parsing de HTML y navegación entre múltiples páginas.

### 🛠️ Tecnologías Utilizadas
<p align="left">
  <img src="https://skillicons.dev/icons?i=py,vscode,r,mssql" />
</p>

### 📁 Contenido del Repositorio

#### 1. Extractor Web Básico (`01-conceptos-basicos/`)
Un script introductorio que demuestra los fundamentos del scraping:
* Conexión a servidores mediante `requests`.
* Navegación por el DOM usando `BeautifulSoup`.
* Extracción de etiquetas específicas (párrafos, títulos).
* **Descarga de archivos:** Automatización de descarga de imágenes en formato binario.

#### 2. Buscador de Libros con Rating (`02-buscador-libros/`)
Un proyecto más avanzado que simula un proceso de extracción real:
* **Paginación:** Itera automáticamente a través de 10 páginas de catálogo.
* **Lógica de Filtrado:** Identifica y extrae solo los libros con una valoración de 4 o 5 estrellas.
* **Limpieza de Datos:** Almacenamiento organizado de títulos en listas de Python.

---

### 🚀 Configuración e Instalación

1. **Clonar el repositorio:**
   ```bash
   git clone [https://github.com/tu-usuario/nombre-del-repo.git](https://github.com/tu-usuario/nombre-del-repo.git)
2. **Instalar dependencias:**
   ```bash
    pip install -r requirements.txt
3. **Ejecutar los scripts:**
   ```bash
    python 02-buscador-libros/buscador_libros.py

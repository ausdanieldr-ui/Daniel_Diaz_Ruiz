# 🛡️ Detección de Cyberbullying: End-to-End ML Pipeline

Este módulo implementa una solución profesional de **Procesamiento de Lenguaje Natural (NLP)** para la clasificación de contenido ofensivo. El sistema evoluciona desde modelos estadísticos clásicos (Logistic Regression, SVM) hasta arquitecturas de vanguardia en **Deep Learning** como **DistilBERT**.

---

## 🏗️ Arquitectura del Proyecto (Clean Architecture)

El proyecto ha sido estructurado siguiendo estándares de **ML Engineering** para garantizar la modularidad, escalabilidad y reproducibilidad del código.

* **`src/` (Source Code):** Núcleo del proyecto. Contiene la lógica modular para el entrenamiento (`train.py`), la inferencia (`predict.py`) y el preprocesamiento de datos (`clean_data.py`).
* **`models/` (Artifacts):** Repositorio central donde se almacenan los modelos entrenados en formatos `.joblib` y `.pkl`.
* **`data/` (Data Management):** Organización jerárquica con separación estricta entre datos crudos (`raw/`) y datos procesados (`processed/`).
* **`notebooks/` (Experimentation):** Entorno dedicado a la investigación, Análisis Exploratorio de Datos (EDA) y prototipado rápido.
* **`docs/` (Documentation):** Contiene los reportes técnicos y la base teórica del proyecto.

---

## 🚀 Uso y Automatización

El sistema está diseñado para ser operado mediante **interfaces de línea de comandos (CLI)**, lo que facilita su integración en flujos de trabajo automatizados.

### 1. Entrenamiento de Modelos
El script permite entrenar modelos específicos o ejecutar el pipeline completo de forma masiva:

* #### Entrenar todos los modelos del pipeline
python src/train.py --model all

* #### Entrenar específicamente DistilBERT
python src/train.py --model DistilBERT --retrain

### 2. Inferencia (Predicción)
Interfaz limpia para clasificar nuevos textos en tiempo real:

* #### Clasificar un texto de forma directa
python src/predict.py "ejemplo de texto" --model "Logistic Regression"





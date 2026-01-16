import os
import argparse
import joblib
import pandas as pd
import numpy as np


def predict_text(text, model_name="Logistic Regression", models_dir="models"):
    """
    Predice la categoría de ciberbullying para un texto dado usando un modelo clásico.
    """
    # Ajustar nombre de carpeta (espacios a guiones bajos)
    model_folder = model_name.replace(" ", "_")
    base_path = os.path.join(models_dir, model_folder)

    model_path = os.path.join(base_path, "model.joblib")
    vectorizer_path = os.path.join(base_path, "vectorizer.joblib")
    encoder_path = os.path.join(base_path, "encoder.joblib")

    # Verificar existencia
    if not os.path.exists(model_path):
        print(
            f"Error: No se encontró el modelo en {base_path}. Ejecute train.py primero.")
        return

    try:
        # Cargar artefactos
        print(f"Cargando modelo {model_name}...")
        model = joblib.load(model_path)
        vectorizer = joblib.load(vectorizer_path)
        encoder = joblib.load(encoder_path)

        # Preprocesamiento (Vectorización)
        # Nota: Aquí deberías aplicar la misma limpieza que en el training si no está incluida en el vectorizador.
        # Asumimos que el texto entra limpio o el vectorizador maneja lo básico.
        text_vec = vectorizer.transform([text])

        # Predicción
        pred_idx = model.predict(text_vec)
        pred_label = encoder.inverse_transform(pred_idx)[0]

        probs = model.predict_proba(text_vec)
        confidence = np.max(probs)

        return pred_label, confidence

    except Exception as e:
        print(f"Error en predicción: {e}")
        return None, 0.0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Script de Predicción Cyberbullying")
    parser.add_argument('text', type=str, help='Texto a analizar', nargs='?')
    parser.add_argument(
        '--model', type=str, default='Logistic Regression', help='Nombre del modelo a usar')

    args = parser.parse_args()

    if args.text:
        label, conf = predict_text(args.text, args.model)
        print(f"\nTexto: {args.text}")
        print(f"Predicción: {label} (Confianza: {conf:.2f})")
    else:
        print("Modo Interactivo (Escribe 'salir' para terminar)")
        while True:
            text = input("\nIngresa texto: ")
            if text.lower() == 'salir':
                break
            label, conf = predict_text(text, args.model)
            if label:
                print(f"Predicción: {label} (Confianza: {conf:.2f})")

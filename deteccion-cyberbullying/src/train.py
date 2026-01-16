from cyberbullying_dl import run_pipeline as run_dl
from cyberbullying_transformers import run_pipeline as run_transformer
from cyberbullying_classical import run_pipeline as run_classical
from cyberbullying_DistilBert import run_pipeline as run_distilbert
import os
import sys
import argparse
import pandas as pd
import warnings

# Suprimir advertencias
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
warnings.filterwarnings('ignore')

# Importar modelos (asumiendo que están en el mismo directorio src/)

# Configuración
DEFAULT_DATASET = os.path.join(
    "data", "processed", "dataset_bullying_final.csv")
MODELS_DIR = "models"
RESULTS_DIR = "results"


def run_training_pipeline(model_name, dataset_file, force_retrain=False):
    text_col = 'text'  # Ajustar según dataset_bullying_final.csv
    label_col = 'label'
    use_saved = not force_retrain

    # Crear directorios si no existen
    os.makedirs(MODELS_DIR, exist_ok=True)
    os.makedirs(RESULTS_DIR, exist_ok=True)

    print(f"Iniciando entrenamiento/evaluación para: {model_name}")

    try:
        if model_name == 'DistilBERT':
            run_distilbert(dataset_file, text_col, label_col,
                           model_dir=os.path.join(MODELS_DIR, "DistilBERT"),
                           output_image_dir=os.path.join(
                               RESULTS_DIR, "DistilBERT"),
                           use_saved=use_saved)

        elif model_name in ['RoBERTa', 'BERTweet']:
            run_transformer(model_name.lower(), dataset_file, text_col, label_col,
                            output_image_dir=os.path.join(
                                RESULTS_DIR, model_name),
                            use_saved=use_saved)

        elif model_name in ['LSTM', 'Bi-LSTM', 'CNN']:
            run_dl(model_name, dataset_file, text_col, label_col,
                   output_image_dir=os.path.join(RESULTS_DIR, model_name),
                   use_saved=use_saved)

        else:  # Clásicos
            # Lista de clásicos soportados
            classics = ['Naive Bayes', 'Logistic Regression',
                        'SVM', 'Random Forest', 'XGBoost', 'LightGBM']
            if model_name in classics:
                run_classical(model_name, dataset_file, text_col, label_col,
                              model_dir_base=MODELS_DIR,
                              output_image_dir=os.path.join(
                                  RESULTS_DIR, model_name.replace(" ", "_")),
                              use_saved=use_saved)
            else:
                print(f"Modelo {model_name} no reconocido.")

    except Exception as e:
        print(f"Error entrenando {model_name}: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Script de Entrenamiento Cyberbullying")
    parser.add_argument('--model', type=str, default='all',
                        help='Nombre del modelo a entrenar o "all"')
    parser.add_argument('--dataset', type=str,
                        default=DEFAULT_DATASET, help='Ruta al dataset')
    parser.add_argument('--retrain', action='store_true',
                        help='Forzar re-entrenamiento ignorando guardados')

    args = parser.parse_args()

    if args.model == 'all':
        # Lista definida de modelos prioritarios
        models_to_run = ['Logistic Regression', 'DistilBERT',
                         'Bi-LSTM']  # Ejemplo reducido o completo
        print("Ejecutando todos los modelos definidos...")
        for m in models_to_run:
            run_training_pipeline(m, args.dataset, args.retrain)
    else:
        run_training_pipeline(args.model, args.dataset, args.retrain)

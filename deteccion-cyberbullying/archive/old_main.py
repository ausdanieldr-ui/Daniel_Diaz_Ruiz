import os
import sys
import time
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings

# Suprimir advertencias de TensorFlow y oneDNN
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
warnings.filterwarnings('ignore')

# Importar modelos
from cyberbullying_DistilBert import run_pipeline as run_distilbert
from cyberbullying_classical import run_pipeline as run_classical
from cyberbullying_transformers import run_pipeline as run_transformer
from cyberbullying_dl import run_pipeline as run_dl

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def run_all_models(dataset_file, text_col, label_col, base_image_dir, force_retrain=False):
    """Ejecuta todos los modelos y genera una comparativa, con capacidad de reanudación."""
    comparison_dir = os.path.join(base_image_dir, "COMPARATIVA_FINAL")
    if not os.path.exists(comparison_dir):
        os.makedirs(comparison_dir)
    
    csv_path = os.path.join(comparison_dir, "resultados_comparativos.csv")
    use_saved = not force_retrain

    # Definición de tareas
    tasks = [
        ('DistilBERT', lambda: run_distilbert(dataset_file, text_col, label_col, model_dir="./modelo_ciberbullying_distilbert", output_image_dir=os.path.join(base_image_dir, "DistilBERT"), use_saved=use_saved)),
        ('RoBERTa', lambda: run_transformer('roberta', dataset_file, text_col, label_col, output_image_dir=os.path.join(base_image_dir, "RoBERTa"), use_saved=use_saved)),
        ('BERTweet', lambda: run_transformer('bertweet', dataset_file, text_col, label_col, output_image_dir=os.path.join(base_image_dir, "BERTweet"), use_saved=use_saved)),
        ('LSTM', lambda: run_dl('LSTM', dataset_file, text_col, label_col, output_image_dir=os.path.join(base_image_dir, "LSTM"), use_saved=use_saved)),
        ('Bi-LSTM', lambda: run_dl('Bi-LSTM', dataset_file, text_col, label_col, output_image_dir=os.path.join(base_image_dir, "Bi-LSTM"), use_saved=use_saved)),
        ('CNN', lambda: run_dl('CNN', dataset_file, text_col, label_col, output_image_dir=os.path.join(base_image_dir, "CNN"), use_saved=use_saved)),
        ('Naive Bayes', lambda: run_classical('Naive Bayes', dataset_file, text_col, label_col, output_image_dir=os.path.join(base_image_dir, "Naive_Bayes"), use_saved=use_saved)),
        ('Logistic Regression', lambda: run_classical('Logistic Regression', dataset_file, text_col, label_col, output_image_dir=os.path.join(base_image_dir, "Logistic_Regression"), use_saved=use_saved)),
        ('SVM', lambda: run_classical('SVM', dataset_file, text_col, label_col, output_image_dir=os.path.join(base_image_dir, "SVM"), use_saved=use_saved)),
        ('Random Forest', lambda: run_classical('Random Forest', dataset_file, text_col, label_col, output_image_dir=os.path.join(base_image_dir, "Random_Forest"), use_saved=use_saved)),
        ('XGBoost', lambda: run_classical('XGBoost', dataset_file, text_col, label_col, output_image_dir=os.path.join(base_image_dir, "XGBoost"), use_saved=use_saved)),
        ('LightGBM', lambda: run_classical('LightGBM', dataset_file, text_col, label_col, output_image_dir=os.path.join(base_image_dir, "LightGBM"), use_saved=use_saved)),
    ]

    results = []
    executed_models = set()

    # Verificar si existe un archivo de resultados previo para reanudar
    if os.path.exists(csv_path):
        try:
            df_existing = pd.read_csv(csv_path)
            if not df_existing.empty and 'Modelo' in df_existing.columns:
                executed_models = set(df_existing['Modelo'].tolist())
                print(f"\n⚠️ Se encontró una ejecución previa con {len(executed_models)} modelos procesados.")
                print(f"Modelos completados: {', '.join(executed_models)}")
                
                if len(executed_models) < len(tasks):
                    resp = input("¿Desea continuar desde donde se quedó? (s/n): ").lower().strip()
                    if resp == 's':
                        results = df_existing.to_dict('records')
                        print("🔄 Reanudando ejecución...")
                    else:
                        print("🔄 Reiniciando ejecución desde cero...")
                        executed_models = set()
                else:
                    print("✅ Todos los modelos parecen haber sido ejecutados anteriormente.")
                    resp = input("¿Desea volver a ejecutarlos todos? (s/n): ").lower().strip()
                    if resp != 's':
                        print("Mostrando resultados existentes...")
                        results = df_existing.to_dict('records')
                        # Saltar al final para graficar
                        executed_models = set(t[0] for t in tasks) 
                    else:
                        executed_models = set()
        except Exception as e:
            print(f"⚠️ Error leyendo archivo previo: {e}. Se iniciará desde cero.")

    print("\n🚀 INICIANDO EJECUCIÓN MASIVA DE TODOS LOS MODELOS...")
    print("Esto puede tomar bastante tiempo. Por favor espere.\n")

    for name, func in tasks:
        if name in executed_models:
            print(f"⏩ Saltando {name} (ya procesado).")
            continue

        print(f"\n>>> Ejecutando {name}...")
        start_time = time.time()
        try:
            acc = func()
            elapsed_time = time.time() - start_time
            results.append({'Modelo': name, 'Accuracy': acc, 'Tiempo (s)': elapsed_time})
            print(f"✅ {name} finalizado. Acc: {acc:.4f}, Tiempo: {elapsed_time:.2f}s")
            
            # Guardado incremental para seguridad
            pd.DataFrame(results).to_csv(csv_path, index=False)
            
        except Exception as e:
            print(f"❌ Error en {name}: {e}")
            results.append({'Modelo': name, 'Accuracy': 0.0, 'Tiempo (s)': 0.0})
            pd.DataFrame(results).to_csv(csv_path, index=False)

    # Generar DataFrame y Gráficos
    if not results:
        print("No hay resultados para mostrar.")
        return

    df_res = pd.DataFrame(results)
    print("\n--- RESULTADOS FINALES ---")
    print(df_res)
    
    # Guardar CSV Final
    df_res.to_csv(csv_path, index=False)

    # Gráfico de Accuracy
    plt.figure(figsize=(12, 6))
    sns.barplot(x='Accuracy', y='Modelo', data=df_res.sort_values('Accuracy', ascending=False), palette='viridis')
    plt.title('Comparativa de Accuracy por Modelo')
    plt.xlim(0, 1.0)
    plt.tight_layout()
    plt.savefig(os.path.join(comparison_dir, "comparativa_accuracy.png"))
    plt.close()

    # Gráfico de Tiempo
    plt.figure(figsize=(12, 6))
    sns.barplot(x='Tiempo (s)', y='Modelo', data=df_res.sort_values('Tiempo (s)', ascending=True), palette='magma')
    plt.title('Comparativa de Tiempo de Ejecución (s)')
    plt.tight_layout()
    plt.savefig(os.path.join(comparison_dir, "comparativa_tiempo.png"))
    plt.close()

    print(f"\n✅ Estudio comparativo guardado en: {comparison_dir}")

def main_menu():
    # ==========================================
    # CONFIGURACIÓN GLOBAL
    # ==========================================
    DATASET_FILE = '../Dataset/tweets_trad.csv'
    TEXT_COLUMN = 'texto_traducido'
    LABEL_COLUMN = 'cyberbullying_type'
    BASE_IMAGE_DIR = "./images"
    
    # Asegurar que el directorio base de imágenes existe
    if not os.path.exists(BASE_IMAGE_DIR):
        os.makedirs(BASE_IMAGE_DIR)

    force_retrain = False

    while True:
        clear_screen()
        print("==================================================")
        print("   SISTEMA DE CLASIFICACIÓN DE CIBERBULLYING")
        print("==================================================")
        print(f"MODO ACTUAL: {'🔄 RE-ENTRENAR (Ignorar guardados)' if force_retrain else '💾 USAR GUARDADOS (Si existen)'}")
        print("--------------------------------------------------")
        print("Seleccione el modelo que desea ejecutar:")
        print("")
        print("--- Transformers (Hugging Face) ---")
        print("1. DistilBERT")
        print("2. RoBERTa")
        print("3. BERTweet")
        print("")
        print("--- Deep Learning (PyTorch) ---")
        print("4. LSTM")
        print("5. Bi-LSTM")
        print("6. CNN")
        print("")
        print("--- Machine Learning Clásico ---")
        print("7. Naive Bayes (MultinomialNB)")
        print("8. Logistic Regression")
        print("9. SVM")
        print("10. Random Forest")
        print("11. XGBoost")
        print("12. LightGBM")
        print("")
        print("--- Opciones ---")
        print("99. CAMBIAR MODO (Usar Guardados / Re-entrenar)")
        print("100. EJECUTAR TODOS Y COMPARAR")
        print("")
        print("0. Salir")
        print("==================================================")
        
        choice = input("Opción: ")
        
        use_saved = not force_retrain

        try:
            if choice == '1':
                print("\nEjecutando DistilBERT...")
                run_distilbert(DATASET_FILE, TEXT_COLUMN, LABEL_COLUMN, 
                             model_dir="./modelo_ciberbullying_distilbert", 
                             output_image_dir=os.path.join(BASE_IMAGE_DIR, "DistilBERT"),
                             use_saved=use_saved)
            
            elif choice == '2':
                print("\nEjecutando RoBERTa...")
                run_transformer('roberta', DATASET_FILE, TEXT_COLUMN, LABEL_COLUMN, 
                              output_image_dir=os.path.join(BASE_IMAGE_DIR, "RoBERTa"),
                              use_saved=use_saved)
                
            elif choice == '3':
                print("\nEjecutando BERTweet...")
                run_transformer('bertweet', DATASET_FILE, TEXT_COLUMN, LABEL_COLUMN, 
                              output_image_dir=os.path.join(BASE_IMAGE_DIR, "BERTweet"),
                              use_saved=use_saved)
            
            elif choice in ['4', '5', '6']:
                models = {'4': 'LSTM', '5': 'Bi-LSTM', '6': 'CNN'}
                model_name = models[choice]
                print(f"\nEjecutando {model_name}...")
                run_dl(model_name, DATASET_FILE, TEXT_COLUMN, LABEL_COLUMN, 
                       output_image_dir=os.path.join(BASE_IMAGE_DIR, model_name),
                       use_saved=use_saved)
                
            elif choice in ['7', '8', '9', '10', '11', '12']:
                models = {
                    '7': 'Naive Bayes', '8': 'Logistic Regression', '9': 'SVM',
                    '10': 'Random Forest', '11': 'XGBoost', '12': 'LightGBM'
                }
                model_name = models[choice]
                print(f"\nEjecutando {model_name}...")
                run_classical(model_name, DATASET_FILE, TEXT_COLUMN, LABEL_COLUMN, 
                            output_image_dir=os.path.join(BASE_IMAGE_DIR, model_name.replace(" ", "_")),
                            use_saved=use_saved)
            
            elif choice == '99':
                force_retrain = not force_retrain
                print(f"\nModo cambiado a: {'RE-ENTRENAR' if force_retrain else 'USAR GUARDADOS'}")

            elif choice == '100':
                run_all_models(DATASET_FILE, TEXT_COLUMN, LABEL_COLUMN, BASE_IMAGE_DIR, force_retrain=force_retrain)

            elif choice == '0':
                print("\nSaliendo del sistema...")
                break
            else:
                print("\nOpción no válida.")
                
            input("\nPresione Enter para continuar...")
            
        except Exception as e:
            print(f"\n❌ Error durante la ejecución: {e}")
            input("\nPresione Enter para continuar...")

if __name__ == "__main__":
    main_menu()

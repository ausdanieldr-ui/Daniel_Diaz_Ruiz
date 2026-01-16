import pandas as pd
import numpy as np
import os
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, label_binarize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, roc_curve, auc, precision_recall_curve, average_precision_score
from itertools import cycle
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier

def get_model(model_name, num_labels):
    """Retorna la instancia del modelo según el nombre."""
    if model_name == 'Naive Bayes':
        return MultinomialNB()
    elif model_name == 'Logistic Regression':
        return LogisticRegression(max_iter=1000)
    elif model_name == 'SVM':
        return SVC(probability=True)
    elif model_name == 'Random Forest':
        # Reducimos profundidad y estimadores para evitar overfitting y lentitud en alta dimensionalidad
        return RandomForestClassifier(n_estimators=100, max_depth=20, n_jobs=-1)
    elif model_name == 'XGBoost':
        return XGBClassifier(use_label_encoder=False, eval_metric='mlogloss', n_jobs=-1)
    elif model_name == 'LightGBM':
        return LGBMClassifier(n_jobs=-1, verbose=-1)
    else:
        raise ValueError(f"Modelo desconocido: {model_name}")

def run_pipeline(model_name, csv_path, text_col, label_col, model_dir_base="./modelos_clasicos", use_saved=True, output_image_dir="."):
    print(f"\n--- Iniciando Pipeline para {model_name} ---")
    
    # Directorio específico para este modelo
    model_dir = os.path.join(model_dir_base, model_name.replace(" ", "_"))
    if not os.path.exists(model_dir):
        os.makedirs(model_dir)
        
    model_path = os.path.join(model_dir, "model.joblib")
    vectorizer_path = os.path.join(model_dir, "vectorizer.joblib")
    encoder_path = os.path.join(model_dir, "encoder.joblib")

    # 1. Carga de Datos
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"No se encuentra el archivo: {csv_path}")
        
    print("Cargando dataset...")
    df = pd.read_csv(csv_path)
    df = df.dropna(subset=[text_col, label_col])
    
    # Codificación de etiquetas
    le = LabelEncoder()
    df['label_encoded'] = le.fit_transform(df[label_col])
    label_map = dict(zip(le.classes_, range(len(le.classes_))))
    print("Mapeo de etiquetas:", label_map)
    
    texts = df[text_col].tolist()
    labels = df['label_encoded'].tolist()
    
    # División Train/Test
    X_train_raw, X_test_raw, y_train, y_test = train_test_split(
        texts, labels, test_size=0.2, random_state=42, stratify=labels
    )
    
    # 2. Vectorización (TF-IDF)
    # Para modelos de árboles (RF, XGB, LGBM) limitamos features para controlar dimensionalidad
    max_features = 5000 if model_name in ['Random Forest', 'XGBoost', 'LightGBM'] else 10000
    
    if use_saved and os.path.exists(vectorizer_path):
        print("Cargando vectorizador guardado...")
        vectorizer = joblib.load(vectorizer_path)
        X_train = vectorizer.transform(X_train_raw)
        X_test = vectorizer.transform(X_test_raw)
    else:
        print(f"Entrenando vectorizador (max_features={max_features})...")
        vectorizer = TfidfVectorizer(max_features=max_features, stop_words='english')
        X_train = vectorizer.fit_transform(X_train_raw)
        X_test = vectorizer.transform(X_test_raw)
        joblib.dump(vectorizer, vectorizer_path)
        joblib.dump(le, encoder_path)

    # 3. Modelo
    model = None
    if use_saved and os.path.exists(model_path):
        print(f"Cargando modelo guardado desde {model_path}...")
        try:
            model = joblib.load(model_path)
        except Exception as e:
            print(f"Error cargando modelo: {e}")
            
    if model is None:
        print(f"Entrenando {model_name}...")
        model = get_model(model_name, len(label_map))
        model.fit(X_train, y_train)
        print(f"Guardando modelo en {model_path}...")
        joblib.dump(model, model_path)
        
    # 4. Evaluación
    print("\n--- Evaluación ---")
    # Convertir explícitamente a array numpy para satisfacer al linter y asegurar compatibilidad
    y_pred = np.array(model.predict(X_test))
    
    acc = accuracy_score(y_test, y_pred)
    print(f"Accuracy: {acc:.4f}")
    
    target_names = [k for k, v in sorted(label_map.items(), key=lambda item: item[1])]
    print("\nReporte de Clasificación:")
    print(classification_report(y_test, y_pred, target_names=target_names))
    
    # 5. Gráficos
    print("\nGenerando gráficos...")
    labels_indices = [v for k, v in sorted(label_map.items(), key=lambda item: item[1])]
    
    cm = confusion_matrix(y_test, y_pred, labels=labels_indices)
    
    plt.figure(figsize=(10, 8))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Greens', 
                xticklabels=target_names, 
                yticklabels=target_names)
    plt.title(f'Matriz de Confusión - {model_name}')
    plt.xlabel('Predicción')
    plt.ylabel('Realidad')
    
    if not os.path.exists(output_image_dir):
        os.makedirs(output_image_dir)
        
    plot_filename = os.path.join(output_image_dir, f"confusion_matrix_{model_name.replace(' ', '_')}.png")
    plt.savefig(plot_filename)
    print(f"✅ Gráfico guardado como '{plot_filename}'")
    plt.close()

    # --- Gráficos Adicionales ---
    
    # 1. Matriz de Confusión Normalizada
    cm_normalized = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
    plt.figure(figsize=(10, 8))
    sns.heatmap(cm_normalized, annot=True, fmt='.2f', cmap='Greens', 
                xticklabels=target_names, 
                yticklabels=target_names)
    plt.title(f'Matriz de Confusión Normalizada - {model_name}')
    plt.xlabel('Predicción')
    plt.ylabel('Realidad')
    plt.savefig(os.path.join(output_image_dir, f"confusion_matrix_normalized_{model_name.replace(' ', '_')}.png"))
    plt.close()

    # Obtener probabilidades para curvas ROC/PR
    try:
        if hasattr(model, "predict_proba"):
            y_score = model.predict_proba(X_test)
        else:
            # Para modelos que no tienen predict_proba (ej. SVM sin probability=True, aunque aquí lo forzamos)
            # O si falla por alguna razón
            y_score = None
            print(f"⚠️ El modelo {model_name} no soporta predict_proba o falló. Saltando curvas ROC/PR.")
    except Exception as e:
        y_score = None
        print(f"⚠️ Error obteniendo probabilidades: {e}")

    if y_score is not None:
        n_classes = len(label_map)
        y_test_bin = label_binarize(y_test, classes=list(range(n_classes)))
        
        # 2. Curva ROC (Macro-Average)
        fpr = dict()
        tpr = dict()
        roc_auc = dict()
        for i in range(n_classes):
            fpr[i], tpr[i], _ = roc_curve(y_test_bin[:, i], y_score[:, i])
            roc_auc[i] = auc(fpr[i], tpr[i])

        # Compute micro-average ROC curve and ROC area
        fpr["micro"], tpr["micro"], _ = roc_curve(y_test_bin.ravel(), y_score.ravel())
        roc_auc["micro"] = auc(fpr["micro"], tpr["micro"])

        # Compute macro-average ROC curve and ROC area
        all_fpr = np.unique(np.concatenate([fpr[i] for i in range(n_classes)]))
        mean_tpr = np.zeros_like(all_fpr)
        for i in range(n_classes):
            mean_tpr += np.interp(all_fpr, fpr[i], tpr[i])
        mean_tpr /= n_classes
        fpr["macro"] = all_fpr
        tpr["macro"] = mean_tpr
        roc_auc["macro"] = auc(fpr["macro"], tpr["macro"])

        plt.figure(figsize=(10, 8))
        plt.plot(fpr["micro"], tpr["micro"],
                 label='micro-average ROC curve (area = {0:0.2f})'.format(roc_auc["micro"]),
                 color='deeppink', linestyle=':', linewidth=4)

        plt.plot(fpr["macro"], tpr["macro"],
                 label='macro-average ROC curve (area = {0:0.2f})'.format(roc_auc["macro"]),
                 color='navy', linestyle=':', linewidth=4)

        colors = cycle(['aqua', 'darkorange', 'cornflowerblue', 'green', 'red', 'purple'])
        for i, color in zip(range(n_classes), colors):
            plt.plot(fpr[i], tpr[i], color=color, lw=2,
                     label='ROC curve of class {0} (area = {1:0.2f})'.format(target_names[i], roc_auc[i]))

        plt.plot([0, 1], [0, 1], 'k--', lw=2)
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title(f'Receiver Operating Characteristic (ROC) - {model_name}')
        plt.legend(loc="lower right")
        plt.savefig(os.path.join(output_image_dir, f"roc_curve_{model_name.replace(' ', '_')}.png"))
        plt.close()
        
        # 3. Curva Precision-Recall (Macro-Average)
        precision = dict()
        recall = dict()
        average_precision = dict()
        for i in range(n_classes):
            precision[i], recall[i], _ = precision_recall_curve(y_test_bin[:, i], y_score[:, i])
            average_precision[i] = average_precision_score(y_test_bin[:, i], y_score[:, i])

        # A "micro-average": quantifying score on all classes jointly
        precision["micro"], recall["micro"], _ = precision_recall_curve(y_test_bin.ravel(), y_score.ravel())
        average_precision["micro"] = average_precision_score(y_test_bin, y_score, average="micro")

        plt.figure(figsize=(10, 8))
        plt.step(recall['micro'], precision['micro'], where='post',
                 label='micro-average PR (AP = {0:0.2f})'.format(average_precision["micro"]))
        
        for i, color in zip(range(n_classes), colors):
            plt.plot(recall[i], precision[i], color=color, lw=2,
                     label='PR curve of class {0} (AP = {1:0.2f})'.format(target_names[i], average_precision[i]))
            
        plt.xlabel('Recall')
        plt.ylabel('Precision')
        plt.ylim([0.0, 1.05])
        plt.xlim([0.0, 1.0])
        plt.title(f'Precision-Recall Curve - {model_name}')
        plt.legend(loc="lower left")
        plt.savefig(os.path.join(output_image_dir, f"pr_curve_{model_name.replace(' ', '_')}.png"))
        plt.close()
    
    return acc

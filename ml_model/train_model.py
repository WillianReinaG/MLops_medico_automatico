"""
Modelo ML para predicción de enfermedades basado en síntomas
Utiliza RandomForest y TfidfVectorizer para clasificación
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder
import joblib
import os
from datetime import datetime

# Dataset de síntomas y enfermedades
SYMPTOM_DISEASE_DATA = {
    'symptoms': [
        'fiebre dolor cabeza cuerpo',
        'tos seca fiebre respiracion',
        'dolor pecho respiracion dificultad',
        'dolor garganta fiebre inflamacion',
        'nausea vomito diarrea dolor abdomen',
        'mareo vertigo vision borrosa',
        'presion alta dolor cabeza palpitaciones',
        'presion baja mareo fatiga debilidad',
        'erupcion piel picazon inflamacion',
        'dolor articulaciones inflamacion rigidez',
        'fiebre escalofrios debilidad dolor',
        'congestion nasal estornudos goteo nasal',
        'dificultad respirar sibilancias opresion pecho',
        'dolor oido audiencia reducida inflamacion',
        'cambios vision dolor ojo enrojecimiento',
    ],
    'disease': [
        'Gripe/Influenza',
        'Bronquitis',
        'Neumonía',
        'Faringitis',
        'Gastroenteritis',
        'Mareos/Vértigo',
        'Hipertensión',
        'Hipotensión',
        'Dermatitis/Alergia',
        'Artritis',
        'Infección Viral',
        'Resfriado Común',
        'Asma',
        'Otitis',
        'Conjuntivitis',
    ],
    'exam_needed': [
        True, True, True, False, True, True, False, False, False, False,
        True, False, True, False, False
    ],
    'severity': [
        'Moderada', 'Moderada', 'Alta', 'Leve', 'Moderada', 'Leve',
        'Alta', 'Leve', 'Leve', 'Moderada', 'Moderada', 'Leve', 'Alta', 'Leve', 'Leve'
    ]
}

# Medicamentos por enfermedad
MEDICATIONS = {
    'Gripe/Influenza': [
        'Ibuprofeno 400mg cada 6 horas',
        'Paracetamol 500mg cada 8 horas',
        'Oseltamivir 75mg cada 12 horas'
    ],
    'Bronquitis': [
        'Bromexina 8mg cada 8 horas',
        'Amoxicilina 500mg cada 8 horas',
        'Guaifenesina expectorante'
    ],
    'Neumonía': [
        'Azitromicina 500mg día 1, luego 250mg',
        'Ceftriaxona 1g cada 12 horas',
        'Paracetamol para la fiebre'
    ],
    'Faringitis': [
        'Ibuprofeno 400mg cada 6 horas',
        'Amoxicilina 500mg cada 8 horas',
        'Pastillas para la garganta'
    ],
    'Gastroenteritis': [
        'Metoclopramida 10mg cada 8 horas',
        'Loperamida si hay diarrea',
        'Rehidratación oral'
    ],
    'Mareos/Vértigo': [
        'Meclozina 25mg cada 8 horas',
        'Dimenhidrinato 50mg cada 6 horas',
        'Ejercicios de equilibrio'
    ],
    'Hipertensión': [
        'Losartán 50mg diarios',
        'Metoprolol 100mg diarios',
        'Control de dieta baja en sodio'
    ],
    'Hipotensión': [
        'Aumentar ingesta de líquidos y sal',
        'Midodrina 5mg cada 8 horas',
        'Ejercicio regular'
    ],
    'Dermatitis/Alergia': [
        'Hidrocortisona crema 1% cada 12 horas',
        'Cetirizina 10mg diarios',
        'Loción humectante'
    ],
    'Artritis': [
        'Ibuprofeno 400mg cada 6 horas',
        'Metotrexato bajo supervisión',
        'Fisioterapia'
    ],
    'Infección Viral': [
        'Paracetamol 500mg cada 8 horas',
        'Ibuprofen 400mg cada 6 horas',
        'Descanso y líquidos'
    ],
    'Resfriado Común': [
        'Vitamina C 500mg diarios',
        'Paracetamol para síntomas',
        'Descanso'
    ],
    'Asma': [
        'Salbutamol inhalador PRN',
        'Fluticasona inhalador diario',
        'Montelukast 10mg nocturnos'
    ],
    'Otitis': [
        'Amoxicilina 500mg cada 8 horas',
        'Gotas óticas con anestésico',
        'Ibuprofeno para el dolor'
    ],
    'Conjuntivitis': [
        'Gotas oftalmológicas antibióticas',
        'Compresas frías',
        'Higiene ocular'
    ]
}

def create_dataset():
    """Crear dataset de entrenamiento"""
    df = pd.DataFrame(SYMPTOM_DISEASE_DATA)
    return df

def train_model():
    """Entrenar el modelo de predicción"""
    df = create_dataset()
    
    # Pipeline con vectorización y clasificador
    model = Pipeline([
        ('tfidf', TfidfVectorizer(max_features=100, lowercase=True)),
        ('clf', RandomForestClassifier(n_estimators=100, random_state=42, max_depth=10))
    ])
    
    X = df['symptoms']
    y = df['disease']
    
    # Entrenar modelo
    model.fit(X, y)
    
    # Crear diccionarios para mapeos
    disease_info = {}
    for idx, row in df.iterrows():
        disease = row['disease']
        disease_info[disease] = {
            'exam_needed': bool(row['exam_needed']),
            'severity': row['severity'],
            'medications': MEDICATIONS.get(disease, [])
        }
    
    return model, disease_info

def save_model(model, disease_info, save_path='models'):
    """Guardar modelo entrenado"""
    os.makedirs(save_path, exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    model_path = os.path.join(save_path, f'disease_model_{timestamp}.pkl')
    info_path = os.path.join(save_path, f'disease_info_{timestamp}.pkl')
    
    joblib.dump(model, model_path)
    joblib.dump(disease_info, info_path)
    
    # Guardar también versión 'latest'
    joblib.dump(model, os.path.join(save_path, 'disease_model_latest.pkl'))
    joblib.dump(disease_info, os.path.join(save_path, 'disease_info_latest.pkl'))
    
    print(f"Modelo guardado en: {model_path}")
    print(f"Info guardada en: {info_path}")
    
    return model_path, info_path

def load_model(save_path='models'):
    """Cargar modelo entrenado"""
    model_path = os.path.join(save_path, 'disease_model_latest.pkl')
    info_path = os.path.join(save_path, 'disease_info_latest.pkl')
    
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Modelo no encontrado en {model_path}")
    
    model = joblib.load(model_path)
    disease_info = joblib.load(info_path)
    
    return model, disease_info

if __name__ == '__main__':
    print("Entrenando modelo de predicción de enfermedades...")
    model, disease_info = train_model()
    save_model(model, disease_info)
    print("¡Modelo entrenado exitosamente!")

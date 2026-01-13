"""
Tests para el modelo ML
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'ml_model'))

from train_model import train_model, create_dataset, load_model, save_model

def test_dataset_creation():
    """Test de creación del dataset"""
    df = create_dataset()
    assert len(df) > 0
    assert 'symptoms' in df.columns
    assert 'disease' in df.columns
    assert 'exam_needed' in df.columns
    assert 'severity' in df.columns

def test_model_training():
    """Test de entrenamiento del modelo"""
    model, disease_info = train_model()
    
    assert model is not None
    assert disease_info is not None
    assert len(disease_info) > 0

def test_model_prediction():
    """Test de predicción del modelo"""
    model, disease_info = train_model()
    
    symptoms = "fiebre dolor cabeza cuerpo"
    prediction = model.predict([symptoms])
    
    assert prediction is not None
    assert len(prediction) > 0
    assert prediction[0] in disease_info

def test_model_confidence():
    """Test de confianza de predicción"""
    model, disease_info = train_model()
    
    symptoms = "fiebre dolor cabeza cuerpo"
    probabilities = model.predict_proba([symptoms])
    
    assert probabilities is not None
    assert len(probabilities[0]) > 0
    assert all(0 <= p <= 1 for p in probabilities[0])

def test_model_saving_loading(tmp_path):
    """Test de guardar y cargar modelo"""
    model, disease_info = train_model()
    
    # Guardar
    model_path, info_path = save_model(model, disease_info, str(tmp_path))
    
    assert os.path.exists(model_path)
    assert os.path.exists(info_path)
    
    # Cargar
    loaded_model, loaded_info = load_model(str(tmp_path))
    
    assert loaded_model is not None
    assert loaded_info is not None
    assert len(loaded_info) == len(disease_info)

@pytest.fixture
def trained_model():
    """Fixture para modelo entrenado"""
    model, disease_info = train_model()
    return model, disease_info

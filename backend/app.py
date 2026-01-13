"""
API REST para Sistema de Diagnóstico Médico
Endpoints para predicción de enfermedades, solicitud de exámenes y generación de reportes
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import sys
import logging
from functools import wraps

# Agregar ruta del modelo
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'ml_model'))

from train_model import load_model

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Inicializar Flask
app = Flask(__name__)
CORS(app)

# Configuración de base de datos
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://admin:password@db:5432/medical_db')
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar BD
db = SQLAlchemy(app)

# ==================== MODELOS DE BASE DE DATOS ====================

class Patient(db.Model):
    __tablename__ = 'patients'
    
    cedula = db.Column(db.String(20), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10))
    email = db.Column(db.String(255), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    medical_history = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relaciones
    diagnoses = db.relationship('Diagnosis', backref='patient', lazy=True, cascade='all, delete-orphan')
    exams = db.relationship('MedicalExam', backref='patient', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'cedula': self.cedula,
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
            'email': self.email,
            'phone': self.phone,
            'medical_history': self.medical_history,
            'created_at': self.created_at.isoformat()
        }

class Diagnosis(db.Model):
    __tablename__ = 'diagnoses'
    
    id = db.Column(db.Integer, primary_key=True)
    patient_cedula = db.Column(db.String(20), db.ForeignKey('patients.cedula'), nullable=False)
    symptoms = db.Column(db.Text, nullable=False)
    predicted_disease = db.Column(db.String(255), nullable=False)
    confidence = db.Column(db.Float)
    severity = db.Column(db.String(50))
    requires_exam = db.Column(db.Boolean, default=False)
    medications = db.Column(db.JSON)
    report_generated = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'patient_cedula': self.patient_cedula,
            'symptoms': self.symptoms,
            'predicted_disease': self.predicted_disease,
            'confidence': self.confidence,
            'severity': self.severity,
            'requires_exam': self.requires_exam,
            'medications': self.medications,
            'report_generated': self.report_generated,
            'created_at': self.created_at.isoformat()
        }

class MedicalExam(db.Model):
    __tablename__ = 'medical_exams'
    
    id = db.Column(db.Integer, primary_key=True)
    patient_cedula = db.Column(db.String(20), db.ForeignKey('patients.cedula'), nullable=False)
    diagnosis_id = db.Column(db.Integer, db.ForeignKey('diagnoses.id'))
    exam_type = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(50), default='pending')  # pending, scheduled, completed
    appointment_date = db.Column(db.DateTime)
    results = db.Column(db.Text)
    requested_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'patient_cedula': self.patient_cedula,
            'diagnosis_id': self.diagnosis_id,
            'exam_type': self.exam_type,
            'description': self.description,
            'status': self.status,
            'appointment_date': self.appointment_date.isoformat() if self.appointment_date else None,
            'results': self.results,
            'requested_at': self.requested_at.isoformat()
        }

# ==================== CARGA DEL MODELO ====================

model = None
disease_info = None

def load_ml_model():
    """Cargar modelo ML al iniciar la aplicación"""
    global model, disease_info
    try:
        model_path = os.path.join(os.path.dirname(__file__), '..', 'ml_model', 'models')
        model, disease_info = load_model(model_path)
        logger.info("Modelo ML cargado exitosamente")
    except Exception as e:
        logger.error(f"Error cargando modelo: {str(e)}")
        raise

# ==================== DECORADORES ====================

def require_patient_cedula(f):
    """Validar que el paciente exista"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        patient_cedula = kwargs.get('patient_cedula') or request.json.get('patient_cedula')
        if not patient_cedula:
            return jsonify({'error': 'patient_cedula requerido'}), 400
        
        patient = Patient.query.get(patient_cedula)
        if not patient:
            return jsonify({'error': 'Paciente no encontrado'}), 404
        
        return f(*args, **kwargs)
    return decorated_function

# ==================== ENDPOINTS ====================

@app.route('/health', methods=['GET'])
def health_check():
    """Verificar salud de la API"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'model_loaded': model is not None
    }), 200

# -------- Endpoints de Pacientes --------

@app.route('/api/patients', methods=['POST'])
def create_patient():
    """Crear nuevo paciente"""
    try:
        data = request.json
        
        # Validar datos requeridos
        if not all(k in data for k in ['cedula', 'name', 'age', 'email']):
            return jsonify({'error': 'Datos incompletos: cedula, name, age, email requeridos'}), 400
        
        # Verificar si el paciente ya existe
        existing = Patient.query.get(data['cedula'])
        if existing:
            return jsonify({'error': 'Paciente con esta cédula ya existe'}), 400
        
        patient = Patient(
            cedula=data['cedula'],
            name=data['name'],
            age=data['age'],
            gender=data.get('gender'),
            email=data['email'],
            phone=data.get('phone'),
            medical_history=data.get('medical_history')
        )
        
        db.session.add(patient)
        db.session.commit()
        
        logger.info(f"Paciente creado: {patient.cedula}")
        return jsonify(patient.to_dict()), 201
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error creando paciente: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/patients/<cedula>', methods=['GET'])
def get_patient(cedula):
    """Obtener información del paciente"""
    patient = Patient.query.get(cedula)
    if not patient:
        return jsonify({'error': 'Paciente no encontrado'}), 404
    
    return jsonify(patient.to_dict()), 200

@app.route('/api/patients', methods=['GET'])
def list_patients():
    """Listar todos los pacientes"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    pagination = Patient.query.paginate(page=page, per_page=per_page)
    
    return jsonify({
        'patients': [p.to_dict() for p in pagination.items],
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page
    }), 200

# -------- Endpoints de Diagnóstico --------

@app.route('/api/diagnose', methods=['POST'])
@require_patient_cedula
def diagnose_patient():
    """Realizar diagnóstico basado en síntomas"""
    try:
        if model is None:
            return jsonify({'error': 'Modelo no disponible'}), 503
        
        data = request.json
        patient_cedula = data.get('patient_cedula')
        symptoms = data.get('symptoms', '')
        
        if not symptoms:
            return jsonify({'error': 'Síntomas requeridos'}), 400
        
        # Predicción
        predicted_disease = model.predict([symptoms])[0]
        probabilities = model.predict_proba([symptoms])[0]
        max_confidence = float(max(probabilities))
        
        # Información de la enfermedad
        disease_details = disease_info.get(predicted_disease, {
            'exam_needed': False,
            'severity': 'Desconocida',
            'medications': []
        })
        
        # Crear diagnóstico en BD
        diagnosis = Diagnosis(
            patient_cedula=patient_cedula,
            symptoms=symptoms,
            predicted_disease=predicted_disease,
            confidence=round(max_confidence * 100, 2),
            severity=disease_details.get('severity', 'Desconocida'),
            requires_exam=disease_details.get('exam_needed', False),
            medications=disease_details.get('medications', [])
        )
        
        db.session.add(diagnosis)
        
        # Si requiere examen, crear orden
        if diagnosis.requires_exam:
            exam = MedicalExam(
                patient_cedula=patient_cedula,
                diagnosis_id=diagnosis.id,
                exam_type=f'Examen para {predicted_disease}',
                description=f'Examen recomendado debido a diagnóstico de {predicted_disease}',
                status='pending'
            )
            db.session.add(exam)
        
        db.session.commit()
        
        response = {
            'diagnosis_id': diagnosis.id,
            'patient_cedula': patient_cedula,
            'symptoms': symptoms,
            'predicted_disease': predicted_disease,
            'confidence': diagnosis.confidence,
            'severity': diagnosis.severity,
            'requires_exam': diagnosis.requires_exam,
            'medications': diagnosis.medications,
            'message': 'Diagnóstico completado'
        }
        
        if diagnosis.requires_exam:
            response['medical_exam_required'] = True
            response['exam_order'] = {
                'type': f'Examen para {predicted_disease}',
                'status': 'pending',
                'appointment_scheduling_required': True,
                'message': 'Se requiere nuevo examen médico y cita para confirmar diagnóstico'
            }
        else:
            response['message'] = 'Diagnóstico claro. Dicta médica generada.'
        
        logger.info(f"Diagnóstico realizado para paciente {patient_cedula}: {predicted_disease}")
        return jsonify(response), 200
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error en diagnóstico: {str(e)}")
        return jsonify({'error': str(e)}), 500

# -------- Endpoints de Exámenes --------

@app.route('/api/exams', methods=['POST'])
def create_exam():
    """Solicitar examen médico"""
    try:
        data = request.json
        
        exam = MedicalExam(
            patient_cedula=data.get('patient_cedula'),
            diagnosis_id=data.get('diagnosis_id'),
            exam_type=data.get('exam_type'),
            description=data.get('description'),
            status='pending'
        )
        
        db.session.add(exam)
        db.session.commit()
        
        logger.info(f"Examen solicitado: {exam.id}")
        return jsonify(exam.to_dict()), 201
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error creando examen: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/exams/<int:exam_id>', methods=['GET'])
def get_exam(exam_id):
    """Obtener detalles del examen"""
    exam = MedicalExam.query.get(exam_id)
    if not exam:
        return jsonify({'error': 'Examen no encontrado'}), 404
    
    return jsonify(exam.to_dict()), 200

@app.route('/api/exams/<int:exam_id>/schedule', methods=['PUT'])
def schedule_exam(exam_id):
    """Programar cita para examen"""
    try:
        data = request.json
        exam = MedicalExam.query.get(exam_id)
        
        if not exam:
            return jsonify({'error': 'Examen no encontrado'}), 404
        
        exam.appointment_date = datetime.fromisoformat(data.get('appointment_date'))
        exam.status = 'scheduled'
        
        db.session.commit()
        logger.info(f"Examen programado: {exam_id}")
        
        return jsonify({
            'message': 'Cita programada exitosamente',
            'exam': exam.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error programando examen: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/patients/<cedula>/exams', methods=['GET'])
def get_patient_exams(cedula):
    """Obtener exámenes de un paciente"""
    patient = Patient.query.get(cedula)
    if not patient:
        return jsonify({'error': 'Paciente no encontrado'}), 404
    
    exams = MedicalExam.query.filter_by(patient_cedula=cedula).all()
    return jsonify([exam.to_dict() for exam in exams]), 200

# -------- Endpoints de Reportes --------

@app.route('/api/diagnoses/<int:diagnosis_id>/report', methods=['GET'])
def generate_report(diagnosis_id):
    """Generar reporte médico"""
    try:
        diagnosis = Diagnosis.query.get(diagnosis_id)
        if not diagnosis:
            return jsonify({'error': 'Diagnóstico no encontrado'}), 404
        
        patient = diagnosis.patient
        
        report = {
            'report_id': f'RPT-{diagnosis_id}-{datetime.now().strftime("%Y%m%d%H%M%S")}',
            'generated_at': datetime.utcnow().isoformat(),
            'patient_info': {
                'name': patient.name,
                'age': patient.age,
                'gender': patient.gender,
                'email': patient.email
            },
            'diagnosis': {
                'disease': diagnosis.predicted_disease,
                'confidence': f'{diagnosis.confidence}%',
                'severity': diagnosis.severity,
                'symptoms': diagnosis.symptoms
            },
            'medical_prescription': {
                'medications': diagnosis.medications,
                'instructions': f'Seguir instrucciones médicas para {diagnosis.predicted_disease}',
                'follow_up': 'Consultar si síntomas persisten en 7 días'
            }
        }
        
        if diagnosis.requires_exam:
            report['exam_order'] = {
                'required': True,
                'message': 'Se requiere examen médico para confirmación del diagnóstico',
                'schedule_new_appointment': True
            }
        
        diagnosis.report_generated = True
        db.session.commit()
        
        logger.info(f"Reporte generado: {report['report_id']}")
        return jsonify(report), 200
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error generando reporte: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/patients/<cedula>/diagnoses', methods=['GET'])
def get_patient_diagnoses(cedula):
    """Obtener historial de diagnósticos"""
    patient = Patient.query.get(cedula)
    if not patient:
        return jsonify({'error': 'Paciente no encontrado'}), 404
    
    diagnoses = Diagnosis.query.filter_by(patient_cedula=cedula).order_by(Diagnosis.created_at.desc()).all()
    return jsonify([d.to_dict() for d in diagnoses]), 200

# ==================== INICIALIZACIÓN ====================

@app.before_request
def before_request():
    """Antes de cada request"""
    pass

@app.teardown_appcontext
def shutdown_session(exception=None):
    """Limpiar sesión de BD"""
    db.session.remove()

# ==================== MANEJO DE ERRORES ====================

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Ruta no encontrada'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Error interno del servidor'}), 500

# ==================== STARTUP ====================

# Intentar cargar modelo al iniciar
def init_app():
    """Inicializar aplicación"""
    with app.app_context():
        # Crear tablas (ignorar errores si ya existen)
        try:
            db.create_all()
            logger.info("Tablas de BD creadas")
        except Exception as e:
            logger.info(f"Tablas ya existen o error al crear: {str(e)}")
        
        # Cargar modelo
        try:
            load_ml_model()
            logger.info("Modelo ML cargado exitosamente al iniciar")
        except Exception as e:
            logger.warning(f"Modelo no disponible inicialmente: {str(e)}")

# Ejecutar al iniciar
init_app()

# ==================== MAIN ====================

if __name__ == '__main__':
    
    app.run(
        host='0.0.0.0',
        port=int(os.getenv('FLASK_PORT', 5000)),
        debug=os.getenv('FLASK_ENV') == 'development'
    )

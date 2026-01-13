"""
API REST para Sistema de Diagnóstico Médico
Endpoints para predicción de enfermedades, solicitud de exámenes y generación de reportes
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
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
    
    # Datos vitales
    height = db.Column(db.Float)  # cm
    weight = db.Column(db.Float)  # kg
    blood_pressure_systolic = db.Column(db.Integer)  # mmHg
    blood_pressure_diastolic = db.Column(db.Integer)  # mmHg
    temperature = db.Column(db.Float)  # °C
    
    # Antecedentes médicos
    previous_diseases = db.Column(db.Text)  # Enfermedades previas
    surgeries = db.Column(db.Text)  # Cirugías
    allergies = db.Column(db.Text)  # Alergias
    medications = db.Column(db.Text)  # Medicamentos actuales
    
    # Historia familiar
    parents_health = db.Column(db.Text)  # Salud de padres
    
    # Estilo de vida
    diet = db.Column(db.Text)  # Descripción de dieta
    exercise = db.Column(db.String(100))  # Frecuencia: sedentario, moderado, activo
    smokes = db.Column(db.Boolean, default=False)
    alcohol_consumption = db.Column(db.String(100))  # Frecuencia: nunca, ocasional, frecuente
    
    # Otros datos
    medical_history = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    diagnoses = db.relationship('Diagnosis', backref='patient', lazy=True, cascade='all, delete-orphan')
    exams = db.relationship('MedicalExam', backref='patient', lazy=True, cascade='all, delete-orphan')
    appointments = db.relationship('Appointment', backref='patient', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'cedula': self.cedula,
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
            'email': self.email,
            'phone': self.phone,
            'height': self.height,
            'weight': self.weight,
            'blood_pressure': f"{self.blood_pressure_systolic}/{self.blood_pressure_diastolic}" if self.blood_pressure_systolic else None,
            'temperature': self.temperature,
            'previous_diseases': self.previous_diseases,
            'surgeries': self.surgeries,
            'allergies': self.allergies,
            'medications': self.medications,
            'parents_health': self.parents_health,
            'diet': self.diet,
            'exercise': self.exercise,
            'smokes': self.smokes,
            'alcohol_consumption': self.alcohol_consumption,
            'medical_history': self.medical_history,
            'created_at': self.created_at.isoformat()
        }

class Diagnosis(db.Model):
    __tablename__ = 'diagnoses'
    
    id = db.Column(db.Integer, primary_key=True)
    patient_cedula = db.Column(db.String(20), db.ForeignKey('patients.cedula'), nullable=False)
    symptoms = db.Column(db.Text, nullable=False)
    symptoms_json = db.Column(db.JSON)  # Síntomas detallados con tiempo e intensidad
    predicted_disease = db.Column(db.String(255), nullable=False)
    confidence = db.Column(db.Float)
    severity = db.Column(db.String(50))
    requires_exam = db.Column(db.Boolean, default=False)
    recommended_tests = db.Column(db.JSON)  # Pruebas recomendadas si confidence < 84%
    medications = db.Column(db.JSON)
    recommendations = db.Column(db.Text)
    report_generated = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relaciones
    medical_tests = db.relationship('MedicalTest', backref='diagnosis', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'patient_cedula': self.patient_cedula,
            'symptoms': self.symptoms,
            'symptoms_detail': self.symptoms_json,
            'predicted_disease': self.predicted_disease,
            'confidence': self.confidence,
            'severity': self.severity,
            'requires_exam': self.requires_exam,
            'recommended_tests': self.recommended_tests,
            'medications': self.medications,
            'recommendations': self.recommendations,
            'report_generated': self.report_generated,
            'created_at': self.created_at.isoformat()
        }

class MedicalTest(db.Model):
    """Pruebas de apoyo recomendadas (sangre, radiografía, ecografía, etc.)"""
    __tablename__ = 'medical_tests'
    
    id = db.Column(db.Integer, primary_key=True)
    diagnosis_id = db.Column(db.Integer, db.ForeignKey('diagnoses.id'), nullable=False)
    patient_cedula = db.Column(db.String(20), db.ForeignKey('patients.cedula'), nullable=False)
    test_type = db.Column(db.String(255), nullable=False)  # Análisis de sangre, Radiografía, Ecografía, etc.
    description = db.Column(db.Text)
    status = db.Column(db.String(50), default='recommended')  # recommended, scheduled, completed
    scheduled_date = db.Column(db.DateTime)
    results = db.Column(db.Text)
    requested_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'diagnosis_id': self.diagnosis_id,
            'patient_cedula': self.patient_cedula,
            'test_type': self.test_type,
            'description': self.description,
            'status': self.status,
            'scheduled_date': self.scheduled_date.isoformat() if self.scheduled_date else None,
            'results': self.results,
            'requested_at': self.requested_at.isoformat()
        }

class Appointment(db.Model):
    """Citas de seguimiento"""
    __tablename__ = 'appointments'
    
    id = db.Column(db.Integer, primary_key=True)
    patient_cedula = db.Column(db.String(20), db.ForeignKey('patients.cedula'), nullable=False)
    diagnosis_id = db.Column(db.Integer, db.ForeignKey('diagnoses.id'))
    scheduled_date = db.Column(db.DateTime, nullable=False)
    reason = db.Column(db.String(255))  # Seguimiento, Evaluación de pruebas, etc.
    notes = db.Column(db.Text)
    status = db.Column(db.String(50), default='scheduled')  # scheduled, completed, cancelled
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'patient_cedula': self.patient_cedula,
            'diagnosis_id': self.diagnosis_id,
            'scheduled_date': self.scheduled_date.isoformat(),
            'reason': self.reason,
            'notes': self.notes,
            'status': self.status,
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
@app.route('/api/health', methods=['GET'])
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
        
        # Validar que los campos no estén vacíos
        if not data['cedula'] or not str(data['cedula']).strip():
            return jsonify({'error': 'La cédula no puede estar vacía'}), 400
        if not data['name'] or not str(data['name']).strip():
            return jsonify({'error': 'El nombre no puede estar vacío'}), 400
        if not data['email'] or not str(data['email']).strip():
            return jsonify({'error': 'El email no puede estar vacío'}), 400
        if not data['age'] or data['age'] < 1 or data['age'] > 120:
            return jsonify({'error': 'La edad debe ser un número entre 1 y 120'}), 400
        
        # Validar cedula format
        cedula_str = str(data['cedula']).strip()
        
        # Verificar si el paciente ya existe por cédula
        existing_cedula = Patient.query.get(cedula_str)
        if existing_cedula:
            return jsonify({'error': 'Paciente con esta cédula ya existe'}), 400
        
        # Verificar si el email ya existe
        existing_email = Patient.query.filter_by(email=data['email'].strip()).first()
        if existing_email:
            return jsonify({'error': 'Ya existe un paciente registrado con este email'}), 400
        
        patient = Patient(
            cedula=cedula_str,
            name=data['name'].strip(),
            age=int(data['age']),
            gender=data.get('gender', '').strip() if data.get('gender') else None,
            email=data['email'].strip(),
            phone=data.get('phone', '').strip() if data.get('phone') else None,
            # Datos vitales
            height=data.get('height'),
            weight=data.get('weight'),
            blood_pressure_systolic=data.get('blood_pressure_systolic'),
            blood_pressure_diastolic=data.get('blood_pressure_diastolic'),
            temperature=data.get('temperature'),
            # Antecedentes médicos
            previous_diseases=data.get('previous_diseases', '').strip() if data.get('previous_diseases') else None,
            surgeries=data.get('surgeries', '').strip() if data.get('surgeries') else None,
            allergies=data.get('allergies', '').strip() if data.get('allergies') else None,
            medications=data.get('medications', '').strip() if data.get('medications') else None,
            # Historia familiar
            parents_health=data.get('parents_health', '').strip() if data.get('parents_health') else None,
            # Estilo de vida
            diet=data.get('diet', '').strip() if data.get('diet') else None,
            exercise=data.get('exercise', '').strip() if data.get('exercise') else None,
            smokes=data.get('smokes', False),
            alcohol_consumption=data.get('alcohol_consumption', '').strip() if data.get('alcohol_consumption') else None,
            # Otros datos
            medical_history=data.get('medical_history', '').strip() if data.get('medical_history') else None
        )
        
        db.session.add(patient)
        db.session.commit()
        
        logger.info(f"Paciente creado: {patient.cedula}")
        return jsonify(patient.to_dict()), 201
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error creando paciente: {str(e)}")
        return jsonify({'error': f'Error al crear paciente: {str(e)}'}), 500

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
        symptoms_detail = data.get('symptoms_detail', [])  # Síntomas detallados con tiempo e intensidad
        
        if not symptoms:
            return jsonify({'error': 'Síntomas requeridos'}), 400
        
        # Predicción
        predicted_disease = model.predict([symptoms])[0]
        probabilities = model.predict_proba([symptoms])[0]
        max_confidence = float(max(probabilities))
        confidence_percent = round(max_confidence * 100, 2)
        
        # Información de la enfermedad
        disease_details = disease_info.get(predicted_disease, {
            'exam_needed': False,
            'severity': 'Desconocida',
            'medications': []
        })
        
        # Determinar si se requieren pruebas de apoyo (si confianza < 84%)
        requires_support_tests = confidence_percent < 84
        recommended_tests = []
        
        if requires_support_tests:
            # Recomendar pruebas de apoyo estándar
            recommended_tests = [
                {
                    'test_type': 'Análisis de sangre',
                    'description': 'Hemograma completo para confirmar diagnóstico'
                },
                {
                    'test_type': 'Radiografía',
                    'description': 'Radiografía de tórax o área afectada según síntomas'
                },
                {
                    'test_type': 'Ecografía',
                    'description': 'Ecografía para evaluación detallada'
                }
            ]
        
        # Crear diagnóstico en BD
        diagnosis = Diagnosis(
            patient_cedula=patient_cedula,
            symptoms=symptoms,
            symptoms_json=symptoms_detail,
            predicted_disease=predicted_disease,
            confidence=confidence_percent,
            severity=disease_details.get('severity', 'Desconocida'),
            requires_exam=disease_details.get('exam_needed', False) or requires_support_tests,
            recommended_tests=recommended_tests,
            medications=disease_details.get('medications', [])
        )
        
        db.session.add(diagnosis)
        db.session.flush()  # Para obtener el ID antes de commit
        
        # Crear pruebas de apoyo si confianza < 84%
        if requires_support_tests:
            for test in recommended_tests:
                medical_test = MedicalTest(
                    diagnosis_id=diagnosis.id,
                    patient_cedula=patient_cedula,
                    test_type=test['test_type'],
                    description=test['description'],
                    status='recommended'
                )
                db.session.add(medical_test)
            
            # Programar cita de seguimiento para revisar pruebas
            follow_up_date = datetime.utcnow() + timedelta(days=7)
            appointment = Appointment(
                patient_cedula=patient_cedula,
                diagnosis_id=diagnosis.id,
                scheduled_date=follow_up_date,
                reason='Evaluación de pruebas de apoyo',
                status='scheduled'
            )
            db.session.add(appointment)
        
        db.session.commit()
        
        response = {
            'diagnosis_id': diagnosis.id,
            'patient_cedula': patient_cedula,
            'symptoms': symptoms,
            'predicted_disease': predicted_disease,
            'confidence': confidence_percent,
            'severity': diagnosis.severity,
            'requires_exam': diagnosis.requires_exam,
            'medications': diagnosis.medications,
            'message': 'Diagnóstico completado'
        }
        
        if requires_support_tests:
            response['low_confidence'] = True
            response['confidence_message'] = f'Confiabilidad {confidence_percent}% < 84%. Se requieren pruebas de apoyo.'
            response['recommended_tests'] = recommended_tests
            response['follow_up_appointment'] = {
                'scheduled_date': follow_up_date.isoformat(),
                'reason': 'Evaluación de pruebas de apoyo'
            }
        else:
            response['message'] = 'Diagnóstico confiable. Dicta médica generada.'
        
        logger.info(f"Diagnóstico realizado para paciente {patient_cedula}: {predicted_disease} ({confidence_percent}%)")
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
    """Generar reporte médico en PDF"""
    try:
        from reportlab.lib.pagesizes import letter, A4
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import inch
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
        from reportlab.lib import colors
        from io import BytesIO
        
        diagnosis = Diagnosis.query.get(diagnosis_id)
        if not diagnosis:
            return jsonify({'error': 'Diagnóstico no encontrado'}), 404
        
        patient = diagnosis.patient
        
        # Crear PDF en memoria
        pdf_buffer = BytesIO()
        doc = SimpleDocTemplate(pdf_buffer, pagesize=A4)
        styles = getSampleStyleSheet()
        story = []
        
        # Título
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#667eea'),
            spaceAfter=30,
            alignment=1  # Center
        )
        story.append(Paragraph('REPORTE MÉDICO', title_style))
        story.append(Spacer(1, 0.2*inch))
        
        # Información del paciente
        story.append(Paragraph('<b>INFORMACIÓN DEL PACIENTE</b>', styles['Heading2']))
        patient_data = [
            ['Cédula:', patient.cedula],
            ['Nombre:', patient.name],
            ['Edad:', f'{patient.age} años'],
            ['Género:', patient.gender or 'No especificado'],
            ['Email:', patient.email],
            ['Teléfono:', patient.phone or 'No registrado']
        ]
        
        if patient.weight or patient.height:
            patient_data.append(['Peso/Altura:', f'{patient.weight} kg / {patient.height} cm' if patient.weight and patient.height else 'No completado'])
        
        if patient.blood_pressure_systolic:
            patient_data.append(['Presión Arterial:', f'{patient.blood_pressure_systolic}/{patient.blood_pressure_diastolic} mmHg'])
        
        if patient.temperature:
            patient_data.append(['Temperatura:', f'{patient.temperature}°C'])
        
        patient_table = Table(patient_data, colWidths=[2*inch, 4*inch])
        patient_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f0f0f0')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey)
        ]))
        story.append(patient_table)
        story.append(Spacer(1, 0.3*inch))
        
        # Diagnóstico
        story.append(Paragraph('<b>DIAGNÓSTICO</b>', styles['Heading2']))
        diagnosis_data = [
            ['Enfermedad:', diagnosis.predicted_disease],
            ['Confiabilidad:', f'{diagnosis.confidence}%'],
            ['Gravedad:', diagnosis.severity],
            ['Síntomas:', diagnosis.symptoms]
        ]
        
        diagnosis_table = Table(diagnosis_data, colWidths=[2*inch, 4*inch])
        diagnosis_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e8f5e9')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey)
        ]))
        story.append(diagnosis_table)
        story.append(Spacer(1, 0.3*inch))
        
        # Medicamentos
        if diagnosis.medications and len(diagnosis.medications) > 0:
            story.append(Paragraph('<b>MEDICAMENTOS RECOMENDADOS</b>', styles['Heading2']))
            for med in diagnosis.medications:
                story.append(Paragraph(f'• {med}', styles['BodyText']))
            story.append(Spacer(1, 0.3*inch))
        
        # Pruebas recomendadas
        if diagnosis.recommended_tests and len(diagnosis.recommended_tests) > 0:
            story.append(Paragraph('<b>PRUEBAS DE APOYO RECOMENDADAS</b>', styles['Heading2']))
            for test in diagnosis.recommended_tests:
                story.append(Paragraph(f'<b>{test["test_type"]}</b>', styles['Normal']))
                story.append(Paragraph(f'{test["description"]}', styles['BodyText']))
                story.append(Spacer(1, 0.1*inch))
            story.append(Spacer(1, 0.2*inch))
        
        # Antecedentes médicos si existen
        if patient.previous_diseases or patient.surgeries or patient.allergies:
            story.append(Paragraph('<b>ANTECEDENTES MÉDICOS</b>', styles['Heading2']))
            if patient.previous_diseases:
                story.append(Paragraph(f'<b>Enfermedades previas:</b> {patient.previous_diseases}', styles['BodyText']))
            if patient.surgeries:
                story.append(Paragraph(f'<b>Cirugías:</b> {patient.surgeries}', styles['BodyText']))
            if patient.allergies:
                story.append(Paragraph(f'<b>Alergias:</b> {patient.allergies}', styles['BodyText']))
            story.append(Spacer(1, 0.3*inch))
        
        # Pie de página
        story.append(Spacer(1, 0.5*inch))
        footer_text = f'Reporte generado: {datetime.utcnow().strftime("%d/%m/%Y %H:%M:%S")}'
        story.append(Paragraph(footer_text, styles['Italic']))
        story.append(Paragraph('Este reporte fue generado automáticamente por el Sistema de Diagnóstico Médico MLOps', 
                             styles['Italic']))
        
        # Generar PDF
        doc.build(story)
        pdf_buffer.seek(0)
        
        # Guardar en BD
        diagnosis.report_generated = True
        db.session.commit()
        
        logger.info(f"Reporte PDF generado: Diagnóstico {diagnosis_id}")
        
        # Retornar PDF
        from flask import send_file
        return send_file(
            pdf_buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f'Reporte_Medico_{diagnosis_id}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf'
        )
        
    except ImportError:
        logger.error("ReportLab no está instalado")
        return jsonify({'error': 'Generador de PDF no disponible'}), 503
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error generando PDF: {str(e)}")
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

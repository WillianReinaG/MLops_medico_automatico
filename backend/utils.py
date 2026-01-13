"""
Utilidades y funciones auxiliares para la API
"""

import json
from datetime import datetime
from functools import wraps
from flask import jsonify, request

def response_json(status_code, data=None, message=None, error=None):
    """Crear respuesta JSON estándar"""
    response = {
        'timestamp': datetime.utcnow().isoformat(),
        'status_code': status_code
    }
    
    if message:
        response['message'] = message
    
    if data:
        response['data'] = data
    
    if error:
        response['error'] = error
    
    return jsonify(response), status_code

def validate_json(*required_fields):
    """Decorador para validar JSON en request"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not request.is_json:
                return response_json(400, error='Content-Type debe ser application/json')
            
            data = request.get_json()
            
            for field in required_fields:
                if field not in data or data[field] is None:
                    return response_json(400, error=f'Campo requerido: {field}')
            
            return f(*args, **kwargs)
        
        return decorated_function
    return decorator

def paginate_query(query, page=1, per_page=10):
    """Paginar resultados de query"""
    pagination = query.paginate(page=page, per_page=per_page)
    return {
        'items': [item.to_dict() if hasattr(item, 'to_dict') else item for item in pagination.items],
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page,
        'has_next': pagination.has_next,
        'has_prev': pagination.has_prev
    }

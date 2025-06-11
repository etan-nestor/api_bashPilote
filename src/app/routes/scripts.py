from flask import Blueprint, request, jsonify
from app.core.scheduler import Scheduler
from app.extensions import db
from app.models.script import Script
from app.utils.auth import api_key_required
from app.core.script_exec import execute_script

scripts_bp = Blueprint('scripts', __name__)

@scripts_bp.route('/scripts', methods=['POST'])
@api_key_required
def add_script():
    data = request.get_json()
    if not data or 'content' not in data:
        return jsonify({'error': 'Script content is required'}), 400
    
    try:
        script = Script(
            name=data.get('name', 'Untitled Script'),
            content=data['content']
        )
        db.session.add(script)
        db.session.commit()
        return jsonify(script.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@scripts_bp.route('/scripts/<int:script_id>/run', methods=['POST'])
@api_key_required
def run_script(script_id):
    script = Script.query.get_or_404(script_id)
    
    try:
        result = execute_script(script.content, script.id)
        return jsonify({
            'output': result.output,
            'return_code': result.return_code,
            'execution_time': result.execution_time
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400
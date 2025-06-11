from flask import Blueprint, request, jsonify
from app.core.scheduler import Scheduler
from app.extensions import db
from app.models.job import Job
from app.models.script import Script
from app.utils.auth import api_key_required
from app.core.script_exec import execute_script

jobs_bp = Blueprint('jobs', __name__)

@jobs_bp.route('/jobs', methods=['POST'])
@api_key_required
def schedule_job():
    data = request.get_json()
    if not data or 'script_id' not in data or 'cron_expression' not in data:
        return jsonify({'error': 'Script ID and cron expression are required'}), 400
    
    script = Script.query.get_or_404(data['script_id'])
    
    try:
        job = Job(
            script_id=script.id,
            cron_expression=data['cron_expression']
        )
        db.session.add(job)
        db.session.commit()
        
        # Ajouter la tâche au scheduler
        scheduler.add_job(
            id=str(job.id),
            func=execute_script,
            args=[script.content, script.id],
            trigger='cron',
            **parse_cron_expression(data['cron_expression'])
        )
        
        return jsonify(job.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

def parse_cron_expression(expression):
    parts = expression.split()
    if len(parts) != 5:
        raise ValueError("Invalid cron expression")
    
    return {
        'minute': parts[0],
        'hour': parts[1],
        'day': parts[2],
        'month': parts[3],
        'day_of_week': parts[4]
    }
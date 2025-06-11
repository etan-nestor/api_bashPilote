import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from app.config import Config
import json
from datetime import datetime

def setup_logging(app):
    log_dir = Config.LOGS_DIR
    log_file = log_dir / 'bashpilot.log'
    
    # Configuration du logging
    handler = RotatingFileHandler(
        log_file,
        maxBytes=1024 * 1024 * 10,  # 10MB
        backupCount=5
    )
    
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.INFO)

class ScriptLogger:
    @staticmethod
    def log_execution(script_id, output, return_code, execution_time):
        log_entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'script_id': script_id,
            'output': output,
            'return_code': return_code,
            'execution_time': execution_time
        }
        
        log_file = Config.LOGS_DIR / f'script_{script_id}.log'
        
        with open(log_file, 'a') as f:
            f.write(json.dumps(log_entry) + '\n')
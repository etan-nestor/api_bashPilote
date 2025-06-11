import uuid
from pathlib import Path
from app.config import Config
from app.models import Script
from app.extensions import db
from .script_exec import execute_script
from .logging import ScriptLogger

class ScriptManager:
    @staticmethod
    def create_script(name, content):
        """Crée un nouveau script"""
        script = Script(name=name, content=content)
        db.session.add(script)
        db.session.commit()
        
        # Sauvegarder dans le système de fichiers
        script_path = Config.SCRIPTS_DIR / f'script_{script.id}.sh'
        with open(script_path, 'w') as f:
            f.write(content)
        
        return script
    
    @staticmethod
    def execute_script(script_id):
        """Exécute un script et log le résultat"""
        script = Script.query.get_or_404(script_id)
        result = execute_script(script.content)
        
        # Loguer l'exécution
        ScriptLogger.log_execution(
            script_id=script.id,
            output=result.output,
            return_code=result.return_code,
            execution_time=result.execution_time
        )
        
        return result
    
    @staticmethod
    def get_script_logs(script_id, limit=50):
        """Récupère les logs d'un script"""
        log_file = Config.LOGS_DIR / f'script_{script_id}.log'
        if not log_file.exists():
            return []
            
        with open(log_file, 'r') as f:
            lines = f.readlines()[-limit:]
            return [json.loads(line) for line in lines]
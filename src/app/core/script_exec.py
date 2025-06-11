import subprocess
import uuid
from datetime import datetime
from pathlib import Path
from app.extensions import db
from app.models.script import ScriptLog
from app.config import Config
from app.utils.security import is_script_safe

class ScriptResult:
    def __init__(self, output, return_code, execution_time):
        self.output = output
        self.return_code = return_code
        self.execution_time = execution_time

def execute_script(script_content, script_id=None):
    if not is_script_safe(script_content):
        raise ValueError("Script contains potentially dangerous commands")
    
    # Créer un fichier temporaire
    script_path = Path(Config.SCRIPTS_DIR) / f'temp_{uuid.uuid4()}.sh'
    try:
        with open(script_path, 'w') as f:
            f.write('#!/bin/bash\n')
            f.write(script_content)
        
        script_path.chmod(0o755)  # Rendre exécutable
        
        start_time = datetime.now()
        process = subprocess.run(
            [str(script_path)],
            capture_output=True,
            text=True,
            timeout=300  # 5 minutes timeout
        )
        execution_time = (datetime.now() - start_time).total_seconds()
        
        result = ScriptResult(
            output=process.stdout + process.stderr,
            return_code=process.returncode,
            execution_time=execution_time
        )
        
        if script_id:
            log = ScriptLog(
                script_id=script_id,
                output=result.output,
                return_code=result.return_code,
                execution_time=result.execution_time,
                timestamp=datetime.now()
            )
            db.session.add(log)
            db.session.commit()
        
        return result
    finally:
        if script_path.exists():
            script_path.unlink()
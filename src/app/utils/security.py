import re
import shlex
from pathlib import Path
from app.config import Config

DANGEROUS_COMMANDS = [
    'rm', 'mkfs', 'dd', 'chmod', 'mv', 'wget', 'curl',
    '>', '>>', '<', '|', '&', ';', '`', '$('
]

SAFE_COMMAND_WHITELIST = [
    'echo', 'ls', 'cat', 'grep', 'find', 'awk', 'sed',
    'date', 'tar', 'gzip', 'ping', 'nc', 'netstat'
]

def sanitize_script(script_content):
    """Nettoie le script en autorisant uniquement les commandes sûres"""
    lines = []
    for line in script_content.split('\n'):
        line = line.strip()
        if not line or line.startswith('#'):
            lines.append(line)
            continue
            
        parts = shlex.split(line)
        if not parts:
            continue
            
        command = parts[0]
        if command in DANGEROUS_COMMANDS:
            raise ValueError(f"Dangerous command detected: {command}")
            
        if command not in SAFE_COMMAND_WHITELIST:
            raise ValueError(f"Command not in whitelist: {command}")
            
        lines.append(line)
    
    return '\n'.join(lines)

def validate_cron_expression(expression):
    """Valide une expression CRON"""
    parts = expression.split()
    if len(parts) != 5:
        return False
        
    for part in parts:
        if not all(c in '0123456789,-*/' for c in part):
            return False
            
    return True

def is_script_safe(script_content):
    """
    Renvoie True si le script est considéré comme sûr.
    """
    try:
        sanitize_script(script_content)
        return True
    except ValueError:
        return False

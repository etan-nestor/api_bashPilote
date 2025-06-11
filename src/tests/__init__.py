# tests/__init__.py

import os
import tempfile

# On peut aussi pré-configurer un environnement de test
os.environ['FLASK_ENV'] = 'testing'
os.environ['API_KEYS'] = 'test-key'
os.environ['SECRET_KEY'] = 'test-secret'

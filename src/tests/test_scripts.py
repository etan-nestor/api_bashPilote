import pytest
from app import create_app
from app.models import db, Script
import json
import os

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['WTF_CSRF_ENABLED'] = False
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()

def test_add_script(client):
    # Test avec une clé API valide
    headers = {'X-API-KEY': 'test-key'}
    data = {
        'name': 'Test Script',
        'content': 'echo "Hello World"'
    }
    
    response = client.post('/api/v1/scripts', 
                         data=json.dumps(data),
                         headers=headers,
                         content_type='application/json')
    
    assert response.status_code == 201
    assert 'id' in response.json
    
    # Test sans clé API
    response = client.post('/api/v1/scripts', 
                         data=json.dumps(data),
                         content_type='application/json')
    assert response.status_code == 401

def test_run_script(client):
    headers = {'X-API-KEY': 'test-key'}
    
    # D'abord créer un script
    script = Script(name='Test', content='echo "Hello"')
    db.session.add(script)
    db.session.commit()
    
    # Exécuter le script
    response = client.post(f'/api/v1/scripts/{script.id}/run',
                         headers=headers)
    
    assert response.status_code == 200
    assert 'Hello' in response.json['output']
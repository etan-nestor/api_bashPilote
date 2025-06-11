import pytest
from datetime import datetime
from app import create_app
from app.models import db, Script, Job
import json

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            
            # Ajouter un script de test
            script = Script(name='Test', content='echo "Hello"')
            db.session.add(script)
            db.session.commit()
            
        yield client
        with app.app_context():
            db.drop_all()

def test_schedule_job(client):
    headers = {'X-API-KEY': 'test-key'}
    data = {
        'script_id': 1,
        'cron_expression': '* * * * *'
    }
    
    response = client.post('/api/v1/jobs',
                         data=json.dumps(data),
                         headers=headers,
                         content_type='application/json')
    
    assert response.status_code == 201
    assert 'id' in response.json
    assert response.json['cron_expression'] == '* * * * *'
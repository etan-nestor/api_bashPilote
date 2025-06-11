from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from app.extensions import db
import atexit

class Scheduler:
    def __init__(self, app):
        self.app = app
        with self.app.app_context():
            self.scheduler = BackgroundScheduler(
                jobstores={
                    'default': SQLAlchemyJobStore(
                        engine=db.engine,
                        tablename='scheduled_jobs'
                    )
                },
                timezone='UTC'
            )
        
    def start(self):
        with self.app.app_context():
            self.scheduler.start()
            self._load_existing_jobs()
        
        atexit.register(self.shutdown)
    
    def shutdown(self):
        self.scheduler.shutdown(wait=False)
    
    def _load_existing_jobs(self):
        from app.models.job import Job
        jobs = Job.query.all()
        for job in jobs:
            self.add_job_from_model(job)
    
    def add_job_from_model(self, job):
        from app.models.script import Script
        script = Script.query.get(job.script_id)
        
        self.scheduler.add_job(
            id=str(job.id),
            func=self._execute_script,
            args=[script.content, script.id],
            trigger='cron',
            **self._parse_cron(job.cron_expression),
            replace_existing=True
        )
    
    def _execute_script(self, script_content, script_id):
        from app.core.script_exec import execute_script
        with self.app.app_context():
            execute_script(script_content, script_id)
    
    def _parse_cron(self, expression):
        parts = expression.split()
        return {
            'minute': parts[0],
            'hour': parts[1],
            'day': parts[2],
            'month': parts[3],
            'day_of_week': parts[4]
        }

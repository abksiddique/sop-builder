from app import db
from datetime import datetime


class SOPRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    process_name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    roles = db.Column(db.String(500), nullable=True)
    exceptions = db.Column(db.Text, nullable=True)
    sop_content = db.Column(db.Text, nullable=False)
    bpmn_xml = db.Column(db.Text, nullable=True)
    mermaid_code = db.Column(db.Text, nullable=True)
    ai_model_used = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<SOP {self.process_name}>'
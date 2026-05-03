from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.ai_engine import generate_sop
from app.models import SOPRecord
from app import db
import markdown as md

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/generate', methods=['POST'])
def generate():
    process_name = request.form.get('process_name', '').strip()
    description  = request.form.get('description', '').strip()
    roles        = request.form.get('roles', '').strip()
    exceptions   = request.form.get('exceptions', '').strip()

    if not process_name or not description:
        flash('Process name and description are required.', 'error')
        return redirect(url_for('main.index'))

    sop_content, bpmn_xml, mermaid_code, model_used = generate_sop(
        process_name, description, roles, exceptions
    )

    if not sop_content:
        flash('AI generation failed. Please try again in a moment.', 'error')
        return redirect(url_for('main.index'))

    sop_html = md.markdown(sop_content, extensions=['extra'])

    record = SOPRecord(
        process_name=process_name,
        description=description,
        roles=roles,
        exceptions=exceptions,
        sop_content=sop_content,
        bpmn_xml=bpmn_xml if bpmn_xml else '',
        mermaid_code=mermaid_code if mermaid_code else '',
        ai_model_used=model_used
    )
    db.session.add(record)
    db.session.commit()

    return render_template('result.html',
        process_name=process_name,
        sop_html=sop_html,
        sop_raw=sop_content,
        bpmn_xml=bpmn_xml if bpmn_xml else '',
        mermaid_code=mermaid_code if mermaid_code else '',
        model_used=model_used,
        record_id=record.id
    )


@main.route('/history')
def history():
    records = SOPRecord.query.order_by(SOPRecord.created_at.desc()).all()
    return render_template('history.html', records=records)


@main.route('/view/<int:record_id>')
def view_record(record_id):
    record = SOPRecord.query.get_or_404(record_id)
    sop_html = md.markdown(record.sop_content, extensions=['extra'])
    return render_template('result.html',
        process_name=record.process_name,
        sop_html=sop_html,
        sop_raw=record.sop_content,
        bpmn_xml=record.bpmn_xml if record.bpmn_xml else '',
        mermaid_code=record.mermaid_code if record.mermaid_code else '',
        model_used=record.ai_model_used,
        record_id=record.id
    )


@main.route('/print/<int:record_id>')
def print_sop(record_id):
    record = SOPRecord.query.get_or_404(record_id)
    sop_html = md.markdown(record.sop_content, extensions=['extra'])
    return render_template('print.html',
        process_name=record.process_name,
        sop_html=sop_html,
        model_used=record.ai_model_used,
        created_at=record.created_at
    )


@main.route('/delete/<int:record_id>', methods=['POST'])
def delete_record(record_id):
    record = SOPRecord.query.get_or_404(record_id)
    db.session.delete(record)
    db.session.commit()
    flash('SOP deleted successfully.', 'success')
    return redirect(url_for('main.history'))
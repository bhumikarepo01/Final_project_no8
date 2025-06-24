from flask import Blueprint, render_template, request, redirect, url_for, current_app
from .models import Incident
from . import db, mail
from datetime import timedelta
from flask_mail import Message

main = Blueprint('main', __name__)

@main.route('/')
def index():
    incidents = Incident.query.all()

    # Convert UTC to IST for display
    for incident in incidents:
        if incident.created_at:
            incident.created_at_ist = incident.created_at + timedelta(hours=5, minutes=30)
        else:
            incident.created_at_ist = None

    return render_template('incidents.html', incidents=incidents)


@main.route('/report', methods=['GET', 'POST'])
def report():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        assigned_to = request.form.get('assigned_to')

        new_incident = Incident(
            title=title,
            description=description,
            assigned_to=assigned_to
        )

        db.session.add(new_incident)
        db.session.commit()

        # ✅ Send email when new incident is created
        msg = Message(
            subject=f"New Incident: {title}",
            sender=current_app.config['MAIL_USERNAME'],
            recipients=['bhumikajayswal01@gmail.com'],
            body=f'''New Incident Created:

Title: {title}
Description: {description}
Assigned To: {assigned_to or 'Unassigned'}
Status: Open
'''
        )
        mail.send(msg)

        return redirect(url_for('main.index'))

    return render_template('report.html')


@main.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_incident(id):
    incident = Incident.query.get_or_404(id)

    if request.method == 'POST':
        incident.title = request.form['title']
        incident.description = request.form['description']
        incident.status = request.form['status']
        incident.assigned_to = request.form['assigned_to']
        db.session.commit()

        # ✅ Send email when incident is updated
        msg = Message(
            subject=f"Incident Updated: {incident.title}",
            sender=current_app.config['MAIL_USERNAME'],
            recipients=['bhumikajayswal01@gmail.com'],
            body=f'''Incident Updated:

Title: {incident.title}
Description: {incident.description}
Assigned To: {incident.assigned_to or 'Unassigned'}
Status: {incident.status}
'''
        )
        mail.send(msg)

        return redirect(url_for('main.index'))

    return render_template('edit.html', incident=incident)


@main.route('/delete/<int:id>', methods=['POST'])
def delete_incident(id):
    incident = Incident.query.get_or_404(id)
    db.session.delete(incident)
    db.session.commit()
    return redirect(url_for('main.index'))

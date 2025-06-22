from flask import Blueprint, render_template, request, redirect, url_for
from .models import Incident
from . import db 
from datetime import timedelta
from flask_mail import Message
from . import mail

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

# @main.route('/report', methods=['GET', 'POST'])
# def report():
#     if request.method == 'POST':
#         title = request.form['title']
#         description = request.form['description']
#         new_incident = Incident(title=title, description=description)
#         db.session.add(new_incident)
#         db.session.commit()
#         return redirect(url_for('main.index'))
#     return render_template('report.html')

@main.route('/report', methods=['GET', 'POST'])
def report():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        new_incident = Incident(title=title, description=description)
        db.session.add(new_incident)
        db.session.commit()

        # ✅ Send email
        msg = Message(
            subject='New Incident Reported',
            sender='bhumikajayswal01@gmail.com',
            recipients=['bhumikajayswal01@gmail.com'],  # can be your same email or any other
            body=f'Title: {title}\nDescription: {description}'
        )
        mail.send(msg)

        return redirect(url_for('main.index'))
    return render_template('report.html')

@main.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_incident(id):
    incident = Incident.query.get_or_404(id)

    if request.method == 'POST':
        incident.status = request.form['status']
        incident.assigned_to = request.form['assigned_to']
        db.session.commit()
        return redirect(url_for('main.index'))

    return render_template('edit.html', incident=incident)

@main.route('/delete/<int:id>', methods=['POST'])
def delete_incident(id):
    incident = Incident.query.get_or_404(id)
    db.session.delete(incident)
    db.session.commit()
    return redirect(url_for('main.index'))

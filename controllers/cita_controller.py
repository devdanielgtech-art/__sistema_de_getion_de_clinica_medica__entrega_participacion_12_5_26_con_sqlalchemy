from flask import request, redirect, url_for, Blueprint
from datetime import datetime
from models.cita_model import Cita
from models.medico_model import Medico
from models.paciente_model import Paciente
from views import cita_view

cita_bp = Blueprint('cita', __name__, url_prefix="/citas")

@cita_bp.route("/")
def index():
    citas = Cita.get_all()
    return cita_view.list(citas)

@cita_bp.route("/create", methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        medico_id = request.form['medico_id']
        paciente_id = request.form['paciente_id']
        fecha_hora_str = request.form['fecha_hora']
        motivo = request.form['motivo']
        estado = request.form['estado']
        
        fecha_hora = datetime.strptime(fecha_hora_str, '%Y-%m-%dT%H:%M')
        
        cita = Cita(medico_id, paciente_id, fecha_hora, motivo, estado)
        cita.save()
        return redirect(url_for('cita.index'))
    
    medicos = Medico.query.all()
    pacientes = Paciente.query.all()
    return cita_view.create(medicos, pacientes)

@cita_bp.route("/edit/<int:id>", methods=['GET', 'POST'])
def edit(id):
    cita = Cita.get_by_id(id)
    if request.method == 'POST':
        medico_id = request.form['medico_id']
        paciente_id = request.form['paciente_id']
        fecha_hora_str = request.form['fecha_hora']
        motivo = request.form['motivo']
        estado = request.form['estado']
        
        fecha_hora = datetime.strptime(fecha_hora_str, '%Y-%m-%dT%H:%M')
        
        cita.update(medico_id=medico_id, paciente_id=paciente_id, fecha_hora=fecha_hora,
                   motivo=motivo, estado=estado)
        return redirect(url_for('cita.index'))
    
    medicos = Medico.query.all()
    pacientes = Paciente.query.all()
    return cita_view.edit(cita, medicos, pacientes)

@cita_bp.route("/delete/<int:id>")
def delete(id):
    cita = Cita.get_by_id(id)
    cita.delete()
    return redirect(url_for('cita.index'))

# EXTRA: Agenda de citas
@cita_bp.route("/agenda")
def agenda():
    medico_id = request.args.get('medico_id', type=int)
    fecha_str = request.args.get('fecha')
    fecha = None
    
    if fecha_str:
        fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()
    
    citas = Cita.get_agenda(medico_id, fecha)
    medicos = Medico.get_all()
    
    return cita_view.agenda(citas, medicos, medico_id, fecha)
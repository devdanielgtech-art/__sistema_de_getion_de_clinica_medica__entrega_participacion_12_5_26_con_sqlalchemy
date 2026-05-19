from flask import request, redirect, url_for, Blueprint
from datetime import datetime
from models.consulta_model import Consulta
from models.medico_model import Medico
from models.paciente_model import Paciente
from views import consulta_view

consulta_bp = Blueprint('consulta', __name__, url_prefix="/consultas")

@consulta_bp.route("/")
def index():
    consultas = Consulta.get_all()
    return consulta_view.list(consultas)

@consulta_bp.route("/create", methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        medico_id = request.form['medico_id']
        paciente_id = request.form['paciente_id']
        fecha_str = request.form['fecha']
        diagnostico = request.form['diagnostico']
        tratamiento = request.form['tratamiento']
        
        fecha = datetime.strptime(fecha_str, '%Y-%m-%d')
        
        consulta = Consulta(medico_id, paciente_id, fecha, diagnostico, tratamiento)
        consulta.save()
        return redirect(url_for('consulta.index'))
    
    medicos = Medico.query.all()
    pacientes = Paciente.query.all()
    return consulta_view.create(medicos, pacientes)

@consulta_bp.route("/edit/<int:id>", methods=['GET', 'POST'])
def edit(id):
    consulta = Consulta.get_by_id(id)
    if request.method == 'POST':
        medico_id = request.form['medico_id']
        paciente_id = request.form['paciente_id']
        fecha_str = request.form['fecha']
        diagnostico = request.form['diagnostico']
        tratamiento = request.form['tratamiento']
        
        fecha = datetime.strptime(fecha_str, '%Y-%m-%d')
        
        consulta.update(medico_id=medico_id, paciente_id=paciente_id, fecha=fecha, 
                       diagnostico=diagnostico, tratamiento=tratamiento)
        return redirect(url_for('consulta.index'))
    
    medicos = Medico.query.all()
    pacientes = Paciente.query.all()
    return consulta_view.edit(consulta, medicos, pacientes)

@consulta_bp.route("/delete/<int:id>")
def delete(id):
    consulta = Consulta.get_by_id(id)
    consulta.delete()
    return redirect(url_for('consulta.index'))

# EXTRA: Filtro de consultas por fecha
@consulta_bp.route("/filtrar", methods=['GET', 'POST'])
def filtrar():
    consultas = []
    fecha_inicio = None
    fecha_fin = None
    
    if request.method == 'POST':
        fecha_inicio_str = request.form['fecha_inicio']
        fecha_fin_str = request.form['fecha_fin']
        
        fecha_inicio = datetime.strptime(fecha_inicio_str, '%Y-%m-%d')
        fecha_fin = datetime.strptime(fecha_fin_str, '%Y-%m-%d')
        
        consultas = Consulta.filtrar_por_fecha(fecha_inicio, fecha_fin)
    
    return consulta_view.filtrar(consultas, fecha_inicio, fecha_fin)
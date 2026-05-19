from flask import Flask, request, session, redirect, url_for, render_template
from functools import wraps

from database import db
from controllers import medico_controller, paciente_controller, consulta_controller, cita_controller, usuario_controller, auth_controller

app = Flask(__name__)
app.secret_key = "clave_secreta_clinica_2026"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///clinica_medica.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'usuario_id' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('rol') != 'admin':
            return redirect(url_for('paciente.index'))
        return f(*args, **kwargs)
    return decorated_function

app.register_blueprint(auth_controller.auth_bp)
app.register_blueprint(medico_controller.medico_bp)
app.register_blueprint(paciente_controller.paciente_bp)
app.register_blueprint(consulta_controller.consulta_bp)
app.register_blueprint(cita_controller.cita_bp)
app.register_blueprint(usuario_controller.usuario_bp)

@app.context_processor
def inject_active_path():
    def is_active(path):
        return 'active' if request.path == path else ''
    return dict(is_active=is_active, session=session)

@app.route("/")
def home():
    if 'usuario_id' in session:
        if session.get('rol') == 'admin':
            return redirect(url_for('admin_dashboard'))
        else:
            return redirect(url_for('paciente.index'))
    return redirect(url_for('auth.login'))

@app.route("/admin/dashboard")
@login_required
@admin_required
def admin_dashboard():
    from models.medico_model import Medico
    from models.paciente_model import Paciente
    from models.consulta_model import Consulta
    from models.cita_model import Cita
    from models.usuario_model import Usuario
    
    total_medicos = len(Medico.get_all())
    total_pacientes = len(Paciente.get_all())
    total_consultas = len(Consulta.get_all())
    total_citas = len(Cita.get_all())
    total_usuarios = len(Usuario.get_all())
    
    return render_template('admin/dashboard.html',
                         total_medicos=total_medicos,
                         total_pacientes=total_pacientes,
                         total_consultas=total_consultas,
                         total_citas=total_citas,
                         total_usuarios=total_usuarios)

def crear_usuario_admin():
    from models.usuario_model import Usuario
    admin = Usuario.get_by_username("admin")
    if not admin:
        admin = Usuario("Administrador", "admin", "admin123", "admin")
        admin.save()
        print("Usuario admin creado - Usuario: admin, Password: admin123")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        crear_usuario_admin()
    app.run(debug=True)
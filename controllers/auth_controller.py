from flask import request, redirect, url_for, Blueprint, session, flash
from models.usuario_model import Usuario
from views import auth_view

auth_bp = Blueprint('auth', __name__, url_prefix="/auth")

@auth_bp.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        usuario = Usuario.get_by_username(username)
        if usuario and usuario.verify_password(password):
            session['usuario_id'] = usuario.id
            session['usuario_nombre'] = usuario.nombre
            session['rol'] = usuario.rol
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Usuario o contraseña incorrectos')
    
    return auth_view.login()

@auth_bp.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nombre = request.form['nombre']
        username = request.form['username']
        password = request.form['password']
        rol = request.form['rol']
        
        if Usuario.get_by_username(username):
            flash('El nombre de usuario ya existe')
            return auth_view.register()
        
        usuario = Usuario(nombre, username, password, rol)
        usuario.save()
        flash('Usuario registrado exitosamente')
        return redirect(url_for('auth.login'))
    
    return auth_view.register()

@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('auth.login'))
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from app import db, bcrypt
from app.models import User, Registro
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime

main = Blueprint('main', __name__, template_folder="templates", static_folder="static")

@main.route('/', methods=['GET'])
def index():
    return redirect(url_for('main.login_page'))

# Login page (form)
@main.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'GET':
        return render_template('login.html')
    username = request.form.get('username')
    password = request.form.get('password')
    if not username or not password:
        flash("Completa usuario y contraseña", "warning")
        return redirect(url_for('main.login_page'))
    user = User.query.filter_by(username=username).first()
    if user and bcrypt.check_password_hash(user.password, password):
        login_user(user)
        return redirect(url_for('main.dashboard'))
    flash("Credenciales inválidas", "danger")
    return redirect(url_for('main.login_page'))

# Register page (form)
@main.route('/register', methods=['GET', 'POST'])
def register_page():
    if request.method == 'GET':
        return render_template('register.html')
    username = request.form.get('username')
    password = request.form.get('password')
    if not username or not password:
        flash("Completa usuario y contraseña", "warning")
        return redirect(url_for('main.register_page'))
    if User.query.filter_by(username=username).first():
        flash("Usuario ya existe", "danger")
        return redirect(url_for('main.register_page'))
    pw_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(username=username, password=pw_hash)
    db.session.add(new_user)
    db.session.commit()
    flash("Usuario registrado correctamente. Inicia sesión.", "success")
    return redirect(url_for('main.login_page'))

# Dashboard (requires login)
@main.route('/dashboard')
@login_required
def dashboard():
    registros = Registro.query.filter_by(usuario_id=current_user.id).order_by(Registro.fecha_hora.desc()).all()
    return render_template('dashboard.html', registros=registros)

# Register entrada
@main.route('/registrar/entrada', methods=['POST'])
@login_required
def registrar_entrada():
    r = Registro(usuario_id=current_user.id, tipo='entrada', fecha_hora=datetime.utcnow())
    db.session.add(r)
    db.session.commit()
    flash("Entrada registrada", "success")
    return redirect(url_for('main.dashboard'))

# Register salida
@main.route('/registrar/salida', methods=['POST'])
@login_required
def registrar_salida():
    r = Registro(usuario_id=current_user.id, tipo='salida', fecha_hora=datetime.utcnow())
    db.session.add(r)
    db.session.commit()
    flash("Salida registrada", "success")
    return redirect(url_for('main.dashboard'))

# Historial (HTML or JSON)
@main.route('/historial')
@login_required
def historial():
    registros = Registro.query.filter_by(usuario_id=current_user.id).order_by(Registro.fecha_hora.desc()).all()
    if request.args.get('format') == 'json':
        return jsonify([{"tipo": r.tipo, "fecha_hora": r.fecha_hora.isoformat()} for r in registros])
    return render_template('dashboard.html', registros=registros)

# Logout
@main.route('/logout')
@login_required
def logout_page():
    logout_user()
    flash("Sesión cerrada", "info")
    return redirect(url_for('main.login_page'))

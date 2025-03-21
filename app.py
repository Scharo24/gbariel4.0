from dotenv import load_dotenv
import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime  # Importar datetime
from flask_migrate import Migrate  # Importar Migrate

# Cargar el archivo .env
load_dotenv()

app = Flask(__name__)
app.secret_key = 'clave_secreta'

# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://gbariel4_0_user:gsbycbcOVxEcEmRXF7gixjHiSuSXB5ya@dpg-cvev2mfnoe9s73baqku0-a.oregon-postgres.render.com/gbariel4_0')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar la base de datos y Flask-Migrate
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Modelo de usuario con roles
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)  # Cambiar a 255 caracteres
    rol = db.Column(db.String(20), nullable=False, default='usuario')

# ------------------------------------------------------------------------------------
# AQUI EMPIEZA EL MODELO INVENTARIO
# ------------------------------------------------------------------------------------
class Inventario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer)
    fecha_evento = db.Column(db.Date)  # Usar db.Date o db.DateTime según corresponda
    evento = db.Column(db.String(255))
    venue = db.Column(db.String(255))
    seccion = db.Column(db.String(255))
    fila = db.Column(db.String(255))
    cantidad_tk = db.Column(db.Integer)
    estado = db.Column(db.String(50))
    usuario = db.Column(db.String(50))
    informacion_compra = db.Column(db.Text)  # Usar db.Text para campos más largos
    target = db.Column(db.Text)
    comentarios = db.Column(db.Text)
    link = db.Column(db.String(255))
# ------------------------------------------------------------------------------------
# AQUI TERMINA EL MODELO INVENTARIO
# ------------------------------------------------------------------------------------

# Ruta de inicio - Redirige al panel si ya está logueado
@app.route('/')
def index():
    if 'user' in session:
        return redirect(url_for('panel_principal'))
    return render_template('login.html')

# Ruta para procesar el login
@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    if not username or not password:
        flash("⚠️ Debes completar todos los campos.", "warning")
        return redirect(url_for('index'))

    user = Usuario.query.filter_by(username=username).first()

    if not user:
        flash("❌ El usuario no existe. Regístrate primero.", "danger")
        return redirect(url_for('index'))

    if not check_password_hash(user.password_hash, password):
        flash("🔑 Contraseña incorrecta.", "danger")
        return redirect(url_for('index'))

    session['user'] = username
    session['rol'] = user.rol
    flash("✅ Inicio de sesión exitoso.", "success")
    return redirect(url_for('panel_principal'))

# Ruta de registro de usuarios
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            flash("⚠️ Debes completar todos los campos", "warning")
            return redirect(url_for('register'))

        existing_user = Usuario.query.filter_by(username=username).first()
        if existing_user:
            flash("⚠️ El usuario ya existe", "warning")
            return redirect(url_for('register'))

        password_hash = generate_password_hash(password)
        nuevo_usuario = Usuario(username=username, password_hash=password_hash, rol="usuario")

        db.session.add(nuevo_usuario)
        db.session.commit()

        flash("✅ Usuario registrado con éxito. Inicia sesión.", "success")
        return redirect(url_for('index'))

    return render_template('register.html')

# 🔹 **Panel Principal**
@app.route('/panel_principal')
def panel_principal():
    if 'user' not in session:
        flash("⚠️ Debes iniciar sesión primero", "warning")
        return redirect(url_for('index'))
    return render_template('panel_principal.html', user=session['user'], rol=session['rol'])

# 🔹 **Inventario**
@app.route('/inventario')
def inventario():
    if 'user' not in session:
        flash("⚠️ Debes iniciar sesión primero", "warning")
        return redirect(url_for('index'))

    # Obtener todos los registros del inventario de la base de datos
    inventario = Inventario.query.all()

    # Formatear la fecha para mostrarla en el template
    for item in inventario:
        if item.fecha_evento:
            item.fecha_evento = item.fecha_evento.strftime('%Y-%m-%d')  # Formato YYYY-MM-DD

    return render_template('inventario.html', inventario=inventario)

# 🔹 **Ingreso Masivo**
@app.route('/ingreso_masivo', methods=['GET', 'POST'])
def ingreso_masivo():
    if 'user' not in session:
        flash("⚠️ Debes iniciar sesión primero", "warning")
        return redirect(url_for('index'))

    if request.method == 'POST':
        evento = request.form.get('evento')
        venue = request.form.get('venue')
        estado = request.form.get('estado')
        cantidad_tk = request.form.get('cantidad_tk')
        fecha_evento = request.form.get('fecha_evento')
        link = request.form.get('link')
        secciones = request.form.getlist('secciones[]')
        targets = request.form.getlist('targets[]')
        comentarios = request.form.getlist('comentarios[]')

        # Simulación de procesamiento
        flash(f"✅ Se han ingresado {len(secciones)} secciones para el evento {evento}.", "success")
        return redirect(url_for('ingreso_masivo'))

    return render_template('ingreso_masivo.html')

# 🔹 **Estadísticas**
@app.route('/estadisticas')
def estadisticas():
    if 'user' not in session:
        flash("⚠️ Debes iniciar sesión primero", "warning")
        return redirect(url_for('index'))
    return render_template('estadisticas.html')

# 🔹 **Reportes**
@app.route('/reportes')
def reportes():
    if 'user' not in session:
        flash("⚠️ Debes iniciar sesión primero", "warning")
        return redirect(url_for('index'))
    return render_template('reportes.html')

# Ruta para cerrar sesión
@app.route('/logout')
def logout():
    session.pop('user', None)
    session.pop('rol', None)
    flash("ℹ️ Sesión cerrada", "info")
    return redirect(url_for('index'))

# Función para crear un usuario admin si no existe
def crear_admin():
    with app.app_context():
        admin = Usuario.query.filter_by(username="admin").first()
        if not admin:
            password_hash = generate_password_hash("admin")
            admin = Usuario(username="admin", password_hash=password_hash, rol="admin")
            db.session.add(admin)
            db.session.commit()
            print("👤 Usuario admin creado con éxito.")

# Ejecutar la aplicación
if __name__ == '__main__':
    with app.app_context():
        print("📌 Inicializando la base de datos...")
        db.create_all()
        crear_admin()  # Verifica si el admin existe, si no, lo crea
        print("✅ Base de datos lista.")
    
    # Asegúrate de que Flask esté corriendo en el puerto 8080 para Fly.io
    app.run(host="0.0.0.0", port=8080, debug=True)

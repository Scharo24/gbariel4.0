from app import db, app, Usuario
from werkzeug.security import generate_password_hash

def inicializar_bd():
    with app.app_context():
        db.create_all()  # Crea la base de datos si no existe
        print("✅ Base de datos creada correctamente.")

        # Verificar si el usuario admin ya existe
        admin = Usuario.query.filter_by(username="admin").first()
        if not admin:
            admin = Usuario(username="admin", password_hash=generate_password_hash("1234"), rol="admin")
            db.session.add(admin)
            db.session.commit()
            print("✅ Usuario 'admin' creado con éxito (contraseña: 1234).")
        else:
            print("ℹ️ Usuario 'admin' ya existe.")

if __name__ == "__main__":
    inicializar_bd()

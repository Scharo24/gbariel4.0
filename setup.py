from app import db, app, Usuario
from werkzeug.security import generate_password_hash
import os

def inicializar_bd():
    with app.app_context():
        db.create_all()  # Crea la base de datos si no existe
        print("✅ Base de datos creada correctamente.")

        # Verificar si el usuario admin ya existe
        admin = Usuario.query.filter_by(username="admin").first()
        if not admin:
            # Asegurarse de que la contraseña sea segura
            contraseña_segura = os.getenv('ADMIN_PASSWORD', '1234')  # Usar una contraseña más segura si está en el entorno
            admin = Usuario(username="admin", password_hash=generate_password_hash(contraseña_segura), rol="admin")
            db.session.add(admin)
            db.session.commit()
            print(f"✅ Usuario 'admin' creado con éxito (contraseña: {contraseña_segura}).")
        else:
            print("ℹ️ Usuario 'admin' ya existe.")

if __name__ == "__main__":
    inicializar_bd()

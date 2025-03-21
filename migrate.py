from app import app, db, crear_admin  # Importa app, db y la función crear_admin desde app.py

# Asegúrate de que las tablas estén creadas
with app.app_context():
    print("📌 Inicializando la base de datos...")
    db.create_all()  # Crea las tablas
    crear_admin()  # Verifica si el admin existe, si no, lo crea
    print("✅ Base de datos lista.")

import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# 1. Asegurar que Python encuentre la carpeta 'src'
sys.path.append(os.getcwd())

# 2. Importa las cosas 
from src.database.database import DATABASE_URL
from src.entities.user import User, Base 

# 3. Configuración de la conexión
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def run_seed():
    db = SessionLocal()
    try:
        print("Revisando datos iniciales en Neon...")
        
        # IDEMPOTENCIA: Buscamos si el admin ya existe para no duplicarlo 
        admin_email = "admin@admin.com"
        exists = db.query(User).filter(User.email == admin_email).first()
        
        if not exists:
            # Creamos el usuario por defecto 
            new_admin = User(
                email=admin_email,
                username="admin",
                password="123", 
                is_admin=True
            )
            db.add(new_admin)
            db.commit()
            print(">>> Seeder: Usuario administrador creado con éxito.")
        else:
            print(">>> Seeder: El usuario ya existe. No se realizaron cambios.")
            
    except Exception as e:
        print(f"Error al ejecutar el seeder: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    run_seed()
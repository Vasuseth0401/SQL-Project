
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

# --------------------------------
# Database Configuration
# --------------------------------

DB_USER = "root"
DB_PASSWORD = "Vds0401Mysql"
DB_HOST = "localhost"
DB_PORT = 3306
DB_NAME = "hospital_management"

# --------------------------------
# Database URL
# --------------------------------

DATABASE_URL = (
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# --------------------------------
# Create SQLAlchemy Engine
# --------------------------------

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=3600,
    echo=False
)

# --------------------------------
# Database Connection
# --------------------------------

def create_connection():
    try:
        return engine.connect()

    except SQLAlchemyError as e:
        print("Database connection failed:", e)
        return None

# --------------------------------
# Test Database Connection
# --------------------------------

def test_connection():

    connection = create_connection()

    if connection is None:
        return False

    try:
        connection.execute(text("SELECT 1"))
        print("MySQL Database Connected Successfully!")
        return True

    except SQLAlchemyError as e:
        print("Connection test failed:", e)
        return False

    finally:
        connection.close()

# --------------------------------
# Close Database Engine
# --------------------------------

def close_database():
    engine.dispose()

# --------------------------------
# Main Execution
# --------------------------------

if __name__ == "__main__":
    test_connection()

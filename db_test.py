import psycopg2
from psycopg2 import extensions

def test_postgres_connection():
    """Test superuser postgres connection"""
    try:
        conn = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="development_only",
            host="localhost",
            port="5432"
        )
        print("Postgres superuser connection successful!")
        conn.close()
    except Exception as e:
        print(f"Postgres Error: {str(e)}")

def test_cta_connection():
    """Test application cta user connection"""
    try:
        conn = psycopg2.connect(
            dbname="cta",
            user="cta",
            password="development_only",
            host="localhost",
            port="5432"
        )
        print("CTA user connection successful!")
        conn.close()
    except Exception as e:
        print(f"CTA Error: {str(e)}")

if __name__ == "__main__":
    test_postgres_connection()
    test_cta_connection() 
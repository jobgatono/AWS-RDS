import psycopg2
from datetime import date

# Replace with your actual RDS credentials
db_config = {
    'host': 'kagwandu-db.ch6waw068etj.us-east-1.rds.amazonaws.com',
    'dbname': 'kagwandu_enterprises',
    'user': 'kagwandu',
    'password': 'SockiDoha36',
    'port': '5432'
}

def connect_db():
    return psycopg2.connect(**db_config)

def create_tables(conn):
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS brands (
                brand_id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL
            );
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS models (
                model_id SERIAL PRIMARY KEY,
                brand_id INTEGER REFERENCES brands(brand_id),
                name VARCHAR(100) NOT NULL
            );
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS sales (
                sale_id SERIAL PRIMARY KEY,
                model_id INTEGER REFERENCES models(model_id),
                sale_date DATE NOT NULL,
                quantity INTEGER NOT NULL,
                price_per_unit NUMERIC(10,2) NOT NULL
            );
        """)
        conn.commit()
        print("✅ Tables created (if not already existing).")

def insert_sample_data(conn):
    with conn.cursor() as cur:
        # Insert brands
        cur.execute("INSERT INTO brands (name) VALUES (%s) RETURNING brand_id", ('Toyota',))
        toyota_id = cur.fetchone()[0]

        cur.execute("INSERT INTO brands (name) VALUES (%s) RETURNING brand_id", ('Honda',))
        honda_id = cur.fetchone()[0]

        # Insert models
        cur.execute("INSERT INTO models (name, brand_id) VALUES (%s, %s) RETURNING model_id", ('Corolla', toyota_id))
        corolla_id = cur.fetchone()[0]

        cur.execute("INSERT INTO models (name, brand_id) VALUES (%s, %s) RETURNING model_id", ('Civic', honda_id))
        civic_id = cur.fetchone()[0]

        # Insert sales
        cur.execute("""
            INSERT INTO sales (model_id, sale_date, quantity, price_per_unit)
            VALUES (%s, %s, %s, %s)
        """, (corolla_id, date.today(), 5, 23000.00))

        cur.execute("""
            INSERT INTO sales (model_id, sale_date, quantity, price_per_unit)
            VALUES (%s, %s, %s, %s)
        """, (civic_id, date.today(), 3, 21000.00))

        conn.commit()
        print("✅ Sample data inserted.")

def main():
    try:
        conn = connect_db()
        create_tables(conn)
        insert_sample_data(conn)
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    main()
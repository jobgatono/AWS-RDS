import psycopg2
import pandas as pd

# RDS connection config
db_config = {
    'host': 'kagwandu-db.ch6waw068etj.us-east-1.rds.amazonaws.com',
    'dbname': 'kagwandu_enterprises',
    'user': 'kagwandu',
    'password': 'SockiDoha36',
    'port': '5432'
}

def connect_db():
    return psycopg2.connect(**db_config)

def query_table(conn, table_name):
    cursor = conn.cursor()
    try:
        cursor.execute(f"SELECT * FROM {table_name} LIMIT 10;")
        rows = cursor.fetchall()
        colnames = [desc[0] for desc in cursor.description]

        print(f"\n📋 Data from '{table_name}':")
        print(pd.DataFrame(rows, columns=colnames))
    except Exception as e:
        print(f"❌ Error querying {table_name}: {e}")

def main():
    conn = connect_db()
    try:
        # Query all three tables
        for table in ['brands', 'models', 'sales']:
            query_table(conn, table)

    except Exception as e:
        print("❌ Error:", e)
    finally:
        conn.close()

if __name__ == "__main__":
    main()

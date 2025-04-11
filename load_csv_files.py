import psycopg2
import pandas as pd
import boto3
from io import StringIO

# RDS connection config
db_config = {
    'host': 'kagwandu-db.ch6waw068etj.us-east-1.rds.amazonaws.com',
    'dbname': 'kagwandu_enterprises',
    'user': 'kagwandu',
    'password': 'SockiDoha36',
    'port': '5432'
}

# S3 config
s3_config = {
    'bucket': 'gatunu-redshift-demo',  # Your bucket name
    'files': {
        'brands': 'car-sales/brands.csv',  # S3 key for the brands CSV file
        'models': 'car-sales/models.csv',  # S3 key for the models CSV file
        'sales': 'car-sales/sales.csv'     # S3 key for the sales CSV file
    }
}

# Connect to S3 and read CSV into a DataFrame
def read_csv_from_s3(bucket, key):
    s3 = boto3.client('s3')
    try:
        obj = s3.get_object(Bucket=bucket, Key=key)
        return pd.read_csv(StringIO(obj['Body'].read().decode('utf-8')))
    except Exception as e:
        print(f"❌ Error reading {key}: {e}")
        raise

# Connect to PostgreSQL RDS
def connect_db():
    return psycopg2.connect(**db_config)

# Insert DataFrame into PostgreSQL with conflict handling
def load_csv_to_table(conn, df, table_name):
    cursor = conn.cursor()
    for _, row in df.iterrows():
        cols = ', '.join(row.index)
        placeholders = ', '.join(['%s'] * len(row))
        values = tuple(row.values)

        # Define conflict columns based on the table
        conflict_col = 'sale_id' if table_name == 'sales' else \
                       'model_id' if table_name == 'models' else 'brand_id'

        query = f"""
        INSERT INTO {table_name} ({cols})
        VALUES ({placeholders})
        ON CONFLICT ({conflict_col}) DO NOTHING;
        """

        try:
            cursor.execute(query, values)
        except Exception as e:
            print(f"❌ Error inserting row into {table_name}: {e}")
            conn.rollback()  # Reset the failed transaction
            cursor = conn.cursor()  # Reset the cursor

    conn.commit()
    print(f"✅ Data inserted into '{table_name}'")
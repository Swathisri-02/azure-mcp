import psycopg2
import os
from dotenv import load_dotenv
from decimal import Decimal

load_dotenv()

def convert_to_json_serializable(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    return obj

def query_postgres(sql_query):
    try:
        conn = psycopg2.connect(
            host=os.getenv("PG_HOST"),
            port=os.getenv("PG_PORT"),
            dbname=os.getenv("PG_DB"),
            user=os.getenv("PG_USER"),
            password=os.getenv("PG_PASSWORD"),
            sslmode="require"
        )
        cur = conn.cursor()
        cur.execute(sql_query)
        rows = cur.fetchall()
        colnames = [desc[0] for desc in cur.description]

        results = [
            {
                col: convert_to_json_serializable(val)
                for col, val in zip(colnames, row)
            }
            for row in rows
        ]

        cur.close()
        conn.close()
        return results
    except Exception as e:
        return {"error": str(e)}
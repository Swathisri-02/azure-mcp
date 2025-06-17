import os
import openai
import psycopg2
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_table_schema(table_name):
    conn = psycopg2.connect(
        host=os.getenv("PG_HOST"),
        port=os.getenv("PG_PORT"),
        user=os.getenv("PG_USER"),
        password=os.getenv("PG_PASSWORD"),
        dbname=os.getenv("PG_DATABASE")
    )
    cursor = conn.cursor()
    cursor.execute("""
        SELECT column_name, data_type
        FROM information_schema.columns
        WHERE table_name = %s
        ORDER BY ordinal_position;
    """, (table_name,))
    columns = cursor.fetchall()
    cursor.close()
    conn.close()

    return f"{table_name}(\n" + ",\n".join([f"  {col} {dtype}" for col, dtype in columns]) + "\n)"

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def nl_to_sql(nl_query, table_schema):
    prompt = f"""
You are an expert SQL generator. Convert the natural language request into a SQL query using this schema:

{table_schema}

Request: "{nl_query}"
SQL:
"""
    res = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    return res.choices[0].message.content.strip()
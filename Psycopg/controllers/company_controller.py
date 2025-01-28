import psycopg2
import os
import flask


database_name = os.environ.get("DATABASE_NAME")

conn = psycopg2.connect(f"dbname={database_name}")
cursor = conn.cursor()

def create_company(company_name):
    cursor.execute("""
        INSERT INTO Companies
            (company_name)
            VALUES(%s)
        """,
        (company_name,)
    )


    conn.commit()
    return {"message": f'{company_name} has been added to the Company table.'}

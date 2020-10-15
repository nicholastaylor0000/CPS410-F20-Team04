import os
import psycopg2
import secrets

DATABASE_URL = os.environ['DATABASE_URL']

def task():

    conn = psycopg2.connect(DATABASE_URL, sslmode='require')

    cur = conn.cursor()

    cur.execute('SELECT id FROM museum_museum')

    for museum in cur.fetchall():
        pk, = museum
        cur.execute("""
            UPDATE museum_museum
            SET secret_key = %s
            WHERE id = %s;
            """,
            (secrets.token_hex(12), pk)
        )

    cur.close()
    conn.commit()
    conn.close()
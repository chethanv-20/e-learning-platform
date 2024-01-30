# domain.py
from database import connect_to_database

def get_all_domains():
    db = connect_to_database()
    cursor = db.cursor()

    try:
        # Fetch all domains from the database
        query = "SELECT * FROM domain"
        cursor.execute(query)
        domains = cursor.fetchall()

        return domains

    except Exception as e:
        return []

    finally:
        db.close()

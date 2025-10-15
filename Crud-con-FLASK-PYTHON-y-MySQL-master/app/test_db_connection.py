from conexionBD import connectionBD


def test_connection():
    try:
        db = connectionBD()
        cursor = db.cursor()
        cursor.execute("SHOW TABLES;")
        tables = cursor.fetchall()
        print("Tablas en la base de datos:")
        for t in tables:
            print(t)
        cursor.close()
        db.close()
        return True
    except Exception as e:
        print("Error conectando a la base de datos:", e)
        return False


if __name__ == '__main__':
    ok = test_connection()
    if ok:
        print("Conexión exitosa")
    else:
        print("Conexión fallida")

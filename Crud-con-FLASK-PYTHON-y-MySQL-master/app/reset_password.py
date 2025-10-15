import sys
from conexionBD import connectionBD
from werkzeug.security import generate_password_hash

USAGE = "Uso: python reset_password.py correo@ejemplo.com NuevaContraseña"


def reset_password(email, new_password):
    try:
        db = connectionBD()
        cur = db.cursor()
        hashed = generate_password_hash(new_password)
        cur.execute("UPDATE usuario SET `contraseña` = %s WHERE email = %s", (hashed, email))
        db.commit()
        if cur.rowcount == 0:
            print('No se encontró ningún usuario con ese email:', email)
        else:
            print('Contraseña actualizada correctamente para:', email)
        cur.close()
        db.close()
    except Exception as e:
        print('Error actualizando contraseña:', e)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print(USAGE)
        sys.exit(1)
    email = sys.argv[1]
    newpass = sys.argv[2]
    reset_password(email, newpass)

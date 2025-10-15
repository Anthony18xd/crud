from conexionBD import connectionBD
from werkzeug.security import generate_password_hash, check_password_hash


def crear_usuario(email, password):
    """Crea un usuario nuevo en la tabla `usuario`.
    Retorna True si se creó correctamente, False en caso de error.
    """
    try:
        db = connectionBD()
        cur = db.cursor()
        hashed = generate_password_hash(password)
        cur.execute("INSERT INTO usuario (email, `contraseña`) VALUES (%s, %s)", (email, hashed))
        db.commit()
        cur.close()
        db.close()
        return True
    except Exception as e:
        print('Error crear_usuario:', e)
        return False


def obtener_usuario_por_email(email):
    """Devuelve un dict con el usuario o None si no existe."""
    try:
        db = connectionBD()
        cur = db.cursor(dictionary=True)
        cur.execute("SELECT * FROM usuario WHERE email = %s", (email,))
        user = cur.fetchone()
        cur.close()
        db.close()
        return user
    except Exception as e:
        print('Error obtener_usuario_por_email:', e)
        return None


def verificar_credenciales(email, password):
    """Verifica email+password. Retorna el usuario (dict) si son correctas, sino None."""
    user = obtener_usuario_por_email(email)
    if not user:
        return None
    # La columna de la contraseña en tu BD es `contraseña` (con ñ).
    # Intentamos obtener esa clave directamente; si no existe, probamos otras claves comunes.
    hashed = None
    if 'contraseña' in user:
        hashed = user['contraseña']
    elif 'contrasena' in user:
        hashed = user['contrasena']
    elif 'password' in user:
        hashed = user['password']
    elif 'passwd' in user:
        hashed = user['passwd']

    if not hashed:
        return None

    try:
        if check_password_hash(hashed, password):
            return user
    except Exception as e:
        print('Error verificar_credenciales:', e)

    return None

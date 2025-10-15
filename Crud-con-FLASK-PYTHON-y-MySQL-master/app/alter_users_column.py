from conexionBD import connectionBD

ALTER_SQL = "ALTER TABLE `usuario` MODIFY COLUMN `contraseña` VARCHAR(255) NOT NULL;"


def run_alter():
    try:
        db = connectionBD()
        cur = db.cursor()
        cur.execute(ALTER_SQL)
        db.commit()
        print('ALTER TABLE ejecutado correctamente')
        cur.close()
        db.close()
    except Exception as e:
        print('Error ejecutando ALTER TABLE:', e)


if __name__ == '__main__':
    run_alter()

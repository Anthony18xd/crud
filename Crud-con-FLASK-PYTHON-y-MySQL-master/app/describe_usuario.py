from conexionBD import connectionBD

def describe_usuario():
    db = connectionBD()
    cur = db.cursor()
    cur.execute('DESCRIBE usuario')
    cols = cur.fetchall()
    for c in cols:
        print(c)
    cur.close()
    db.close()

if __name__ == '__main__':
    describe_usuario()

from flask import Flask, render_template, request, redirect, url_for, jsonify, session, flash
from controller.controllerCarro import *
from controller.controllerUser import crear_usuario, verificar_credenciales, obtener_usuario_por_email


#Para subir archivo tipo foto al servidor
import os
from werkzeug.utils import secure_filename 


#Declarando nombre de la aplicación e inicializando, crear la aplicación Flask
app = Flask(__name__)
application = app

# Secret key necesaria para sesiones y flash
app.secret_key = 'cambiar_por_una_clave_segura'

msg  =''
tipo =''


#Creando mi decorador para el home, el cual retornara la Lista de Carros
@app.route('/', methods=['GET','POST'])
def inicio():
    # Requerir que el usuario esté autenticado antes de mostrar los carros
    if not session.get('user'):
        # Si no está autenticado, redirigimos a registro para que se cree una cuenta primero
        return redirect(url_for('register'))

    return render_template('public/layout.html', miData = listaCarros())


#RUTAS
@app.route('/registrar-carro', methods=['GET','POST'])
def addCarro():
    return render_template('public/acciones/add.html')


 
#Registrando nuevo carro
@app.route('/carro', methods=['POST'])
def formAddCarro():
    if request.method == 'POST':
        marca               = request.form['marca']
        modelo              = request.form['modelo']
        year                = request.form['year']
        color               = request.form['color']
        puertas             = request.form['puertas']
        favorito            = request.form['favorito']
        
        
        if(request.files['foto'] !=''):
            file     = request.files['foto'] #recibiendo el archivo
            nuevoNombreFile = recibeFoto(file) #Llamado la funcion que procesa la imagen
            resultData = registrarCarro(marca, modelo, year, color, puertas, favorito, nuevoNombreFile)
            if(resultData ==1):
                return render_template('public/layout.html', miData = listaCarros(), msg='El Registro fue un éxito', tipo=1)
            else:
                return render_template('public/layout.html', msg = 'Metodo HTTP incorrecto', tipo=1)   
        else:
            return render_template('public/layout.html', msg = 'Debe cargar una foto', tipo=1)
            


@app.route('/form-update-carro/<string:id>', methods=['GET','POST'])
def formViewUpdate(id):
    if request.method == 'GET':
        resultData = updateCarro(id)
        if resultData:
            return render_template('public/acciones/update.html',  dataInfo = resultData)
        else:
            return render_template('public/layout.html', miData = listaCarros(), msg='No existe el carro', tipo= 1)
    else:
        return render_template('public/layout.html', miData = listaCarros(), msg = 'Metodo HTTP incorrecto', tipo=1)          
 
   
  
@app.route('/ver-detalles-del-carro/<int:idCarro>', methods=['GET', 'POST'])
def viewDetalleCarro(idCarro):
    msg =''
    if request.method == 'GET':
        resultData = detallesdelCarro(idCarro) #Funcion que almacena los detalles del carro
        
        if resultData:
            return render_template('public/acciones/view.html', infoCarro = resultData, msg='Detalles del Carro', tipo=1)
        else:
            return render_template('public/acciones/layout.html', msg='No existe el Carro', tipo=1)
    return redirect(url_for('inicio'))
    

@app.route('/actualizar-carro/<string:idCarro>', methods=['POST'])
def  formActualizarCarro(idCarro):
    if request.method == 'POST':
        marca           = request.form['marca']
        modelo          = request.form['modelo']
        year            = request.form['year']
        color           = request.form['color']
        puertas         = request.form['puertas']
        favorito        = request.form['favorito']
        
        # Verificar si se envió una foto
        foto_carro = None
        if 'foto' in request.files and request.files['foto'].filename != '':
            file = request.files['foto']
            foto_carro = recibeFoto(file)

        # Llamar a la función para actualizar el carro
        resultData = recibeActualizarCarro(
            marca, modelo, year, color, puertas, favorito, foto_carro, idCarro
        )
        
        if(resultData ==1):
            return render_template('public/layout.html', miData = listaCarros(), msg='Datos del carro actualizados', tipo=1)
        else:
            return render_template('public/layout.html', miData = listaCarros(), msg='No se pudo actualizar', tipo=1)


#Eliminar carro
@app.route('/borrar-carro', methods=['GET', 'POST'])
def formViewBorrarCarro():
    if request.method == 'POST':
        idCarro         = request.form['id']
        nombreFoto      = request.form['nombreFoto']
        resultData      = eliminarCarro(idCarro, nombreFoto)

        if resultData ==1:
            #Nota: retorno solo un json y no una vista para evitar refescar la vista
            return jsonify([1])
            #return jsonify(["respuesta", 1])
        else: 
            return jsonify([0])




def eliminarCarro(idCarro='', nombreFoto=''):
        
    conexion_MySQLdb = connectionBD() #Hago instancia a mi conexion desde la funcion
    cur              = conexion_MySQLdb.cursor(dictionary=True)
    
    cur.execute('DELETE FROM carros WHERE id=%s', (idCarro,))
    conexion_MySQLdb.commit()
    resultado_eliminar = cur.rowcount #retorna 1 o 0
    #print(resultado_eliminar)
    
    basepath = os.path.dirname (__file__) #C:\xampp\htdocs\localhost\Crud-con-FLASK-PYTHON-y-MySQL\app
    url_File = os.path.join (basepath, 'static/assets/fotos_carros', nombreFoto)
    os.remove(url_File) #Borrar foto desde la carpeta
    #os.unlink(url_File) #Otra forma de borrar archivos en una carpeta
    

    return resultado_eliminar



def recibeFoto(file):
    basepath = os.path.dirname (__file__) #La ruta donde se encuentra el archivo actual
    filename = secure_filename(file.filename) #Nombre original del archivo

    #capturando extensión del archivo ejemplo: (.png, .jpg, .pdf ...etc)
    extension           = os.path.splitext(filename)[1]
    nuevoNombreFile     = stringAleatorio() + extension
    #print(nuevoNombreFile)
        
    upload_path = os.path.join (basepath, 'static/assets/fotos_carros', nuevoNombreFile) 
    file.save(upload_path)

    return nuevoNombreFile


# RUTAS DE AUTENTICACIÓN
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        if not email or not password:
            flash('Email y contraseña son requeridos', 'danger')
            return redirect(url_for('register'))

        # Verificar si ya existe
        if obtener_usuario_por_email(email):
            flash('El usuario ya existe', 'warning')
            return redirect(url_for('register'))

        ok = crear_usuario(email, password)
        if ok:
            # Auto-login: obtener el usuario recien creado y guardar en sesión
            user = obtener_usuario_por_email(email)
            if user:
                session['user'] = {'id': user.get('id'), 'email': user.get('email')}
            flash('Cuenta creada correctamente. Has iniciado sesión.', 'success')
            return redirect(url_for('inicio'))
        else:
            flash('Error creando la cuenta', 'danger')
            return redirect(url_for('register'))

    return render_template('public/register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = verificar_credenciales(email, password)
        if user:
            session['user'] = {'id': user.get('id'), 'email': user.get('email')}
            flash('Has iniciado sesión', 'success')
            return redirect(url_for('inicio'))
        else:
            flash('Credenciales incorrectas', 'danger')
            return redirect(url_for('login'))

    return render_template('public/login.html')


@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('Sesión cerrada', 'info')
    return redirect(url_for('inicio'))

       
  
  
#Redireccionando cuando la página no existe
@app.errorhandler(404)
def not_found(error):
    return redirect(url_for('inicio'))
    
    
    
    
if __name__ == "__main__":
    app.run(debug=True, port=8000)
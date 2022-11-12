from flask import Flask,render_template,redirect,url_for,jsonify,request,flash,session
from flask_bootstrap import Bootstrap
import requests
from suds.client import Client
app=Flask(__name__)
Bootstrap(app)
app.secret_key='MyCla4ve'
#URL de los servicios
url_servicio="http://172.16.1.148:8000/"
url_wsdl="http://localhost:8090/TitulaTECSOAP/AlumnoService?WSDL"

#seccion de usuarios
@app.route('/')
def inicio():
    return render_template('usuarios/login.html')
@app.route('/usuarios/alumnos/nuevo')
def nuevoAlumno():
    return render_template('usuarios/registro.html')
@app.route('/principal')
def principal():
    return render_template('comunes/principal.html')
@app.route('/usuarios/login',methods=['POST'])
def login():
    datos={"email":request.form['email'],"password":request.form['password']}
    url_alumno=url_servicio+'alumnos/autenticar'
    respuesta=requests.get(url_alumno,json=datos).json()
    if respuesta['estatus']=='Ok':
        session['usuario']=respuesta['alumno']
        return redirect(url_for("principal"))
    else:
        flash(respuesta['mensaje'])
        return redirect(url_for("inicio"))
@app.route('/cerrarSesion')
def cerrarSesion():
    session.clear()
    return redirect(url_for("inicio"))
#fin de seccion
#seccion de opciones
@app.route('/opciones')
def consultaOpciones():
    url_opciones=url_servicio+'opciones'
    respuesta=requests.get(url_opciones).json()
    print(respuesta)
    if respuesta['estatus']=='OK'  and respuesta['mensaje']=="Listado de Opciones":

        return render_template('opciones/listar.html',opciones=respuesta['opciones'])
    else:
        flash(respuesta['mensaje'])
        return render_template('opciones/listar.html')
#fin de seccion
#seccion de solicitudes
@app.route('/solicitudes')
def consultaSolicitudes():
    url_solicitudes=url_servicio+'Solicitudes/alumno/'+str(session['usuario'].get('id'))
    respuesta=requests.get(url_solicitudes).json()
    print(respuesta)
    if respuesta['estatus'] == 'OK' and respuesta['mensaje'] == "Listado de Solicitudes":
        return render_template('solicitudes/listar.html',solicitudes=respuesta['solicitudes'])
    else:
        flash(respuesta['mensaje'])
        return render_template('solicitudes/listar.html')
@app.route('/solicitudes/nueva')
def nuevaSolicitud():
    url_opciones = url_servicio + 'opciones'
    respuesta = requests.get(url_opciones).json()
    if respuesta['estatus'] == 'OK' and respuesta['mensaje'] == "Listado de Opciones":
        return render_template('solicitudes/crear.html',opciones=respuesta['opciones'])
    else:
        flash(respuesta['mensaje'])
        return render_template('solicitudes/crear.html')
@app.route('/solicitudes/registrar',methods=['POST'])
def registrarSolicitud():
    url_solicitudess=url_servicio+'Solicitudes'
    datos={"tituloProyecto":request.form['proyecto'],"opcion":request.form['opcion'],"alumno":session['usuario'].get('id')}
    respuesta=requests.post(url_solicitudess,json=datos).json()
    flash(respuesta['mensaje'])
    return redirect(url_for('nuevaSolicitud'))
@app.route('/solicitudes/editar/<int:id>')
def editarSolicitud(id):
    url_solicitudes = url_servicio + 'Solicitudes/'+str(id)
    respuesta=requests.get(url_solicitudes).json()
    if respuesta['estatus']=='OK':
        url_opciones = url_servicio + 'opciones'
        respuesta2 = requests.get(url_opciones).json()
        return render_template('solicitudes/editar.html',solicitud=respuesta['solicitud'],opciones=respuesta2['opciones'])
    else:
        flash(respuesta['mensaje'])
        return render_template('solicitudes/editar.html')
@app.route('/solicitudes/modificar',methods=['POST'])
def modificarSolicitud():
    url_solicitudes=url_servicio+'Solicitudes'
    datos={"idSolicitud":int(request.form['id']),"tituloProyecto":request.form['proyecto'],"estatus":"",
           "opcion":request.form['opcion'],"administrativo":0,"tipoUsuario":"E"}
    print(datos)
    respuesta=requests.put(url_solicitudes,json=datos).json()
    flash(respuesta['mensaje'])
    return redirect(url_for('editarSolicitud',id=request.form['id']))
@app.route('/solicitudes/eliminar/<id>')
def eliminarSolicitud(id):
    url_solicitudes = url_servicio + 'Solicitudes/'+id
    respuesta = requests.delete(url_solicitudes).json()
    flash(respuesta['mensaje'])
    return redirect(url_for('consultaSolicitudes'))
#fin de seccion
#seccion de alumnos
@app.route('/alumnos/consultar/<nocontrol>',methods=['get'])
def consultarAlumno(nocontrol):
    clienteWS=Client(url_wsdl)
    #print(clienteWS)
    respuesta=clienteWS.service.consultarAlumno(nocontrol)
    salida={"estatus":"","mensaje":""}
    if "noControl" in respuesta:
        salida['estatus']="OK"
        salida['mensaje'] = "Alumno identificado"
        #print(respuesta)
        alumno={"noControl":respuesta.noControl,"nombre":respuesta.nombre,
                "sexo":respuesta.sexo,"telefono":respuesta.telefono,
                "email":respuesta.email,"creditos":respuesta.credito,
                "idCarrera":respuesta.idCarrera,"carrera":respuesta.nombreCarrera
                }
        salida['alumno'] = alumno
    else:
        salida['estatus'] = "Error"
        salida['mensaje'] = "No se encontro al alumno."
    print(salida)
    return jsonify(salida)
@app.route('/alumnos/registrar',methods=['post'])
def registrarAlumno():
    url = url_servicio+'alumnos'
    nombre=request.form['nombre']
    sexo=request.form['sexo']
    telefono=request.form['telefono']
    email=request.form['email']
    password=request.form['password']
    nocontrol=request.form['nocontrol']
    anioEgreso=request.form['anio']
    creditos=request.form['creditos']
    idCarrera=request.form['idCarrera']
    dict_alumno={"nombre":nombre,"sexo":sexo,"telefono":telefono,"email":email,
                 "password":password,"nocontrol":nocontrol,"anioEgreso":anioEgreso,
                 "creditos":creditos,"idCarrera":idCarrera}
    respuesta = requests.post(url,json=dict_alumno).json()
    flash(respuesta['mensaje'])
    return redirect(url_for('nuevoAlumno'))
#fin de seccion

if __name__=='__main__':
    app.run(debug=True)
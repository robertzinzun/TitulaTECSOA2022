from flask import Flask,request
from model import db,Opcion,Solicitud, Alumno

import json
app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://titulatec_soa:Hola.123@localhost/TitulaTEC_SOA'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


@app.route('/')
def inicio():
    respuesta={"estatus":"OK","mensaje":"Escuchando los Servicios REST"}
    return json.dumps(respuesta)

@app.route('/opciones',methods=['GET'])
def consultarOpciones():
    opcion=Opcion()
    return opcion.consultaGeneral();

@app.route('/Solicitudes',methods=['POST'])
def agregarSolicitud():
    sol=Solicitud()
    json=request.get_json()
    return sol.agregar(json)

@app.route('/Solicitudes',methods=['PUT'])
def modificarSolicitud():
    sol = Solicitud()
    json = request.get_json()
    return sol.modificar(json)

@app.route('/Solicitudes/<int:id>',methods=['DELETE'])
def eliminarSolicitud(id):
    sol = Solicitud()
    return sol.eliminar(id)

@app.route('/Solicitudes',methods=['GET'])
def consultaSolicitudes():
    sol = Solicitud()
    return sol.consultaGeneral()

@app.route('/Solicitudes/<int:id>',methods=['GET'])
def consultaSolicitud(id):
    sol = Solicitud()
    return sol.consultaIndividual(id)

@app.route('/Solicitudes/alumno/<int:id>',methods=['GET'])
def consultaSolicitudesPorAlumno(id):
    sol = Solicitud()
    return sol.consultaPorAlumno(id)

@app.route('/alumnos',methods=['post'])
def agregarAlumno():
    ojson=request.get_json()
    a=Alumno()
    return a.agregar(ojson)

@app.route('/alumnos/autenticar',methods=['GET'])
def autenticar():
    datos=request.get_json()
    alumno=Alumno()
    salida=alumno.autenticar(datos)
    return salida

if __name__=='__main__':
    db.init_app(app)
    app.run(debug=True,host='0.0.0.0',port=8000)
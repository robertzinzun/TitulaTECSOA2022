from flask import Flask,request
from model import db,Opcion,Solicitud

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

if __name__=='__main__':
    db.init_app(app)
    app.run(debug=True,host='0.0.0.0',port=8000)
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import INTEGER,String,Column
import json
db=SQLAlchemy()

class Opcion(db.Model):
    __tablename__='opciones'
    idOpcion=db.Column(INTEGER,primary_key=True)
    nombre=db.Column(String(80),nullable=False)
    descripcion=db.Column(String(200),nullable=False)
    estatus=db.Column(String(1),nullable=False)

    #Consulta general de las opciones
    def consultaGeneral(self):
        respuesta = {"estatus": "", "mensaje": ""}
        try:
            lista=self.query.all()#select * from opciones
            if len(lista)>0:
                respuesta['estatus']='OK'
                respuesta['mensaje']='Listado de Opciones'
                listaJson = []
                for o in lista:
                    listaJson.append(self.toJson(o))
                respuesta['opciones']=listaJson
            else:
                respuesta['estatus'] = 'OK'
                respuesta['mensaje'] = 'No existen opciones registradas'

        except:
            respuesta['estatus'] = 'Error'
            respuesta['mensaje'] = 'Error en la ejecucion de la consulta'
        return respuesta

    def toJson(self,opcion):
        dict_json={"idOpcion":opcion.idOpcion,"nombre":opcion.nombre,"descripcion":opcion.descripcion}
        return dict_json

class Solicitud(db.Model):
    __tablename__='Solicitudes'
    idSolicitud=Column(INTEGER,primary_key=True)
    def agregar(self,json):
        respuesta={"estatus":"OK","mensaje":"Prueba"}
        db.session.execute('call sp_registrar_solicitud(:tituloProyecto,:opcion,:alumno,@p_estatus,@p_mensaje)',json)
        db.session.commit();
        salida=db.session.execute('select @p_estatus,@p_mensaje').fetchone()
        respuesta['estatus']=salida[0]
        respuesta['mensaje'] = salida[1]
        return respuesta



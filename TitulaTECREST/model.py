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
            lista=self.all()#select * from opciones
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
        respuesta={"estatus":"","mensaje":""}
        db.session.execute('call sp_registrar_solicitud(:tituloProyecto,:opcion,:alumno,@p_estatus,@p_mensaje)',json)
        db.session.commit();
        salida=db.session.execute('select @p_estatus,@p_mensaje').fetchone()
        respuesta['estatus']=salida[0]
        respuesta['mensaje'] = salida[1]
        return respuesta

    def modificar(self,json):
        respuesta = {"estatus": "", "mensaje": ""}
        db.session.execute('call sp_modificar_solicitud(:idSolicitud,:tituloProyecto,:estatus,:opcion,:administrativo,:tipoUsuario,@p_estatus,@p_mensaje)', json)
        db.session.commit();
        salida = db.session.execute('select @p_estatus,@p_mensaje').fetchone()
        respuesta['estatus'] = salida[0]
        respuesta['mensaje'] = salida[1]
        return respuesta

    def eliminar(self,idSolicitud):
        respuesta = {"estatus": "", "mensaje": ""}
        data={"p_idSolicitud":idSolicitud}
        db.session.execute('call sp_eliminar_solicitud(:p_idSolicitud,@p_estatus,@p_mensaje)', data)
        db.session.commit();
        salida = db.session.execute('select @p_estatus,@p_mensaje').fetchone()
        respuesta['estatus'] = salida[0]
        respuesta['mensaje'] = salida[1]
        return respuesta

    def consultaGeneral(self):
        respuesta = {"estatus": "", "mensaje": ""}
        try:
            rs=db.session.execute("select * from vSolicitudes")

            lista=[]
            for row in rs:
                lista.append(self.toJson(row))
            if len(lista)>0:
                respuesta['estatus'] = "OK"
                respuesta['mensaje'] = "Listado de Solicitudes"
                respuesta["solicitudes"]=lista
            else:
                respuesta['estatus'] = "OK"
                respuesta['mensaje'] = "No hay Solicitudes registradas"
        except:
            respuesta['estatus'] = "Error"
            respuesta['mensaje'] = "Error al ejecutar la consulta de solicitudes"
        return respuesta

    def toJson(self,solicitud):
        dict_sol={"administrativo":"","alumno":"","carrera":"","estatus":solicitud[7],
                  "fechaAtencion":solicitud[5],"fechaRegistro":solicitud[6],"id":solicitud[0],
                  "opcion":"","proyecto":solicitud[4]}
        dict_admin={"id":solicitud[10],"nombre":solicitud[11]}
        dict_alumno = {"NC": solicitud[2], "nombre": solicitud[3]}
        dict_carrera = {"id": solicitud[12], "nombre": solicitud[13]}
        dict_opcion = {"id": solicitud[8], "nombre": solicitud[9]}
        dict_sol["administrativo"]=dict_admin
        dict_sol["alumno"] = dict_alumno
        dict_sol["carrera"] = dict_carrera
        dict_sol["opcion"] = dict_opcion
        return dict_sol


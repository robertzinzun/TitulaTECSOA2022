from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import INTEGER,String,Column,ForeignKey
from sqlalchemy.orm import relationship
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

    def consultaIndividual(self,id):
        respuesta = {"estatus": "", "mensaje": ""}
        data={"id":id}
        try:
            row = db.session.execute("select * from vSolicitudes where idSolicitud=:id",data);
            respuesta['estatus'] = "OK"
            row=row.fetchone()
            if row!=None:
                respuesta['mensaje'] = "Listado de Solicitud"
                respuesta["solicitud"] =self.toJson(row)
            else:
                respuesta['mensaje'] = "La solicitud no existe"
        except:
            respuesta['estatus'] = "Error"
            respuesta['mensaje'] = "Error al ejecutar la consulta de solicitudes"
        return respuesta

    def consultaPorAlumno(self,idAlumno):
        respuesta = {"estatus": "", "mensaje": ""}
        data={"id":idAlumno}
        try:
            rs = db.session.execute("select * from vSolicitudes where idAlumno=:id", data);
            respuesta['estatus'] = "OK"
            lista = []
            for row in rs:
                lista.append(self.toJson(row))

            if len(lista)>0:
                respuesta['mensaje'] = "Listado de Solicitudes"
                respuesta["solicitudes"] = lista
            else:
                respuesta['mensaje'] = "El alumno no tiene solicitudes registradas"
        except:
            respuesta['estatus'] = "Error"
            respuesta['mensaje'] = "Error al ejecutar la consulta de solicitudes"
        return respuesta

    def toJson(self,solicitud):
        dict_sol={"administrativo":"","alumno":"","carrera":"","estatus":solicitud[7],
                  "fechaAtencion":solicitud[6],"fechaRegistro":solicitud[5],"id":solicitud[0],
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
#Clases para la manipulación de alumnos
class Usuario(db.Model):
    __tablename__='Usuarios'
    idUsuario=Column(INTEGER,primary_key=True)
    nombre=Column(String(100),nullable=False)
    sexo=Column(String,nullable=False)
    telefono=Column(String(12),nullable=False)
    email=Column(String(100),unique=True)
    password=Column(String(20),nullable=False)
    tipo=Column(String,nullable=False,default='E')
    estatus=Column(String,nullable=False,default='A')

class Alumno(db.Model):
    __tablename__='Alumnos'
    idAlumno=Column(INTEGER,primary_key=True)
    noControl=Column(String(9),unique=True)
    anioEgreso=Column(INTEGER,nullable=False)
    creditos=Column(INTEGER,nullable=False)
    estatus=Column(String,nullable=False,default='E')
    idUsuario=Column(INTEGER,ForeignKey('Usuarios.idUsuario'))
    idCarrera=Column(INTEGER,nullable=False)
    usuario=relationship(Usuario,lazy='select')

    def agregar(self, ojson):
        dict_salida = {"estatus": "", "mensaje": ""}
        try:
            self.from_json(ojson)
            db.session.add(self.usuario)
            db.session.add(self)
            db.session.commit()
            dict_salida['estatus'] = 'Ok'
            dict_salida["mensaje"] = 'Alumno registrado con exito'
        except:
            db.session.rollback()
            dict_salida['estatus'] = 'Error'
            dict_salida["mensaje"] = 'Error al registrar al alumno'
        return json.dumps(dict_salida)

    def from_json(self, ojson):
        usuario = Usuario()
        usuario.nombre = ojson['nombre']
        usuario.sexo = ojson['sexo']
        usuario.telefono = ojson['telefono']
        usuario.email = ojson['email']
        usuario.password = ojson['password']
        self.usuario = usuario
        self.noControl = ojson['nocontrol']
        self.anioEgreso = ojson['anioEgreso']
        self.creditos = ojson['creditos']
        self.idCarrera = ojson['idCarrera']

    def autenticar(self,json):
        respuesta = {"estatus": "", "mensaje": ""}
        try:
            rs = db.session.execute("select * from vAlumnos where email=:email and password=:password and estatus='E'",
                                    json);
            row = rs.fetchone()
            if row != None:
                respuesta['estatus'] = 'Ok'
                respuesta['mensaje'] = "Alumno identificado"
                respuesta["alumno"] = self.toJson(row)
            else:
                respuesta['estatus'] = 'Error'
                respuesta['mensaje'] = "Datos incorrectos"
        except:
            respuesta['estatus'] = "Error"
            respuesta['mensaje'] = "Error al ejecutar la autenticación"
        return respuesta

    def toJson(self,res):
        dict_json={
            "anioEgreso": res[5], "carrera": res[10], "creditos": res[4], "email": res[7],
            "estatus": res[11], "id": res[0],"noControl": res[1], "nombre": res[2],
            "sexo": res[3],"telefono": res[6]
        }
        return dict_json



from flask import Flask,render_template,redirect,url_for
from flask_bootstrap import Bootstrap

app=Flask(__name__)
Bootstrap(app)
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
    return redirect(url_for("principal"))
@app.route('/opciones')
def consultaOpciones():
    return render_template('opciones/listar.html')
@app.route('/solicitudes')
def consultaSolicitudes():
    return render_template('solicitudes/listar.html')
@app.route('/solicitudes/nueva')
def nuevaSolicitud():
    return render_template('solicitudes/crear.html')
@app.route('/solicitudes/editar')
def editarSolicitud():
    return render_template('solicitudes/editar.html')
if __name__=='__main__':
    app.run(debug=True)
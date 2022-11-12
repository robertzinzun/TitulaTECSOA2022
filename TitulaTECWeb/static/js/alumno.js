function mensaje(){
    alert('JS cargado');
}

function consultarAlumno(){
    var ajax=new XMLHttpRequest();
    var nocontrol=document.getElementById("nocontrol").value;
    var url='/alumnos/consultar/'+nocontrol;
    ajax.open('get',url,true);
    ajax.onreadystatechange=function(){
        if(this.readyState==4 && this.status==200 ){
            llenarCampos(this.responseText);
        }
    };
    ajax.send();
}
function llenarCampos(respuesta){
    var resp=JSON.parse(respuesta);
    if(resp.estatus!="Error"){
        alumno=resp.alumno;
        document.getElementById("nombre").value=alumno.nombre;
        document.getElementById("telefono").value=alumno.telefono;
        document.getElementById("email").value=alumno.email;
        document.getElementById("creditos").value=alumno.creditos;
        document.getElementById("idCarrera").value=alumno.idCarrera;
        document.getElementById("nombreCarrera").value=alumno.carrera;
        if(alumno.sexo=='M'){
            document.getElementById('f').removeAttribute('checked');
            document.getElementById('m').setAttribute('checked',true);
        }
        else{
            document.getElementById('m').removeAttribute('checked');
            document.getElementById('f').setAttribute('checked',true);    
        }
        document.getElementById("registrar").removeAttribute('disabled');
    }
    else{
        document.getElementById("registrar").setAttribute('disabled',true);
        alert(resp.mensaje);
    }
}
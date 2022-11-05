/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package modelo;

import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;

/**
 *
 * @author roberto
 */
public class AlumnoDAO {
    public Alumno consultar(String noControl){
        String query="select noControl, nombre_completo,sexo,promedio,credito,idCarrera,nombre_carrera,idEstatus,"
                + "estatus,telefono,email from vAlumno where noControl=?";
        Alumno alumno=new Alumno();
        try{
            PreparedStatement comando=Conexion.getInstance().getConnection().prepareStatement(query);
            comando.setString(1, noControl);
            ResultSet rs=comando.executeQuery();
            if(rs.next()){
                alumno.setNoControl(rs.getString("noControl"));
                alumno.setNombre(rs.getString("nombre_completo"));
                alumno.setSexo(rs.getString("sexo"));
                alumno.setPromedio(rs.getFloat("promedio"));
                alumno.setCredito(rs.getInt("creditos"));
                alumno.setIdCarrera(rs.getInt("idCarrera"));
                alumno.setNombreCarrera(rs.getString("nombre_carrera"));
                alumno.setIdEstatus(rs.getInt("idEstatus"));
                alumno.setEstatus(rs.getString("estatus"));
                alumno.setTelefono(rs.getString("telefono"));
                alumno.setEmail(rs.getString("email"));      
            }
            rs.close();
            comando.close();
            Conexion.getInstance().cerrar();
            
        }
        catch(SQLException e){
            System.out.println("Error:"+e.getMessage());
        }
        return alumno;
    }
}

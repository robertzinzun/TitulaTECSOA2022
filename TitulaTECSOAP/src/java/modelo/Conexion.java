/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package modelo;

import java.sql.Connection;
import java.sql.SQLException;
import java.util.logging.Level;
import java.util.logging.Logger;
import javax.naming.Context;
import javax.naming.InitialContext;
import javax.naming.NamingException;
import javax.sql.DataSource;

/**
 *
 * @author roberto
 */
public class Conexion {
    private static Conexion conexion;
    private Connection connection; 
    private Conexion(){
        try {
            Context  ctx=new InitialContext();
            DataSource ds=(DataSource) ctx.lookup("java:app/jdbc/SIE");
            connection=ds.getConnection();
        } catch (NamingException ex) {
            Logger.getLogger(Conexion.class.getName()).log(Level.SEVERE, null, ex);
        } catch (SQLException ex) {
            Logger.getLogger(Conexion.class.getName()).log(Level.SEVERE, null, ex);
        }
    }
    public static Conexion getInstance(){
        if(conexion==null)
            conexion=new Conexion();
        return conexion;
    }
    public Connection getConnection(){
        return connection;
    }
    public void cerrar(){
        try {
            connection.close();
            conexion=null;
        } catch (SQLException ex) {
            Logger.getLogger(Conexion.class.getName()).log(Level.SEVERE, null, ex);
        }
    }
}

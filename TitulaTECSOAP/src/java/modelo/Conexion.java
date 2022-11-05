/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package modelo;

import java.sql.Connection;
import java.sql.DriverManager;
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
    private String url="jdbc:sqlserver://10.211.55.3\\SQL12DEV:1433;databaseName=SIE_DB";
    private Conexion(){
        try{
            Class.forName("com.microsoft.sqlserver.jdbc.SQLServerDriver");
            connection=DriverManager.getConnection(url,"SIE_USER","SIE.123");
            System.out.println("Conectado...");
        }
        catch(ClassNotFoundException e){
            System.out.println("Error al cargar el driver de SQLServer"
                    +e.getMessage());
        } catch (SQLException ex) {
            System.out.println("Error al realizarr la conexion"+ex.getMessage());
            
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

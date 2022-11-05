/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package clienteservicioweb;

import ClienteServicio.Alumno;

/**
 *
 * @author roberto
 */
public class ClienteServicioWeb {

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        // TODO code application logic here
        System.out.println(consultarAlumno("14010003").getNoControl());
    }

    private static Alumno consultarAlumno(java.lang.String noControl) {
        ClienteServicio.SIEService_Service service = new ClienteServicio.SIEService_Service();
        ClienteServicio.SIEService port = service.getSIEServicePort();
        return port.consultarAlumno(noControl);
    }
    
}

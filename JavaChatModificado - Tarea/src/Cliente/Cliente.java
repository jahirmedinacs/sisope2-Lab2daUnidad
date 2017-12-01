/*
 * Cliente.java
 *
 * Created on 21 de marzo de 2008, 12:11 PM
 *
 * To change this template, choose Tools | Template Manager
 * and open the template in the editor.
 */

package Cliente;

import java.io.*;
import java.net.*;
import java.util.Vector;
import java.util.logging.Level;
import java.util.logging.Logger;
import javax.swing.JOptionPane;

/**
 *
 * @author Administrador
 */
public class Cliente
{
   public static String IP_SERVER;
   VentCliente vent;
   DataInputStream entrada = null;
   DataOutputStream salida = null;
   DataInputStream entrada2 = null;
   Socket comunication = null;//para la comunicacion
   Socket comunication2 = null;//para recivir msg
   
   String nomCliente;
   /** Creates a new instance of Cliente */
   public Cliente(VentCliente vent) throws IOException
   {      
      this.vent=vent;
   }
   
   public void conexion() throws IOException 
   {
      try {
         comunication = new Socket(Cliente.IP_SERVER, 8081);
         comunication2 = new Socket(Cliente.IP_SERVER, 8082);
         entrada = new DataInputStream(comunication.getInputStream());
         salida = new DataOutputStream(comunication.getOutputStream());
         entrada2 = new DataInputStream(comunication2.getInputStream());
         nomCliente = JOptionPane.showInputDialog("Introducir Nick :");
         vent.setNombreUser(nomCliente);         
         salida.writeUTF(nomCliente);
      } catch (IOException e) {
         System.out.println("\tEl servidor no esta levantado");
         System.out.println("\t=============================");
      }
      new threadCliente(entrada2, vent).start();
   }
   public String getNombre()
   {
      return nomCliente;
   }
   public Vector<String> pedirUsuarios()
   {
      Vector<String> users = new Vector();
      try {         
         salida.writeInt(2);
         int numUsers=entrada.readInt();
         for(int i=0;i<numUsers;i++)
            users.add(entrada.readUTF());
      } catch (IOException ex) {
         Logger.getLogger(Cliente.class.getName()).log(Level.SEVERE, null, ex);
      }
      return users;
   }
   public void flujo(String mens) 
   {
      try {             
         System.out.println("el mensaje enviado desde el cliente es :"
             + mens);
         salida.writeInt(1);
         salida.writeUTF(mens);
      } catch (IOException e) {
         System.out.println("error...." + e);
      }
   }
   public void flujo2(String mens) 
   {
      try {             
         System.out.println("el mensaje enviado desde el cliente es :"
             + mens);
         salida.writeInt(4);
         salida.writeUTF(mens);
      } catch (IOException e) {
         System.out.println("error...." + e);
      }
   }   
   public void flujo(String amigo,String mens) 
   {
      try {             
         System.out.println("el mensaje enviado desde el cliente es :"
             + mens);
         salida.writeInt(3);//opcion de mensage a amigo
         salida.writeUTF(amigo);
         salida.writeUTF(mens);
      } catch (IOException e) {
         System.out.println("error...." + e);
      }
   }
   public void flujo3(int puntaje) 
   {
      try {             
         System.out.println("el mensaje enviado desde el cliente es :"
             +puntaje);
         salida.writeInt(7);//opcion de mensage a amigo
         salida.writeInt(puntaje);
      } catch (IOException e) {
         System.out.println("error...." + e);
      }
   }
   public void flujo4() 
   {
      try {             
         System.out.println("el mensaje enviado desde el cliente es :"
             +8);
         salida.writeInt(8);
      } catch (IOException e) {
         System.out.println("error...." + e);
      }
   }
   
   public void factorial(String mens){
       try {
         int n = Integer.parseInt( mens.substring(3) );
         System.out.println("Se solicita el factorial de"
             + Integer.toString(n));
         salida.writeInt(5);//opcion de mensage a amigo
         salida.writeUTF(this.getNombre());
         salida.writeUTF(Integer.toString(n));
      } catch (IOException e) {
         System.out.println("error...." + e);
      }
   }
   
   public void obtenerHora(){
       try {
         System.out.println("Se solicita la hora al servidor");
         salida.writeInt(6);//opcion de mensage a amigo
         salida.writeUTF(this.getNombre());
      } catch (IOException e) {
         System.out.println("error...." + e);
      }
   }
  
}

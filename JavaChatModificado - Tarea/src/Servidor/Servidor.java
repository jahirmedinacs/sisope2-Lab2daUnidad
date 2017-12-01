/*
 * Server.java
 *
 * Created on 21 de marzo de 2008, 12:02 PM
 *
 * To change this template, choose Tools | Template Manager
 * and open the template in the editor.
 */

package Servidor;

/**
 *
 * @author Administrador
 */
import java.awt.*;
import java.io.*;
import java.net.*;
import java.util.*;
import javax.swing.*;

class Servidor extends JFrame
{
   JTextArea txaMostrar;
   public Servidor()
   {
      super("Consola servidor");
      txaMostrar=new JTextArea();      
    
      this.setContentPane(new JScrollPane(txaMostrar));
      setSize(350,350);
      setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
      setVisible(true);      
      
   }
   public void mostrar(String msg)
   {
      txaMostrar.append(msg+"\n");
   }
   public void runServer()
   {
      ServerSocket serv=null;//para comunicacion
      ServerSocket serv2=null;//para enviar mensajes
      boolean listening=true;
      try{
         serv=new ServerSocket(8081);
         serv2=new ServerSocket(8082);
         mostrar(".::Servidor activo :");
         while(listening)
         {
            Socket sock=null,sock2=null;
            try {
               mostrar("Esperando Usuarios");
               sock=serv.accept();
               sock2=serv2.accept();
            } catch (IOException e)
            {
               mostrar("Accept failed: " + serv + ", " + e.getMessage());
               continue;
            }
            threadServidor user=new threadServidor(sock,sock2,this);            
	    user.start();
         }
         
      }catch(IOException e){
         mostrar("error :"+e);
      }
   }
   
   public static void main(String abc[]) throws IOException
   {                
     Servidor ser= new Servidor();
     ser.runServer(); 
   }
}




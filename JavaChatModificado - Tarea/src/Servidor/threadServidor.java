/*
 * threadServidor.java
 *
 * Created on 23 de marzo de 2008, 19:36
 *
 * To change this template, choose Tools | Template Manager
 * and open the template in the editor.
 */

package Servidor;

import java.awt.*;
import java.io.*;
import java.net.*;
import java.util.*;
import javax.swing.*;

/**
 *
 * @author Administrador
 */
public class threadServidor extends Thread
{
     Socket scli=null;
     Socket scli2=null;
     DataInputStream entrada=null;
     DataOutputStream salida=null;
     DataOutputStream salida2=null;
     public static Vector<threadServidor> clientesActivos=new Vector();	
     String nameUser;
     int puntaje;
     Servidor serv;
     
     public threadServidor(Socket scliente,Socket scliente2,Servidor serv)
     {
        scli=scliente;
        scli2=scliente2;
        this.serv=serv;
        nameUser="";
        clientesActivos.add(this);        
        serv.mostrar("cliente agregado: "+this);			
     }
     
     public String getNameUser()
     {
       return nameUser;
     }
     
     public void setNameUser(String name)
     {
       nameUser=name;
     }
     
     public void run()
     {
    	serv.mostrar(".::Esperando Mensajes :");
    	
    	try
    	{
          entrada=new DataInputStream(scli.getInputStream());
          salida=new DataOutputStream(scli.getOutputStream());
          salida2=new DataOutputStream(scli2.getOutputStream());
          this.setNameUser(entrada.readUTF());
          enviaUserActivos();
    	}
    	catch (IOException e) {  e.printStackTrace();     }
    	
        int opcion=0,numUsers=0;
        String amigo="",mencli="";
                
    	while(true)
    	{
          try
          {
             opcion=entrada.readInt();
             switch(opcion)
             {
                case 1://envio de mensage a todos
                   mencli=entrada.readUTF();
                   serv.mostrar("mensaje recibido "+mencli);
                   enviaMsg(mencli);
                   break;
                case 2://envio de lista de activos
                   numUsers=clientesActivos.size();
                   salida.writeInt(numUsers);
                   for(int i=0;i<numUsers;i++)
                      salida.writeUTF(clientesActivos.get(i).nameUser);
                   break;
                case 3: // envia mensage a uno solo
                   amigo=entrada.readUTF();//captura nombre de amigo
                   mencli=entrada.readUTF();//mensage enviado
                   enviaMsg(amigo,mencli);
                   break;
                case 4://envio de color de fondo a todos
                   mencli=entrada.readUTF();
                   serv.mostrar("mensaje recibido "+mencli);
                   enviaFondo(mencli);
                   break;
                   
                case 5://Retornar factorial
                    amigo=entrada.readUTF();
                    mencli=entrada.readUTF();
                    serv.mostrar("Numero Recibido" + mencli + " ; Calculando Factorial");
                    enviarFactorial(amigo,Integer.parseInt(mencli));
                    break;
                
                case 6://Retornar horas
                    amigo=entrada.readUTF();
                    serv.mostrar("Solicitud de Hora Recibida");
                    enviarHora(amigo);
                    break;    
                   
                case 7://recibe puntaje
                    puntaje=entrada.readInt();
                    break;
                case 8:
                    threadServidor user=null;
                    int mayor=-1;
                    String ganador="";
                    try
                        {                            
                        for(int i=0;i<clientesActivos.size();i++)
                        {
                            user=clientesActivos.get(i);
                            if(mayor<user.puntaje)
                            {
                                mayor=user.puntaje; 
                                ganador=user.getNameUser();
                            }
                        }
                        user.salida2.writeInt(8);//opcion de mensage 
                        user.salida2.writeUTF(ganador);              
                       }catch (IOException e) {e.printStackTrace();}
                    break;
              }                  
          }
          catch (IOException e) {System.out.println("El cliente termino la conexion");break;}
    	}
    	serv.mostrar("Se removio un usuario");
    	clientesActivos.removeElement(this);
    	try
    	{
          serv.mostrar("Se desconecto un usuario");
          scli.close();
    	}	
        catch(Exception et)
        {serv.mostrar("no se puede cerrar el socket");}   
     }
     
     public void enviaMsg(String mencli2)
     {
        threadServidor user=null;
        for(int i=0;i<clientesActivos.size();i++)
        {
           serv.mostrar("MENSAJE DEVUELTO:"+mencli2);
           try
            {
              user=clientesActivos.get(i);
              user.salida2.writeInt(1);//opcion de mensage 
              user.salida2.writeUTF(""+this.getNameUser()+" >"+ mencli2);              
            }catch (IOException e) {e.printStackTrace();}
        }
     }
     public void enviaFondo(String mencli2)
     {
        threadServidor user=null;
        for(int i=0;i<clientesActivos.size();i++)
        {
           serv.mostrar("MENSAJE DEVUELTO:"+mencli2);
           try
            {
              user=clientesActivos.get(i);
              user.salida2.writeInt(4);//opcion de mensaje 
              user.salida2.writeUTF(mencli2);              
            }catch (IOException e) {e.printStackTrace();}
        }
     }

     public void enviaUserActivos()
     {
        threadServidor user=null;
        for(int i=0;i<clientesActivos.size();i++)
        {           
           try
            {
              user=clientesActivos.get(i);
              if(user==this)continue;//ya se lo envie
              user.salida2.writeInt(2);//opcion de agregar 
              user.salida2.writeUTF(this.getNameUser());	
            }catch (IOException e) {e.printStackTrace();}
        }
     }

   private void enviaMsg(String amigo, String mencli) 
   {
      threadServidor user=null;
        for(int i=0;i<clientesActivos.size();i++)
        {           
           try
            {
              user=clientesActivos.get(i);
              if(user.nameUser.equals(amigo))
              {
                 user.salida2.writeInt(3);//opcion de mensage amigo   
                 user.salida2.writeUTF(this.getNameUser());
                 user.salida2.writeUTF(""+this.getNameUser()+">"+mencli);
              }
            }catch (IOException e) {e.printStackTrace();}
        }
   }
   
   private void enviarHora(String amigo) 
   {
      threadServidor user=null;
        for(int i=0;i<clientesActivos.size();i++)
        {           
           try
            {
              user=clientesActivos.get(i);
              if(user.nameUser.equals(amigo))
              {
                 user.salida2.writeInt(3);//opcion de mensage amigo   
                 user.salida2.writeUTF(this.getNameUser());
                 user.salida2.writeUTF(" HORA SERVIDOR >\t" + AuxilarMethods.time().toString());
              }
            }catch (IOException e) {e.printStackTrace();}
        }
   }
   
   private void enviarFactorial(String amigo, int n) 
   {
      threadServidor user=null;
        for(int i=0;i<clientesActivos.size();i++)
        {           
           try
            {
              user=clientesActivos.get(i);
              if(user.nameUser.equals(amigo))
              {
                 user.salida2.writeInt(3);//opcion de mensage amigo   
                 user.salida2.writeUTF(this.getNameUser());
                 user.salida2.writeUTF(" Factorial de " + Integer.toString(n)+
                         " >\t" + Integer.toString(AuxilarMethods.Factorial(n)));
              }
            }catch (IOException e) {e.printStackTrace();}
        }
   }
   
}
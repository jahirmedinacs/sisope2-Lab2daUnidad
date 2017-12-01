/*
 * Cliente.java
 *
 * Created on 12 de marzo de 2008, 06:06 AM
 *
 * To change this template, choose Tools | Template Manager
 * and open the template in the editor.
 */

package Cliente;

import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.Font;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.*;
import java.net.Socket;
import java.util.Vector;
import javax.swing.*;
import javax.swing.border.Border;
import javax.swing.JOptionPane.*;
import java.math.*;

/**
 * 
 * @author Administrador
 */
public class VentCliente extends JFrame implements ActionListener {
     String mensajeCliente;
     JTextArea panMostrar;
     JTextField txtMensage;
     JButton butEnviar;
     JButton butTirarDado;
     JButton butVerGanador;
     JLabel lblNomUser;
     JList lstActivos;
     JButton butPrivado;
     Cliente cliente;	
     
      
      JMenuBar barraMenu;
      JMenu JMAyuda;
      JMenuItem help;
      JMenu JMAcerca;
      JMenu JFondo;
      JMenuItem rojo,verde,azul;
      JMenuItem acercaD;
      VentanaAyuda va;
      
      JOptionPane AcercaDe;
     
     Vector<String> nomUsers;
     VentPrivada ventPrivada;
     /** Creates a new instance of Cliente */
     public VentCliente() throws IOException {
             super("Cliente Chat");
             txtMensage = new JTextField(30);
             butEnviar = new JButton("Enviar");
             butTirarDado = new JButton("Tirar Dado");
             butVerGanador = new JButton("Ver Ganador");
             
             lblNomUser = new JLabel("Usuario <<  >>");
             lblNomUser.setHorizontalAlignment(JLabel.CENTER);
             panMostrar = new JTextArea();             
             panMostrar.setColumns(25);
             txtMensage.addActionListener(this);
             butEnviar.addActionListener(this);
             butTirarDado.addActionListener(this);
             butVerGanador.addActionListener(this);
             lstActivos=new JList();             
             butPrivado=new JButton("Privado");
             butPrivado.addActionListener(this);
             
             barraMenu=new JMenuBar();
             JMAyuda=new JMenu("Ayuda");
             help=new JMenuItem("Ayuda");
             help.setActionCommand("help");
             help.addActionListener(this);
             
             JFondo=new JMenu("Fondo");
             rojo=new JMenuItem("Rojo");
             rojo.setActionCommand("Frojo");
             rojo.addActionListener(this);
             verde=new JMenuItem("Verde");
             verde.setActionCommand("Fverde");
             verde.addActionListener(this);
             azul=new JMenuItem("Azul");
             azul.setActionCommand("Fazul");
             azul.addActionListener(this);
             
             JMAcerca=new JMenu("Acerca de");
             acercaD=new JMenuItem("Creditos");
             acercaD.setActionCommand("Acerca");
             acercaD.addActionListener(this);
             
             JMAyuda.add(help);
             JMAcerca.add(acercaD);
             JFondo.add(rojo);
             JFondo.add(verde);
             JFondo.add(azul);
             barraMenu.add(JMAcerca);
             barraMenu.add(JMAyuda); 
             barraMenu.add(JFondo);
             
             
             panMostrar.setEditable(false);            
             panMostrar.setForeground(Color.BLUE);
             panMostrar.setBorder(javax.swing.BorderFactory.createMatteBorder(3,3,3,3,new Color(25,10,80)));		

             JPanel panAbajo = new JPanel();
             panAbajo.setLayout(new BorderLayout());
                panAbajo.add(new JLabel("  Ingrese mensage a enviar:"),BorderLayout.NORTH);
                panAbajo.add(txtMensage, BorderLayout.CENTER);
                panAbajo.add(butEnviar, BorderLayout.EAST);
                panAbajo.add(butTirarDado,BorderLayout.NORTH);
                panAbajo.add(butVerGanador,BorderLayout.SOUTH);
             JPanel panRight = new JPanel();
             panRight.setLayout(new BorderLayout());
                panRight.add(lblNomUser, BorderLayout.NORTH);
                panRight.add(new JScrollPane(panMostrar), BorderLayout.CENTER);
                panRight.add(panAbajo,BorderLayout.SOUTH);
             JPanel panLeft=new JPanel();
             panLeft.setLayout(new BorderLayout());
               panLeft.add(new JScrollPane(this.lstActivos),BorderLayout.CENTER);
               panLeft.add(this.butPrivado,BorderLayout.NORTH);
             JSplitPane sldCentral=new JSplitPane();  
             sldCentral.setDividerLocation(100);
             sldCentral.setDividerSize(7);
             sldCentral.setOneTouchExpandable(true);
               sldCentral.setLeftComponent(panLeft);
               sldCentral.setRightComponent(panRight);
             
             
             setLayout(new BorderLayout());
             add(sldCentral, BorderLayout.CENTER);   
             add(barraMenu,BorderLayout.NORTH);
             
             txtMensage.requestFocus();//pedir el focus	
             
             cliente=new Cliente(this);
             cliente.conexion();     
             nomUsers=new Vector();
             ponerActivos(cliente.pedirUsuarios());
             
             ventPrivada=new VentPrivada(cliente);
                  
             setSize(450, 430);
             setLocation(120, 90);
             setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);				
             setVisible(true);
     }
     
     public void setNombreUser(String user)
     {
        lblNomUser.setText("Usuario " + user);
     }
     public void mostrarMsg(String msg)
     {
        this.panMostrar.append(msg+"\n");
     }
     public void ponerActivos(Vector datos)
     {
        nomUsers=datos;
        ponerDatosList(this.lstActivos,nomUsers);
     }
     public void agregarUser(String user)
     {
        nomUsers.add(user);
        ponerDatosList(this.lstActivos,nomUsers);
     }
     public void cambiarFondo(String color)
     {
        if(color.compareTo("rojo")==0)
            panMostrar.setBackground(Color.RED);
        if(color.compareTo("verde")==0)
            panMostrar.setBackground(Color.GREEN);
        if(color.compareTo("azul")==0)
            panMostrar.setBackground(Color.BLUE);
     }

     public void retirraUser(String user)
     {        
        nomUsers.remove(user);
        ponerDatosList(this.lstActivos,nomUsers);
     }
    private void ponerDatosList(JList list,final Vector datos)
    {
        list.setModel(new AbstractListModel() {            
            @Override
            public int getSize() { return datos.size(); }
            @Override
            public Object getElementAt(int i) { return datos.get(i); }
        });
    }
    @Override
     public void actionPerformed(ActionEvent evt) {
         
       String comand=(String)evt.getActionCommand();
        if(comand.compareTo("help")==0)
        {
                va=new VentanaAyuda();
                va.setVisible(true);
                
        }
        if(comand.compareTo("Frojo")==0)
        {
                cliente.flujo2("rojo");
        }
        if(comand.compareTo("Fverde")==0)
        {
                cliente.flujo2("verde");
        }
        if(comand.compareTo("Fazul")==0)
        {
                cliente.flujo2("azul");
        }
       if(comand.compareTo("Acerca")==0)
       {   
           JOptionPane.showMessageDialog(this,"Informática\n USE:"
                   + "\n\t @!f seguido de un numero natural para calcular factorial"
                   + "\n\t @!h para obtener la hora del servidor","Escuela de",JOptionPane.INFORMATION_MESSAGE);           
       }
        if(evt.getSource()==this.butEnviar || evt.getSource()==this.txtMensage)
        {  
            String subSequence = "";
            Boolean do_factorial = false;
            Boolean do_hour = false;
            try{
                subSequence += this.txtMensage.getText().substring(0, 3);
                
                if(subSequence.equals("@!f")){
                    /* */
                    
                    try{
                        Integer.parseInt(this.txtMensage.getText().substring(3));
                        do_factorial = true;
                    } catch(NumberFormatException e){
                        
                    }
                     /* */     
                }
                else if(subSequence.equals("@!h")){
                    /* */        
                    
                    do_hour = true;
                    
                    /* */     
                }
                
            } catch (IndexOutOfBoundsException  e) {
                
            }
            
           if(do_factorial){
               /* */
               String mensaje = txtMensage.getText();        
               cliente.factorial(mensaje);
               txtMensage.setText("");
                /* */     
           }
           else if(do_hour){
               /* */        
               cliente.obtenerHora();
               txtMensage.setText("");
               /* */     
           }
           else{
               String mensaje = txtMensage.getText();        
               cliente.flujo(mensaje);
               txtMensage.setText("");  
           }
        }
        
        else if(evt.getSource()==this.butPrivado)
        {
           int pos=this.lstActivos.getSelectedIndex();
           if(pos>=0)              
           {
              ventPrivada.setAmigo(nomUsers.get(pos));           
              ventPrivada.setVisible(true);
           }
        }
        else if(evt.getSource()==this.butTirarDado)
        {
            int puntaje;
            puntaje = (int) (Math.random()*6+1);
            System.out.println("El dado salio"+puntaje);
            cliente.flujo3(puntaje);
        }
        else if(evt.getSource()==this.butVerGanador)
        {
           cliente.flujo4();
        }
     }
     
     public void mensageAmigo(String amigo,String msg)
     {
        ventPrivada.setAmigo(amigo);           
        ventPrivada.mostrarMsg(msg);        
        ventPrivada.setVisible(true);
     }

     public static void main(String args[]) throws IOException {
             Cliente.IP_SERVER = JOptionPane.showInputDialog("Introducir IP_SERVER :","localhost");
             VentCliente p = new VentCliente();
     }

    private void and(boolean b) {
        throw new UnsupportedOperationException("Not supported yet."); //To change body of generated methods, choose Tools | Templates.
    }
}

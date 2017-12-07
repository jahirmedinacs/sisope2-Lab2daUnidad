/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

package Cliente;
import java.awt.BorderLayout;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.WindowEvent;
import java.awt.event.WindowListener;
import javax.swing.*;
/**
 *
 * @author Administrador
 */
public class VentPrivada extends JFrame implements ActionListener
{
   JTextArea panMostrar;
   JTextField txtMensage;
   JButton butEnviar;
   
   Cliente cliente;
   String amigo;
   
   public VentPrivada(Cliente cliente)
   {
      super("Amigo");
      this.cliente=cliente;
      txtMensage = new JTextField(30);
      butEnviar = new JButton("Enviar");
      panMostrar = new JTextArea(); 
      panMostrar.setEditable(false);
      txtMensage.requestFocus();
      txtMensage.addActionListener(this);
      butEnviar.addActionListener(this);
      
      JPanel panAbajo = new JPanel();
             panAbajo.setLayout(new BorderLayout());
             panAbajo.add(new JLabel("  Ingrese mensage a enviar:"),
                                BorderLayout.NORTH);
             panAbajo.add(txtMensage, BorderLayout.CENTER);
             panAbajo.add(butEnviar, BorderLayout.EAST);
      
      setLayout(new BorderLayout());
      add(new JScrollPane(panMostrar),BorderLayout.CENTER);
      add(panAbajo,BorderLayout.SOUTH);
       
      amigo="";
      
      this.addWindowListener(new WindowListener()
      {         
         public void windowClosing(WindowEvent e) {
            cerrarVentana();
         }
         public void windowClosed(WindowEvent e) {}         
         public void windowOpened(WindowEvent e) {}
         public void windowIconified(WindowEvent e) {}
         public void windowDeiconified(WindowEvent e) {}
         public void windowActivated(WindowEvent e) {}
         public void windowDeactivated(WindowEvent e) {}
        
      });
      
      setSize(300,300);
      setLocation(570,90);      			      
   }
   public void setAmigo(String ami)
   {      
      this.amigo=ami;
      this.setTitle(ami);      
   }
    private void cerrarVentana() 
    {       
      this.setVisible(false);      
    }
    public void mostrarMsg(String msg)
     {
        this.panMostrar.append(msg+"\n");
     }
    
   @Override
   public void actionPerformed(ActionEvent e) 
   {
      String mensaje = txtMensage.getText();              
      mostrarMsg(cliente.getNombre()+">"+mensaje);
      cliente.flujo(amigo,mensaje);
      txtMensage.setText("");
   }
}

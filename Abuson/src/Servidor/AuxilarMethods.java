package Servidor;

import java.time.LocalTime;
import java.time.temporal.ChronoUnit;

/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

/**
 *
 * @author coitu
 */
public class AuxilarMethods {

    public AuxilarMethods() {
    }
    
    public static int Factorial(int n){
        int acumulador = 1;
        for(int i=0; i < n; i++){
            acumulador *= (i+1);
        }
        return acumulador;
    }
    
    public static LocalTime time() {
    LocalTime ldt = java.time.LocalTime.now();

    ldt = ldt.truncatedTo(ChronoUnit.MINUTES);
    System.out.println(ldt);
    return ldt;
}
}

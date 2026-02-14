/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package com.pucp.ui.model;

/**
 *
 * @author fmenesest
 */
public class Alumno {
    private String codigoAlumno;
    private String nombreCurso;
    private String observacion;
    
    public Alumno(String codigoAlumno, String nombreCurso, String observacion){
        this.codigoAlumno = codigoAlumno;
        this.nombreCurso = codigoCurso;
        this.observacion = observacion;
    }

    public String getCodigoAlumno() {
        return codigoAlumno;
    }

    public void setCodigoAlumno(String codigoAlumno) {
        this.codigoAlumno = codigoAlumno;
    }

    public String getNombreCurso() {
        return nombreCurso;
    }

    public void setNombreCurso(String codigoCurso) {
        this.nombreCurso = codigoCurso;
    }

    public String getObservacion() {
        return observacion;
    }

    public void setObservacion(String observacion) {
        this.observacion = observacion;
    }
}

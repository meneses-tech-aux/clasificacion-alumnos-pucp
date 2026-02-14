package com.pucp.ui.service;

import com.pucp.ui.model.Alumno;
import okhttp3.OkHttpClient;

import java.util.List;

public class PostAlumnosRobot {
    // URL DE API PARA ENVIAR A FLASK API LOCAL
    private static final String API_URL = "http://localhost:5000";
    private final OkHttpClient client = new OkHttpClient();

    public void enviarAlumnosARobot(List<Alumno> alumnos){
        // Construir el JSON "["II169157", "Inglés Básico 2", "Observación de prueba para alumno 1 II169157"]
        StringBuilder jsonBuilder = new StringBuilder();
        for (int i = 0; i < alumnos.size(); i++) {
            Alumno a = alumnos.get(i);
            jsonBuilder.append("[").append("\"").append(a.getNombreCurso()).append("\",").append("\n");
        }
    }
}

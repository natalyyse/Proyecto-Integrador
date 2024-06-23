package com.miempresa.servicio;

import java.time.ZonedDateTime;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpMethod;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.miempresa.modelo.Comentario;

@Service
public class ComentarioService {

    @Autowired
    private RestTemplate restTemplate;

    private static final String API_URL = "https://hols.pythonanywhere.com/api/comentarios/";
    private static final ObjectMapper objectMapper = new ObjectMapper();
    private static final DateTimeFormatter formatoEntrada = DateTimeFormatter.ISO_OFFSET_DATE_TIME;
    private static final DateTimeFormatter formatoSalida = DateTimeFormatter.ofPattern("dd/MM/yyyy HH:mm");

    public void enviarComentario(Comentario comentario) {
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);

        try {
            String requestBody = objectMapper.writeValueAsString(comentario);
            HttpEntity<String> requestEntity = new HttpEntity<>(requestBody, headers);

            ResponseEntity<String> responseEntity = restTemplate.exchange(
                    API_URL,
                    HttpMethod.POST,
                    requestEntity,
                    String.class
            );

            if (responseEntity.getStatusCode().is2xxSuccessful()) {
                System.out.println("Comentario enviado exitosamente");
            } else {
                System.out.println("Error al enviar el comentario: " + responseEntity.getStatusCode());
                System.out.println(responseEntity.getBody());
            }
        } catch (Exception e) {
            System.out.println("Error al enviar el comentario: " + e.getMessage());
        }
    }

    public List<Comentario> obtenerTodosLosComentarios() {
        Comentario[] comentariosArray = restTemplate.getForObject(API_URL, Comentario[].class);
        List<Comentario> comentarios = new ArrayList<>(Arrays.asList(comentariosArray));

        for (Comentario comentario : comentarios) {
            try {
                ZonedDateTime fechaComentario = ZonedDateTime.parse(comentario.getFecha(), formatoEntrada);
                String fechaFormateada = fechaComentario.format(formatoSalida);
                comentario.setFecha(fechaFormateada);
            } catch (Exception e) {
                e.printStackTrace();
            }
        }

        return comentarios;
    }
}

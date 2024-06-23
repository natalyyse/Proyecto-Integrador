package com.miempresa.servicio;

import java.util.Arrays;
import java.util.List;

import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import com.miempresa.modelo.Entrada;

@Service
public class EntradaService {
    private final RestTemplate restTemplate;

    public EntradaService(RestTemplate restTemplate) {
        this.restTemplate = restTemplate;
    }

    public List<Entrada> obtenerEntradas() {
        String url = "https://hols.pythonanywhere.com/api/entradas/";
        ResponseEntity<Entrada[]> respuesta = restTemplate.getForEntity(url, Entrada[].class);
        Entrada[] entradas = respuesta.getBody();
        return Arrays.asList(entradas);
    }
}

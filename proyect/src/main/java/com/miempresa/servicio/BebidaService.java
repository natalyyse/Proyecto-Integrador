package com.miempresa.servicio;

import java.util.Arrays;
import java.util.List;

import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import com.miempresa.modelo.Bebida;

@Service
public class BebidaService {
    private final RestTemplate restTemplate;

    public BebidaService(RestTemplate restTemplate) {
        this.restTemplate = restTemplate;
    }

    public List<Bebida> obtenerBebidas() {
        String url = "https://hols.pythonanywhere.com/api/bebidas/";
        ResponseEntity<Bebida[]> respuesta = restTemplate.getForEntity(url, Bebida[].class);
        Bebida[] bebidas = respuesta.getBody();

        return Arrays.asList(bebidas);
    }
}

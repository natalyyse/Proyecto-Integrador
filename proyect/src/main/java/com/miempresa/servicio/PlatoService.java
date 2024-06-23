package com.miempresa.servicio;

import java.util.Arrays;
import java.util.List;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;
import com.miempresa.modelo.Plato;

@Service
public class PlatoService {
    private final RestTemplate restTemplate;

    public PlatoService(RestTemplate restTemplate) {
        this.restTemplate = restTemplate;
    }

    public List<Plato> obtenerPlatos() {
        String url = "https://hols.pythonanywhere.com/api/platos/";
        ResponseEntity<Plato[]> respuesta = restTemplate.getForEntity(url, Plato[].class);
        Plato[] platos = respuesta.getBody();
        return Arrays.asList(platos);
    }
}
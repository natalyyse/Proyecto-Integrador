package com.miempresa.servicio;

import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.miempresa.modelo.Contacto;

@Service
public class ContactoService {

    private final RestTemplate restTemplate;
    private final String apiUrl = "https://hols.pythonanywhere.com/api/contactanos/";

    public ContactoService(RestTemplate restTemplate) {
        this.restTemplate = restTemplate;
    }

    public void guardarContacto(Contacto contacto) {
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);
        headers.add("Accept", MediaType.APPLICATION_JSON_VALUE);

        ObjectMapper objectMapper = new ObjectMapper();
        try {
            String requestBody = objectMapper.writeValueAsString(contacto);
            HttpEntity<String> requestEntity = new HttpEntity<>(requestBody, headers);
            restTemplate.postForObject(apiUrl, requestEntity, Void.class);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}




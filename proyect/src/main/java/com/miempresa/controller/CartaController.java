package com.miempresa.controller;


import com.miempresa.modelo.Entrada;
import com.miempresa.modelo.Plato;
import com.miempresa.modelo.Bebida;
import com.miempresa.servicio.EntradaService;
import com.miempresa.servicio.PlatoService;
import com.miempresa.servicio.BebidaService;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;

import java.util.List;

@Controller
public class CartaController {
    private final EntradaService entradaService;
    private final PlatoService platoService;
    private final BebidaService bebidaService;

    public CartaController(EntradaService entradaService, PlatoService platoService, BebidaService bebidaService) {
        this.entradaService = entradaService;
        this.platoService = platoService;
        this.bebidaService = bebidaService;
    }

    @GetMapping("/carta")
    public String getCarta(Model model) {
        List<Entrada> entradas = entradaService.obtenerEntradas();
        List<Plato> platos = platoService.obtenerPlatos();
        List<Bebida> bebidas = bebidaService.obtenerBebidas();
        model.addAttribute("entradas", entradas);
        model.addAttribute("platos", platos);
        model.addAttribute("bebidas", bebidas);
        return "carta";  
    }
}
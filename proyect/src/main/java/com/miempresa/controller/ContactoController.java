package com.miempresa.controller;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.servlet.mvc.support.RedirectAttributes;
import com.miempresa.modelo.Contacto;
import com.miempresa.servicio.ContactoService;
import org.springframework.web.servlet.ModelAndView;

@Controller
public class ContactoController {
    private final ContactoService contactoService;

    public ContactoController(ContactoService contactoService) {
        this.contactoService = contactoService;
    }

    @GetMapping("/contactanos")
    public ModelAndView mostrarFormularioContacto() {
        ModelAndView modelAndView = new ModelAndView("contacto");
        return modelAndView;
    }

    @PostMapping("/contactanos")
    public String procesarFormularioContacto(@ModelAttribute Contacto contacto, RedirectAttributes redirectAttributes) {
        contactoService.guardarContacto(contacto);
        redirectAttributes.addFlashAttribute("mensajeExito", "¡Mensaje enviado exitosamente!");
        return "redirect:/contactanos";
    }
}


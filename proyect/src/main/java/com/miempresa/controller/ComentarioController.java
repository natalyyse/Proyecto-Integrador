package com.miempresa.controller;
import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import com.miempresa.modelo.Comentario;
import com.miempresa.servicio.ComentarioService;

@Controller
@RequestMapping("/comentarios")
public class ComentarioController {

    @Autowired
    private ComentarioService comentarioService;

    @GetMapping
    public String mostrarComentarios(Model model) {
        List<Comentario> comentarios = comentarioService.obtenerTodosLosComentarios();
        model.addAttribute("comentarios", comentarios);
        model.addAttribute("nuevoComentario", new Comentario());
        return "comentarios";
    }

    @PostMapping
    public String enviarComentario(@ModelAttribute("nuevoComentario") Comentario nuevoComentario) {
        comentarioService.enviarComentario(nuevoComentario);
        return "redirect:/comentarios";
    }
}

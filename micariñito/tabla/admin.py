import json
from django.db.models import Sum
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, reverse
from django.utils.html import format_html
from django.utils.safestring import mark_safe
import datetime
from .models import (Contactano, GananciaMe, PromocionDePlato, Usuario, Categoria, NotificacionMovil, ReservaDeMesa, Plato,
                     ComentarioCalificacion, Cliente,
                     RegistroDeVenta, Bebida, Entrada)
from .views import descargar_reporte_pdf

class BasicModelAdmin(admin.ModelAdmin):
    class Media:
        css = {
            'all': ('customadmin.css',)
        }
    def get_list_display_links(self, request, list_display):
        return None

    def has_add_permission(self, request):
        return False
    

class FullCRUDModelAdmin(BasicModelAdmin):
    class Media:
        css = {
            'all': ('customadmin.css',)
        }
    def crud_buttons(self, obj):
        return format_html(
            '<a class="button" href="{}">Editar</a>&nbsp;'
            '<a class="button" href="{}">Eliminar</a>',
            reverse(f'admin:{obj._meta.app_label}_{obj._meta.model_name}_change', args=[obj.pk]),
            reverse(f'admin:{obj._meta.app_label}_{obj._meta.model_name}_delete', args=[obj.pk])
        )
    crud_buttons.short_description = 'Acciones'

    def get_list_display(self, request):
        return list(self.list_display) + ['crud_buttons']

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_add_button'] = True
        return super().changelist_view(request, extra_context=extra_context)

    def has_add_permission(self, request):
        return True

class UsuarioAdmin(BasicModelAdmin):
    list_display = ['nombre', 'apellido', 'correo_electronico', 'nombre_usuario']

    def has_delete_permission(self, request, obj=None):
        return False
    
class CategoriaAdmin(FullCRUDModelAdmin):
    list_display = ['nombre']

class NotificacionMovilAdmin(FullCRUDModelAdmin):
    list_display = ['titulo', 'mensaje', 'fecha']
    list_filter = ['fecha']

class ReservaDeMesaAdmin(BasicModelAdmin):
    list_display = ['usuario', 'num_personas', 'numero_mesa', 'fecha', 'precio', 'hora', 'nota']
    list_filter = ['fecha', 'usuario']

    def has_delete_permission(self, request, obj=None):
        return False

class PlatoAdmin(FullCRUDModelAdmin):
    list_display = ['nombre', 'descripcion', 'categoria', 'precio', 'mostrar_imagen']
    list_filter = ['categoria']

    def mostrar_imagen(self, obj):
        if obj.imagen:
            return mark_safe(f'<img src="{obj.imagen.url}" width="100" height="100" />')
        return "Sin imagen"
    mostrar_imagen.short_description = 'Imagen'

class PromocionDePlatoAdmin(FullCRUDModelAdmin):
    list_display = ['plato', 'enunciado', 'precio_descuento', 'mostrar_imagen']
    list_filter = ['plato']

    def mostrar_imagen(self, obj):
        if obj.plato.imagen:
            return mark_safe(f'<img src="{obj.plato.imagen.url}" width="100" height="100" />')
        return "Sin imagen"
    mostrar_imagen.short_description = 'Imagen del Plato'

class ComentarioCalificacionAdmin(BasicModelAdmin):
    list_display = ['usuario', 'nombre_cliente', 'fecha', 'calificacion', 'comentario_formateado', 'acciones']
    list_filter = ['fecha', 'calificacion']
    
    def comentario_formateado(self, obj):
        return mark_safe(f'<div style="white-space: pre-wrap; word-wrap: break-word; max-width: 300px;">{obj.comentario}</div>')
    comentario_formateado.short_description = 'Comentario'

    def acciones(self, obj):
        return format_html(
            '<a class="button" href="{}">Eliminar</a>',
            reverse(f'admin:{obj._meta.app_label}_{obj._meta.model_name}_delete', args=[obj.pk])
        )
    acciones.short_description = 'Acciones'

    def has_change_permission(self, request, obj=None):
        return False
    
    def response_delete(self, request, obj_display, obj_id):
        return redirect('admin:tabla_comentariocalificacion_changelist')

class ClienteAdmin(BasicModelAdmin):
    list_display = ['nombre', 'apellido', 'correo_electronico']

    def has_delete_permission(self, request, obj=None):
        return False

class RegistroDeVentaAdmin(BasicModelAdmin):
    list_display = ['cliente', 'total', 'fecha_venta', 'plato_info', 'bebida_info', 'entrada_info']
    list_filter = ['fecha_venta']

    def has_delete_permission(self, request, obj=None):
        return False

    def plato_info(self, obj):
        if obj.plato:
            return f"{obj.plato.nombre} (Cantidad: {obj.cantidad_plato})"
        return "Ninguna"
    plato_info.short_description = 'Plato'

    def bebida_info(self, obj):
        if obj.bebida:
            return f"{obj.bebida.nombre} (Cantidad: {obj.cantidad_bebida})"
        return "Ninguna"
    bebida_info.short_description = 'Bebida'

    def entrada_info(self, obj):
        if obj.entrada:
            return f"{obj.entrada.nombre} (Cantidad: {obj.cantidad_entrada})"
        return "Ninguna"
    entrada_info.short_description = 'Entrada'

class BebidaAdmin(FullCRUDModelAdmin):
    list_display = ['nombre', 'precio', 'mostrar_imagen']
    list_filter = ['precio']

    def mostrar_imagen(self, obj):
        if obj.imagen:
            return mark_safe(f'<img src="{obj.imagen.url}" width="100" height="100" />')
        return "Sin imagen"
    mostrar_imagen.short_description = 'Imagen'

class EntradaAdmin(FullCRUDModelAdmin):
    list_display = ['nombre', 'precio', 'mostrar_imagen']
    list_filter = ['precio']

    def mostrar_imagen(self, obj):
        if obj.imagen:
            return mark_safe(f'<img src="{obj.imagen.url}" width="100" height="100" />')
        return "Sin imagen"
    mostrar_imagen.short_description = 'Imagen'

class ContactoAdmin(BasicModelAdmin):
    list_display = ['nombre', 'correo_electronico', 'mensaje_formateado', 'acciones']
    list_filter = ['correo_electronico']

    def has_delete_permission(self, request, obj=None):
        return True

    def has_change_permission(self, request, obj=None):
        return False
    
    def response_delete(self, request, obj_display, obj_id):
        return redirect('admin:tabla_contactano_changelist')
    
    def mensaje_formateado(self, obj):
        return mark_safe(f'<div style="white-space: pre-wrap; word-break: break-word; max-width: 380px;">{obj.mensaje}</div>')
    mensaje_formateado.short_description = 'Mensaje'

    def acciones(self, obj):
        return format_html(
            '<a class="button" href="{}">Eliminar</a>',
            reverse(f'admin:{obj._meta.app_label}_{obj._meta.model_name}_delete', args=[obj.pk])
        )
    acciones.short_description = 'Acciones'

class GananciaMesAdmin(BasicModelAdmin):
    list_display = ['mes_anio', 'total_reservas', 'total_registros_venta', 'ganancia_reservas', 'ganancia_registros_venta', 'ganancia_total', 'acciones']
    change_list_template = 'admin/tabla/gananciames_changelist.html'

    def mes_anio(self, obj):
        return f"{obj.mes.strftime('%B')} {obj.mes.year}"
    mes_anio.short_description = 'Mes'

    def acciones(self, obj):
        return format_html('<a class="button" href="{}">Descargar PDF</a>', reverse('admin:descargar_reporte_pdf', args=[obj.pk]))
    acciones.short_description = 'Acciones'

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        hoy = datetime.date.today()
        primer_dia = datetime.date(hoy.year, hoy.month, 1)
        ultimo_dia = primer_dia + datetime.timedelta(days=32)
        ultimo_dia = ultimo_dia.replace(day=1) - datetime.timedelta(days=1)
        reservas = ReservaDeMesa.objects.filter(fecha_reg__range=(primer_dia, ultimo_dia)).values('fecha_reg').annotate(total_dia=Sum('precio'))
        ventas = RegistroDeVenta.objects.filter(fecha_venta__range=(primer_dia, ultimo_dia)).values('fecha_venta').annotate(total_dia=Sum('total'))
        fechas = [dia for dia in range(1, ultimo_dia.day + 1)]
        ganancias_reservas = [0] * ultimo_dia.day
        ganancias_ventas = [0] * ultimo_dia.day
        for reserva in reservas:
            ganancias_reservas[reserva['fecha_reg'].day - 1] = float(reserva['total_dia'] or 0)
        for venta in ventas:
            ganancias_ventas[venta['fecha_venta'].day - 1] = float(venta['total_dia'] or 0)
        chart_data = [
            fechas,
            ganancias_reservas,
            ganancias_ventas,
        ]
        extra_context.update({
            'chart_data': json.dumps(chart_data),
        })
        return super().changelist_view(request, extra_context=extra_context)

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('descargar-reporte-pdf/<int:pk>/', self.admin_site.admin_view(descargar_reporte_pdf), name='descargar_reporte_pdf'),
        ]
        return custom_urls + urls

admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(NotificacionMovil, NotificacionMovilAdmin)
admin.site.register(ReservaDeMesa, ReservaDeMesaAdmin)
admin.site.register(Plato, PlatoAdmin)
admin.site.register(PromocionDePlato, PromocionDePlatoAdmin)
admin.site.register(ComentarioCalificacion, ComentarioCalificacionAdmin)
admin.site.register(Cliente, ClienteAdmin)
admin.site.register(RegistroDeVenta, RegistroDeVentaAdmin)
admin.site.register(Bebida, BebidaAdmin)
admin.site.register(Entrada, EntradaAdmin)
admin.site.register(Contactano, ContactoAdmin)
admin.site.register(GananciaMe, GananciaMesAdmin)
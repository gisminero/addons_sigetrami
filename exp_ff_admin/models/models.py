# -*- coding: utf-8 -*-
from asyncio import exceptions
from odoo import models, fields, api
from odoo import exceptions

class exp_ff_admin(models.Model):
    _name = 'exp_ff_admin'
    # _order = 'create_date desc'

    #tramite_id = fields.Many2one('procedimiento.procedimiento', string="Trámite")
    name = fields.Char('Nombre', required=False)
    #cuit_titular = fields.Char('CUIT del Titular', required=False)
    #exp_id = fields.Many2one('expediente.expediente', string="Expediente al que correponde", readonly=True)

    """
    def write(self):
        print(("CAMBIANDO NOMBRE DE TITULAR" + self.nombre_titular))
        self.cambio_tramite_en_expte()
        self.exp_id.write({'cambio_de_tramite': False})
        vals = {'tramite_id': self.tramite_id.id, 'nombre_titular': self.nombre_titular,
                'cuit_titular': self.cuit_titular, 'exp_id': self.exp_id.id}
        return super(exp_historia_tramite, self).write(vals)

    def cambio_tramite_en_expte(self):
        exp_obj = self.env['expediente.expediente'].browse([self.exp_id.id])
        print ((" ESTE ES EL EXPEDIENTE ENCONTRADO: " + exp_obj.name))
        vals = {'procedimiento_id': self.tramite_id.id, 'solicitante': self.nombre_titular,
                'solicitante_cuit': self.cuit_titular}
        return exp_obj.write(vals)
    """

class expediente(models.Model):
    _name = 'expediente.expediente'
    _inherit = 'expediente.expediente'
    _description = "Lamando a Sacar o Ingresar en Flujo"

    def exp_flujo_sacar(self):
        print ("CHEQUEANDO OFICINA################################ UBICACION ACTUAL: " + str(self.ubicacion_actual.id))
        # NO SE PUEDE ENVIAR SI NO ESTA EN MI OFICINA
        active_id = self.id
        expte_obj = self.browse([active_id])
        user_id = self.env.user.id
        depart_id = self.userdepart(user_id)
        print ("El departamento del usuario es########: " + str(depart_id))
        #Validacion OFICINA VACIA#
        pase_obj = self.env['pase.pase']
        pase_cerrado = pase_obj.ultima_condicion_recibido(active_id)
        print (( "ULTIMA CONDICION DE RECIBIDO : " +str(pase_cerrado)))
        if pase_cerrado == False:
            if not expte_obj.oficina_destino.name:
                of_enviado = "-"
            else:
                of_enviado = expte_obj.oficina_destino.name
            return {
                    'name': "EL DOCUMENTO SE ENCUENTRA ENVIADO A: " + str(of_enviado),
                    'view_mode': 'form',
                    'res_id': active_id,
                    #'view_id': self.env.ref('pase.form_enviar').id,
                    'res_model': 'expediente.expediente',
                    'type': 'ir.actions.act_window',
                    #'domain': [('ubicacion_actual', '=', env['expediente.expediente'].depart_user())],
                    #'domain': [('recibido', '=', False), ('oficina_destino', '=', self.env['expediente.expediente'].depart_user())],
                    #'context': {'recibido': True, 'ultimo_pase_id': pase_res.id, 'oficina_destino': depart_id},
                    'context': {'recibido': True, 'oficina_destino': depart_id},
                    'views': [[self.env.ref('expediente.form_enviado').id, "form"]],
                    'target': 'new',
                    }
        if depart_id != self.ubicacion_actual.id:
            view = self.env.ref('sh_message.sh_message_wizard')
            view_id = view and view.id or False
            context = dict(self._context or {})
            context['message'] = 'Para enviar el Expte. a una ubicación fuera de flujo es necesario que se encuentre en su oficina.'
            return {
                    'name': 'Informacion',
                    'type': 'ir.actions.act_window',
                    'view_type': 'form',
                    'view_mode': 'form',
                    'res_model': 'sh.message.wizard',
                    'views': [(view.id, 'form')],
                    'view_id': view.id,
                    'target': 'new',
                    'context': context,
                    }
                # FIN NO SE PUEDE ENVIAR SI NO ESTA EN MI OFICINA
        if not self.tramite_tiene_flujo():
            print ((" EL TRAMITE NO TIENE FLUJO DEFINIDO"))
            action = self.enviar()
        else:
            action = {
                'name': "Expedientes en el Sistema...",
                'view_mode': 'form',
                'res_id': self.id,
                'res_model': 'expediente.expediente',
                'type': 'ir.actions.act_window',
                'target': 'new',
                # 'domain': [('ubicacion_actual', '=', self.env['expediente.expediente'].depart_user())],
                'views': [[self.env.ref('exp_ff_admin.expediente_sacar_form').id, "form"]],
                }
        return action

    def exp_flujo_ingresar(self):
        print ("LLAMANDO A INGRESAR EN FLUJO ################################: " + str(self.id))
        user_id = self.env.user.id
        depart_id = self.userdepart(user_id)
        if depart_id != self.ubicacion_actual.id or self.en_flujo == True:
            view = self.env.ref('sh_message.sh_message_wizard')
            view_id = view and view.id or False
            context = dict(self._context or {})
            context['message'] = 'Para ingresar el Expte. es necesario que se encuentre en su oficina y este fuera de flujo.'
            return {
                    'name': 'Informacion',
                    'type': 'ir.actions.act_window',
                    'view_type': 'form',
                    'view_mode': 'form',
                    'res_model': 'sh.message.wizard',
                    'views': [(view.id, 'form')],
                    'view_id': view.id,
                    'target': 'new',
                    'context': context,
                    }
                # FIN NO SE PUEDE ENVIAR SI NO ESTA EN MI OFICINA    
        if not self.tramite_tiene_flujo():
            print ((" EL TRAMITE NO TIENE FLUJO DEFINIDO"))
            action = self.enviar()
        else:
            action = {
                'name': "Expedientes en el Sistema...",
                'view_mode': 'form',
                'res_id': self.id,
                'res_model': 'expediente.expediente',
                'type': 'ir.actions.act_window',
                'target': 'new',
                # 'domain': [('ubicacion_actual', '=', self.env['expediente.expediente'].depart_user())],
                'views': [[self.env.ref('exp_ff_admin.expediente_ingreso_form').id, "form"]],
                }
        return action

    def ingresar_flujo_tarea(self):
        
        return True

    def proxima_tarea_enviar_sacar(self):
            print(("¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿ENVIANDO PASE DE TAREA Y OFICINA 2021_¡¡¡¡???????????????????????????"))
            active_id = self.env.context.get('id_activo')
            expte_obj = self.browse([active_id])
            #OBTENIENDO VALORES DESDE CONTEX DEL POP UP
            proxima_tarea_id = self.env.context.get('tarea_proxima_cont')#PROXIMA TAREA SELECCIONADA POR EL USUARIO
            fojas_new = self.env.context.get('fojas_new')#NUEVO NUMERO DE FOJAS
            destino_new = self.env.context.get('oficina_destino_new')#NUEVA OFICINA DESTINO
            observaciones_new = self.env.context.get('observaciones_new')#oBSERVACIONES DEL PASE
            #tarea_actual_old = self.env.context.get('tarea_actual')#CANDIDATO A SER BORRADO PORQUE NO TRAE NADA DESDE LA VISTA
            en_flujo_new = self.env.context.get('en_flujo_new')
            tipo_vista = self.env.context.get('vista_padre')
            notifica_obj = self.env['notifica']
            if destino_new is False and proxima_tarea_id is not False:
                    view = self.env.ref('sh_message.sh_message_wizard_false')
                    view_id = view and view.id or False
                    context = dict(self._context or {})
                    context['message'] = 'Verifique que el valor de Oficina Destino se muestre en el formulario de envio. Vuelva a intentar el envio.'
                    return {
                                'name': 'Informacion',
                                'type': 'ir.actions.act_window',
                                'view_type': 'form',
                                'view_mode': 'form',
                                'res_model': 'sh.message.wizard',
                                'views': [(view.id, 'form')],
                                'view_id': view.id,
                                'target': 'new',
                                'context': context,
                        }
            if en_flujo_new is False and expte_obj.en_flujo is True:
                    self.cambia_estado_plazos(expte_obj.id, 'suspendido')
                    self.write({'en_flujo': False})
                    self.enviar_conf()
                    return self.mi_oficina_view()

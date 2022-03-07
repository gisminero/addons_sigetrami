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

class pase(models.Model):
    _name = 'pase.pase'
    _inherit = 'pase.pase'
    _description = "Listado de pases"

    """
    def enviados_sin_recepcion_view(self):
        print ("BUSCANDO MI OFICINA ################################")
        user_id = self.env.user.id
        depart_user_id = self.userdepart(user_id)
        if depart_user_id > 0:
            action = {
                'name': "Expedientes en Mi Oficina",
                'view_mode': 'tree, form',
                'res_model': 'pase.pase',
                'type': 'ir.actions.act_window',
                'domain': [('depart_origen_id', '=', depart_user_id), ('fecha_hora_recep', '=', False)],
                'views': [[self.env.ref('exp_envios_admin.envios_no_rec_list').id, "tree"], [self.env.ref('exp_envios_admin.envios_no_rec_form').id, "form"]],
                }
        return action
    # self.env['expediente.expediente'].depart_user()

    def enviados_reclamados_view(self):
        # user_id = self.env.user.id
        # depart_user_id = self.userdepart(user_id)
        view = self.env.ref('sh_message.sh_message_wizard_false')
        view_id = view and view.id or False
        context = dict(self._context or {})
        context[
            'message'] = 'Esta funcionalidad se encuentra en desarrollo.'
        return {
            'name': 'Correccion de envíos erroneos.',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'sh.message.wizard',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'target': 'new',
            'context': context,
        }

    def correccion_flujo_view(self):
        print ("BUSCANDO MI OFICINA ################################")
        user_id = self.env.user.id
        depart_user_id = self.userdepart(user_id)
        if depart_user_id > 0:
            action = {
                'name': "Administrar ubicación de documentos.",
                'view_mode': 'tree',
                #, form
                'res_model': 'expediente.expediente',
                'type': 'ir.actions.act_window',
                # 'target': 'new',
                'domain': [ ('recibido', '=', True)],#('ultimo_pase_id', '!=', False),
                'views': [[self.env.ref('exp_envios_admin.expediente_corregir').id, "tree"]],
            # , [self.env.ref('exp_cambio_tramite.expediente_corregir_form').id, "form"]
                }
        return action
    """



class expediente(models.Model):
    _name = 'expediente.expediente'
    _inherit = 'expediente.expediente'
    _description = "Lamando a Sacar o Ingresar en Flujo"

    def exp_flujo_sacar(self):
        # print ("ENVIO DIRECTO ################################: " + str(self.id))
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
                'views': [[self.env.ref('exp_envios_admin.expediente_corregir_form').id, "form"]],
                }
        return action

    def exp_flujo_ingresar(self):
        # print ("ENVIO DIRECTO ################################: " + str(self.id))
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
                'views': [[self.env.ref('exp_envios_admin.expediente_corregir_form').id, "form"]],
                }
        return action


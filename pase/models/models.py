# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
# from unidecode import unidecode

class pase(models.Model):
    _name = 'pase.pase'
    _order = "fecha_hora_envio desc"

    name = fields.Char("Expediente", store=True, compute="_value_exp") #
    expediente_id = fields.Many2one('expediente.expediente', 'Id Expediente', copy=False, required=False)
    depart_origen_id = fields.Many2one('hr.department', 'Oficina Origen', copy=False, required=False)
    depart_destino_id = fields.Many2one('hr.department', 'Oficina Destino', copy=False, required=False)
    user_origen_id = fields.Many2one('res.users','Usuario envia',required=False)
    user_recep_id = fields.Many2one('res.users','Usuario recibe',required=False)
    fecha_hora_envio = fields.Datetime(string='Hora Envio', default=fields.Datetime.now)
    fecha_hora_recep = fields.Datetime(string='Hora Recepcion' )
    folios = fields.Integer(string='Folios')
    observ_pase = fields.Text(string='Observaciones', translate=True, readonly=True)

    @api.depends('expediente_id', 'user_recep_id')
    def _value_exp(self):
        if self.id:
            self.name = self.expediente_id.name
            exp_obj = self.env['expediente.expediente'].browse(self.expediente_id.id)
            print (("ASIGNANDO: "+ str(exp_obj.name) + " ID del pase: "+ str(self.id)))
            #exp_obj.write({'ultimo_pase_id': 12})
            if not self.user_recep_id:
                ultima_oficina = self.depart_origen_id.id
            else:
                ultima_oficina = self.depart_destino_id.id
            self._cr.execute("""UPDATE public.expediente_expediente
                    SET ultimo_pase_id = %s, ubicacion_actual = %s
                    , oficina_destino = %s
                    WHERE id = %s;"""
                    % (self.id, ultima_oficina, self.depart_destino_id.id,
                        self.expediente_id.id, ))
            print (("TERMINO LA ASIGNACION 2"))

    def valida_pases_abiertos(self, exp_id):
        #Validar si en los pases asociados a un expediente existe mas de un pase abierto #Es decir sin recepci??n
        #Validacion retirada el 03/09/2019 porque al abrir raise queda cargado el ultimo id de expediente y no cambia
        return True
        pase_ids_count = self.search_count([('expediente_id', '=', [exp_id]),
                                            ('user_recep_id', '=', False)])
        if pase_ids_count == 0:
            return True
        elif pase_ids_count == 1:
            return True
        elif pase_ids_count > 1:
            exp_obj = self.env['expediente.expediente'].browse(exp_id)
            raise ValidationError((str(exp_obj.name) + " - HAY MAS DE UN PASE ABIERTO PARA ESTE EXPEDIENTE, COMUNIQUESE CON EL ADMINISTRADOR."))
            return False

    def obtener_ultimo_pase(self, exp_id):
        # Obtener el Ultimo pase realizado a un expediente determinado
        # Se determina el ultimo pase en funcion del numero de expediente y fecha y hora de env??a
        # print (("PARAMETROS RECIBIDOS: ", str(exp_id)))
        r = self.valida_pases_abiertos(exp_id)
        pase_ids_count = self.search_count([('expediente_id', '=', [exp_id])])
        if pase_ids_count == 0:
            return False
        else:
            obj_pase = self.search([('expediente_id', '=', [exp_id])], order="fecha_hora_envio desc", limit=1)
            # print(("EL PASE ID ES: " + str(obj_pase.id)))
            #obj_pase = self.env['pase.pase'].browse(pase_ids)
            if obj_pase:
                return obj_pase[0]
            else:
                return False

    def ultima_condicion_recibido(self, exp_id):
        #Obtener la ultima condicion de recepcion del expediente
        # Si esta recibido devuelve True
        # Si el expediente se encuentra enviado pero no recibido retorna False
        obj_pase = self.obtener_ultimo_pase(exp_id)
        if obj_pase:
            # print(("EN EL PASE: " + unidecode(str(obj_pase.name)) + "  ----  DEPART ORIGEN: " + unidecode(obj_pase.depart_origen_id.name) + " ---- FOLIOS: " + unidecode(
            #         str(obj_pase.folios) + " Envio:" + str(obj_pase.fecha_hora_envio))))
            if obj_pase.user_recep_id:
                return True
            else:
                return False
        else:
            print(("NO TRAE OBJETO PASE"))
        return False

    def ubicacion_actual(self, exp_id):
        #Obtener la ultima condicion de recepcion del expediente
        obj_pase = self.obtener_ultimo_pase(exp_id)
        if obj_pase:
            # print(("EN EL PASE: " + unidecode(str(obj_pase.name)) + "  ----  DEPART ORIGEN: "
            #    + unidecode(obj_pase.depart_origen_id.name) + " ---- FOLIOS: " + unidecode(
            #         str(obj_pase.folios) + " Envio:" + str(obj_pase.fecha_hora_envio))))
            if obj_pase.user_recep_id:
                return obj_pase.depart_destino_id
            else:
                return obj_pase.depart_origen_id
        else:
            print(("NO TRAE OBJETO PASE"))
        return False

    def userdepart(self, user_id):
        num_empl = self.env['hr.employee'].search_count([('user_id', '=', user_id)])
        if num_empl < 1:
            print (("No se encuentra el empleado asociado al usuario: " + str(user_id)))
            return False
        elif num_empl > 1:
            print (("Hay mas de un emplado asociado al usuario: " + str(user_id)))
            return False
        else:
            empl_obj = self.env['hr.employee'].search([('user_id', '=', user_id)])
            if empl_obj.department_id.id:
                # print (("RETORNANDO EL DEPARTAMENTO: " + str(empl_obj.department_id.id)))
                return empl_obj.department_id.id
            else:
                print (("EL EMPLEADO NO TIENE OFICINA ASIGNADA"))
                return False

    def imprimir_pase(self):
        print (("IMPRIMIENDO PASE DESDE LA CLASE PASE..............." + self.name + " ---- "+ self.depart_origen_id.name + " EL ID ES: " + str(self.id)))
        data = {}
        #return self.env.ref('pase.recibo_pase').report_action(self, data=data)
        #view = self.env.ref('pase.form_constancia_envio')
        #view_id = view and view.id or False
        #context = dict(self._context or {})
        #context['message'] = 'Constancia de envio.'
        return {
                'name': "Constancia de pase (vista previa)",
                'view_mode': 'form',
                'res_id': self.id,
                'view_id': self.env.ref('pase.form_constancia_envio').id,
                'res_model': 'pase.pase',
                'type': 'ir.actions.act_window',
                #'domain': [('ubicacion_actual', '=', env['expediente.expediente'].depart_user())],
                #'domain': [('recibido', '=', False), ('oficina_destino', '=', self.env['expediente.expediente'].depart_user())],
                #'context': {'recibido': False, 'oficina_destino': False, 'observ_pase': '', 'id_activo': active_id},
                #'views': [[self.env.ref('pase.form_constancia_envio').id, "form"]],
                'target': 'new',
                #'flags': {'form': {'action_buttons': False}},
                }
        """
        datas = {
            'ids': self,
            'model': 'pase.pase',
            'form': self,
            }
        return {
            'name': 'Nombre del Reporte',
            'model': 'pase.pase',
            'type': 'ir.actions.report',
            'report_name': 'pase.recibo_pase_1', 
            #'datas': datas,
            }
        """

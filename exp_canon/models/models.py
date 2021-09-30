# -*- coding: utf-8 -*-
from odoo import models, fields, api
import datetime
from odoo import exceptions

class exp_canon_obligaciones(models.Model):
    _name = 'exp_canon_obligaciones'
    _description = "Canon Obligaciones a Cumplir"
    #_inherit = ['mail.thread']
    _inherit = ['mail.activity.mixin', 'mail.thread']

    name = fields.Char('Concepto', required=True, readonly=False)
    fecha_vencimiento = fields.Date('Vencimiento', readonly=True)
    fecha_vencimiento_gracia = fields.Date('Plazo Gracia', readonly=False)
    fecha_pago = fields.Date('Fecha de Pago', readonly=True)
    monto_debe = fields.Float('Monto Debe', readonly=True)
    monto_haber = fields.Float('Monto Haber', readonly=True, default=0)
    monto_saldo = fields.Float('Monto de Saldo', readonly=True)
    estado = fields.Selection([
        ('emitido', 'Emitido'),
        ('pagado', 'Pagado'),
        ('vencido', 'Vencido'),], required=False,
        help="Estado de la Obligación", string="Estado", readonly=True)
    notificacion_enviada = fields.Boolean('Notificación Enviada', default=False, readonly=True)
    exp_id = fields.Many2one('expediente.expediente', 'Expediente', required=1, ondelete='cascade')
    partner_id = fields.Many2one('res.partner', 'Responsible')
    guest_ids = fields.Many2many('res.partner', 'Participants')

    def calcular_monto(self):
        return 0

    def crear_obligacion(self, exp, semestre):
        hoy = datetime.date.today()
        anio = hoy.year
        if semestre == 1:
            mes_vto = exp.config_asociada.mes_primer_vencimiento_anual
            mes_vto_gracia = exp.config_asociada.mes_primer_plazo_gracia
            anio_gracia = anio
        else:
            mes_vto = exp.config_asociada.mes_segundo_vencimiento_anual
            mes_vto_gracia = exp.config_asociada.mes_segundo_plazo_gracia
            anio_gracia = anio + 1
        concepto = 'Canon ' + str(anio) + ' - Pago ' + str(semestre)
        fecha_venc = str(anio) +'-'+ str(mes_vto) + '-' + str(self.obtener_ultimo_dia_mes(anio, mes_vto))
        fecha_venc_gracia = str(anio_gracia) +'-'+ str(mes_vto_gracia) + '-' + str(self.obtener_ultimo_dia_mes(anio_gracia, mes_vto_gracia))
        self.calcular_monto()
        self.create({'name': concepto, 'exp_id': exp.id, 'fecha_vencimiento': fecha_venc, 'fecha_vencimiento_gracia': fecha_venc_gracia
                     , 'estado': 'emitido'})
        return True

    def realiza_pago(self):
        return True

    def obtener_ultimo_dia_mes(self, anio, mes):
        anio = anio + 1 if (mes == 12) else anio
        mes = 1 if (mes == 12) else mes + 1
        ultima_fecha_mes = datetime.date(anio, mes, 1) - datetime.timedelta(days=1)
        #print (("LA ULTIMA FECHA DE MES ES IGUAL A : " + str(ultima_fecha_mes) + " ultimo dia: " + str(ultima_fecha_mes.day)))
        return ultima_fecha_mes.day

    def informa_pago(self):
        print (("MAS INFORMACION DEL DOCUMENTO"))
        active_id = self.env.context.get('id_activo')
        print (("ENVIANDO .... " + str(active_id)))
        expte_obj = self.browse([active_id])
        if True:
            return {
            'name': "Informar Pago",
            'view_mode': 'form',
            'res_id': self.id, #SOLO PARA FORM
            'res_model': 'exp_canon_obligaciones',
            'type': 'ir.actions.act_window',
            # 'domain': [('seguimiento_id.expediente_id', '=', active_id)],
            #'context': {'recibido': True, 'ubicacion_actual': depart_id},
            'views': [[self.env.ref('exp_canon.form_popup_informa_pago').id, "form"]],
            'target': 'new',
            'tag': 'reload',
            }
        return True

    def informar_pago(self):
        if self.monto_haber == False or self.fecha_pago == False:
            raise exceptions.ValidationError('Faltan datos para continuar con la operación.')
        self.write({'monto_haber': self.monto_haber, 'fecha_pago': self.fecha_pago, 'estado': 'pagado'})
        return True

    def notificacion_pago(self):
        return True

    def obtener_usuarios_notif(self):
        grupos = self.exp_id.config_asociada.grupos_notificar
        partner_ids = []
        for g in grupos:
            for u in g.user_notificar_id:
                print (("EL PERSONAJE A NOTIFICAR ES: " + u.name + " ID Users: "+ str(u.user_id.partner_id.id) + " Usuario: "+ str(u.user_id.login)+ "Usuario Activo: " + str(u.active)))
                partner_ids.append(u.user_id.partner_id.id)
        return partner_ids

    def notificacion_obligacion_vencida(self):
        print (("DISPARANDO LA NOTIFICACION ..... "))
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        print (("BASE URL: " + str(base_url)))
        partner_notif_list = self.obtener_usuarios_notif()
        if partner_notif_list.__len__ == 0:
            print (("LISTA VACIA"))
        info = "ESTE ES UN MENSAJE DE PRUEBA 9...  <a href='"+base_url+"/web#id="+str(self.id)+"&model=exp_canon_obligaciones&view_type=form&menu_id=200'>"+self.exp_id.name+"</a> "
        kwargs = {'partner_ids': partner_notif_list,}
        #self.message_post(body=info, subject="Plazo Vencido", message_type='notification', parent_id=False, attachments=None)
        self.message_subscribe(partner_ids=partner_notif_list, channel_ids=None, subtype_ids=None)
        self.message_post(body=info, subject=None, message_type='comment', parent_id=False, 
            attachments=None, **kwargs)
        return True

class expediente(models.Model):

    _name = 'expediente.expediente'
    _inherit = 'expediente.expediente'
    _description = "Asociando las obligaciones de pago de canon minero."

    def default_config_canon(self):
        default_canon = self.env['exp_canon_config'].search([('config_defecto', '=', True), ('active', '=', True)])
        return default_canon.id

    canon_obligaciones_id = fields.One2many('exp_canon_obligaciones', 'exp_id', string='Obligaciones', required=False)
    cant_vencimientos_no_cumplidos = fields.Integer('Vencimientos No Cumplidos', help='', default=0)
    config_asociada = fields.Many2one('exp_canon_config', 'Configuracion Canon Asociada', readonly=False, default=default_config_canon, required=False)
    
    def confirmar(self):
        print (("Confirmar"))
        print("CONFIG ASOCIADA ")
        print(self.config_asociada)
        print(self.config_asociada.validado)
        return True

    def canon_cambiar_config_default(self):
        if True:
            return {
                'name': "Cambiar configuración de Canon",
                'view_mode': 'form',
                'res_id': self.id,  # SOLO PARA FORM
                'res_model': 'expediente.expediente',
                'type': 'ir.actions.act_window',
                # 'domain': [('seguimiento_id.expediente_id', '=', active_id)],
                # 'context': {'recibido': True, 'ubicacion_actual': depart_id},
                'views': [[self.env.ref('exp_canon.popup_select_config').id, "form"]],
                'target': 'new',
                #'tag': 'reload',
            }
        return True


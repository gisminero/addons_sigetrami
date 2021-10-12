# -*- coding: utf-8 -*-
from odoo import models, fields, api
import datetime
#from odoo import exceptions
from odoo.exceptions import UserError, ValidationError

class exp_canon_obligaciones(models.Model):
    _name = 'exp_canon_obligaciones'
    _description = "Canon Obligaciones a Cumplir"
    _inherit = ['mail.activity.mixin', 'mail.thread']
    _order = "create_date desc"

    name = fields.Char('Concepto', required=True, readonly=True)
    fecha_vencimiento = fields.Date('Vencimiento', readonly=True)
    fecha_vencimiento_gracia = fields.Date('Plazo Gracia', readonly=True)
    fecha_pago = fields.Date('Fecha de Pago', readonly=True)
    monto_debe = fields.Float('Monto Debe', readonly=True)
    monto_haber = fields.Float('Monto Pago', readonly=True, default=0)
    monto_saldo = fields.Float('Monto de Saldo', readonly=True)
    estado = fields.Selection([
        ('emitido', 'Emitido'),
        ('pagado', 'Pagado'),
        ('vencido', 'Vencido'),
        ('vencido_corregido', 'Corrección de Pago')], required=False,
        help="Estado de la Obligación", string="Estado", readonly=True)
    user_informa_pago = fields.Many2one('res.users','Informado por', required=False)
    notificacion_enviada = fields.Boolean('Notificación Enviada', default=False, readonly=True)
    cuenta_pago = fields.Many2one('exp_canon_config_bancos','Cuenta de pago', required=False)
    exp_id = fields.Many2one('expediente.expediente', 'Expediente', required=1, ondelete='cascade', readonly=True)
    partner_id = fields.Many2one('res.partner', 'Responsible')
    guest_ids = fields.Many2many('res.partner', 'Participants')

    def obtener_valor_global(self):
        """
        val_global_count = self.env['exp_canon_config_global'].search_count([('active', '=', True)])
        if val_global_count == 1:
            val_global =  self.env['exp_canon_config_global'].search([('active', '=', True)])[0]
            return val_global.
        elif num_empl > 1:
            print (("Hay mas de un emplado asociado al usuario: " + str(user_id)))
            return False
        """
        return 1

    def actual_user(self):
        return 2#self.env.user

    def obtener_cant_pertenencias(self, exp_id):
        print(("id DE EXOPEDIENTE BUSCADO: " + str(exp_id)))
        pert_obj = self.env['exp_pertenencias'].search([('exp_id', '=', exp_id)], order="write_date desc", limit=1)
        print(("OBJETOS: " + str(pert_obj)))
        if pert_obj:
            cant = pert_obj[0].pertenencias
        else:
            cant = 0
        return cant

    def calcular_monto(self, exp):
        valor_pertenencia = exp.config_asociada.valor_pertenencia
        valor_pertenencia_factor = exp.config_asociada.valor_pertenencia_factor
        #cant_pertenencias = exp.cant_pertenencias
        cant_pertenencias = self.obtener_cant_pertenencias(exp.id)
        print (("VALORES OBTENIDOS PARA REALIZAR EL CALCULO FINAL DEL EXPEDIENTE: " + str(exp.name)))
        print (("VALOR PERTENECIA: " + str(valor_pertenencia) + "VALOR PERTENECIA FACTOR: " + str(valor_pertenencia_factor) ))
        print (("CANTIDAD DE PERTENENCIAS: " + str(cant_pertenencias) ))
        valor_final = valor_pertenencia * valor_pertenencia_factor * cant_pertenencias
        return valor_final

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
        monto_obligacion = self.calcular_monto(exp)
        self.create({'name': concepto, 'exp_id': exp.id, 'fecha_vencimiento': fecha_venc, 'fecha_vencimiento_gracia': fecha_venc_gracia
                     , 'estado': 'emitido', 'monto_debe': monto_obligacion})
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
            'context': {'default_user_informa_pago': self.actual_user()},
            'views': [[self.env.ref('exp_canon.form_popup_informa_pago').id, "form"]],
            'target': 'new',
            'tag': 'reload',
            }
        return True

    def imprimir_cupon(self):
        print (("IMPIMIR CUPON"))
        if True:
            return {
            'name': "Seleccione entidad de pago",
            'view_mode': 'form',
            'res_id': self.id, #SOLO PARA FORM
            'res_model': 'exp_canon_obligaciones',
            'type': 'ir.actions.act_window',
            # 'domain': [('seguimiento_id.expediente_id', '=', active_id)],
            'context': {'default_user_informa_pago': self.actual_user()},
            'views': [[self.env.ref('exp_canon.form_popup_select_pago').id, "form"]],
            'target': 'new',
            'tag': 'reload',
            }
        return True

    def informar_pago(self):
        if self.monto_haber == False or self.fecha_pago == False:
            raise exceptions.ValidationError('Faltan datos para continuar con la operación.')
        self.write({'monto_haber': self.monto_haber, 'fecha_pago': self.fecha_pago, 'estado': 'pagado'})
        return True

    def informar_entidad(self):
        if self.cuenta_pago == False:
            raise exceptions.ValidationError('Faltan datos para continuar con la operación.')
        self.write({'cuenta_pago': self.cuenta_pago})
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
        info = "Alerta de fecha vencida, por favor haga clic en el siguiente enlace <a href='"+base_url+"/web#id="+str(self.id)+"&model=exp_canon_obligaciones&view_type=form&menu_id=200'>"+self.exp_id.name+"</a> "
        kwargs = {'partner_ids': partner_notif_list,}
        self.message_subscribe(partner_ids=partner_notif_list, channel_ids=None, subtype_ids=None)
        self.message_post(body=info, subject=None, message_type='comment', parent_id=False, 
            attachments=None, **kwargs)
        self.write({'notificacion_enviada': True, 'estado': 'vencido'})
        return True

    def corregir_pago(self):
        self.write({'estado': 'vencido_corregido'})
        return True        

class expediente(models.Model):

    _name = 'expediente.expediente'
    _inherit = 'expediente.expediente'
    _description = "Asociando las obligaciones de pago de canon minero."

    def default_config_canon(self):
        default_canon = self.env['exp_canon_config'].search([('config_defecto', '=', True), ('active', '=', True), ('procedimiento_id', '=', self.procedimiento_id)])
        if default_canon == False:
            #raise UserError(_('No hay configuración por defecto para calcular CANON MINERO en este trámite.'))
            print (("NO HAY CONFIGURACION DE CANON POR DEFECTO PÀRA ESTE TRÁMITE."))
        return default_canon.id

    def activar(self):
        default_canon = self.env['exp_canon_config'].search([('config_defecto', '=', True), ('active', '=', True), ('procedimiento_id', '=', self.procedimiento_id.id)])
        if not default_canon:
            #raise UserError(('No configuración por defecto para este trámite.'))
            print (("NO HAY CONFIGURACION DE CANON POR DEFECTO PÀRA ESTE TRÁMITE."))
        print(("LA CONFIGURACION ASOCIADA ES: " + str(default_canon.id)))
        self.write({'config_asociada' : default_canon.id})
        res = super(expediente, self).activar()
        return True        

    canon_obligaciones_id = fields.One2many('exp_canon_obligaciones', 'exp_id', string='Obligaciones', required=False)
    cant_vencimientos_no_cumplidos = fields.Integer('Vencimientos No Cumplidos', help='', default=0)
    config_asociada = fields.Many2one('exp_canon_config', 'Configuracion Canon Asociada', readonly=False, required=False)#default=default_config_canon, 
    
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


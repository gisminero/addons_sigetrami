# -*- coding: utf-8 -*-
from odoo import models, fields, api
import datetime, re
from odoo.exceptions import ValidationError

class exp_canon_venc_emitidos(models.Model):
    _name = 'exp_canon_venc_emitidos'
    _description = "Vencimientos Anuales Emitidos Automáticamente"

    name = fields.Char('Vencimiento Emitido', required=True, readonly=False)
    anio = fields.Integer('Año', required=True, readonly=False)
    semestre = fields.Integer('Semestre', required=True, readonly=False)

    def obtener_semestre(self, month):
        if (month > 0 and month < 7):
            return 1
        else:
            return 2

    def obtener_vencimiento_emitido(self, year, month):
        semestre = self.obtener_semestre(month)
        cant_venc_emitidos = self.search_count([('anio', '=', year), ('semestre', '=', semestre)])
        if cant_venc_emitidos > 0:
            return True
        else:
            return False

    def crea_vencimientos_exp(self):
        hoy = datetime.date.today()
        mes = hoy.month
        anio = hoy.year
        semestre = self.obtener_semestre(mes)
        nombre = "Primer Semestre " + str(anio) if (mes > 0 and mes < 7) else "Segundo Semestre" + str(anio)
        # self.create({'name': nombre, 'anio': anio, 'semestre': semestre})
        exp_objs = self.env['expediente.expediente'].search([('state', '=', 'active'),('config_asociada', '!=', False)])
        for exp in exp_objs:
            self.env['exp_canon_obligaciones'].crear_obligacion(exp, semestre)
        return True

    def crea_vencimientos(self):
        hoy = datetime.date.today()
        mes = hoy.month
        anio = hoy.year
        semestre = self.obtener_semestre(mes)
        nombre = "Primer Semestre " + str(anio) if (mes > 0 and mes < 7) else "Segundo Semestre" + str(anio)
        self.crea_vencimientos_exp()
        self.create({'name': nombre, 'anio': anio, 'semestre': semestre})
        return True

    def acciones_planificadas(self):
        self.dispara_vencimientos()
        self.busca_obligaciones_vencidas()
        return True

    def dispara_vencimientos(self):
        hoy = datetime.date.today()

        #print (("EL DIA DE HOY ES: " + str(hoy) + " EL AÑO ES: " + str(hoy.year) + "  Y EL MES ES: " + str(hoy.month)))
        if hoy.month == 7 or hoy.month == 10:
            #if not self.obtener_vencimiento_emitido(hoy.year, hoy.month):
            #La siguiente condiciòn se utiliza para desarrollo
            if self.obtener_vencimiento_emitido(hoy.year, hoy.month) or not self.obtener_vencimiento_emitido(hoy.year, hoy.month):
                self.crea_vencimientos()
        return True

    def busca_obligaciones_vencidas(self):
        hoy = datetime.date.today()
        hoy_str = str(hoy)
        obj_obligaciones_vencidas = self.env['exp_canon_obligaciones'].search([('fecha_vencimiento_gracia', '<', hoy_str), 
                                                                        ('estado', '=', 'emitido'), ('notificacion_enviada', '=', False)])
        for linea in obj_obligaciones_vencidas:
            #print((" *** " + linea.name))
            linea.notificacion_obligacion_vencida()
        return True

class exp_canon_config_bancos(models.Model):
    _name = 'exp_canon_config_obligaciones'
    _description = "Entidades de Pago asociadas"

    name = fields.Char('Entidad de Pago', required=True, readonly=False)
    numero_cuenta = fields.Char('Numero de Cuenta', required=False, readonly=False)
    cbu = fields.Char('CBU', required=False, readonly=False)

    def realiza_pago(self):
        return True

class exp_canon_config_global(models.Model):
    _name = 'exp_canon_config_global'
    _description = "Valor general para calcular el valor de propiedad minera."
    #My custom fields
    canon_valor_global = fields.Float('Valor General de Cálculo', default=1)
    canon_valor_global_control = fields.Char('Cadena de Integridad', required=False, readonly=False)
    active = fields.Boolean('Activo', default=True, readonly=True)

    def activar(self):
        return True

class exp_canon_config(models.Model):
    _name = 'exp_canon_config'
    _description = "Configuracion de Obligaciones"

    name = fields.Char('Nombre de la Configuracion', required=True, readonly=False)
    valida_desde = fields.Date('Valida Desde', required=True)
    valida_hasta = fields.Date('Valida Hasta', readonly=True)
    valor_pertenencia_factor = fields.Float('Factor Valor de Pertenencia', help='Factor de recargo o descuento.', default=1)
    valor_pertenencia = fields.Float('Valor de Pertenencia', help='Se calcula como el factor por un valor de ajuste genral. Inserto en Config generales del programa', default=1)
    mes_primer_vencimiento_anual = fields.Integer('Mes primer vencimiento', help='', default=6)
    mes_segundo_vencimiento_anual = fields.Integer('Mes segundo vencimiento', help='', default=12)
    mes_primer_plazo_gracia = fields.Integer('Mes vencimiento primer plazo gracia', help='', default=8)
    mes_segundo_plazo_gracia = fields.Integer('Mes vencimiento segundo plazo gracia', help='', default=2)

    config_defecto  = fields.Boolean('Configuración por Defecto', help='Solo puede haber una configuracion por defecto')

    validado = fields.Boolean('Configuración validada', help='Una vez validada no se puede volver a configurar', readonly=False, default=False)

    active = fields.Boolean('Activo', default=True, readonly=True)
    procedimiento_id = fields.Many2one('procedimiento.procedimiento','Tramite Asociado', required=False)
    categoria_mineral = fields.Selection([
        ('primera', 'Primera'),
        ('segunda', 'Segunda'),
        ('tercera', 'Tercera'),
        ('todas', 'Todas'),
        ('no_corresponde', 'No corresponde'),], required=False,
        help="Categoria del mineral asociada por defecto", string="Cat. Mineral Asociada")
    grupos_notificar = fields.Many2many('grupo', string='Grupos de Usuarios a Notificar',
                        required=False, readonly=False)

    _sql_constraints = [
        ('unique_default_config', 'EXCLUDE (config_defecto WITH =)  WHERE (config_defecto)',
         'No se puede continuar debido a que ya existe una configuración por defecto')
    ]

    def activar(self):
        return True

    def validar(self):
        print("estoy en validar")
        self.write({'validado': True})
        print(self.validado)
        return True

    def realiza_pago(self):
        return True
    
    def establecer_config_defecto(self):
        conf_objs_list = self.search([('config_defecto', '=', True)])
        for obj in conf_objs_list:
            obj.write({'config_defecto': False})
        self.write({'config_defecto': True})
        return True

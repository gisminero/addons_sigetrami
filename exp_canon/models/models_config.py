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
        print(("CREANDO VENCIMIENTOS ..."))
        hoy = datetime.date.today()
        mes = hoy.month
        anio = hoy.year
        semestre = self.obtener_semestre(mes)
        nombre = "Primer Semestre " + str(anio) if (mes > 0 and mes < 7) else "Segundo Semestre" + str(anio)
        # self.create({'name': nombre, 'anio': anio, 'semestre': semestre})
        exp_objs = self.env['expediente.expediente'].search([('state', '=', 'active')])
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

    def dispara_vencimientos(self):
        hoy = datetime.date.today()
        print (("EL DIA DE HOY ES: " + str(hoy) + " EL AÑO ES: " + str(hoy.year) + "  Y EL MES ES: " + str(hoy.month)))
        if hoy.month == 8 or hoy.month == 9:
             if not self.obtener_vencimiento_emitido(hoy.year, hoy.month):
             # if self.obtener_vencimiento_emitido(hoy.year, hoy.month):
                self.crea_vencimientos()
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

    def activar(self):
        return True

class exp_canon_config(models.Model):
    _name = 'exp_canon_config'
    _description = "Configuracion de Obligaciones"

#    @api.onchange('config_defecto')

       


    name = fields.Char('Nombre de la Configuracion', required=True, readonly=False)
    valida_desde = fields.Date('Valida Desde', required=True)
    valida_hasta = fields.Date('Valida Hasta', readonly=True)
    valor_pertenencia_factor = fields.Float('Factor Valor de Pertenencia', help='')
    valor_pertenencia = fields.Float('Valor de Pertenencia', help='Se calcula como el factor por un valor de ajuste genral. Inserto en Config generales del programa')
    mes_primer_vencimiento_anual = fields.Integer('Mes primer vencimiento', help='', default=6)
    mes_segundo_vencimiento_anual = fields.Integer('Mes segundo vencimiento', help='', default=12)
    mes_primer_plazo_gracia = fields.Integer('Mes vencimiento primer plazo gracia', help='', default=8)
    mes_segundo_plazo_gracia = fields.Integer('Mes vencimiento segundo plazo gracia', help='', default=2)
    config_defecto = fields.Boolean('Configuración por Defecto', help='Solo puede haber una configuracion por defecto')

    active = fields.Boolean('Activo', default=True, readonly=True)
    categoria_mineral_asociada = fields.Selection([
        ('primera', 'Primera'),
        ('segunda', 'Segunda'),
        ('tercera', 'Tercera'),
        ('todas', 'Todas'),
        ('no_corresponde', 'No corresponde'),], required=False,
        help="Categoria del mineral asociada por defecto", string="Categoria Mineral Asociada")

    _sql_constraints = [
        ('unique_default_config', 'EXCLUDE (config_defecto WITH =)  WHERE (config_defecto)',
         'No se puede continuar debido a que ya existe una configuración por defecto')
    ]

    def activar(self):
        return True

    def realiza_pago(self):
        return True


    def cambiar_default_canon(self):
        print("Estoy aqui: cambiar_default_canon")
        default_canon = self.env['exp_canon_config'].search([('config_defecto', '=', True), ('active', '=', True)])
        default_canon.config_defecto = False
        self.config_defecto = True

    def mantener_default_canon(self):
        print("Estoy aqui: cancelar")
        return True

    def confirma_cambio(self):
        print("Estoy aqui: confirma_cambio")
        return {
            'name': "Cambiar configuración por defecto",
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': self.id,  # SOLO PARA FORM
            'target': 'new',
            'tag': 'reload',
            'res_model': 'exp_canon_config',
            'views': [[self.env.ref('exp_canon.form_popup_config_canon_por_defecto').id, "form"]],
            'views_id': 'exp_canon_config.form_popup_config_canon_por_defecto'
        }

    @api.onchange('config_defecto')
    def alerta_prueba(self):
        if self.config_defecto == True:
            print("VERDADERO")
            default_canon = self.env['exp_canon_config'].search([('config_defecto', '=', True), ('active', '=', True)])
            print(self._origin.id)
            print(default_canon.id)
            if default_canon.config_defecto == True and default_canon.id!=self._origin.id:
                print("hay configuraciones por defecto VERDADERO")
                print(default_canon.config_defecto )
                self.config_defecto = False
                return self.confirma_cambio()
               # raise ValidationError(('ACA DEBERIA APARECER POPUP'))

            else                                                                                                    :
                print("no hay configuraciones por defecto")

        else:
            print("FALSO")

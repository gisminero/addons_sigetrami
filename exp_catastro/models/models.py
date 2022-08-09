# -*- coding: utf-8 -*-

from odoo import models, fields, api

"""
class expediente(models.Model):
    _name = 'expediente.expediente'
    #_name = 'expediente.expediente'
    _inherit = 'expediente.expediente'

    #name = fields.Char('Nombre', required=True)
    # description = fields.Char('Descripcion', required=False)
    #state_id = fields.Many2one('res.country.state', string="Provincia")
    #distritos = fields.One2many('exp_distrito', 'depart_id', string='Distritos Mineros',required=False)
    #active = fields.Boolean('Activo', default=True)
    #estado_plazos = fields.Char('Estado de Plazos', compute="_estadoPlazo", required=False)
"""

class exp_catastro_minas(models.Model):
    _name = 'exp_catastro_minas'
    #_name = 'expediente.expediente'
    #_inherit = 'expediente.expediente'

    expediente = fields.Char('Expediente', required=True)
    id_expediente = fields.Many2one('expediente.expediente', string="Expediente")
    nombre = fields.Char('Expediente', required=True)
    titular = fields.Char('Titular', required=True)
    mineral = fields.Char('Mineral', required=True)
    categoria = fields.Char('Categoria', required=True)
    # description = fields.Char('Descripcion', required=False)
    #state_id = fields.Many2one('res.country.state', string="Provincia")
    #distritos = fields.One2many('exp_distrito', 'depart_id', string='Distritos Mineros',required=False)
    #active = fields.Boolean('Activo', default=True)
    #estado_plazos = fields.Char('Estado de Plazos', compute="_estadoPlazo", required=False)

# -*- coding: utf-8 -*-

from odoo import models, fields, api

class exp_report(models.Model):
    _name = 'exp_report'
    #_inherit = 'expediente.expediente'

    name = fields.Char('Nombre', required=True)
    # description = fields.Char('Descripcion', required=False)
    #state_id = fields.Many2one('res.country.state', string="Provincia")
    #distritos = fields.One2many('exp_distrito', 'depart_id', string='Distritos Mineros',required=False)
    #active = fields.Boolean('Activo', default=True)
    #estado_plazos = fields.Char('Estado de Plazos', compute="_estadoPlazo", required=False)

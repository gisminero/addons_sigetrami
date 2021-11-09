# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError

class procedimiento(models.Model):
    _name = 'procedimiento.procedimiento'
    name = fields.Char('Nombre', required=True)
    description = fields.Char('Descripcion', required=False)
    active = fields.Boolean('Activo', default=True)
    iniciado = fields.Selection([
        ('1', 'Usuario'),
        ('2', 'Tarea')
        ], 'Iniciado por', index=True, readonly=False,required=True)
    proced_principal = fields.Many2one('procedimiento.procedimiento', 'Procedimiento Principal', required=False, help="""Procedimiento del cual depende""""")
    susplazo = fields.Selection([
        ('1', 'Si'),
        ('2', 'No')
        ], 'Suspede Plazos', index=True, readonly=False,required=True, default='2')
    categoria_mineral = fields.Selection([
        ('primera', 'Primera'),
        ('segunda', 'Segunda'),
        ('tercera', 'Tercera'),
        ('todas', 'Todas'),
        ('no_corresponde', 'No corresponde'),], required=True,
        help="Categoria del mineral asociada por defecto", string="Categoria Mineral")

    @api.onchange ('susplazo')
    def suspende(self):
        if self.iniciado =='1':
            self.susplazo = '2'

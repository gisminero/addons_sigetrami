# -*- coding: utf-8 -*-

from odoo import models, fields, api

# class mineral_lugar(models.Model):
#     _name = 'mineral_lugar'
#     _order = 'categoria asc'
#
#     name = fields.Char('Nombre', required=True)
#     categoria = fields.Selection([
#         ('Primera', 'Primera'),
#         ('Segunda', 'Segunda'),
#         ('Tercera', 'Tercera'),], required=True,
#         help="Categoria del mineral")
#     active = fields.Boolean('Activo', default=True)

class mineral(models.Model):
    _name = 'mineral'
    _order = 'categoria asc'

    name = fields.Char('Nombre', required=True)
    categoria = fields.Selection([
        ('primera', 'Primera'),
        ('segunda', 'Segunda'),
        ('tercera', 'Tercera'),], required=True,
        help="Categoria del mineral")
    tipo = fields.Selection([
        ('uso_comun', 'Aprovechamiento Común'),
        ('uso_propietario', 'Preferencia al Dueño de la Propiedad'),], required=False,
        help="Tipo de Mineral")
    active = fields.Boolean('Activo', default=True)

#
# from odoo import models, fields
#
# class Procedimiento(models.Model):
#     _name = 'procedimiento.procedimiento'
#     _description = 'procedimiento GMN'
#     name = fields.Char('Nombre', required=True)
#     description = fields.Char('Description', required=True)

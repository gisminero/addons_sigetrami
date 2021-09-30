# -*- coding: utf-8 -*-

from odoo import models, fields, api

  
class expediente(models.Model):
    _name = 'expediente.expediente'
    _inherit = 'expediente.expediente'
    _description = "Asociación con pertenencias"
    
    pertenencias= fields.Integer('Cantidad de pertenencias', required = True, default = 0)




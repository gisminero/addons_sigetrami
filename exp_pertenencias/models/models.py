# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo import exceptions

  
class expediente(models.Model):
    _name = 'expediente.expediente'
    _inherit = 'expediente.expediente'
    _description = "Asociación con pertenencias"
    
    pertenencias= fields.Integer('Cantidad de pertenencias', required = False, default = 0)




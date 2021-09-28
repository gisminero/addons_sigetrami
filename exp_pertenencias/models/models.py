# -*- coding: utf-8 -*-
from odoo import models, fields, api
import datetime
from odoo import exceptions
  
class expediente(models.Model):
    _name = 'expediente.expediente'
    _inherit = 'expediente.expediente'
    _description = "Asociación con pertenencias"
    
    pertenencias= fields.One2many('exp_pertenecias', 'exp_id', string = 'Pertenencias')




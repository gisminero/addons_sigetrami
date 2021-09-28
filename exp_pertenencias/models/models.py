# -*- coding: utf-8 -*-
from odoo import models, fields, api
import datetime
from odoo import exceptions


class exp_pertenecias(models.Model):
     _name = 'exp_pertenecias'
     _description = 'exp_pertenecias.exp_pertenecias'

     name = fields.Char('Pertenencias', required = False)
     cant_pertenenias = fields.Integer('Cantidad de Pertenencias', help='', required=True)
     exp_id = fields.Many2one('expediente.expediente', 'Pertenencias', required=1, ondelete='cascade')
     
class expediente(models.Model):
    _name = 'expediente.expediente'
    _inherit = 'expediente.expediente'
    _description = "Asociación con pertenencias"
    
    pertenencia_id = fields.One2many('exp_pertenecias', 'exp_id', string = 'Pertenencias')



